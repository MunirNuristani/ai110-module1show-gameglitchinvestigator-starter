# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.

  Game Glitch Investigator is a number-guessing game built with Streamlit. The player picks a difficulty, guesses a secret number within a limited number of attempts, and gets "Go HIGHER" or "Go LOWER" hints and a score. The code was AI-generated and contains deliberate bugs, and the exercise is to find them, fix them and back the fixes with tests.

- [x] Detail which bugs you found.
  - **Swapped hints:** a guess above the secret said "Go HIGHER!" and a guess below it said "Go LOWER!".
  - **Secret turned into a string on even attempts:** `app.py` converted the secret with `str()` on every even attempt. That made `int > str` raise a `TypeError` in the browser, and the string fallback in `check_guess` compared numbers as text.
  - **New Game didn't fully reset:** it only reset `attempts` and `secret`, so `status`, `score` and `history` carried over. After a win or loss the game stayed stuck on "You already won" or "Game over". The new secret also always came from 1-100, ignoring the difficulty range.

- [x] Explain what fixes you applied.
  - **Hints:** moved `check_guess` into `logic_utils.py`, corrected both hint directions (including the `TypeError` fallback branch), and imported it in `app.py`.
  - **String secret:** removed the `str()` conversion so `check_guess` always receives the secret as an int.
  - **New Game:** added `new_game_state(low, high)` to `logic_utils.py`. It returns fresh attempts, secret, status, score and history, with the secret drawn from the current difficulty's range, and `app.py` now loads those values on New Game.
  - **Tests:** `tests/test_game_logic.py` now covers the win case, both hint directions (with int and string secrets), the New Game reset, and the secret staying within range. A `pytest.ini` puts the project root on the import path so `pytest` runs from the root.

## 📸 Demo Walkthrough

A sample game on Normal difficulty (range 1-100), where the secret number is 42:

1. Run the game and pick a difficulty in the sidebar. The range and attempts allowed are shown.
2. Enter `75` and click **Submit Guess**. The game says "📉 Go LOWER!" because the guess is above the secret.
3. Enter `20`. The game says "📈 Go HIGHER!" because the guess is below the secret.
4. Keep narrowing in with `50` (lower), then `40` (higher). The hints stay correct on every attempt.
5. Enter `42`. The game shows balloons, reveals the secret and displays your final score, then blocks further guesses.
6. Click **New Game**. Status, score and guess history reset, and a new secret is drawn from the current difficulty's range.


**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->
![alt text](<Screenshot 2026-10-08 at 20-25-13 Glitchy Guesser.png>)

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
