# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**First impressions:** The game loads and looks normal: a number-guessing game with a difficulty selector, a text box, and a hint checkbox. It never crashes, but the hints, scoring, attempt counter and New Game button misbehave in ways that only show up when you play several rounds.

**Bugs found**

1. **Hints are backwards.**
   - Guess 10 when the secret is 50.
   - Expected Behavior: "Too Low" with a "Go HIGHER!" message.
   - Actual Behavior: "Go LOWER!". A guess of 90 gets "Go HIGHER!".

2. **Secret is turned into a string on every even attempt.**
   - Any guess made on an even-numbered attempt (2, 4, 6, ...).
   - Expected Behavior: always a numeric comparison.
   - Actual Behavior: secret is set as string:  `secret = str(st.session_state.secret)`. For example "5" vs "30" is compared alphabetically, so the hint can be wrong for numbers of different lengths (like 5 vs 30 or 99 vs 100).

3. **New Game doesn't fully reset.**
   - Win or lose, then click "New Game".
   - Expected Behavior: fresh game with score 0, empty history, status "playing", and a secret inside the chosen difficulty's range.
   - Actual Behavior: only resets attempts and secret. status stays "won"/"lost", so the game is stuck on "You already won / Game over". score and history carry over. The secret is always randint(1, 100) even on Easy/Hard.

4. **Attempt counter is off by one and bad input costs an attempt.**
   - First guess on Normal (8 attempts).
   - Expected Behavior: "Attempts left: 7" after one guess, with the counter starting at 0.
   - Actual Behavior: attempts starts at 1, and New Game sets it to 0, so the two starts disagree. attempts += 1 runs before parse_guess, so "abc" or a blank guess still uses up an attempt.

**Bug Reproduction Log**

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|------------|-------------------|-----------------|------------------------|-------------------------|
| Guess `10`, secret `50` (Normal) | "Too Low" → "Go HIGHER!" | "Go LOWER!" shown (and "Go HIGHER!" for a guess of 90) | none | `app.py`, `check_guess` (lines 37-40) |
| Guess `5` on attempt 6, secret `30` | Hint based on 5 < 30 (numeric) | Compared as the strings "5" and "30" via the `TypeError` fallback, so the hint is unreliable on every even attempt | none (the `TypeError` is silently caught) | `app.py` lines 158-161 and `check_guess` fallback (41-47) |
| Win a game, then click "New Game" | New game starts, score 0, status "playing" | Page still shows "You already won. Start a new game to play again."; score -10 carried over | none | `app.py`, New Game block (lines 134-138) |
| First guess `10` on Normal (8 attempts) | "Attempts left: 7" counted from 0 | `attempts` starts at 1; the first guess already leaves 7 and New Game resets to 0 | none | `app.py` lines 95-96, 134-135, 148 |
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - Used claude code to help me on this project
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - The fixes provided by AI were expansive (encompusing all issues) and clear.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
  - AI did try to solve all the issues in one go. I had to reject the out of scope code and had to reorient and narrow the focus of solution to what was the objective. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - run test, opened the browser and verfied the fixes
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
 - I used AI to create the tests with pytest. It ran the tests, and made sure that the results were as expected. 
- Did AI help you design or understand any tests? How?
 - Yes, AI helped me create the tests, but I verified them visually. 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
