from random import random
from math import exp
from copy import copy, deepcopy

class NeuralNetwork:
    def __init__(self, layers):
        self.structure = layers
        self.layers = []
        inputs = []
        for i in xrange(layers[0]):
            inputs.append(Node([], 0))
        self.layers.append(inputs)
        for i in layers[1:]:
            layer = []
            for j in xrange(i):
                node_inputs = [[n, random() * 2 - 1.0] for n in self.layers[-1]]
                node = Node(node_inputs, 0)
                layer.append(node)
            self.layers.append(layer)

    def compute(self, inputs):
        assert len(inputs) == len(self.layers[0])
        for i in xrange(len(inputs)):
            self.layers[0][i].value = inputs[i]
        for l in self.layers[1:]:
            for n in l:
                n.compute()

    def read_network(self, rf_n):
        rf = open(rf_n, "r")
        data = rf.read()
        rf.close()
        struct = []
        for l in data.split("Layer")[2:]:
            lay = []
            for n in l.split("Node")[1:]:
                wts = [float(x) for x in n.split("\n")[1].split("Bias")[0].split(" ")[:-1]]
                lay.append(wts)
                # print wts
            struct.append(lay)
        for l in xrange(1, len(self.layers)):
            for n in xrange(len(self.layers[l])):
                nd = self.layers[l][n]
                for i in xrange(len(nd.inputs)):
                    nd.inputs[i][1] = struct[l-1][n][i]

    def print_network(self, name):
        wf = open("./Networks/" + name, "w")
        wf.write("Input Layer - " + str(len(self.layers[0])))
        for layer in self.layers[1:]:
            wf.write("\nLayer " + str(self.layers.index(layer)))
            for node in layer:
                wf.write("\nNode " + str(layer.index(node)) + "\n")
                for input in node.inputs:
                    wf.write(str(input[1]) + " ")
                wf.write("Bias " + str(node.bias))
        wf.close()

    def print_out(self):
        k = ""
        for n in self.layers[-1]:
            k += str(n.value) + " "
        print k

    def backprop(self, inp, target, learn_rate = 0.1, autoapply = False):
        self.compute(inp)
        dt_layer = deepcopy(self.layers)
        for l in reversed(xrange(1, len(self.layers))):
            layer = self.layers[l]
            for j in xrange(len(layer)):
                oj = layer[j].compute()
                if l == len(self.layers) - 1:
                    dt_layer[l][j] = (oj - target[j]) * oj * (1.0 - oj)
                else:
                    next_layer = self.layers[l+1]
                    w_sum = 0
                    for k in xrange(len(next_layer)):
                        w_sum += next_layer[k].inputs[j][1] * dt_layer[l+1][k]
                    dt_layer[l][j] = w_sum * oj * (1.0 - oj)
        del dt_layer[0]
        total_dw = []
        for l in xrange(len(dt_layer)):
            dws_lay = []
            for n in xrange(len(dt_layer[l])):
                nd = self.layers[l+1][n]
                dws = []
                for i in xrange(len(nd.inputs)):
                    dw = -learn_rate * nd.inputs[i][0].compute() * dt_layer[l][n]
                    dws.append(dw)
                    if autoapply:
                        nd.inputs[i][1] += dw
                dws_lay.append(dws)
            total_dw.append(dws_lay)
        return total_dw

class Node:
    def __init__(self, inputs, bias):
        self.inputs = inputs# tuples of (node, weight)
        self.bias = bias
        self.activation = sigmoid
        self.value = 0

    def compute(self):
        s = 0
        for i in self.inputs:
            s += i[0].value * i[1]
        s -= self.bias
        self.value = self.activation(s)
        return self.value

def mutate(network, amount, mutate_bias = 1.0):
    for l in network.layers[1:]:
        for node in l:
            for i in node.inputs:
                i[1] += (random() * 2 - 1) * amount
            node.bias += (random() * 2 - 1) * amount * mutate_bias
    return network

def crossover(net1, net2):
    offspring = NeuralNetwork(net1.structure)
    for l in offspring.layers[1:]:
        li = offspring.layers.index(l)
        for n in l:
            ni = l.index(n)
            for i in n.inputs:
                ii = n.inputs.index(i)
                i[1] = lerp(net1.layers[li][ni].inputs[ii][1], net2.layers[li][ni].inputs[ii][1], random())
            n.bias = lerp(net1.layers[li][ni].bias, net2.layers[li][ni].bias, random())
    return offspring

# def crossover(network1, network2, input):
#     offspring  = NeuralNetwork(network1.structure)
#     for l in xrange(1, len(offspring.layers) - 1):
#         for n in xrange(len(offspring.layers[l])):
#             node = offspring.layers[l][n]
#             for w in xrange(len(node.weights)):
#                 node.weights[w] = lerp(network1.layers[l][n].weights[w], network2.layers[l][n].weights[w], random())
#             node.bias = lerp(network1.layers[l][n].bias, network2.layers[l][n].bias, random())
#     return offspring

def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))

def lerp(y1, y2, x):
    return y1 + (y2 - y1) * x

def stretch(x):
    return x * 2.0 - 1.0

def squish(x):
    return (x + 1.0) / 2.0