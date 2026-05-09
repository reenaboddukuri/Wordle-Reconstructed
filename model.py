#MODEL: Manages Wordle data and logic

# Stores the target word, all guesses, current game status, validates input, evaluates letters using colors (green, yellow, dark gray)
class WordleModel:

    MAX_GUESSES = 6

    # constructor for WordleModel 
    def __init__(self, target_word, valid_words, word_length):
        self.target = target_word.upper()
        self.valid_words = valid_words
        self.word_length = word_length
        self.guesses = []       # list of guess strings
        self.status = "playing" # "playing", "won", or "lost"

    # Manages edge cases
    # Returns an error string if invalid, and None if the guess is valid.
    def validate(self, guess):
        if len(guess) != self.word_length:
            return f"Word must be exactly {self.word_length} letters."
        if not guess.isalpha():
            return "Word must contain only letters."
        if guess not in self.valid_words:
            return "Word not in word list."
        return None #if valid, return None

    """
    Compare the guess to the target word letter by letter:
    1) green: correct letter, correct position
    2) yellow: correct letter, wrong position
    3) dark gray: letter not in the word
    """
    def evaluate(self, guess):
        guess = guess.upper()
        results = ["gray"] * self.word_length # Initializes all letters to gray (not in target word)

        # Tracks unmatched letters so a repeated letter in the guess doesn't earn two yellows.
        remaining_letters = list(self.target)

        # First pass: mark exact matches (green).
        # For matched letters, updates color to green and REMOVES from remaining unmatched letters list
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
        self.guesses.append(guess)  # Record the guesses by adding to the list of guesses
        
        # When guess matches the target word, sets the status of the game to “won”
        if guess == self.target:
            self.status = "won"
        elif len(self.guesses) >= self.MAX_GUESSES:
            self.status = "lost"

        return None, feedback

    # Clears guesses and resets status to playing.
    def reset(self):
        self.guesses = []
        self.status = "playing"
        