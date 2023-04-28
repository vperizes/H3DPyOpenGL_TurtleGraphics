import math

import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *

pygame.init()

screen_width = 800
screen_height = 800
ortho_left = -400
ortho_right = 400
ortho_top = 0
ortho_bottom = 800

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Turtle Graphics')


# turtle graphics limits movement to the forward direction so if you want to change direction you must first rotate
# the turtle then move it forward
current_position = (0, 0)
direction = np.array([0, 1, 0])  # turtle facing in y-dir. This is the orientation of the turtle

axiom = 'X'
rule = {
    "F": "FF",
    "X": "F+[-F-XF-X][+FF][--XF[+X]][++F-X]"
}

draw_length = 5  # unit for which turtle moves forward
angle = 10
stack = []  # where we store push and pop for commands
rule_run_number = 5  # this is the number of iterations for the L-system
instructions = ""  # this is where we are storing our iterations


# this method represents an L-system
def run_rule(run_count):
    global instructions
    instructions = axiom
    for loops in range(run_count):
        old_system = instructions  # this identifies the previous iteration of the rule as the "old system" and uses it
        # as an input for the next iteration
        instructions = ""  # reset to an empty string
        for character in range(0, len(old_system)):
            if old_system[character] in rule:
                instructions += rule[old_system[character]]  # if the character is an F this will index into 'rule'
                # to replace F with the rule
            else:
                instructions += old_system[character]  # this compensates for the square brackets
    print("Rule")
    print(instructions)



def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_left, ortho_right, ortho_top, ortho_bottom)


# this method draws a line to input coordinates (x, y). "turtle" moves to input coords
def line_to(x, y):
    global current_position
    glBegin(GL_LINE_STRIP)
    glVertex2f(current_position[0], current_position[1])
    glVertex2f(x, y)
    current_position = (x, y)
    glEnd()


def move_to(pos):
    global current_position
    current_position = (pos[0], pos[1])

def reset_turtle():
    global current_position
    global direction
    current_position = (0, 0)
    direction = np.array([0, 1, 0])


def draw_turtle():
    global direction
    for character in range(0, len(instructions)):  # allows us to loop through each iteration of instructions in the
        # run_rule method and use those to direct the turtle
        if instructions[character] == 'F':
            forward(draw_length)
        elif instructions[character] == '+':
            rotate(angle)
        elif instructions[character] == '-':
            rotate(-angle)
        elif instructions[character] == '[':
            stack.append((current_position, direction))
        elif instructions[character] == ']':
            current_vector = stack.pop()  # removes the last element added to the stack
            move_to(current_vector[0])
            direction = current_vector[1]


def forward(draw_length):
    new_x = current_position[0] + direction[0] * draw_length
    new_y = current_position[1] + direction[1] * draw_length
    line_to(new_x, new_y)


def rotate(angle):
    global direction
    direction = z_rotation(direction, math.radians(angle))


init_ortho()
done = False
glLineWidth(1)
run_rule(rule_run_number)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glBegin(GL_POINTS)
    glVertex2f(0, 0)
    glEnd()
    reset_turtle()  # need to reset the position in the loop so that after glClear our turtle gets reset to 0,0
    # and we see a line
    draw_turtle()
    pygame.display.flip()
pygame.quit()

