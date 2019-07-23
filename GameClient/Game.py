import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math import fabs, pow, sqrt

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
        self.prevX = 0
        self.prevY = 0.1
        self.prevZ = 0
        self.ROIx = 0.026
        self.ROIy = 0.014
        self.ROIz = 0.11
        self.Color = (0.65, 0.08, 0.18)
        self.Radius = 0.1

    def move(self):
        self.prevX = self.X
        self.prevY = self.Y
        self.prevZ = self.Z
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


class Goalie:
    def __init__(self, gple, gpre, gpte, gpbe):
        self.TopRightVertex = (0.1, 1.3, -11)
        self.TopLeftVertex = (-0.1, 1.3, -11)
        self.BottomLeftVertex = (-0.1, 1.1, -11)
        self.BottomRightVertex = (0.1, 1.1, -11)
        self.Center = [0, 1.2, -11]
        self.GoalPostLeftEdge = gple
        self.GoalPostRightEdge = gpre
        self.GoalPostTopEdge = gpte
        self.GoalPostBottomEdge = gpbe
        self.Prev_Pos = self.Center

    def draw(self):
        glBegin(GL_QUADS)
        glColor3fv((1, 1, 1))
        glVertex3fv(self.TopRightVertex)
        glVertex3fv(self.TopLeftVertex)
        glVertex3fv(self.BottomLeftVertex)
        glVertex3fv(self.BottomRightVertex)
        glEnd()

    def move_by_unit(self, x, y):
        self.Prev_Pos = self.Center
        if self.check_move_allowed(x, y):
            self.Center[0] += x
            self.Center[1] += y
            self.TopRightVertex = self.calculate_vertices("TR")
            self.TopLeftVertex = self.calculate_vertices("TL")
            self.BottomLeftVertex = self.calculate_vertices("BL")
            self.BottomRightVertex = self.calculate_vertices("BR")

    def check_move_allowed(self, x, y):
        if (((self.Center[0] + x >= self.GoalPostLeftEdge + 0.1)
                and (self.Center[0] + x <= self.GoalPostRightEdge - 0.1))
            and ((self.Center[1] + y >= self.GoalPostBottomEdge + 0.1)
                and (self.Center[1] + y <= self.GoalPostTopEdge - 0.1))):
            return True
        return False

    def check_new_pos_valid(self, x, y):
        if (((x >= self.GoalPostLeftEdge + 0.1)
                and (x <= self.GoalPostRightEdge - 0.1))
            and ((y >= self.GoalPostBottomEdge + 0.1)
                and (y <= self.GoalPostTopEdge - 0.1))):
            return True
        return False

    def move_to_pos(self, x, y):
        self.Prev_Pos = self.Center
        if self.check_new_pos_valid(x, y):
            self.Center[0] = x
            self.Center[1] = y
            self.TopRightVertex = self.calculate_vertices("TR")
            self.TopLeftVertex = self.calculate_vertices("TL")
            self.BottomLeftVertex = self.calculate_vertices("BL")
            self.BottomRightVertex = self.calculate_vertices("BR")

    def calculate_vertices(self, v):
        if v == "TR":
            return (self.Center[0] + 0.1, self.Center[1] + 0.1, -11)
        elif v == "TL":
            return (self.Center[0] - 0.1, self.Center[1] + 0.1, -11)
        elif v == "BL":
            return (self.Center[0] - 0.1, self.Center[1] - 0.1, -11)
        elif v == "BR":
            return (self.Center[0] + 0.1, self.Center[1] - 0.1, -11)


class ControlBar:
    def __init__(self, verts, ctrl_bar, color):
        self.Vertices = verts
        self.Control = ctrl_bar
        self.Edges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0)
        )
        self.Limits = [self.Vertices[1][0]+0.01, self.Vertices[0][0]-0.01]
        self.Control_Move_Speed = 0.01
        self.Color = color

    def draw(self):
        glPushMatrix()
        self.draw_bar()
        glPopMatrix()

        glPushMatrix()
        self.draw_control()
        glPopMatrix()

    def draw_bar(self):
        glBegin(GL_LINES)
        glColor3fv((1, 1, 1))
        for edge in self.Edges:
            for vertex in edge:
                glVertex3fv(self.Vertices[vertex])
        glEnd()

    def draw_control(self):
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glColor3fv(self.Color)
        glVertex3fv(self.Control[0])
        glVertex3fv(self.Control[1])

        dc = list(map(list, self.Control))
        dc[0][0] += self.Control_Move_Speed
        dc[1][0] += self.Control_Move_Speed
        self.Control = tuple(map(tuple, dc))
        if round(self.Control[0][0], 2) == self.Limits[1] or round(self.Control[0][0], 2) == self.Limits[0]:
            self.Control_Move_Speed = -self.Control_Move_Speed
        glEnd()
        glLineWidth(1.0)


class GUI:
    def __init__(self):
        self.direction_bar = ControlBar(
            (
                (-2, 0.3, 1),
                (-3, 0.3, 1),
                (-3, 0, 1),
                (-2, 0, 1)
            ),
            (
                (-2.9, 0.3, 1),
                (-2.9, 0, 1)
            ),
            (0.16, 0.33, 0.65)
        )
        self.elevation_bar = ControlBar(
            (
                (0.5, 0.3, 1),
                (-0.5, 0.3, 1),
                (-0.5, 0, 1),
                (0.5, 0, 1)
            ),
            (
                (-0.4, 0.3, 1),
                (-0.4, 0, 1)
            ),
            (0.76, 0.19, 0.15)
        )
        self.power_bar = ControlBar(
            (
                (3, 0.3, 1),
                (2, 0.3, 1),
                (2, 0, 1),
                (3, 0, 1)
            ),
            (
                (2.1, 0.3, 1),
                (2.1, 0, 1)
            ),
            (0.76, 0.73, 0.15)
        )


class Game:
    def __init__(self):
        pygame.init()
        display = (1200, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glEnable(GL_COLOR_MATERIAL)
        glTranslatef(0, -1, -5.2)
        glRotatef(20, 2, 0, 0)
        glMatrixMode(GL_MODELVIEW)

        self.football = Football()
        self.goal_post = GoalPost()
        self.ground = Ground()
        self.goalie = Goalie(self.goal_post.TopLeftVertex[0], self.goal_post.TopRightVertex[0], self.goal_post.TopLeftVertex[1], self.goal_post.BottomLeftVertex[1])
        self.gui = GUI()
        self.on_target = None
        self.saved = None
        self.isGameEnd = False
        self.animation_delay = 100
        self.gbd_old = 0
        self.gbd_new = 0
        self.inputs_gathered = False

        # Set goalie to -2.6, 0.2, -11
        # self.goalie.move_to_pos(-2.6, 0.2)

    def move_camera_or_goalie(self):
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
                self.on_target = True
            else:
                self.on_target = False

    def is_goal_saved(self):
        if fabs(self.goal_post.BottomLeftVertex[2]) <= (fabs(self.football.Z)-self.football.Radius):
            self.saved = (((self.football.X <= self.goalie.TopRightVertex[0])
                        and (self.football.X >= self.goalie.TopLeftVertex[0]))
                    and ((self.football.Y <= self.goalie.TopRightVertex[1])
                        and (self.football.Y >= self.goalie.BottomRightVertex[1])))

    def calc_goalie_ball_distance(self):
        self.gbd_old = self.gbd_new
        bx = self.football.X
        by = self.football.Y
        gx = self.goalie.Center[0]
        gy = self.goalie.Center[1]
        self.gbd_new = sqrt(pow(bx - gx, 2) + pow(by - gy, 2))

    def get_user_input(self):
        control_bars = [self.gui.direction_bar, self.gui.elevation_bar, self.gui.power_bar]
        for i in range(3):
            space_tap = False
            while True:
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                control_bars[i].draw()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    # Camera movements
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            control_bars[i].Control_Move_Speed = 0
                            space_tap = True

                if space_tap:
                    break
                pygame.display.flip()
                pygame.time.wait(10)

            print(control_bars[i].Control[0][0])
        self.inputs_gathered = True

    def render_next_frame(self):
        self.move_camera_or_goalie()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Ground
        glPushMatrix()
        self.ground.draw()
        glPopMatrix()

        # Goalpost
        glPushMatrix()
        self.goal_post.draw()
        glPopMatrix()

        # Goalie
        glPushMatrix()
        self.goalie.draw()
        glPopMatrix()

        # Ball Animation
        glPushMatrix()
        # self.football.move()
        # print("{}, {}, {}".format(self.football.X, self.football.Y, self.football.Z))
        # print("{}, {}, {}".format(self.football.ROIx, self.football.ROIy, self.football.ROIz))
        # if round(self.football.X, 1) == 3.6 or round(self.football.Y, 1) == 2.4 or ceil(self.football.Z) == -11:
        #     self.football.stop_moving()
        #     break
        self.football.draw()
        glPopMatrix()

        self.check_goal()
        self.is_goal_saved()
        self.calc_goalie_ball_distance()
        if self.on_target is not None:
            print("Goalie Final: {}, {}, {}".format(self.goalie.Center[0], self.goalie.Center[1], self.goalie.Center[2]))
            print("On Target? {}, Saved? {}".format(self.on_target, self.saved))
            if self.on_target:
                # print("Scored!!")
                if self.saved is False:
                    self.football.Color = (0.42, 0.78, 0.125)
                self.football.stop_moving()
                self.isGameEnd = True
            else:
                # print("Missed!!")
                self.football.stop_moving()
                self.isGameEnd = True

        pygame.display.flip()
        pygame.time.wait(self.animation_delay)

    def wait_after_complete(self):
        pygame.time.wait(500)

    def next_state(self):
        self.football.move()
        self.check_goal()
        self.is_goal_saved()
        self.calc_goalie_ball_distance()
        if self.on_target is not None:
            # print("Goalie Final: {}, {}, {}".format(self.goalie.Center[0], self.goalie.Center[1], self.goalie.Center[2]))
            # print("On Target? {}, Saved? {}".format(self.on_target, self.saved))
            if self.on_target:
                # print("Scored!!")
                # if self.saved is False:
                    # self.football.Color = (0.42, 0.78, 0.125)
                self.football.stop_moving()
                self.isGameEnd = True
            else:
                # print("Missed!!")
                self.football.stop_moving()
                self.isGameEnd = True


    def play(self):
        while self.isGameEnd is False:
            self.render_next_frame()


g = Game()
while not g.inputs_gathered:
    g.get_user_input()
#
# # Range -3.5 to 3.5 for goal
# # g.football.ROIx = -0.017
# g.football.ROIx = randrange(-35, 35)/1000
# # Range 2.3 to 0 for goal
# # g.football.ROIy = 0.021
# g.football.ROIy = randrange(0, 23)/1000
# # Range 0 to TBD
# # g.football.ROIz = 0.11
#
g.play()
# if g.on_target:
#     if g.saved:
#         print("Saved by the goalie!!")
#     else:
#         print("Scored!!")
# else:
#     print("Missed!!")
# print("{}, {}, {}".format(g.football.X, g.football.Y, g.football.Z))