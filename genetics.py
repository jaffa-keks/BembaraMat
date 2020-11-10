from car import Car
from neural import Node, NeuralNetwork, mutate, crossover
from math import sqrt, atan2, pi
from random import randint, random

class Population:
    def __init__(self, world, size):
        self.cars = []
        self.networks = []
        self.size = size
        self.world = world
        self.new_cars(size)
        self.generation = 1
        self.time = 0

    def update(self):
        crashed = 0
        self.time += 1
        for c in self.cars:
            if c.crashed:
                crashed += 1
        if crashed == len(self.cars) or self.time > 300 + self.generation * 5:
            self.repopulate()
            return
        for c in self.cars:
            if c.crashed:
                continue
            i = self.cars.index(c)
            goal = self.goal(c)
            net_input = [s for s in c.sensors]
            net_input += goal

            # print "Inputs"
            # print net_input
            # print "==="

            self.networks[i].compute(c.sensors)
            c.drive(self.networks[i].layers[-1][0].value * 2.0 - 1)
            c.fw_ang = (self.networks[i].layers[-1][1].value * 2.0 - 1) * c.max_fw_ang
            c.update()

    def new_cars(self, num):
        for i in xrange(num):
            self.cars.append(Car(self.world))
            net = NeuralNetwork([5, 6, 6, 2])
            net.read_network("Networks/Backprop.txt")
            self.networks.append(net)

    def render(self, display):
        for c in self.cars:
            c.render(display)

    def goal(self, car):
        target_park = (1000, 600)
        MAX_DIST = 1024 * sqrt(2)
        dist = sqrt((target_park[0] - car.pos[0]) ** 2 + (target_park[1] - car.pos[1]) ** 2)
        ang = atan2(target_park[1] - car.pos[1], target_park[0] - car.pos[0])
        return (dist / MAX_DIST, ang / pi)

    def repopulate(self):
        from copy import deepcopy
        COPY_PER = 0.2
        MUTATE_PER = 0.2
        CROSS_PER = 0.4
        sort_fit(self)
        new_networks = []
        self.cars = []
        self.time = 0
        for i in xrange(self.size):
            self.cars.append(Car(self.world))            
        for i in xrange(int(self.size * COPY_PER)):
            new_networks.append(self.networks[i])
        for i in xrange(int(self.size * MUTATE_PER)):
            new_networks.append(mutate(deepcopy(self.networks[i]), 0.4))
        f = self.size * CROSS_PER
        for i in xrange(int(self.size * CROSS_PER)):
            net = crossover(self.networks[randint(0, f-1)], self.networks[randint(0, f-1)])
            mutate(net, 0.2)
            new_networks.append(net)
        for i in xrange(self.size - len(new_networks)):
            net = NeuralNetwork([5, 6, 6, 2])
            new_networks.append(net)
        self.networks = new_networks
        if self.generation % 5 == 0:
            self.networks[0].print_network("Net 0 Gen " + str(self.generation))
            self.networks[1].print_network("Net 1 Gen " + str(self.generation))
        self.time = 0
        self.generation += 1

def sort_fit(pop):
    for i in xrange(len(pop.networks)):
        pop.networks[i].fitness = pop.goal(pop.cars[i])[0]
    pop.networks.sort(key=lambda x: x.fitness, reverse=False)
    for i in xrange(len(pop.networks)):
        print "Fitness", pop.networks[i].fitness
    print ""