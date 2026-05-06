#VIEW: Builds the UI and manages the Tkinter widgets.

import tkinter as tk
from tkinter import font

#Includes methods that the Controller calls to read input and to push updates back to the screen.
class WordleView:
    # Wordle-style color list
    COLOR = {
        "green":  "#6aaa63",
        "yellow": "#c9b458",
        "gray":   "#787c7e",
        "empty":  "#f7f1df",
        "divider":"#d3d6da",
        "background": "#f7f1df"
    }

    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.root.title("Wordle")
        self.root.resizable(True, True)
        self.root.config(bg = self.COLOR["background"])
        self._build_ui()

    def _build_ui(self):
        #Construct every widget in the window.

        # Title bar
        title_font = font.Font(family="Helvetica", size=22, weight="bold")
        tk.Label(self.root, text="WORDLE", font=title_font, bg=self.COLOR["background"]).pack(pady=(16, 6))
        tk.Frame(self.root, height=2, bg=self.COLOR["divider"]).pack(
            fill="x", padx=20
        )

        # For the 6 by 5 wordle grid
        grid_frame = tk.Frame(self.root, pady=14, bg=self.COLOR["background"])
        grid_frame.pack()

        cell_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.cells = []  # self.cells[row][col] is a tk.Label

        for row in range(self.model.MAX_GUESSES):
            row_cells = []
            for col in range(self.model.WORD_LENGTH):
                gridBorder = tk.Frame(grid_frame, bg = "#b0aeae")
                gridBorder.grid(row=row, column=col, padx=3, pady=3)
                lbl = tk.Label(gridBorder, text="", width=2, font=cell_font, bg=self.COLOR["background"], fg="white")
                lbl.pack(padx=2, pady=2, ipadx=8, ipady=10)
                row_cells.append(lbl)
            self.cells.append(row_cells)  # Add the row cells to the cells list

        # Input row
        input_frame = tk.Frame(self.root, pady=10, bg=self.COLOR["background"])
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
        tk.Label(self.root, textvariable=self.status_var, font=msg_font, bg=self.COLOR["background"]).pack(pady=(4, 8))

        # Play Again button — hidden until the game ends
        self.retry_frame = tk.Frame(self.root, bg=self.COLOR["background"])
        self.retry_btn = tk.Button(self.retry_frame, text="Play Again", font=entry_font, padx=10)
        self.retry_btn.pack()

    # Public interface for the Controller

    # Return what the user has typed in the entry field.
    def get_input(self):
        return self.entry_var.get().strip()

    # Clear the entry field.
    def clear_input(self):
        self.entry_var.set("")

    # Replace the status message.
    def show_status(self, message):
        self.status_var.set(message)

    # Color one row of the grid to reflect guess feedback received from WordleModel.evaluate()
    def display_feedback(self, row, feedback):
        for col, (letter, color_name) in enumerate(feedback):
            self.cells[row][col].config(
                text=letter,
                bg=self.COLOR.get(color_name, self.COLOR["gray"]),
                relief="flat",
            )

    # Lock entry and button after the game ends.
    def disable_input(self):
        self.entry.config(state="disabled")
        self.submit_btn.config(state="disabled")

    # Reset to empty grid
    def reset_grid(self):
        for row in self.cells:
            for cell in row:
                cell.config(text="", bg=self.COLOR["background"], relief="flat")

    # Re-enable entry and submit button for a new round.
    def enable_input(self):
        self.entry.config(state="normal")
        self.submit_btn.config(state="normal")
        self.entry.focus()

    # Show the Play Again button.
    def show_retry_button(self):
        self.retry_frame.pack(pady=(0, 14))

    # Hide the Play Again button.
    def hide_retry_button(self):
        self.retry_frame.pack_forget()

    # Wire the Guess button and the Enter key to a handler function.
    def bind_submit(self, handler):
        self.submit_btn.config(command=handler)
        self.root.bind("<Return>", lambda _event: handler())

    # Wire the Play Again button to a handler function.
    def bind_retry(self, handler):
        self.retry_btn.config(command=handler)