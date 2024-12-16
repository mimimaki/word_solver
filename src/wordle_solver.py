# This is a Python word solver mainly for solving a wordle

# Dictianery used here is created by sujithps 
# under MIT License and can be found in: 
# https://github.com/sujithps/Dictionary/tree/master

# Originally written by mimimaki in 16.11.2024

# MIT License, free to use as you wish

import re

class WordSolver:

    def __init__(self, filepath):
        self.filepath = filepath
        self.dictionary = self.parse_dict()

    def parse_dict(self):
        # There is explanations and usage examples we want to remove
        parsed_dict= []

        # Word is played with 5 letter words only
        with open(self.filepath, 'r') as file:
            for line in file:
                if (len(line.split())>0):
                    word = line.split()[0].lower()
                    if (len(word)==5):
                        parsed_dict.append(word)

        # The Oxford English Dictionary includes words with numbers and slashes, remove them
        parsed_dict = [word for word in parsed_dict if not re.search(r"[0-9\-]", word)]

        # This gets rid of duplicates
        parsed_dict = list(set(parsed_dict))

        # Create a new file for the parsed dictionary
        with open("parsed_dict.txt", 'w') as file:
            for word in parsed_dict:
                file.write(word + '\n')

        return parsed_dict

    def ask_input(self):
        # Ask input from user
        # position known, correct letter, excluded letter

        correct = input("Write each known letters in its place or \".\" if not known: \n").lower()
        misplaced = []
        row = "init"
        while (row!=""):
            row = input("Write known letters on positions they can't be or \".\" if there is none: \n").lower()
            if (len(row)!=0):
                misplaced.append(row)

        excluded = input("Write discarded letters: \n").lower()

        return correct, misplaced, excluded

    # search from dict 
    def solve_wordle(self, correct, misplaced, excluded):

        # find words matching correct letters
        matches = [word for word in self.dictionary if re.fullmatch(correct, word)]

        # remove words with excluded letters
        for word in matches:
            if any(disc in word for disc in excluded):
                matches = list(filter(lambda item: item != word, matches))

        # find positions of misplaced letters
        misses = []
        for miss in misplaced:
            misses.extend([(char, i) for i, char in enumerate(miss) if char != '.'])

        # find words with misplaced letters elsewhere
        for word in matches:
            for letter, not_pos in misses:
                if (letter not in word or (word[not_pos] == letter)):
                    matches = list(filter(lambda item: item != word, matches))
                    break

        self.matches = matches

if __name__=="__main__":

    self = WordSolver("../Dictionary/Oxford English Dictionary.txt")

    puzzle = input("Hello. Hit <ENTER> to find your word. ").lower()
    while True:
        correct, misplaced, excluded = self.ask_input()
        self.solve_wordle(correct, misplaced, excluded)
        if (len(self.matches)==0):
            print("There is no possible words in the dictionary")
            break
        else:
            print("Here are the possible words:", dict)
            cont = input("Continue? y/n     ").lower()
            if (cont == "no" or cont == "n"):
                break