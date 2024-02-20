"""
    gerrymandering.py
    Project 3 - Gerrymandering

    A module allowing to create a panel of one state votes distibution
    based on Democrats vs. Republicans percentages and the number of districts. 

    Created by Kaito Sekiya on 08/06/23.
    Copyright © 2023 Shanon Reckinger. All rights reserved.
"""

import turtle


def draw_rectangle(t, length, width, color):
    """
        draw_rectangle

        Draws a rectangle with the given length, width and color.
        
        @param t: The Turtle object used to draw the rectangle
        @type t: Turtle
        @param length: The length of the rectangle to draw
        @type length: int
        @param width: The width of the rectangle to draw
        @type width: int
        @param color: The name of the color
        @type color: string
        @return: Nothing
        @rtype: void
    """
    # Set color
    t.color(color)
    t.fillcolor(color)
    t.pendown()

    # Draw and fill a rectangle
    t.begin_fill()
    for i in range(2):
        t.forward(length)
        t.right(90)
        t.forward(width)
        t.right(90)
    t.end_fill()

    # Move forward to the next move 
    t.forward(length)
    t.penup()


def draw_bar(t, dem_percent, rep_percent, districts_num):
    """
        draw_bar

        Draws a bar with the given Democrats vs. Republicans percentages.
        The width of the bar depends on the number of the districts
        
        @param t: The Turtle object used to draw the bar
        @type t: Turtle
        @param dem_percent: The percentage of the Democrats votes
        @type length: int
        @param rep_percent: The percentage of the Republican votes
        @type width: int
        @param districts_num: The number of the districts
        @type districts_num: int
        @return: Nothing
        @rtype: void
    """
    # Honestly, I do not remember this part
    t.right(90)
    t.forward(500)
    t.left(180)
    
    # Set the bar width based the number of the districts
    # More districts, thinner the bar
    if districts_num > 47:
        width = 4
    elif districts_num > 31:
        width = 5
    elif districts_num > 23:
        width = 10
    elif districts_num > 15:
        width = 15
    elif districts_num > 9:
        width = 25
    else:
        width = 45

    # Draw two rectangle for both Dem and Rep which will form a bar together
    draw_rectangle(t, 500 * dem_percent / 100, width, "blue") # Dems are blue
    draw_rectangle(t, 500 * rep_percent / 100, width, "red") # Reps are red

    # Move forward to the next move 
    t.right(90)
    t.forward(width + 5)


def draw_panel(eligible_voters, percents, districts_num):
    """
        draw_panel

        Draws a panel of one state votes distibution based on
        Democrats vs. Republicans percentages and the number of districts. 
        
        @param eligible_voters: The state name and the number of eligible voters
        @type eligible_voters: list
        @param percents: 
        @type percents: list of tuples
        @param districts_num: The number of the districts
        @type districts_num: int
        @return: Nothing
        @rtype: void
    """
    # Hide inital Turtle
    turtle.hideturtle()
    # Set the window title
    turtle.title("Gerrymandering Panel")

    # Set up a turtle
    t = turtle.Turtle()
    t.hideturtle()
    t.color("black")
    t.speed(0)
    t.penup()

    # Set up a screen
    screen = turtle.getscreen()
    screen.setup(500, 500)
    screen.colormode(255)
    screen.bgcolor("white")

    t.forward(250)
    t.left(90)
    t.forward(230)

    # Draw a panel body
    t.pendown()
    t.left(90) 
    t.forward(250)
    t.left(90)
    t.forward(480)
    t.left(180)
    t.forward(510)
    t.left(180)
    t.forward(30)
    t.right(90)
    t.forward(250)
    t.penup()

    t.right(180)
    t.forward(10)

    # Write the state name at the top left corner
    t.write(eligible_voters[0], move=False, align="left", font=("Times New Roman", 14, "normal"))
    t.forward(475)
    # Write the number of eligible voters at the top right corner
    t.write(str(eligible_voters[1].strip()) + " eligible voters", move=False, align="right", font=("Times New Roman", 14, "normal"))

    # Move to the position to draw bars
    t.forward(15)
    t.right(90)
    t.forward(5)

    # Draw bars
    for dem_percent, rep_percent in percents:
        draw_bar(t, dem_percent, rep_percent, districts_num)

    # Close the panel on screen click
    turtle.exitonclick()