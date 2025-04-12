import tkinter as tk

class WordleSolverApp:

    def __init__(self, root, solver):
        self.root = root
        self.solver = solver
        self.root.title("Word solver")

        # Instructions
        self.instructions = tk.Label(root, text="Enter letters:")
        self.instructions.pack(pady=5)

        # Correct letter entry
        self.correct_frame = tk.Frame(root)
        self.correct_frame.pack(pady=5)
        self.correct_label = tk.Label(self.correct_frame, text="Known letters:")
        self.correct_label.pack(side=tk.LEFT, padx=5)
        self.correct_entries = []
        for _ in range(5):
            entry = tk.Entry(self.correct_frame, width=2, justify='center')
            entry.pack(side=tk.LEFT, padx=2)
            self.correct_entries.append(entry)

        # Misplaced letters entry 
        self.misplaced_frame = tk.Frame(root)
        self.misplaced_frame.pack(pady=5)
        self.misplaced_label = tk.Label(self.misplaced_frame, text="Misplaced letters:")
        self.misplaced_label.pack(side=tk.LEFT, padx=5)
        self.misplaced_entries = []
        for _ in range(5):
            row_frame = tk.Frame(self.misplaced_frame)
            row_frame.pack(pady=2)
            row_entries = []
            for _ in range(5):
                entry = tk.Entry(row_frame, width=2, justify='center')
                entry.pack(side=tk.LEFT, padx=2)
                row_entries.append(entry)
            self.misplaced_entries.append(row_entries)

        # Excluded letters entry
        self.excluded_frame = tk.Frame(root)
        self.excluded_frame.pack(pady=5)
        self.excluded_label = tk.Label(self.excluded_frame, text="Excluded letters:")
        self.excluded_label.pack(side=tk.LEFT, padx=5)
        self.excluded_entry = tk.Entry(self.excluded_frame, width=10)
        self.excluded_entry.pack(side=tk.LEFT, padx=5)

        # Solve button
        self.solve_button = tk.Button(root, text="Solve", command=self.solve)
        self.solve_button.pack(pady=10)

        # Clear button
        self.clear_button = tk.Button(root, text="Clear", command=self.clear)
        self.clear_button.pack(pady=5)

        # Results list
        self.results_frame = tk.Frame(root)
        self.results_frame.pack(pady=5)
        self.results_label = tk.Label(self.results_frame, text="Possible words:")
        self.results_label.pack(pady=2)
        self.results_list = tk.Listbox(self.results_frame, width=30, height=10)
        self.results_list.pack()

        # Odds list
        self.odds_frame = tk.Frame(root)
        self.odds_frame.pack(pady=5)
        self.odds_label = tk.Label(self.odds_frame, text="Most likely letters:")
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
        self.results_list.delete(0, tk.END)
        if results:
            for word in results:
                self.results_list.insert(tk.END, word)
        else:
            self.results_list.insert(tk.END, "There is no possible words in the dictionary")

        # Display odds
        self.odds_list.delete(0, tk.END)
        if odds:
            # Find 5 most likely letters to display
            likely5 = sorted(odds.items(), key=lambda x: x[1], reverse=True)[:5]
            for letter, odd in likely5:
                self.odds_list.insert(tk.END, f"{letter}: {odd*100:.2f}%")
        else:
            self.results_list.insert(tk.END, "There is no possible words in the dictionary")


    def clear(self):
        # Clear inputs
        for entry in self.correct_entries:
            entry.delete(0, tk.END)
        for row in self.misplaced_entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.excluded_entry.delete(0, tk.END)

        # Clear results
        self.results_list.delete(0, tk.END)

        # Clear odds 
        self.odds_list.delete(0, tk.END)