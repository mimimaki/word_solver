# This is a Python anagram solver

# Dictianery used here is created by sujithps 
# under MIT License and can be found in: 
# https://github.com/sujithps/Dictionary/tree/master

# Originally written by mimimaki in 16.11.2024

# MIT License, free to use as you wish

import re
from collections import Counter

class AnagramSolver:

    def __init__(self, filepath):
        self.filepath = filepath
        self.dictionary = self.parse_dict()
        self.odds = []

    def parse_dict(self):
        # There is explanations and usage examples we want to remove
        parsed_dict= []

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

        letters = input("Give the letters for your anagram: \n").lower()

        return letters

    # search from dict 
    def solve_anagram(self, letters):

        letters_count = Counter(letters.lower())
        anagrams = []

        # Search for equal lenght and check for letters
        for word in self.dictionary:
            if (len(word) == len(letters.lower())):
                if (Counter(word) == letters_count):
                    anagrams.append(word) 

        self.matches = anagrams