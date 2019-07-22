import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math import floor, ceil, fabs


class GoalPost:
    def __init__(self):
        self.TopRightVertex = (3.6, 2.4, -11)
        self.TopLeftVertex = (-3.6, 2.4, -11)
        self.BottomLeftVertex = (-3.6, 0, -11)
        self.BottomRightVertex = (3.6, 0, -11)
        self.Vertices = (self.TopRightVertex,
                         self.TopLeftVertex,
                         self.BottomLeftVertex,
                         self.BottomRightVertex)
        self.Edges = (
            (0, 1),
            (0, 3),
            (1, 2)
        )

    def draw(self):
        glBegin(GL_LINES)
        glColor3fv((1, 1, 1))
        for edge in self.Edges:
            for vertex in edge:
                glVertex3fv(self.Vertices[vertex])

        glEnd()


class Ground:
    def __init__(self):
        self.Vertices = (
            (-8, 0, 5),
            (8, 0, 5),
            (8, 0, -15),
            (-8, 0, -15)
        )

    def draw(self):
        glBegin(GL_QUADS)
        x = 0
        for vertex in self.Vertices:
            x += 1
            glColor3fv((0, 0.5, 0.5))
            glVertex3fv(vertex)
        glEnd()


class Football:
    def __init__(self):
        self.X = 0
        self.Y = 0.1
        self.Z = 0
        self.ROIx = 0.026
        self.ROIy = 0.014
        self.ROIz = 0.11
        self.Color = (0.65, 0.08, 0.18)
        self.Radius = 0.1

    def move(self):
        self.X += self.ROIx
        self.Y += self.ROIy
        self.Z -= self.ROIz

    def stop_moving(self):
        self.ROIx = self.ROIy = self.ROIz = 0

    def draw(self):
        glTranslatef(self.X, self.Y, self.Z)
        Q = gluNewQuadric()
        gluQuadricTexture(Q, GL_TRUE)
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
        color = [1.0, 1.0, 0.0, 0.0]
        glColor3fv(self.Color)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        gluSphere(Q, self.Radius, 40, 40)


class Game:
    def __init__(self):
        pygame.init()
        display = (1200, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glEnable(GL_COLOR_MATERIAL)
        glTranslatef(0, -2, -5.2)
        glRotatef(20, 2, 0, 0)
        glMatrixMode(GL_MODELVIEW)

        self.football = Football()
        self.goal_post = GoalPost()
        self.ground = Ground()
        self.scored = None

    def move_camera(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Camera movements
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(0.5, 0, 0)
                elif event.key == pygame.K_RIGHT:
                    glTranslatef(-0.5, 0, 0)
                elif event.key == pygame.K_UP:
                    glTranslatef(0, -0.2, 0)
                elif event.key == pygame.K_DOWN:
                    glTranslatef(0, 0.2, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)
                elif event.button == 5:
                    glTranslatef(0, 0, -1.0)

    def check_goal(self):
        if fabs(self.goal_post.BottomLeftVertex[2]) <= (fabs(self.football.Z)-self.football.Radius):
            if (((self.goal_post.TopLeftVertex[1] >= (self.football.Y + self.football.Radius))
                    and (self.goal_post.BottomLeftVertex[1] <= (self.football.Y - self.football.Radius)))
                and ((self.goal_post.TopRightVertex[0] >= (self.football.X + self.football.Radius))
                    and (self.goal_post.TopLeftVertex[0] <= (self.football.X + self.football.Radius)))):
                self.scored = True
            else:
                self.scored = False

    def play(self):
        while True:
            self.move_camera()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Ground
            glPushMatrix()
            self.ground.draw()
            glPopMatrix()

            # Ball Animation
            glPushMatrix()
            self.football.move()
            # print("{}, {}, {}".format(self.football.X, self.football.Y, self.football.Z))
            # print("{}, {}, {}".format(self.football.ROIx, self.football.ROIy, self.football.ROIz))
            # if round(self.football.X, 1) == 3.6 or round(self.football.Y, 1) == 2.4 or ceil(self.football.Z) == -11:
            #     self.football.stop_moving()
            #     break
            self.football.draw()
            glPopMatrix()

            # Goalpost
            glPushMatrix()
            self.goal_post.draw()
            glPopMatrix()

            self.check_goal()
            if self.scored is not None:
                if self.scored:
                    # print("Scored!!")
                    self.football.Color = (0.42, 0.78, 0.125)
                    self.football.stop_moving()
                    break
                else:
                    # print("Missed!!")
                    self.football.stop_moving()
                    break

            pygame.display.flip()
            pygame.time.wait(50)


g = Game()
g.football.ROIx = -0.026
g.football.ROIy = 0
g.football.ROIz = 0.11
g.play()
if g.scored:
    print("Scored!!")
else:
    print("Missed!!")
print("{}, {}, {}".format(g.football.X, g.football.Y, g.football.Z))
