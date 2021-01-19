from tkinter import Tk
from tkinter.filedialog import askopenfilename
from numba import njit, prange
import pygame
import numpy
import math


def translate(pos):
    x, y, z = pos
    return numpy.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1]
    ])


def rotate_x(a):
    return numpy.array([
        [1,            0,           0, 0],
        [0,  math.cos(a), math.sin(a), 0],
        [0, -math.sin(a), math.cos(a), 0],
        [0,            0,           0, 1]
    ])


def rotate_y(a):
    return numpy.array([
        [math.cos(a), 0, -math.sin(a), 0],
        [          0, 1,            0, 0],
        [math.sin(a), 0,  math.cos(a), 0],
        [          0, 0,            0, 1]
    ])


def rotate_z(a):
    return numpy.array([
        [ math.cos(a), math.sin(a), 0, 0],
        [-math.sin(a), math.cos(a), 0, 0],
        [           0,           0, 1, 0],
        [           0,           0, 0, 1]
    ])


def scale(a):
    return numpy.array([
        [a, 0, 0, 0],
        [0, a, 0, 0],
        [0, 0, a, 0],
        [0, 0, 0, 1]
    ])


@njit(fastmath=True)
def numpyFastAny(arr, a, b):
    return numpy.any((arr == a) | (arr == b))


class Menu:
    def __init__(self):
        pygame.init()
        self.SIZE = self.WIDTH, self.HEIGHT = 1280, 720
        pygame.display.set_caption("V3DM")
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.isMenu = True
        self.screen = pygame.display.set_mode(self.SIZE)
        self.background = pygame.image.load("data/background.jpg")
        self.filename = "data/AstroBoy.obj"

        self.game = V3DM(self, self.filename)
        self.start_btn = (100, 100)
        self.change_file_btn = (100, 300)
        self.exit_btn = (100, 500)

    
    def start(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 100)
        wait = font.render("Loading...", True, pygame.Color("yellow"))
        self.screen.blit(wait, (450, 350))
        pygame.display.flip()
        self.game.setFile(self.filename)
        self.game.running = True
        self.game.draw()
        self.isMenu = False

    def changeFile(self):
        select_file = Tk()
        select_file.withdraw()
        self.filename = askopenfilename()
        select_file.destroy()
        font = pygame.font.Font(None, 40)
        self.drawInterface()

    def drawInterface(self):
        self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, pygame.Color("green"), (*self.start_btn, 300, 100))
        pygame.draw.rect(self.screen, pygame.Color("green"), (*self.change_file_btn, 300, 100))
        pygame.draw.rect(self.screen, pygame.Color("green"), (*self.exit_btn, 300, 100))
        font = pygame.font.Font(None, 100)
        start = font.render("Start", True, pygame.Color("blue"))
        self.screen.blit(start, (self.start_btn[0] + 65, self.start_btn[1] + 20))
        change_file = font.render("Set file", True, pygame.Color("blue"))
        self.screen.blit(change_file, (self.change_file_btn[0] + 40, self.change_file_btn[1] + 20))
        exit = font.render("Exit", True, pygame.Color("blue"))
        self.screen.blit(exit, (self.exit_btn[0] + 80, self.exit_btn[1] + 20))
        font = pygame.font.Font(None, 40)
        x, y = 500, 100
        info = font.render('Программа для просмотра файлов с расширением ".obj"', True, pygame.Color("red"))
        self.screen.blit(info, (x, y))
        info = font.render('Нажмите "Start", чтобы просмотреть модель', True, pygame.Color("red"))
        self.screen.blit(info, (x, y + 50))
        info = font.render('Нажмите "Set file", чтобы сменить модель', True, pygame.Color("red"))
        self.screen.blit(info, (x, y + 50 * 2))
        info = font.render('Нажмите "Exit", чтобы выйти из программы', True, pygame.Color("red"))
        self.screen.blit(info, (x, y + 50 * 3))
        info = font.render('Для перемещения используйте "WASD" и "QE"', True, pygame.Color("red"))
        self.screen.blit(info, (x, y + 50 * 5))
        info = font.render('Нажмите "Escape" при просмотре, чтобы выйти в', True, pygame.Color("red"))
        self.screen.blit(info, (x, y + 50 * 6))
        info = font.render('главное меню', True, pygame.Color("red"))
        self.screen.blit(info, (x, y + 50 * 7 - 10))
        pygame.draw.rect(self.screen, pygame.Color("green"), (100, 40, 300, 50), 10)
        file = font.render(self.filename.split("/")[-1], True, (255, 0, 0))
        self.screen.blit(file, (110, 50))

    def draw(self):
        self.drawInterface()
        while self.isMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if (self.start_btn[0] <= event.pos[0] <= self.start_btn[0] + 300
                        and self.start_btn[1] <= event.pos[1] <= self.start_btn[1] + 100):
                        self.start()
                    elif (self.change_file_btn[0] <= event.pos[0] <= self.change_file_btn[0] + 300
                        and self.change_file_btn[1] <= event.pos[1] <= self.change_file_btn[1] + 100):
                        self.changeFile()
                    elif (self.exit_btn[0] <= event.pos[0] <= self.exit_btn[0] + 300
                        and self.exit_btn[1] <= event.pos[1] <= self.exit_btn[1] + 100):
                        exit()

            pygame.display.flip()



class Object:
    def __init__(self, render, vertexes='', polygons=''):
        self.render = render
        self.vertexes = numpy.array([numpy.array(i) for i in vertexes])
        self.polygons = numpy.array([numpy.array(i) for i in polygons])
        self.translate([0.0001, 0.0001, 0.0001])

    def draw(self):
        vertexes = self.vertexes @ self.render.camera.cameraMatrix()
        vertexes = vertexes @ self.render.projection.projectionMatrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        vertexes = vertexes @ self.render.projection.toScreenMatrix
        vertexes = vertexes[:, :2]
        for i in self.polygons:
            if not numpyFastAny(vertexes[i], self.render.H_WIDTH, self.render.H_HEIGHT):
                pygame.draw.polygon(self.render.screen, (190, 190, 190, 155), vertexes[i]) # - отображение граней модели
                pygame.draw.polygon(self.render.screen, (0, 0, 0, 255), vertexes[i], 1) # - отображение ребер модели

    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)

    def scale(self, value):
        self.vertexes = self.vertexes @ scale(value)

    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)


class Projection:
    def __init__(self, render):
        NEAR = render.camera.near_plane
        FAR = render.camera.far_plane
        RIGHT = math.tan(render.camera.h_fov / 2)
        LEFT = -RIGHT
        TOP = math.tan(render.camera.v_fov / 2)
        BOTTOM = -TOP

        self.projectionMatrix = numpy.array([
            [2 / (RIGHT - LEFT), 0                 , 0                             , 0],
            [0                 , 2 / (TOP - BOTTOM), 0                             , 0],
            [0                 , 0                 , (FAR + NEAR) / (FAR - NEAR)   , 1],
            [0                 , 0                 , -2 * NEAR * FAR / (FAR - NEAR), 0]
        ])


        self.toScreenMatrix = numpy.array([
            [render.H_WIDTH, 0               , 0, 0],
            [0             , -render.H_HEIGHT, 0, 0],
            [0             , 0               , 1, 0],
            [render.H_WIDTH, render.H_HEIGHT , 0, 1]
        ])


class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = numpy.array([*position, 1.0])
        self.forward = numpy.array([0, 0, 1, 1])
        self.up = numpy.array([0, 1, 0, 1])
        self.right = numpy.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * render.HEIGHT / render.WIDTH
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 1
        self.rotation_speed = 0.025

    def control(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pygame.K_d]:
            self.position += self.right * self.moving_speed
        if key[pygame.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pygame.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pygame.K_q]:
            self.position += self.up * self.moving_speed
        if key[pygame.K_e]:
            self.position -= self.up * self.moving_speed

        if key[pygame.K_LEFT]:
            self.yaw(-self.rotation_speed)
        if key[pygame.K_RIGHT]:
            self.yaw(self.rotation_speed)

    def yaw(self, angle):
        rotate = rotate_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def translateMatrix(self):
        x, y, z, w = self.position
        return numpy.array([
            [ 1,  0,  0, 0],
            [ 0,  1,  0, 1],
            [ 0,  0,  1, 0],
            [-x, -y, -z, 1]
        ])

    def rotateMatrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return numpy.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [ 0,  0,  0, 1]
        ])

    def cameraMatrix(self):
        return self.translateMatrix() @ self.rotateMatrix()


class V3DM:
    def __init__(self, menu, filename):
        pygame.init()
        self.menu = menu
        self.WIDTH, self.HEIGHT = self.menu.WIDTH, self.menu.HEIGHT
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.running = False
        self.screen = self.menu.screen
        self.clock = pygame.time.Clock()
        self.createObjects(filename)
        self.setFile(filename)

    def setFile(self, filename):
        self.object = self.getObjectFromFile(filename)

    def createObjects(self, filename):
        self.camera = Camera(self, [-10, 10, -55])
        self.projection = Projection(self)

    def getObjectFromFile(self, filename):
        vertex, polygons = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    polygon = line.split()[1:]
                    polygons.append([int(i.split('/')[0]) - 1 for i in polygon])
        return Object(self, vertex, polygons)

    def draw(self):
        while self.running:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.menu.isMenu = True
                self.menu.draw()
                self.running = False
            self.screen.fill((0, 132, 165, 1))
            self.object.draw()
            self.camera.control()
            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            #pygame.display.set_caption(str(self.clock.get_fps())) # - для проверки FPS
            pygame.display.flip()
            self.clock.tick(self.FPS)
                



def main():
    numpy.warnings.filterwarnings('ignore', category=numpy.VisibleDeprecationWarning)
    app = Menu()
    app.draw()


if __name__ == '__main__':
    main()