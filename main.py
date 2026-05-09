# A Wordle game using Model-View-Controller desgin pattern

import tkinter as tk
from model import WordleModel
from view import WordleView
from controller import WordleController
from tkinter import font
import random

# Reading words from a word list
def wordList(filepath):
    with open(filepath, "r") as f:
        return [row.strip() for row in f if row.strip()]


# Play the select length puzzle
def play_puzzle(root, word_length):
    if word_length == 5:
        words = wordList("words.txt")
    else:
        words = wordList("words6.txt")
    
    targetWord = random.choice(words)
    model = WordleModel(target_word=targetWord, valid_words=words, word_length=word_length)
    view  = WordleView(root, model)
    controller = WordleController(model, view, words, back=lambda: home_page(root))

# Shows wordle home page
def home_page(root):
    # Title bar
    title_font = font.Font(family="Helvetica", size=24, weight="bold")
    heading_font = font.Font(family="Helvetica", size=12)
    button_font = font.Font(family="Helvetica", size=14, weight="bold")

    option_frame = tk.Frame(root, bg="#f7f1df")
    option_frame.pack(expand=True)

    tk.Label(option_frame, text = "W O R D L E", font=title_font, bg="#f7f1df", fg="black").pack(pady=(30, 8))
    tk.Label(option_frame, text = "Choose word length:", font=heading_font, bg="#f7f1df", fg="black").pack(pady=(24, 16))

    button_frame = tk.Frame(option_frame, bg="#f7f1df")
    button_frame.pack(pady=10)

    def selectGame(length):
        option_frame.destroy() #removes frame from screen
        play_puzzle(root, length)
    
    button_five = tk.Label(button_frame, text="5 letters", font=button_font, bg="#6aaa63", fg="white", padx=24, pady=14)
    button_five.pack(side="left", padx=12)
    button_five.bind("<Button-1>", lambda e: selectGame(5))

    button_six = tk.Label(button_frame, text="6 letters", font=button_font, bg="#6aaa63", fg="white", padx=24, pady=14)
    button_six.pack(side="left", padx=12)
    button_six.bind("<Button-1>", lambda e: selectGame(6))

def main():
    root = tk.Tk()
    root.title("Wordle")
    root.minsize(480, 680)
    root.config(bg = "#f7f1df")

    home_page(root) #passing root config to home page function
    root.mainloop()

if __name__ == "__main__":
    main()
