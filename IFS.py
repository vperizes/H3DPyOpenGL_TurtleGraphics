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
points = []  # each coordinate that we generate in draw_turtle will be stored here and read by draw_points
x = 0
y = 0


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


def move_to(pos):
    global current_position
    current_position = (pos[0], pos[1])

def draw_points():
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()

def reset_turtle():
    global current_position
    global direction
    current_position = (0, 0)
    direction = np.array([0, 1, 0])


# this now defines how we update x, y using the initial point of (0,0) defined above
def draw_turtle():
    global x, y
    points.append((x, y))
    r = np.random.rand()  # generates a num between 0 and 1
    if r < 0.1:
        x, y = 0.00 * x + 0.00 * y + 0.00, 0.00 * x + 0.16 * y + 0.00
    elif r < 0.86:
        x, y = 0.85 * x + 0.04 * y + 0.00, -0.04 * x + 0.85 * y + 1.6
    elif r < 0.93:
        x, y = 0.2 * x - 0.26 * y + 0.00, 0.23 * x + 0.22 * y + 1.6
    else:
        x, y = -0.15 * x + 0.28 * y + 0.00, 0.26 * x + 0.24 * y + 0.44


init_ortho()
done = False
glPointSize(1)
glColor3f(0, 1, 0)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glScaled(80, 80, 1)  # this is scaling our points. Could also change ortho values for same effect
    glBegin(GL_POINTS)
    glVertex2f(0, 0)
    glEnd()
    reset_turtle()  # need to reset the position in the loop so that after glClear our turtle gets reset to 0,0
    # and we see a line
    draw_turtle()  # this is looping around and creating different point
    draw_points()
    pygame.display.flip()
    pygame.time.wait(1)
pygame.quit()