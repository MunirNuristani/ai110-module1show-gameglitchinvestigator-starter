from pathlib import Path

from streamlit.testing.v1 import AppTest

from logic_utils import check_guess, get_range_for_difficulty, new_game_state, parse_guess, update_score

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")


def run_app():
    at = AppTest.from_file(APP_PATH)
    at.run()
    assert not at.exception
    return at


def submit_guess(at, text):
    at.text_input[0].set_value(text).run()
    at.button[0].click().run()
    assert not at.exception

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome is "Too High" and hint says go lower
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome is "Too Low" and hint says go higher
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_too_high_hint_with_string_secret():
    # The TypeError fallback branch must give the same hint direction
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_hint_with_string_secret():
    outcome, message = check_guess(40, "50")
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_new_game_resets_status_score_and_history():
    # A finished game must not carry over its status, score or history
    state = new_game_state(1, 100)
    assert state["status"] == "playing"
    assert state["score"] == 0
    assert state["history"] == []
    assert state["attempts"] == 0

def test_new_game_secret_respects_difficulty_range():
    # Easy range is 1-20; the secret must never fall outside it
    for _ in range(200):
        assert 1 <= new_game_state(1, 20)["secret"] <= 20


# --- Attempt counter / invalid input ---

def test_parse_guess_rejects_blank_and_non_numeric():
    for raw in [None, "", "abc"]:
        ok, value, err = parse_guess(raw)
        assert ok is False
        assert value is None
        assert err

def test_parse_guess_accepts_whole_number():
    assert parse_guess("42") == (True, 42, None)

def test_fresh_game_starts_with_zero_attempts():
    # A fresh page load must agree with New Game, which also starts at 0
    at = run_app()
    assert at.session_state["attempts"] == 0

def test_invalid_guess_does_not_use_an_attempt():
    at = run_app()
    submit_guess(at, "abc")
    assert at.session_state["attempts"] == 0
    submit_guess(at, "")
    assert at.session_state["attempts"] == 0

def test_valid_guess_uses_one_attempt():
    at = run_app()
    submit_guess(at, "50")
    assert at.session_state["attempts"] == 1


# --- Scoring ---

def test_too_high_always_costs_points():
    # Previously even attempts earned +5 for a wrong "Too High" guess
    for attempt in range(1, 9):
        assert update_score(50, "Too High", attempt) == 45

def test_too_low_always_costs_points():
    for attempt in range(1, 9):
        assert update_score(50, "Too Low", attempt) == 45

def test_win_adds_points_and_never_drops_below_ten():
    assert update_score(0, "Win", 1) == 80
    assert update_score(0, "Win", 20) == 10

def test_wrong_guess_never_beats_not_guessing():
    # A wrong guess must never raise the score, whatever the attempt number
    for outcome in ["Too High", "Too Low"]:
        for attempt in range(1, 9):
            assert update_score(0, outcome, attempt) < 0


# --- Difficulty changes ---

def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_switching_difficulty_redraws_secret_in_new_range():
    # A Normal secret of 99 is impossible on Easy (1-20)
    at = run_app()
    at.session_state["secret"] = 99
    at.sidebar.selectbox[0].select("Easy").run()
    assert not at.exception
    assert 1 <= at.session_state["secret"] <= 20

def test_switching_difficulty_starts_a_fresh_game():
    at = run_app()
    submit_guess(at, "50")
    assert at.session_state["attempts"] == 1
    at.sidebar.selectbox[0].select("Hard").run()
    assert at.session_state["attempts"] == 0
    assert at.session_state["history"] == []
    assert at.session_state["status"] == "playing"
