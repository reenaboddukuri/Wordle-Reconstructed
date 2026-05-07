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
        self.root.minsize(480, 680)
        self.root.config(bg = self.COLOR["background"])
        self.puzzle_frame = tk.Frame(root, bg = self.COLOR["background"])
        self.puzzle_frame.pack(fill="both", expand=True)
        self.build_ui()

    #Construct every widget in the window.
    def build_ui(self):

        # Title bar
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        tk.Label(self.puzzle_frame, text="WORDLE", font=title_font, bg=self.COLOR["background"]).pack(pady=(12, 2))
        heading_font = font.Font(family="Helvetica", size=10)
        tk.Label(self.puzzle_frame, text=f"({self.model.word_length} letters)", font=heading_font, bg=self.COLOR["background"], fg="gray").pack(pady=(0,4))
        tk.Frame(self.puzzle_frame, height=2, bg=self.COLOR["divider"]).pack(fill="x", padx=16)

        # For the wordle grid
        grid_frame = tk.Frame(self.puzzle_frame, pady=10, bg=self.COLOR["background"])
        grid_frame.pack()

        cell_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.cells = []  # self.cells[row][col] is a tk.Label

        for row in range(self.model.MAX_GUESSES):
            row_cells = []
            for col in range(self.model.word_length):
                gridBorder = tk.Frame(grid_frame, bg = "#b0aeae")
                gridBorder.grid(row=row, column=col, padx=3, pady=3)
                lbl = tk.Label(gridBorder, text="", width=2, font=cell_font, bg=self.COLOR["background"], fg="white")
                lbl.pack(padx=2, pady=2, ipadx=10, ipady=12)
                row_cells.append(lbl)
            self.cells.append(row_cells)  # Add the row cells to the cells list

        self.entry_var = tk.StringVar() # String variable to store the user's input
        self.current_row = 0  # current row which shows the letters being typed
        self.disableInput = False

        # Status / message label
        msg_font = font.Font(family="Helvetica", size=11)
        self.status_var = tk.StringVar(value=f"Guess the {self.model.word_length}-letter word!")
        tk.Label(self.puzzle_frame, textvariable=self.status_var, font=msg_font, bg=self.COLOR["background"]).pack(pady=(3, 6))

        # Play Again and Change length button — hidden until the game ends
        self.retry_frame = tk.Frame(self.puzzle_frame, bg=self.COLOR["background"])
        retry_font = font.Font(family="Helvetica", size=12, weight="bold")

        self.retry_btn = tk.Label(self.retry_frame, text="Play Again", font=retry_font, bg=self.COLOR["green"], fg="white", padx=24, pady=10)
        self.retry_btn.pack(side="left", padx=8)

        self.back_btn = tk.Label(self.retry_frame, text="Change Length", font=retry_font, bg=self.COLOR["green"], fg="white", padx=24, pady=10)
        self.back_btn.pack(side="left", padx=8)

        # Keyboard
        self.keyboard = tk.Frame(self.puzzle_frame, bg=self.COLOR["background"])
        self.keyboard.pack(pady=(8, 12))
        keyboard_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.letterColor = {}

        # Keyboard layout
        layout = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"], ["A", "S", "D", "F", "G", "H", "J", "K", "L"], ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "DELETE"]]

        for row in layout:
            rowFrame = tk.Frame(self.keyboard, bg=self.COLOR["background"])
            rowFrame.pack()

            for key in row:
                temp = 12 if len(key)>1 else 8
                indivdualKey = tk.Label(rowFrame, text=key, font=keyboard_font, bg="#b0aeae", fg="black", padx=temp, pady=10)
                indivdualKey.pack(side="left", padx=2,  pady=2)
                indivdualKey.bind("<Button-1>", lambda e, k=key: self.onClick(k))
                if len(key) == 1: # when key is a character (not enter or delete)
                    self.letterColor[key] = indivdualKey   #saving key for color coding

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
        for col in range(len(feedback)):
            letter = feedback[col][0]
            colorName = feedback[col][1]
            self.cells[row][col].config(text=letter, bg=self.COLOR[colorName], fg="white")
        self.current_row = row+1

    # Lock keyboard after the game ends.
    def disable_input(self):
        self.disableInput = True

    #update keyboard colors
    def update_keyboard_color(self, feedback):
        for char, color in feedback:
            element = self.letterColor.get(char)
            colorUpdate = self.COLOR[color]
            currentColor = element.cget("bg")

            if currentColor == self.COLOR["green"]:
                continue
            if currentColor == self.COLOR["yellow"] and color!="green":
                continue
            element.config(bg=colorUpdate, fg = "white")
            

    # reset keyboard
    def reset_keyboard(self):
        for i in self.letterColor.values():
            i.config(bg = "#b0aeae", fg="black")

    # Reset to empty grid
    def reset_grid(self):
        for row in self.cells:
            for cell in row: #resets background and characters
                cell.config(text="", bg=self.COLOR["background"], fg="white")
        self.current_row = 0 #reset to row 0

    # Re-enable entry and submit button for a new round.
    def enable_input(self):
        self.disableInput = False

    # Show the Play Again button.
    def show_retry_button(self):
        self.retry_frame.pack(pady=(0, 14))

    # Hide the Play Again button from the UI.
    def hide_retry_button(self):
        self.retry_frame.pack_forget()

    # Wire the Guess button and the Enter key to a handler function.
    def bind_submit(self, handler):
        self.submit_handler = handler
        self.root.bind("<Return>", lambda action: handler())
        self.root.bind("<Key>", self.realKeyBoardClick)

    # Wire the Play Again button to a handler function.
    def bind_retry(self, handler):
        self.retry_btn.config(command=handler)

    def onClick(self, key):
        #disabled
        if self.disableInput:
            return
        
        #based on key
        if key == "ENTER":
            self.submit_handler()
        elif key == "DELETE":
            current = self.entry_var.get()
            self.entry_var.set(current[:-1])
            self.rowWithGuess()
        else:
            current = self.entry_var.get()
            #only allow typing up to puzzle's max letter, then stop accepting more letters
            if len(current) < self.model.word_length:
                self.entry_var.set(current + key)
                self.rowWithGuess()
    
    # manages the keys entered from a real keyboard
    def realKeyBoardClick(self, action):
        #disabled
        if self.disableInput:
            return
        
        enteredKey = action.char.upper()
        if enteredKey.isalpha() and len(enteredKey) == 1:
            current = self.entry_var.get()
            if len(current) < self.model.word_length:
                self.entry_var.set(current + enteredKey)
                self.rowWithGuess()
        elif action.keysym == "BackSpace":
            current = self.entry_var.get()
            self.entry_var.set(current[:-1]) # excludes last character
            self.rowWithGuess()
    

    # to show guess in the grid
    def rowWithGuess(self):
        typedGuess = self.entry_var.get()
        row = self.current_row
        if row >= self.model.MAX_GUESSES:
            return
        for col in range(self.model.word_length):
            if col < len(typedGuess):
                self.cells[row][col].config(text=typedGuess[col], fg="black")
            else:
                self.cells[row][col].config(text="", fg="white")

    #unbind keys
    def cleanUp(self):
        self.root.unbind("<Return>")
        self.root.unbind("<Key>")
        self.puzzle_frame.destroy() #clears the screen of widgets
        