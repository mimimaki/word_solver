import tkinter as tk
import ttkbootstrap as ttk

class AnagramSolverApp:

    def __init__(self, root, solver):
        self.root = root
        self.solver = solver
        self.root.title("Anagram solver")

        # Letters entry
        self.letters_frame = ttk.Frame(root)
        self.letters_frame.pack(pady=5)
        self.letters_label = ttk.Label(self.letters_frame, text="Enter letters:")
        self.letters_label.pack(side=ttk.LEFT, padx=5)
        self.letters_entry = ttk.Entry(self.letters_frame, width=10)
        self.letters_entry.pack(side=ttk.LEFT, padx=5)

        # Solve button
        self.solve_button = ttk.Button(root, text="Solve", command=self.solve)
        self.solve_button.pack(pady=10)

        # Clear button
        self.clear_button = ttk.Button(root, text="Clear", command=self.clear)
        self.clear_button.pack(pady=5)

        # Results list
        self.results_frame = ttk.Frame(root)
        self.results_frame.pack(pady=5)
        self.results_label = ttk.Label(self.results_frame, text="Possible words:")
        self.results_label.pack(pady=2)
        self.results_list = tk.Listbox(self.results_frame, width=30, height=10)
        self.results_list.pack()


    def solve(self):
        # Get inputs
        letters = self.letters_entry.get().strip().lower()

        # Solve
        self.solver.solve_anagram(letters)
        results = self.solver.matches

        # Display results
        self.results_list.delete(0, ttk.END)
        if results:
            for word in results:
                self.results_list.insert(ttk.END, word)
        else:
            self.results_list.insert(ttk.END, "There is no possible words in the dictionary")


    def clear(self):
        # Clear inputs
        self.letters_entry.delete(0, ttk.END)

        # Clear results
        self.results_list.delete(0, ttk.END)