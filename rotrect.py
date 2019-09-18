import pygame
from math import sin, cos

class RotRect:

    def __init__(self, pos, size, rot, col = (255, 255, 255)):
        self.pos = pos
        self.size = size
        self.rot = rot
        self.col = col
        self.mid = False
        self.cnr_pts = [(0, 0)] * 4
        self.mid_pts = [(0, 0)] * 4
        self.set_pts()

    def set_pts(self):
        rbx = cos(self.rot) * self.size[1] / 2 - sin(self.rot) * (self.size[0] / 2)
        rby = sin(self.rot) * (self.size[1] / 2) + self.size[0] / 2 * cos(self.rot)

        lbx = cos(self.rot) * self.size[1] / 2 + sin(self.rot) * (self.size[0] / 2)
        lby = sin(self.rot) * (self.size[1] / 2) - self.size[0] / 2 * cos(self.rot)

        rtx = -cos(self.rot) * self.size[1] / 2 - sin(self.rot) * (self.size[0] / 2)
        rty = sin(self.rot) * (-self.size[1] / 2) + self.size[0] / 2 * cos(self.rot)

        ltx = -cos(self.rot) * self.size[1] / 2 + sin(self.rot) * (self.size[0] / 2)
        lty = sin(self.rot) * (-self.size[1] / 2) - self.size[0] / 2 * cos(self.rot)

        self.cnr_pts[0] = (self.pos[0] - ltx, self.pos[1] + lty)
        self.cnr_pts[1] = (self.pos[0] - rtx, self.pos[1] + rty)
        self.cnr_pts[2] = (self.pos[0] - rbx, self.pos[1] + rby)
        self.cnr_pts[3] = (self.pos[0] - lbx, self.pos[1] + lby)

    def set_mid_pts(self):
        vx = cos(self.rot) * self.size[1] / 2
        vy = sin(self.rot) * self.size[1] / 2

        hx = sin(self.rot) * self.size[0] / 2
        hy = cos(self.rot) * self.size[0] / 2

        self.mid_pts[0] = (self.pos[0] + vx, self.pos[1] - vy)
        self.mid_pts[1] = (self.pos[0] + hx, self.pos[1] + hy)
        self.mid_pts[2] = (self.pos[0] - vx, self.pos[1] + vy)
        self.mid_pts[3] = (self.pos[0] - hx, self.pos[1] - hy)

    def update(self, pos, rot):
        self.pos = pos
        self.rot = rot
        self.set_pts()
        if self.mid:
            self.set_mid_pts()

    def render(self, display):
        pygame.draw.polygon(display, self.col, self.cnr_pts)
#        if self.mid:
#            pygame.draw.polygon(display, (32, 64, 192), self.mid_pts)