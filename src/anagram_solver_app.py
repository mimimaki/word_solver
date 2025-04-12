import tkinter as tk

class AnagramSolverApp:

    def __init__(self, root, solver):
        self.root = root
        self.solver = solver
        self.root.title("Anagram solver")

        # Letters entry
        self.letters_frame = tk.Frame(root)
        self.letters_frame.pack(pady=5)
        self.letters_label = tk.Label(self.letters_frame, text="Enter letters:")
        self.letters_label.pack(side=tk.LEFT, padx=5)
        self.letters_entry = tk.Entry(self.letters_frame, width=10)
        self.letters_entry.pack(side=tk.LEFT, padx=5)

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


    def solve(self):
        # Get inputs
        letters = self.letters_entry.get().strip().lower()

        # Solve
        self.solver.solve_anagram(letters)
        results = self.solver.matches

        # Display results
        self.results_list.delete(0, tk.END)
        if results:
            for word in results:
                self.results_list.insert(tk.END, word)
        else:
            self.results_list.insert(tk.END, "There is no possible words in the dictionary")


    def clear(self):
        # Clear inputs
        self.letters_entry.delete(0, tk.END)

        # Clear results
        self.results_list.delete(0, tk.END)