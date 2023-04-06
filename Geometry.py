import math
import pygame
import Lightings

class Mesh():

    def __init__(self, screen: pygame.display, light: Lightings.DirectionalLight, scale: int, perspective: float):
        self.screen = screen
        self.light = light
        self.scale = scale
        self.perspective = perspective
        self.center = Vertex(self.screen, (0, 0, 0))
        self.vertices = []
        self.new_vertices = []
        self.faces = []

    def normalize(self):
		# met l'objet à l'endroit
        for i in self.vertices:
            rot_x = Rotation(0, 180)
            rot_x.apply(i)

		# met l'objet au centre
        x = [self.vertices[0].x,self.vertices[0].x]
        y = [self.vertices[0].y,self.vertices[0].y]
        z = [self.vertices[0].z,self.vertices[0].z]
        for i in self.vertices:
            if i.x < x[0]:
                x[0] = i.x
            if i.x > x[1]:
                x[1] = i.x
            if i.y < y[0]:
                y[0] = i.y
            if i.y > y[1]:
                y[1] = i.y
            if i.z < z[0]:
                z[0] = i.z
            if i.z > z[1]:
                z[1] = i.z
        for i in self.vertices:
            i.x -= (x[0] + x[1]) / 2
            i.y -= (y[0] + y[1]) / 2
            i.z -= (z[0] + z[1]) / 2
	
    def calcul_vectors(self):
        self.new_vertices = []
        for i in self.vertices:
            x = i.x - self.center.x
            y = i.y - self.center.y
            z = i.z - self.center.z
            self.new_vertices.append(Vertex(self.screen, (x, y, z)))
        
    def draw(self, mode: int):
        self.calcul_vectors()
        screenWidth = self.screen.get_size()[0]
        screenHeight = self.screen.get_size()[1]
        
        for i in self.faces:
            dots = []
            dots_normal = []
            appear = -1
            for j in i:
                currentDot = self.new_vertices[j[0]-1]
                dots_normal.append(currentDot)
                result = (currentDot.x * self.scale + (screenWidth / 2), currentDot.y * self.scale + (screenHeight / 2))
                dots.append(result)
            v1 = Vector(dots_normal[0].to_vector(dots_normal[1]))
            v2 = Vector(dots_normal[1].to_vector(dots_normal[2]))
            normal = v1.product(v2)
            if normal.coords[2] < 0:
                appear = mode
            lightRatio = self.light.lightingPercentage(normal)
            pygame.draw.polygon(self.screen, (self.light.color[0] * lightRatio, self.light.color[1] * lightRatio, self.light.color[2] * lightRatio), dots, appear)



class Vector():

    def __init__(self, coords: tuple):
        self.coords = coords

    def getLenght(self):
        return math.sqrt(self.coords[0]**2 + self.coords[1]**2 + self.coords[2]**2)

    def normalize(self):
        self.coords = (self.coords[0] / self.getLenght(), self.coords[1] / self.getLenght(), self.coords[2] / self.getLenght())

    def dotProduct(self, vector):
        return self.coords[0] * vector.coords[0] + self.coords[1] * vector.coords[1] + self.coords[2] * vector.coords[2]

    def product(self, vector):
        return self.__class__((
            self.coords[1] * vector.coords[2] - self.coords[2] * vector.coords[1],
            self.coords[2] * vector.coords[0] - self.coords[0] * vector.coords[2],
            self.coords[0] * vector.coords[1] - self.coords[1] * vector.coords[0]
        ))
    
    def debug(self):
        return f"Vector : {self.coords}, {self.getLenght()}"



class Vertex():

    def __init__(self, screen: pygame.display, coords: tuple):
        self.screen = screen
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]

    def link(self, vertex, scale, perspectiveRatio):
        screenWidth = 500
        screenHeight = 500

        pygame.draw.line(
         self.screen,
         (255, 255, 255),
         (self.x * scale * (1 + perspectiveRatio * self.z) + (screenWidth / 2),
         self.y * scale * (1 + perspectiveRatio * self.z) + (screenHeight / 2)),
         (vertex.x * scale * (1 + perspectiveRatio * vertex.z) + (screenWidth / 2),
         vertex.y * scale * (1 + perspectiveRatio * vertex.z) + (screenHeight / 2)),
         1
         )

    def to_vector(self, vertex):
        return (vertex.x - self.x, vertex.y - self.y, vertex.z - self.z)
    
    def getCoords(self):
        return self.x, self.y, self.z



class Rotation():

    def __init__(self, axe: int, angle: int):
        self.axe = axe
        self.angle = angle * math.pi / 180

    def apply(self, dot: Vertex):
    
        match self.axe:
            # X rotation
            case 0:
                matrice = [[1, 0, 0], [0, math.cos(self.angle), -math.sin(self.angle)], [0, math.sin(self.angle), math.cos(self.angle)]]
            # Y rotation
            case 1:
                matrice = [[math.cos(self.angle), 0, math.sin(self.angle)], [0, 1, 0], [-math.sin(self.angle), 0, math.cos(self.angle)]]
            # Z rotation
            case 2:
                matrice = [[math.cos(self.angle), -math.sin(self.angle), 0], [math.sin(self.angle), math.cos(self.angle), 0], [0, 0, 1]]
        
        coords_x = matrice[0][0] * dot.x + matrice[0][1] * dot.y + matrice[0][2] * dot.z
        coords_y = matrice[1][0] * dot.x + matrice[1][1] * dot.y + matrice[1][2] * dot.z
        coords_z = matrice[2][0] * dot.x + matrice[2][1] * dot.y + matrice[2][2] * dot.z
        
        dot.x = coords_x
        dot.y = coords_y
        dot.z = coords_z



class Encoder():

    def __init__(self, path: str, strength: int):
        self.path = path
        self.strength = strength
        self.package = []

    def load(self):
        file = open(self.path, "r")
        for lines in file:
            array = lines.split()
            if array != []:
                self.package.append(array)

    def encode(self, mesh: Mesh):
        for i in self.package:
            match i[0]:
                # Vertex
                case "v":
                    mesh.vertices.append(Vertex(mesh.screen, (float(i[1]), float(i[2]), float(i[3]))))
                # Faces
                case "f":
                    result = []
                    for j in range(1, len(i)):
                        values = i[j].split("/")
                        for k in range(len(values)):
                            if values[k] != "":
                                values[k] = int(values[k])
                        result.append(values)
                    mesh.faces.append(result)




