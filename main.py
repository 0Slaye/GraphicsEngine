import pygame
import sys
from pygame.locals import QUIT
import Geometry
import Lightings
import Colors
import Camera

# Constants
SCREEN_SIZE = (500, 500)
FPS = 60
# Pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Graphics engine")
clock = pygame.time.Clock()

# Objects
camera = Camera.Camera(Geometry.Vector((0, 0, 0)), 80)
light = Lightings.DirectionalLight(Geometry.Vector((5, 10, 0)), Colors.CRIMSON)
mesh = Geometry.Mesh(screen, light, 1, 0)
encoder = Geometry.Encoder("Mesh/LowPolyCar.obj", 1)
encoder.load()
encoder.encode(mesh)
mesh.normalize()

while True:
    # Events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Camera

    keys = pygame.key.get_pressed()
    camera.movements(mesh, 10)

    # Engine
    screen.fill((0, 0, 0))
    rot_x = Geometry.Rotation(0, 1)
    rot_y = Geometry.Rotation(1, 1)
    rot_z = Geometry.Rotation(2, 1)
    for i in mesh.vertices:
        rot_x.apply(i)
        rot_y.apply(i)
        rot_z.apply(i)
    mesh.draw(0)

    # Update screen
    clock.tick(FPS)
    pygame.display.update()
