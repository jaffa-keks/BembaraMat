AI_DRIVE = True

import pygame
from car import Car
from genetics import Population

class World:

    def __init__(self, inp):
        self.image_data = pygame.image.load("worldbigger.png").convert_alpha()
        self.width = self.image_data.get_width()
        self.height = self.image_data.get_height()
        if AI_DRIVE:
            self.population = Population(self, 20)
        else:
            self.car = Car(self, inp)

    def update(self):
        if AI_DRIVE:
            self.population.update()
        else:
            self.car.update()

    def render(self, display):
        display.blit(self.image_data, (0, 0))
        if AI_DRIVE:
            self.population.render(display)
        else:
            self.car.render(display)

    def get_terrain(self, point):
        if point[0] < 0 or point[0] >= self.width:
            return True
        if point[1] < 0 or point[1] >= self.height:
            return True
        p_alpha = self.image_data.get_at((int(point[0]), int(point[1])))
        return p_alpha == (255, 0, 0)