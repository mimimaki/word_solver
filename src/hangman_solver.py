# This is a Python word solver for solving a hangman

# Dictianery used here is created by sujithps 
# under MIT License and can be found in: 
# https://github.com/sujithps/Dictionary/tree/master

# Originally written by mimimaki in 16.11.2024

# MIT License, free to use as you wish

import re
import string
from collections import Counter 

class HangmanSolver:

    def __init__(self, filepath):
        self.filepath = filepath
        self.dictionary = self.parse_dict()
        self.odds = []

    def parse_dict(self):
        # There is explanations and usage examples we want to remove
        parsed_dict= []

        # Parse 
        with open(self.filepath, 'r') as file:
            for line in file:
                if (len(line.split())>0):
                    word = line.split()[0].lower()
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

        excluded = input("Write discarded letters: \n").lower()

        return correct, excluded

    # search from dict 
    def solve_hangman(self, correct, excluded):

        # find words matching correct letters
        matches = [word for word in self.dictionary if re.fullmatch(correct, word)]

        # remove words with excluded letters
        for word in matches:
            if any(disc in word for disc in excluded):
                matches = list(filter(lambda item: item != word, matches))

        counts = Counter(correct)
        if '.' in counts:
            del counts['.']
        final_matches = []

        for word in matches:
            word_count = Counter(word)
            if all(word_count[char] == counts[char] for char in counts):
                final_matches.append(word)

        self.matches = final_matches

    # Calculate the odds of the next letter
    def find_odds(self, correct):

        # Use matches to find most likely letter
        words = self.matches    
        used = ''.join(correct)
        used = used.replace('.', '')
                          
        # Count all letters in all words minus used letters
        counter = {letter: 0 for letter in string.ascii_lowercase}
        for word in words:
            for letter in word:
                if letter in counter:
                    counter[letter] += 1
            for letter in used:
                if letter in counter:
                    counter[letter] = 0

        # Cleaning
        filtered_counter = {letter: 0 for letter in string.ascii_lowercase}
        for letter, count in counter.items():
            remaining = count
            if remaining > 0:
                filtered_counter[letter] = remaining

        total = sum(filtered_counter.values())

        # Return odds
        self.odds = {letter: (count/total) if total>0 else 0 for letter, count in filtered_counter.items()}