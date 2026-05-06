#CONTROLLER: Handles user actions, communicates with Model and View.

from model import WordleModel
import random

class WordleController:
    #Listens for user input, asks the Model to process it, and tells the View what to display.   

    def __init__(self, model, view, words):
        self.model = model
        self.view = view
        self.current_row = 0  # which grid row to fill next
        self.words = words

        # Connect submit and retry handlers to the View.
        self.view.bind_submit(self.on_submit)
        self.view.bind_retry(self.on_retry)

    def on_submit(self):
        #Called every time the user clicks Guess or presses Enter.
        raw_input = self.view.get_input()

        # Ask the Model to validate and evaluate the guess.
        error, feedback = self.model.submit_guess(raw_input)

        if error:
            # Bad input then show the message and let the user try again
            self.view.show_status(error)
            self.view.clear_input()
            return

        # Valid guess then update the grid row with colored feedback
        self.view.display_feedback(self.current_row, feedback)
        self.view.clear_input()
        self.current_row += 1

        # React to the new game status
        if self.model.status == "won":
            self.view.show_status(f"You won in {self.current_row} guess(es)!")
            self.view.disable_input()
            self.view.show_retry_button()

        elif self.model.status == "lost":
            self.view.show_status(f"Game over! The word was {self.model.target}.")
            self.view.disable_input()
            self.view.show_retry_button()

        else:
            remaining = WordleModel.MAX_GUESSES - self.current_row
            self.view.show_status(f"{remaining} guess(es) remaining.")

    def on_retry(self):
        #Reset the model with the random word and clear the grid
        current_word = random.choice(self.words)
        self.model.target = current_word
        self.model.reset()
        self.current_row = 0
        self.view.reset_grid()
        self.view.clear_input()
        self.view.enable_input()
        self.view.hide_retry_button()
        self.view.show_status("Guess the 5-letter word!")
