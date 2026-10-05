# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The first time I ran the game it looked finished: a title, a difficulty sidebar, a guess box and a debug panel. But playing it with the "Developer Debug Info" panel open showed it was broken. With the secret at 82, guessing 81 told me to "Go LOWER", and guessing 95 told me to "Go HIGHER", so the hints pointed away from the answer. After I won a game, clicking "New Game" did nothing useful: the app kept saying I had already won and wouldn't take another guess.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret 82, guess 81 | Hint says go HIGHER | Hint says "Go LOWER" (opposite) | No error. Suspect `check_guess` in app.py lines 37–40 |
| Secret 82, guess 95 | Hint says go LOWER | Hint says "Go HIGHER" (opposite) | No error. Same function: messages swapped |
| Win a game, then click "New Game" | A fresh game I can play | Still says "You already won", can't guess again | No error. Suspect the New Game block in app.py (~line 135): `status` is never reset |
| Secret 82, 2nd guess of 9 (found by reading the code with Claude) | Hint says go HIGHER | Secret is turned into text on even attempts, so "9" > "82" counts as too high | No error. app.py converted the secret with `str()` on every even attempt |

---

## 2. How did you use AI as a teammate?

I used Claude (Claude Code) as my AI teammate. I was short on time, so Claude did a lot of the hands-on work: it set up the project, made the code changes and drafted the documentation, including this reflection, from our session. My part was playing the game to find and confirm bugs, approving each change, and reviewing what it wrote. A suggestion that was correct: Claude said the outcome logic in `check_guess` was right but the two hint messages were swapped. I verified it because the two new hint tests failed before the swap and passed after it, and because the hints pointed the right way when I played again. A suggestion I did not take as written: the provided tests expected `check_guess` to return just `"Win"`, but the app needs both the outcome and the message. Instead of changing the function to match the tests, we kept the `(outcome, message)` pair and changed the tests to unpack it. That fit the codebase better, and all 5 tests confirm it works.

---

## 3. Debugging and testing your fixes

I treated a bug as fixed only when a test that failed before the change passed after it, and the game behaved correctly when I played it. The clearest example was the hint bug. We first moved the logic into `logic_utils.py` without fixing it, and pytest showed `2 failed, 3 passed`. After swapping the messages it showed `5 passed`. That proved the tests really catch the bug, rather than passing by accident. Claude designed those tests by turning my bug reproduction (secret 82, guesses 81 and 95) directly into test cases, which taught me to write tests from real bug reports. The New Game fix is in the UI code, so I verified it manually by winning and then starting a new game.

---

## 4. What did you learn about Streamlit and state?

Streamlit re-runs the whole Python script from top to bottom every time you click a button or type something, so normal variables start fresh on every click. `st.session_state` is the app's memory: it keeps values like the secret number, attempts and status between those reruns. That's why the New Game bug happened. The button reset some values in session state but left `status` as "won", so on the next rerun the app read that old value and stopped the game. Every value that defines a game has to be reset together.

---

## 5. Looking ahead: your developer habits

The habit I want to keep is writing a test that reproduces a bug and fails first, then fixing the code until it passes; that gave me real proof instead of "it looks fine". I also want to keep committing after each small step, with a message that says what changed and why. Next time, I'll start earlier, do more of the fixes myself, and use the AI more for explanation and review, so I understand every line better and don't depend on it under deadline pressure. This project showed me that AI-generated code can look production-ready and still contain several subtle logic bugs (a kind of hallucinated confidence), so it always needs a human-in-the-loop with a test set and verification before I trust it.
