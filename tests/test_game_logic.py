from logic_utils import check_guess

# check_guess returns (outcome, message); the app shows the message as the hint.

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# Bug #1: the hint message told players to go the wrong way.

def test_too_high_hint_says_go_lower():
    # Secret 82, guess 95 -> the player must go LOWER
    _, message = check_guess(95, 82)
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    # Secret 82, guess 81 -> the player must go HIGHER
    _, message = check_guess(81, 82)
    assert "HIGHER" in message
