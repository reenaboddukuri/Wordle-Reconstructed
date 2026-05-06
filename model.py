#MODEL: Handles game data, rules, and state.

class WordleModel:
    # Stores the target word, all guesses, current game status, validates input, letter evaluation using colors (green, yellow, dark gray)

    WORD_LENGTH = 5
    MAX_GUESSES = 6

    def __init__(self, target_word):
        self.target = target_word.upper()
        self.guesses = []       # list of guess strings
        self.status = "playing" # "playing", "won", or "lost"

    # Checks if guess is valid
    # Returns an error string if invalid, and None if the guess is valid.
    def validate(self, guess):
        if len(guess) != self.WORD_LENGTH:
            return f"Word must be exactly {self.WORD_LENGTH} letters."
        if not guess.isalpha():
            return "Word must contain only letters."
        return None

    """
    Compare the guess to the target word letter by letter:
    1) green: correct letter, correct position
    2) yellow: correct letter, wrong position
    3) dark gray: letter not in the word
    """
    def evaluate(self, guess):
        guess = guess.upper()
        results = ["gray"] * self.WORD_LENGTH

        # Keep track of which letters are still unmatched,
        # so a repeated letter in the guess doesn't earn two yellows.
        remaining_letters = list(self.target)

        # First pass: mark exact matches (green).
        for i, letter in enumerate(guess):
            if letter == self.target[i]:
                results[i] = "green"
                remaining_letters[i] = None  # remove the letter from the remaining letters

        # Second pass: mark letters present but misplaced (yellow).
        for i, letter in enumerate(guess):
            if results[i] == "green":
                continue  # already handled
            if letter in remaining_letters:
                results[i] = "yellow"
                remaining_letters[remaining_letters.index(letter)] = None  # remove the letter from the remaining letters once

        return list(zip(guess, results))

    # Validates the guess and updates game status.
    # Returns error message if invalid guess, and (None, feedback) if guess was accepted
    def submit_guess(self, guess):
        guess = guess.upper()
        error = self.validate(guess)  # Check if the guess is valid
        if error: return error, None
        feedback = self.evaluate(guess)  # Evaluate the guess
        self.guesses.append(guess)  # Record the guesses
        if guess == self.target:
            self.status = "won"
        elif len(self.guesses) >= self.MAX_GUESSES:
            self.status = "lost"

        return None, feedback

    def reset(self):
        #Clear guesses and status to play again.
        self.guesses = []
        self.status = "playing"