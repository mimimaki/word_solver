import tkinter as tk
import ttkbootstrap as ttk
from tkinter import StringVar

class HangmanSolverApp:

    def __init__(self, root, solver):
        self.root = root
        self.solver = solver
        self.frame = ttk.Frame(root)
        self.root.title("Hangman solver")
        self.frame.pack(expand=True)

        # Ask letter count 
        self.lettercount_frame = ttk.Frame(self.frame)
        self.lettercount_frame.pack(pady=5)
        self.lettercount_label = ttk.Label(self.lettercount_frame, text="How many letters in the word?")
        self.lettercount_label.pack(side=ttk.LEFT, padx=5)
        self.lettercount_entry = ttk.Entry(self.lettercount_frame, width=2, justify='center')
        self.lettercount_entry.pack(side=ttk.LEFT, padx=5)

        self.continnue_button = ttk.Button(self.frame, text="Continue", 
                            command=self.play_hangman)
        self.continnue_button.pack(pady=10)

    # Focus on next letter
    def on_key(self, event, vars, lettercount, idx):

        # Ignore Tab and Backspace since they also move the focus
        if event.keysym in ("BackSpace", "Tab", "ISO_Left_Tab"):
                return

        value = vars[idx].get()
        
        # Take only 1 character
        if len(value) > 1:
            vars[idx].set(value[-1])

        # Jump to next letter 
        if (value and (idx < lettercount-1)):
            self.correct_entries[idx+1].focus()

    # Focus on last letter
    def on_backspace(self, event, vars, idx):
        if (not vars[idx].get() and (idx>0)):
            self.correct_entries[idx-1].focus()
            self.correct_entries[idx-1].delete(0, ttk.END)

    def play_hangman(self):

        # Destroy root and start new
        letter_count = int(self.lettercount_entry.get())
        self.frame.destroy()
        self.lettercount_frame.destroy()
        self.root.title("Hangman solver")
        self.frame = ttk.Frame(self.root)
        self.frame.pack(expand=True)

        # Instructions
        self.instructions = ttk.Label(self.root, text="Enter letters. For unknown letters, enter \".\"")
        self.instructions.pack(pady=5)

        # Correct letter entry
        self.correct_frame = ttk.Frame(self.root)
        self.correct_frame.pack(pady=5)
        self.correct_label = ttk.Label(self.correct_frame, text="Known letters:")
        self.correct_label.pack(side=ttk.LEFT, padx=5)
        self.correct_entries = []
        vars = []
        for i in range(letter_count):
            var = StringVar()
            entry = ttk.Entry(self.correct_frame, textvariable=var, width=2, justify='center')
            entry.pack(side=ttk.LEFT, padx=2)
            self.correct_entries.append(entry)
            vars.append(var)
            entry.bind("<KeyRelease>", lambda e, idx=i: self.on_key(e, vars, letter_count, idx))
            entry.bind("<BackSpace>", lambda e, idx=i: self.on_backspace(e, vars, idx))
        self.correct_entries[0].focus()

        # Excluded letters entry
        self.excluded_frame = ttk.Frame(self.root)
        self.excluded_frame.pack(pady=5)
        self.excluded_label = ttk.Label(self.excluded_frame, text="Excluded letters:")
        self.excluded_label.pack(side=ttk.LEFT, padx=5)
        self.excluded_entry = ttk.Entry(self.excluded_frame, width=10)
        self.excluded_entry.pack(side=ttk.LEFT, padx=5)

        # Solve button
        self.solve_button = ttk.Button(self.root, text="Solve", command=self.solve)
        self.solve_button.pack(pady=10)

        # Clear button
        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear)
        self.clear_button.pack(pady=5)

        # Results list
        self.results_frame = ttk.Frame(self.root)
        self.results_frame.pack(pady=5)
        self.results_label = ttk.Label(self.results_frame, text="Possible words:")
        self.results_label.pack(pady=2)
        self.results_list = tk.Listbox(self.results_frame, width=30, height=10)
        self.results_list.pack()

        # Odds list
        self.odds_frame = ttk.Frame(self.root)
        self.odds_frame.pack(pady=5)
        self.odds_label = ttk.Label(self.odds_frame, text="Most likely letters:")
        self.odds_label.pack(pady=2)
        self.odds_list = tk.Listbox(self.odds_frame, width=30, height=5)
        self.odds_list.pack()

    def solve(self):
        # Get inputs
        correct = ''.join([entry.get().strip().lower() if entry.get().strip() else '.' for entry in self.correct_entries])
        excluded = self.excluded_entry.get().strip().lower()

        # Solve
        self.solver.solve_hangman(correct, excluded)
        self.solver.find_odds(correct)
        results = self.solver.matches
        odds = self.solver.odds

        # Display results
        self.results_list.delete(0, ttk.END)
        if results:
            for word in results:
                self.results_list.insert(ttk.END, word)
        else:
            self.results_list.insert(ttk.END, "There is no possible words in the dictionary")

        # Display odds
        self.odds_list.delete(0, ttk.END)
        if odds:
            # Find 5 most likely letters to display
            likely5 = sorted(odds.items(), key=lambda x: x[1], reverse=True)[:5]
            for letter, odd in likely5:
                self.odds_list.insert(ttk.END, f"{letter}: {odd*100:.2f}%")
        else:
            self.results_list.insert(ttk.END, "There is no possible words in the dictionary")


    def clear(self):
        # Clear inputs
        for entry in self.correct_entries:
            entry.delete(0, ttk.END)
        self.excluded_entry.delete(0, ttk.END)

        # Clear results
        self.results_list.delete(0, ttk.END)

        # Clear odds 
        self.odds_list.delete(0, ttk.END)