# This is a Python word solver mainly for solving a wordle

# Dictianery used here is created by sujithps 
# under MIT License and can be found in: 
# https://github.com/sujithps/Dictionary/tree/master

# Originally written by mimimaki in 16.11.2024

# MIT License, free to use as you wish

import tkinter as tk
from wordle_solver import WordSolver 
from wordle_solver_app import WordleSolverApp
from anagram_solver import AnagramSolver
from anagram_solver_app import AnagramSolverApp
from hangman_solver import HangmanSolver
from hangman_solver_app import HangmanSolverApp

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True)

        self.label = tk.Label(self.frame, text="Welcome to the Word Solver!\nPick your poison:", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.wordle_button = tk.Button(self.frame, text="Wordle", command=self.start_wordle, font=("Helvetica", 12))
        self.anagram_button = tk.Button(self.frame, text="Anagram", command=self.start_anagram, font=("Helvetica", 12))
        self.hangman_button = tk.Button(self.frame, text="Hangman", command=self.start_hangman, font=("Helvetica", 12))
        self.wordle_button.pack(pady=10)
        self.anagram_button.pack(pady=10)
        self.hangman_button.pack(pady=10)

    def start_wordle(self):
        self.frame.destroy()
        self.start_callback = launch_wordle_app
        self.start_callback()

    def start_anagram(self):
        self.frame.destroy()
        self.start_callback = launch_anagram_app
        self.start_callback()

    def start_hangman(self):
        self.frame.destroy()
        self.start_callback = launch_hangman_app
        self.start_callback()

# Run the Tkinter main loop
if __name__ == "__main__":

    # Start the GUI application
    root = tk.Tk()

    def launch_wordle_app():
        WordleSolverApp(root, WordSolver("../Dictionary/Oxford English Dictionary.txt"))

    def launch_anagram_app():
        AnagramSolverApp(root, AnagramSolver("../Dictionary/Oxford English Dictionary.txt"))
        
    def launch_hangman_app():
        HangmanSolverApp(root, HangmanSolver("../Dictionary/Oxford English Dictionary.txt"))
        
    game = StartScreen(root)

    root.mainloop()