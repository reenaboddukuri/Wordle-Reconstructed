# ─────────────────────────────────────────────────────────────────────────────
# VIEW
# Builds the UI and manages the Tkinter widgets.
# ─────────────────────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import font

class WordleView:
    """
    Creates and manages the frontend using Tkinter.
    Includes methods that the Controller calls to read input
    and to push updates back to the screen.
    """
    # Wordle-style color list
    COLOR = {
        "green":  "#6aaa64",
        "yellow": "#c9b458",
        "gray":   "#787c7e",
        "empty":  "#ffffff",
        "divider":"#d3d6da",
    }

    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.root.title("Wordle")
        self.root.resizable(True, True)
        self._build_ui()

    def _build_ui(self):
        """Construct every widget in the window."""

        # Title bar
        title_font = font.Font(family="Helvetica", size=22, weight="bold")
        tk.Label(self.root, text="WORDLE", font=title_font).pack(pady=(16, 6))
        tk.Frame(self.root, height=2, bg=self.COLOR["divider"]).pack(
            fill="x", padx=20
        )

        # 6 × 5 guess grid
        grid_frame = tk.Frame(self.root, pady=14)
        grid_frame.pack()

        cell_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.cells = []  # self.cells[row][col] is a tk.Label

        for row in range(self.model.MAX_GUESSES):
            row_cells = []
            for col in range(self.model.WORD_LENGTH):
                lbl = tk.Label(grid_frame, text="", width=2, font=cell_font, bg=self.COLOR["empty"], fg="white", relief="solid", borderwidth=2)
                lbl.grid(row=row, column=col, padx=3, pady=3, ipadx=8, ipady=10)
                row_cells.append(lbl)
            self.cells.append(row_cells)  # Add the row cells to the cells list

        # Input row
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack()

        # Entry field
        entry_font = font.Font(family="Helvetica", size=13)
        self.entry_var = tk.StringVar()  # String variable to store the user's input
        self.entry = tk.Entry(input_frame, textvariable=self.entry_var, font=entry_font, width=9, justify="center")  # Entry field
        self.entry.pack(side="left", padx=(0, 8))  
        self.entry.focus()  

        # Submit button
        self.submit_btn = tk.Button(input_frame, text="Guess", font=entry_font, padx=10)
        self.submit_btn.pack(side="left")

        # Status / message label
        msg_font = font.Font(family="Helvetica", size=12)
        self.status_var = tk.StringVar(value="Guess the 5-letter word!")
        tk.Label(self.root, textvariable=self.status_var, font=msg_font).pack(pady=(4, 8))

        # Play Again button — hidden until the game ends
        self.retry_frame = tk.Frame(self.root)
        self.retry_btn = tk.Button(self.retry_frame, text="Play Again", font=entry_font, padx=10)
        self.retry_btn.pack()

    # Public interface for the Controller
    def get_input(self):
        """Return whatever the user has typed in the entry field."""
        return self.entry_var.get().strip()

    def clear_input(self):
        """Empty the entry field."""
        self.entry_var.set("")

    def show_status(self, message):
        """Replace the status label text."""
        self.status_var.set(message)

    def display_feedback(self, row, feedback):
        """
        Color one row of the grid to reflect guess feedback received from WordleModel.evaluate()
        """
        for col, (letter, color_name) in enumerate(feedback):
            self.cells[row][col].config(
                text=letter,
                bg=self.COLOR.get(color_name, self.COLOR["gray"]),
                relief="flat",
            )

    def disable_input(self):
        """Lock entry and button after the game ends."""
        self.entry.config(state="disabled")
        self.submit_btn.config(state="disabled")

    def reset_grid(self):
        """Return every cell to its blank, white state."""
        for row in self.cells:
            for cell in row:
                cell.config(text="", bg=self.COLOR["empty"], relief="solid")

    def enable_input(self):
        """Re-enable entry and submit button for a new round."""
        self.entry.config(state="normal")
        self.submit_btn.config(state="normal")
        self.entry.focus()

    def show_retry_button(self):
        """Show the Play Again button."""
        self.retry_frame.pack(pady=(0, 14))

    def hide_retry_button(self):
        """Hide the Play Again button."""
        self.retry_frame.pack_forget()

    def bind_submit(self, handler):
        """Wire the Guess button and the Enter key to a handler function."""
        self.submit_btn.config(command=handler)
        self.root.bind("<Return>", lambda _event: handler())

    def bind_retry(self, handler):
        """Wire the Play Again button to a handler function."""
        self.retry_btn.config(command=handler)
