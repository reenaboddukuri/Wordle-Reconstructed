# ─────────────────────────────────────────────────────────────────────────────
# A basic 5-letter Wordle game with Model-View-Controller architecture
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from model import WordleModel
from view import WordleView
from controller import WordleController

def main():
    root = tk.Tk()

    model = WordleModel(target_word="APPLE")  # static word for testing
    view  = WordleView(root, model)
    controller = WordleController(model, view)

    root.mainloop()

if __name__ == "__main__":
    main()
