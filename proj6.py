# You will need this function to write this milestone 
# but you will also need the code you wrote from Milestone #1

# This function reads in data from the file named filename.
# (e.g. words, solution = readFile("Day0.txt")
# sets up list of words and solution for Day 0 board
# INPUT:
# filename - a string, e.g. "Day0.txt."
# OUTPUTS:
# words - a list of words (strings) that will make up the 4 by 4 gameboard
# solution - a dictionary of the solution, e.g. solution = {"data types": {"int",
# "float", "string", "boolean"}, ...}
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


#------------------------------------------

import turtle
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BOX_SIZE = 100
NUM_BOXES = 16
SELECT_LIMIT = 4
MISTAKES_ALLOWED = 3

# Constants for grid and box dimensions
GRID_SIZE = 4
SPACE_BETWEEN_BOXES = 10  # Adjust the space between boxes
FONT_SIZE = 12

# Function to draw a box with a word
def draw_word_box(t, x, y, text, color="lightgray"):
    t.penup()
    t.goto(x - BOX_SIZE / 2, y - BOX_SIZE / 2)
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(BOX_SIZE)
        t.left(90)
    t.end_fill()
    t.goto(x, y - FONT_SIZE//2)
    write_text(t, text, "black")

# Function to write text
def write_text(t, text, color):
    t.color(color)
    t.write(text, align='center', font=('Arial', FONT_SIZE, 'bold'))

# Function to draw the submit button
def draw_button(t, x, y, text, color="gray"):
    t.penup()
    t.goto(x - 100, y - 25)
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(200)
        t.left(90)
        t.forward(50)
        t.left(90)
    t.end_fill()
    t.goto(x, y - 12)
    write_text(t, text, "white")

# Update the mistakes remaining display
def update_mistakes_display():
    mistakes_display.clear()
    draw_button(mistakes_display, 0, -350, f"Mistakes Remaining: {mistakes_left}", "red")

# Handle click events
def handle_click(x, y):
    # Check if the submit button is clicked
    if -100 <= x <= 100 and -210 <= y <= -160:
        if selected_count == SELECT_LIMIT:
            check_selected_words()
        return

    # Determine which word box was clicked
    for i, (bx, by) in enumerate(box_positions):
        if bx - BOX_SIZE/2 <= x <= bx + BOX_SIZE/2 and by - BOX_SIZE/2 <= y <= by + BOX_SIZE/2:
            toggle_word_selection(i, bx, by)
            break
    update_button_state()

# Toggle the selection state of a word box
def toggle_word_selection(index, bx, by):
    global selected_count 
    word = words[index]
    if selected[index]:
        selected[index] = False
        selected_words.remove(word)
        selected_count -= 1
        draw_word_box(turtles[index], bx, by, word)
    elif not selected[index] and selected_count < SELECT_LIMIT:
        selected[index] = True
        selected_words.add(word)
        selected_count += 1
        draw_word_box(turtles[index], bx, by, word, "blue")
        
# This funtion checks if wordsSelected match a category in solution.
def checkSolution(solution, wordsSelected):
    for category in solution:
        if wordsSelected == solution[category]:
            return category
    return ""

# Check the selected words against the solution
def check_selected_words():
    global mistakes_left
    found_category = checkSolution(solution, selected_words)
    if found_category:
        banner("You found a category:", found_category)
    else:
        mistakes_left -= 1
        update_mistakes_display()
        if mistakes_left <= 0:
            banner("You lost!")
            turtle.bye()

# Display a banner message on the screen
def banner(message, category=""):
    turtle.penup()
    turtle.goto(0, 0)
    turtle.color("black")
    turtle.write(message + " " + category, align="center", font=("Arial", 24, "bold"))


# Update the submit button based on the number of selected words
def update_button_state():
    if selected_count == SELECT_LIMIT:
        draw_button(submit_button, 0, -190, "Submit", "blue")
    else:
        draw_button(submit_button, 0, -190, "Submit")

# Main setup for turtle graphics
screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
words, solution = readFile("Day0.txt")
random.shuffle(words) 
selected = [False] * NUM_BOXES
selected_words = set()
selected_count = 0
mistakes_left = MISTAKES_ALLOWED

# Prepare turtles for each word box
turtles = [turtle.Turtle() for _ in range(NUM_BOXES)]
box_positions = [(-300 + (i % 4) * 200, 200 - (i // 4) * 150) for i in range(NUM_BOXES)]
for i, t in enumerate(turtles):
    t.speed(0)
    t.hideturtle()
    draw_word_box(t, box_positions[i][0], box_positions[i][1], words[i])

# Submit button
submit_button = turtle.Turtle()
submit_button.speed(0)
submit_button.hideturtle()
draw_button(submit_button, 0, -190, "Submit")

# Mistakes display
mistakes_display = turtle.Turtle()
mistakes_display.speed(0)
mistakes_display.hideturtle()
update_mistakes_display()

# Listen to click events
screen.onclick(handle_click)

# Start the game
turtle.mainloop()