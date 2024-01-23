import random

# This function will shuffle the word list, which can be used to shuffle board.
def shuffle(list):
    random.seed(10)
    n = len(list)
    new_list = []
    while len(list) != 0: # randomly select words until list is empty
        ind = random.randint(0, len(list) - 1)
        new_list.append(list[ind])
        list.pop(ind) # remove from original list
    for i in range(n): # since passed by assignment, we must update list
        list.append(new_list.pop())

# This function reads the file
def readFile(filename):
    file = open(filename)
    list = file.readlines()
    words = []  # list of all words
    solution = {}  # dictionary of solution
    for line in range(1, len(list) + 1): # line is line number
        if line % 2 == 1: # odd, 1, 3, 5, 7 (categories)
            category = list[line - 1]
        else:  # even, 2, 4, 6, 8 (words)
            tokens = list[line - 1].split(", ")
            tokens[-1] = tokens[-1].strip()
            solution[category] = set(tokens)
            words.extend(tokens)  # clean up new line character
    return words, solution

# This funtion checks if wordsSelected match a category in solution.
def checkSolution(solution, wordsSelected):
    for category in solution:
        if wordsSelected == solution[category]:
            return category
    return ""

#Welcome user

print('Connections')
print('Group words that share a common thread.')

name = input('Enter your name:')

print(' Welcome,', name + '!')

input('Press enter to start: ')

#input number of the day and read the file
num_day = input('Enter number (0-6): ')
gameboard, solution = readFile(f"Day{num_day}.txt")

#pass the gameboard to the shuffle function
shuffle(gameboard)

# Output the shuffled game board
print("\nCreate four groups of four!")
for i in range(0, len(gameboard), 4):
    group = gameboard[i:i + 4]
    group = [word.upper() for word in group]
    print("| {:<10} | {:<10} | {:<10} | {:<10} |".format(*group))

categories_found = set()

#repeating until all categories are found

while len(categories_found) < len(solution):
    #input words
    word1 = input('\nEnter first word: \n').lower()
    word2 = input('Enter second word: \n').lower()
    word3 = input('Enter third word: \n').lower()
    word4 = input('Enter four word: \n').lower()

    words_list = [word1, word2, word3, word4]
    words_selected = set(words_list)


    # Matching Check 
    category_found = checkSolution(solution, words_selected)
    category_found = category_found.strip()

    # Output the results
    if category_found and category_found not in categories_found:
        categories_found.add(category_found)


        # Remove the found words from the game board
        for word in words_selected:
            gameboard.remove(word)

        # Output updated game board
        print("\nUpdated game board:")

        
        for i in range(0, len(gameboard), 4):
            group = gameboard[i:i + 4]
            print("| {:<10} | {:<10} | {:<10} | {:<10} |".format(*group))
            
            
        # Output found categories
        if categories_found:
            
            for cat in categories_found:
                print(cat.upper())

            
    elif not category_found:
        print("\nNo category found for the selected words. Try again.")


print("\nCongratulations! You have found all categories.")
