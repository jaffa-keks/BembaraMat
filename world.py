import pygame
from car import Car

class World:

    def __init__(self, inp):
        self.image_data = pygame.image.load("world1.png").convert_alpha()
        self.width = self.image_data.get_width()
        self.height = self.image_data.get_height()
        self.car = Car(self, None, inp)

    def update(self):
        self.car.update()

    def render(self, display):
        display.blit(self.image_data, (0, 0))
        self.car.render(display)

    def get_terrain(self, point):
        if point[0] < 0 or point[0] >= self.width:
            return True
        if point[1] < 0 or point[1] >= self.height:
            return True
        p_alpha = self.image_data.get_at((int(point[0]), int(point[1])))
        return True if p_alpha == (255, 0, 0) else False