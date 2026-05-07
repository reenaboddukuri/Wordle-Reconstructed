#CONTROLLER: Handles user actions, communicates with Model and View.

from model import WordleModel
import random

#Listens for user input, asks the Model to process it, and tells the View what to display.   
class WordleController:

    def __init__(self, model, view, words, back):
        self.model = model
        self.view = view
        self.current_row = 0  # which grid row to fill next
        self.words = words
        self.back = back

        # Connect submit and retry handlers to the View.
        self.view.submit_handler = self.on_submit
        self.view.retry_btn.bind("<Button-1>", lambda e: self.on_replay())
        self.view.root.bind("<Return>", lambda e: self.on_submit())
        self.view.root.bind("<Key>", self.view.realKeyBoardClick)
        self.view.back_btn.bind("<Button-1>", lambda e: self.on_back())

    #Called every time the user enters guess.
    def on_submit(self):
        raw_input = self.view.get_input()

        # Ask the Model to validate and evaluate the guess.
        error, feedback = self.model.submit_guess(raw_input)

        # Bad input then show the message and let the user try again
        if error:
            self.view.show_status(error)
            return

        # Valid guess then update the grid row with colored feedback
        self.view.display_feedback(self.current_row, feedback)
        self.view.update_keyboard_color(feedback)
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

    #Reset the model with the random word of equal length and clear the grid
    def on_replay(self):
        current_word = random.choice(self.words)
        self.model.target = current_word
        self.model.reset()
        self.current_row = 0
        self.view.reset_grid()
        self.view.reset_keyboard()
        self.view.clear_input()
        self.view.enable_input()
        self.view.hide_retry_button()
        self.view.show_status(f"Guess the {self.model.word_length}-letter word!")

    #Navigate back to the home page to select between puzzle options
    def on_back(self):
        self.view.cleanUp()
        self.back()
        