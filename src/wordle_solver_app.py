import tkinter as tk
from tkinter import StringVar
import ttkbootstrap as ttk

class WordleSolverApp:

    def __init__(self, root, solver):
        self.root = root
        self.solver = solver
        self.root.title("Word solver")

        # Instructions
        self.instructions = ttk.Label(root, text="Enter letters:")
        self.instructions.pack(pady=5)

        self.play_wordle()

    # Focus on next letter
    def on_key(self, event, vars, row, col):

        # Ignore Tab and Backspace since they also move the focus
        if event.keysym in ("BackSpace", "Tab", "ISO_Left_Tab"):
                return

        value = vars[row][col].get()
        
        # Take only 1 character
        if len(value) > 1:
            vars[row][col].set(value[-1])
            value = value[-1]

        # Jump to next letter 
        if (value and (col < 4)):
            if (row == 0):
                self.correct_entries[col+1].focus()
            else:
                self.misplaced_entries[row-1][col+1].focus()
        elif (value and (col == 4) and (row<7)):
                self.misplaced_entries[row][0].focus()

    # Focus on last letter
    def on_backspace(self, event, vars, row, col):

        if (not vars[row][col].get()):
            if (col>0):
                if (row == 0):
                    self.correct_entries[col-1].focus()
                    self.correct_entries[col-1].delete(0, ttk.END)
                else:
                    self.misplaced_entries[row-1][col-1].focus()
                    self.misplaced_entries[row-1][col-1].delete(0, ttk.END)
            elif (col == 0):
                if (row == 1):
                    self.correct_entries[4].focus()
                    self.correct_entries[4].delete(0, ttk.END)
                elif (row > 1):
                    self.misplaced_entries[row-2][4].focus()
                    self.misplaced_entries[row-2][4].delete(0, ttk.END)


    def play_wordle(self):

        # Correct letter entry
        self.correct_frame = ttk.Frame(self.root)
        self.correct_frame.pack(pady=5)
        self.correct_label = ttk.Label(self.correct_frame, text="Known letters:")
        self.correct_label.pack(side=ttk.LEFT, padx=5)
        self.correct_entries = []
        vars = [[None]*5 for i in range(6)]
        for i in range(5):
            var = StringVar()
            entry = ttk.Entry(self.correct_frame, textvariable=var, width=2, justify='center')
            entry.pack(side=ttk.LEFT, padx=2)
            self.correct_entries.append(entry)
            vars[0][i] = var
            entry.bind("<KeyRelease>", lambda e, idx=i: self.on_key(e, vars, 0, idx))
            entry.bind("<BackSpace>", lambda e, idx=i: self.on_backspace(e, vars, 0, idx))
        self.correct_entries[0].focus()

        # Misplaced letters entry 
        self.misplaced_frame = ttk.Frame(self.root)
        self.misplaced_frame.pack(pady=5)
        self.misplaced_label = ttk.Label(self.misplaced_frame, text="Misplaced letters:")
        self.misplaced_label.pack(side=ttk.LEFT, padx=5)
        #self.misplaced_entries = []
        self.misplaced_entries = [[None]*5 for i in range(5)]
        for row in range(1, 6):
            row_frame = ttk.Frame(self.misplaced_frame)
            row_frame.pack(pady=2)
            for col in range(5):
                var = StringVar()
                vars[row][col] = var
                entry = ttk.Entry(row_frame, textvariable=var, width=2, justify='center')
                entry.pack(side=ttk.LEFT, padx=2)
                self.misplaced_entries[row-1][col] = entry
                entry.bind("<KeyRelease>", lambda e, r=row, c=col: self.on_key(e, vars, r, c))
                entry.bind("<BackSpace>", lambda e, r=row, c=col: self.on_backspace(e, vars, r, c))

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
        misplaced = [''.join([entry.get().strip().lower() if entry.get().strip().lower() else '.' for entry in row]) for row in self.misplaced_entries]
        excluded = self.excluded_entry.get().strip().lower()

        # Solve
        self.solver.solve_wordle(correct, misplaced, excluded)
        self.solver.find_odds(correct, misplaced)
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
        for row in self.misplaced_entries:
            for entry in row:
                entry.delete(0, ttk.END)
        self.excluded_entry.delete(0, ttk.END)

        # Clear results
        self.results_list.delete(0, ttk.END)

        # Clear odds 
        self.odds_list.delete(0, ttk.END)