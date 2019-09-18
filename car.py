import pygame
from math import sin, cos, radians, atan2, pi, tan
from rotrect import RotRect

class Car:

    def __init__(self, world, dna, inp = None):
        self.world = world
        self.inp = inp
        if inp:
            self.inp.car = self
        self.pos = [60, 120]
        self.rot = 0
        self.bw = 60 # body wid
        self.bl = 100 # body len
        self.axle = 60 # axle width
        self.wb = 70 # wheel base
        self.fw_ang = 0 # forward wheel ang
        self.max_fw_ang = radians(25)
        self.sdz = radians(2) # steer deadzone
        self.st_speed = 0.02 # steer speed
        self.ws = 20 # wheel size
        self.ww = 12 # wheel width
        self.ms = 4.5 # move speed
        self.col_pts = [(0, 0)] * 8
        self.bdr = RotRect(self.pos, (self.bw, self.bl), self.rot) # body rect
        self.bdr.mid = True
        self.wr = RotRect(self.pos, (self.axle, self.wb), self.rot) # wheel points rect
        self.wheels = self.init_wheels()
        self.sd = 300 # sensor max dist
        self.sa = 14 # sensor amount
        self.msa = radians(60) # max sensor ang
        self.sds = 5 # sensor directions
        self.so = 40 # sensor offset
        self.sensors = [1] * self.sds
        self.srp = [(0,0)] * (self.sa * self.sds) # sensor render points
        self.tpa = 16 # turn path amount (density)
        self.tp = [(0,0)] * self.tpa
        self.tc = [0, 0]
        self.reverse = False

    def update(self):
#        self.steer(self.inp.hor)
#        self.drive(self.inp.ver)
        self.drive_by_sensors()
        self.wr.update(self.pos, self.rot)
        self.upd_sensors()
        for i in xrange(0, 4):
            w_rot = self.rot + self.fw_ang if i < 2 else self.rot
            self.wheels[i].update(self.wr.cnr_pts[i], w_rot)

    def render(self, display):
        self.bdr.render(display)
        for wl in self.wheels:
            wl.render(display)
        for rp in self.srp:
            pygame.draw.rect(display, (32, 32, 255), (rp[0], rp[1], 4, 4))
        for rp in self.tp:
            pygame.draw.rect(display, (32, 255, 32), (rp[0], rp[1], 4, 4))
            
    def init_wheels(self):
        w0 = RotRect(self.wr.cnr_pts[0], (self.ww, self.ws), self.fw_ang + self.rot, col = (255, 0, 0))
        w1 = RotRect(self.wr.cnr_pts[1], (self.ww, self.ws), self.fw_ang + self.rot, col = (255, 0, 0))
        w2 = RotRect(self.wr.cnr_pts[2], (self.ww, self.ws), self.rot, col = (64, 64, 64))
        w3 = RotRect(self.wr.cnr_pts[3], (self.ww, self.ws), self.rot, col = (64, 64, 64))
        self.cbp = [(self.wr.cnr_pts[2][0] + self.wr.cnr_pts[3][0]) / 2, (self.wr.cnr_pts[2][1] + self.wr.cnr_pts[3][1]) / 2]
        self.cfp = [(self.wr.cnr_pts[0][0] + self.wr.cnr_pts[1][0]) / 2, (self.wr.cnr_pts[0][1] + self.wr.cnr_pts[1][1]) / 2]
        return (w0, w1, w2, w3)

    def steer(self, amount):
        if amount == 0:
            return
        self.fw_ang -= amount * self.st_speed
        self.fw_ang = min(self.max_fw_ang, max(-self.max_fw_ang, self.fw_ang))

    def drive(self, amount):
        if amount == 0:
            return
        amount *= -1
        tmpf = [self.pos[0] + cos(self.rot) * self.wb / 2, self.pos[1] - sin(self.rot) * self.wb / 2]
        tmpb = [self.pos[0] - cos(self.rot) * self.wb / 2, self.pos[1] + sin(self.rot) * self.wb / 2]
        tmpf[0] += cos(self.rot + self.fw_ang) * self.ms * amount
        tmpf[1] -= sin(self.rot + self.fw_ang) * self.ms * amount
        tmpb[0] += cos(self.rot) * self.ms * amount
        tmpb[1] -= sin(self.rot) * self.ms * amount
        dx = (tmpf[0] + tmpb[0]) / 2
        dy = (tmpf[1] + tmpb[1]) / 2
        dr = atan2(tmpb[1] - tmpf[1], tmpf[0] - tmpb[0])
        self.bdr.update([dx, dy], dr)
        self.set_col_pts()
        if self.fw_ang <> 0 :
            self.trajectory(amount)
        if self.coll() == False:
            self.pos = [dx, dy]
            self.rot = dr
            self.cfp = tmpf
            self.cbp = tmpb
        else:
            self.bdr.update(self.pos, self.rot)
            self.set_col_pts()
        
    def set_col_pts(self):
        for i in xrange(0, 4):
            self.col_pts[i] = self.bdr.cnr_pts[i]
            self.col_pts[i + 4] = self.bdr.mid_pts[i]

    def coll(self):
        for clp in self.col_pts:
            if self.world.get_terrain(clp):
                return True
        return False

    def upd_sensors(self):
        ang_inc = self.msa * 2.0 / (self.sds - 1.0) # dif between each ang
        angles = [self.rot + (pi if self.reverse else 0.0) + self.msa - i * ang_inc for i in xrange(self.sds)] # calc ang of each dir
        ang_i = -1
        self.sensors = [1] * self.sds
        for ang in angles:
            ang_i += 1
            for i in xrange(0, self.sa):
                cd = self.sd / self.sa * i
                spx = self.pos[0] + self.so * cos(ang) + cos(ang) * cd
                spy = self.pos[1] - self.so * sin(ang) - sin(ang) * cd
                sensor_point = (int(spx), int(spy))
                self.srp[ang_i * self.sa + i] = sensor_point
                if self.world.get_terrain(sensor_point):
                    self.sensors[ang_i] = float(cd) / self.sd
                    break

    def drive_by_sensors(self):
        pref_turn = 0
        mid = int(self.sds / 2)
        for i in xrange(self.sds):
            if i ==  mid:
                continue
            pref_turn += self.sensors[i] * (1.0 if i < mid else -1.0)
        drive_power = self.sensors[mid] * -1.0
        if self.sensors[mid] < 0.2:
            self.reverse = not self.reverse
        self.drive(drive_power * (1.0 if not self.reverse else -1.0))
        self.steer_to(pref_turn)

    def steer_to(self, pos):
        pos = min(1, max(-1, pos * 1.5))
        pos_ang = pos * self.max_fw_ang
        dif = self.fw_ang - pos_ang
        self.steer(self.signof(dif))

    def trajectory(self, speed):
        r = self.wb / tan(self.fw_ang)
        cx = self.pos[0] - r * sin(self.rot)
        cy = self.pos[1] - r * cos(self.rot)
        self.tc = (cx, cy)
        for i in xrange(self.tpa):
            xp = cx + r * sin(self.rot + tan(self.fw_ang) * i * self.signof(speed) * 0.4)
            yp = cy + r * cos(self.rot + tan(self.fw_ang) * i * self.signof(speed) * 0.4)
            self.tp[i] = (xp, yp)

    def signof(self, x):
        if x == 0:
            return 0
        else:
            return x / abs(x)