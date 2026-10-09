from logic_utils import check_guess, new_game_state

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
