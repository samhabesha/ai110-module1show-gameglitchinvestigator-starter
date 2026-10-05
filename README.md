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

- [x] **Game's purpose:** a Streamlit number-guessing game. The player guesses a secret number within a range set by the difficulty (Easy 1–20, Normal 1–100, Hard 1–50), gets "go higher / go lower" hints, earns a score, and has a limited number of attempts.
- [x] **Bugs found:**
  1. **Reversed hints:** a guess that was too high told the player to "Go HIGHER" (and vice versa), so hints pointed away from the secret.
  2. **New Game didn't restart:** after winning or losing, "New Game" left `status` as "won"/"lost", so the app stopped before accepting any guess. It also didn't clear history or score, and it ignored the difficulty when choosing a new secret.
  3. **Text comparison on even guesses:** on every 2nd attempt the secret was converted to a string, so guesses were compared alphabetically (`"9" > "82"`), producing wrong hints.
  4. **Off-by-one attempts:** the attempt counter started at 1, so the first game showed one fewer attempt than allowed, and the info box always said "between 1 and 100" whatever the difficulty.
- [x] **Fixes applied:**
  - Moved the game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) from `app.py` into `logic_utils.py`, so it can be tested without the UI.
  - Swapped the hint messages in `check_guess` so "Too High" says "Go LOWER" and "Too Low" says "Go HIGHER".
  - New Game now resets `status`, `history`, `score` and `attempts`, and picks the secret from the current difficulty's range.
  - Always compares the guess with the numeric secret; the counter starts at 0; the info box shows the real range.
  - Tests: updated the provided tests to unpack `(outcome, message)`, and added two tests that check hint direction. Both failed before the fix and pass after it.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest -v
tests/test_game_logic.py::test_winning_guess PASSED                      [ 20%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 40%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 60%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 80%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [100%]

============================== 5 passed in 0.08s ==============================
```

Before the fix, the two hint tests failed (`2 failed, 3 passed`), which confirmed they catch the reversed-hint bug. Full output is in `test_results.txt`.

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
