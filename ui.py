import pygame

class UI:

    def __init__(self, car):
        self.car = car
        self.ui_font  = pygame.font.SysFont("arial", 24)

    def render(self, display):
        self.render_steering(display)

    def render_steering(self, display):
        pygame.draw.rect(display, (255, 255, 255), (60, 900, 200, 20))
        steer_pos = -100 / self.car.max_fw_ang * self.car.fw_ang
        pygame.draw.rect(display, (32, 255, 32), (156 + steer_pos, 890, 8, 40))
        ss = " | ".join("{:4.2f}".format(x) for x in self.car.sensors) # sensor render string
        sensors = self.ui_font.render(ss, False, (255, 255, 255))
        display.blit(sensors, (60, 950))