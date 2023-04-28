import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *

pygame.init()

screen_width = 800
screen_height = 800
ortho_left = -400
ortho_right = 400
ortho_top = -400
ortho_bottom = 400

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Turtle Graphics')


# turtle graphics limits movement to the forward direction so if you want to change direction you must first rotate
# the turtle then move it forward
current_position = (0, 0)
direction = np.array([0, 1, 0])  # turtle facing in y-dir. This is the orientation of the turtle
points = []  # each coordinate that we generate in draw_turtle will be stored here and read by draw_points
x = 0
y = 0


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


# this now defines how we update x, y using the initial point of (0,0) defined above
def draw_turtle():
    global x, y

    points.append((x, y))
    r = np.random.rand()  # generates a num between 0 and 1
    if r < 0.33:
        x, y = 0.50 * x + 0.00 * y + 0.00, 0.00 * x + 0.50 * y + 0.50
    elif r < 0.66:
        x, y = 0.50 * x + 0.00 * y + 0.50, 0.00 * x + 0.50 * y + 0.00
    else:
        x, y = 0.50 * x + 0.00 * y + 0.00, 0.00 * x + 0.50 * y + 0.00


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
    glTranslate(-100, -50, 0)
    glScaled(300, 300, 1)
    draw_turtle()  # this is looping around and creating different point
    draw_points()
    pygame.display.flip()
    pygame.time.wait(1)
pygame.quit()
