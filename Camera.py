import Geometry
import pygame


class Camera():

    def __init__(self, vector: Geometry.Vector, fov):
        self.vector = vector
        self.fov = fov
        self.x = 0
        self.y = 0
        self.z = 0

    def movements(self, mesh: Geometry.Mesh, velocity: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            mesh.center = Geometry.Vertex(mesh.screen,
                                          (mesh.center.x, mesh.center.y, mesh.center.z + 1 * velocity))

        if keys[pygame.K_s]:
            mesh.center = Geometry.Vertex(mesh.screen,
                                          (mesh.center.x, mesh.center.y, mesh.center.z - 1 * velocity))

        if keys[pygame.K_q]:
            mesh.center = Geometry.Vertex(mesh.screen,
                                          (mesh.center.x + 1 * velocity, mesh.center.y, mesh.center.z))

        if keys[pygame.K_d]:
            mesh.center = Geometry.Vertex(mesh.screen,
                                          (mesh.center.x - 1 * velocity, mesh.center.y, mesh.center.z))

        if keys[pygame.K_SPACE]:
            mesh.center = Geometry.Vertex(mesh.screen,
                                          (mesh.center.x, mesh.center.y + 1 * velocity, mesh.center.z))

        if keys[pygame.K_LSHIFT]:
            mesh.center = Geometry.Vertex(mesh.screen,
                                          (mesh.center.x, mesh.center.y - 1 * velocity, mesh.center.z))

    def getCoords(self):
        return self.x, self.y, self.z
