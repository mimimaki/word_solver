import tkinter as tk

class HangmanSolverApp:

    def __init__(self, root, solver):
        self.root = root
        self.solver = solver
        self.frame = tk.Frame(root)
        self.root.title("Hangman solver")
        self.frame.pack(expand=True)

        # Ask letter count 
        self.lettercount_frame = tk.Frame(root)
        self.lettercount_frame.pack(pady=5)
        self.lettercount_label = tk.Label(self.lettercount_frame, text="How many letters in the word?")
        self.lettercount_label.pack(side=tk.LEFT, padx=5)
        self.lettercount_entry = tk.Entry(self.lettercount_frame, width=2, justify='center')
        self.lettercount_entry.pack(side=tk.LEFT, padx=5)

        self.continnue_button = tk.Button(self.frame, text="Continue", 
                            command=self.play_hangman,
                            font=("Helvetica", 12))
        self.continnue_button.pack(pady=10)

    def play_hangman(self):

        # Destroy root and start new
        letter_count = int(self.lettercount_entry.get())
        self.frame.destroy()
        self.lettercount_frame.destroy()
        self.root.title("Hangman solver")
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)

        # Instructions
        self.instructions = tk.Label(self.root, text="Enter letters. For unknown letters, enter \".\"")
        self.instructions.pack(pady=5)

        # Correct letter entry
        self.correct_frame = tk.Frame(self.root)
        self.correct_frame.pack(pady=5)
        self.correct_label = tk.Label(self.correct_frame, text="Known letters:")
        self.correct_label.pack(side=tk.LEFT, padx=5)
        self.correct_entries = []
        for _ in range(letter_count):
            entry = tk.Entry(self.correct_frame, width=2, justify='center')
            entry.pack(side=tk.LEFT, padx=2)
            self.correct_entries.append(entry)

        # Excluded letters entry
        self.excluded_frame = tk.Frame(self.root)
        self.excluded_frame.pack(pady=5)
        self.excluded_label = tk.Label(self.excluded_frame, text="Excluded letters:")
        self.excluded_label.pack(side=tk.LEFT, padx=5)
        self.excluded_entry = tk.Entry(self.excluded_frame, width=10)
        self.excluded_entry.pack(side=tk.LEFT, padx=5)

        # Solve button
        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        self.solve_button.pack(pady=10)

        # Clear button
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        self.clear_button.pack(pady=5)

        # Results list
        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(pady=5)
        self.results_label = tk.Label(self.results_frame, text="Possible words:")
        self.results_label.pack(pady=2)
        self.results_list = tk.Listbox(self.results_frame, width=30, height=10)
        self.results_list.pack()

        # Odds list
        self.odds_frame = tk.Frame(self.root)
        self.odds_frame.pack(pady=5)
        self.odds_label = tk.Label(self.odds_frame, text="Most likely letters:")
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
        self.excluded_entry.delete(0, tk.END)

        # Clear results
        self.results_list.delete(0, tk.END)

        # Clear odds 
        self.odds_list.delete(0, tk.END)