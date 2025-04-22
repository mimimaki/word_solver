# This is a Python word solver mainly for solving a wordle

# Dictianery used here is created by sujithps 
# under MIT License and can be found in: 
# https://github.com/sujithps/Dictionary/tree/master

# Originally written by mimimaki in 16.11.2024

# MIT License, free to use as you wish

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from wordle_solver import WordleSolver 
from wordle_solver_app import WordleSolverApp
from anagram_solver import AnagramSolver
from anagram_solver_app import AnagramSolverApp
from hangman_solver import HangmanSolver
from hangman_solver_app import HangmanSolverApp

class WSApp:
    def __init__(self, root):
        self.root = root
        self.startscreen()

    def startscreen(self):
        self.frame = ttk.Frame(root)
        self.frame.pack(expand=True)
        self.label = ttk.Label(self.frame, text="Welcome to the Word Solver!\nPick your poison:")
        self.label.pack(pady=20)
        self.wordle_button = ttk.Button(self.frame, text="Wordle", command=self.start_wordle)
        self.anagram_button = ttk.Button(self.frame, text="Anagram", command=self.start_anagram)
        self.hangman_button = ttk.Button(self.frame, text="Hangman", command=self.start_hangman)
        self.wordle_button.pack(pady=10)
        self.anagram_button.pack(pady=10)
        self.hangman_button.pack(pady=10)

    def moveback(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.start_callback = self.startscreen
        self.start_callback()

    def start_wordle(self):
        self.frame.destroy()
        self.return_frame = ttk.Frame(root)
        self.return_frame.pack(expand=True)
        self.return_button = ttk.Button(self.return_frame, text="Return", command=self.moveback)
        self.return_button.pack(pady=10)
        self.start_callback = launch_wordle_app
        self.start_callback()

    def start_anagram(self):
        self.frame.destroy()
        self.return_frame = ttk.Frame(root)
        self.return_frame.pack(expand=True)
        self.return_button = ttk.Button(self.return_frame, text="Return", command=self.moveback)
        self.return_button.pack(pady=10)
        self.start_callback = launch_anagram_app
        self.start_callback()

    def start_hangman(self):
        self.frame.destroy()
        self.return_frame = ttk.Frame(root)
        self.return_frame.pack(expand=True)
        self.return_button = ttk.Button(self.return_frame, text="Return", command=self.moveback)
        self.return_button.pack(pady=10)
        self.start_callback = launch_hangman_app
        self.start_callback()

# Run the ttk main loop
if __name__ == "__main__":

    # Start the GUI application
    root = ttk.Window(themename="darkly")
    root.title("Word solver")

    def launch_wordle_app():
        WordleSolverApp(root, WordleSolver("../Dictionary/Oxford English Dictionary.txt"))

    def launch_anagram_app():
        AnagramSolverApp(root, AnagramSolver("../Dictionary/Oxford English Dictionary.txt"))
        
    def launch_hangman_app():
        HangmanSolverApp(root, HangmanSolver("../Dictionary/Oxford English Dictionary.txt"))
        
    game = WSApp(root)

    root.mainloop()