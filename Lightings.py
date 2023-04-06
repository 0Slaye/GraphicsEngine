import Geometry
import math


class DirectionalLight():

    def __init__(self, vector, color: tuple):
        self.vector = vector
        self.color = color

    def lightingPercentage(self, vector):
        VectorsLenght = self.vector.getLenght() * vector.getLenght()
        angle = 0
        if (VectorsLenght != 0):
            angle = self.vector.dotProduct(vector) / VectorsLenght
            angle = math.acos(angle)
        lightPercentage = angle * 100 / 360

        return lightPercentage
