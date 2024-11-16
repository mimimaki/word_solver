# This is a Python word solver mainly for solving a wordle

# Dictianery used here is created by sujithps 
# under MIT License and can be found in: 
# https://github.com/sujithps/Dictionary/tree/master

# Originally written by mimimaki in 16.11.2024

# MIT License, free to use as you wish
import re

def parse_dict(filepath):
    # There is explanations and usage examples we want to remove
    parsed_dict= []

    # Wordle is played with 5 letter words only
    with open(filepath, 'r') as file:
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

def ask_input():
    # Ask input from user
    # position known, correct letter, discarded letter

    green = input("Write each known letters in its place or \".\" if not known: \n").lower()
    yellow = []
    row = "init"
    while (row!=""):
        row = input("Write known letters on positions they can't be or \".\" if there is none: \n").lower()
        if (len(row)!=0):
            yellow.append(row)

    discarded = input("Write discarded letters: \n").lower()

    return green, yellow, discarded

# search from dict 
def solve_wordle(dict, green, yellow, discarded):

    # find words matching green letters
    matches = [word for word in dict if re.fullmatch(green, word)]

    # remove words with discarded letters
    for word in matches:
        if any(disc in word for disc in discarded):
            matches = list(filter(lambda item: item != word, matches))

    # find positions of yellow letters
    misses = []
    for miss in yellow:
        misses.extend([(char, i) for i, char in enumerate(miss) if char != '.'])

    # find words with yellow letters elsewhere
    for word in matches:
        for letter, not_pos in misses:
            if (letter not in word or (word[not_pos] == letter)):
                matches = list(filter(lambda item: item != word, matches))
                break

    return matches 

if __name__=="__main__":

    dict = parse_dict(filepath="../Dictionary/Oxford English Dictionary.txt")

    puzzle = input("Hello. Hit <ENTER> to find your word. ").lower()
    while True:
        green, yellow, discarded = ask_input()
        dict = solve_wordle(dict, green, yellow, discarded)
        if (len(dict)==0):
            print("There is no possible words in the dictionary")
            break
        else:
            print("Here are the possible words:", dict)
            cont = input("Continue? y/n     ").lower()
            if (cont == "no" or cont == "n"):
                break