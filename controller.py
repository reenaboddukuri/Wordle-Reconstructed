# ─────────────────────────────────────────────────────────────────────────────
# CONTROLLER
# Handles user actions, communicates with Model and View.
# ─────────────────────────────────────────────────────────────────────────────

from model import WordleModel

class WordleController:
    """
    Listens for user input, asks the Model to process it, and tells the View what to display.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_row = 0  # which grid row to fill next

        # Connect the submit handler with the View.
        self.view.bind_submit(self.on_submit)

    def on_submit(self):
        """Called every time the user clicks Guess or presses Enter."""
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
            self.view.show_status(
                f"You won in {self.current_row} guess(es)! "
            )
            self.view.disable_input()

        elif self.model.status == "lost":
            self.view.show_status(
                f"Game over! The word was {self.model.target}."
            )
            self.view.disable_input()

        else:
            remaining = WordleModel.MAX_GUESSES - self.current_row
            self.view.show_status(f"{remaining} guess(es) remaining.")
