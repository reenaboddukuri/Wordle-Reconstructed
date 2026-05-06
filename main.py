#A basic 5-letter Wordle game using Model-View-Controller architecture

import tkinter as tk
from model import WordleModel
from view import WordleView
from controller import WordleController
import random

#reading words from the word list
def wordList(filepath="words.txt"):
    with open(filepath, "r") as f:
        return [row.strip() for row in f if row.strip()]

def main():
    root = tk.Tk()
    words = wordList()
    targetWord = random.choice(words)

    model = WordleModel(target_word=targetWord)
    view  = WordleView(root, model)
    controller = WordleController(model, view, words)

    root.mainloop()

if __name__ == "__main__":
    main()
