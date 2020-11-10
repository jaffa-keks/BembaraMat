def l_sum(a, b):
    assert type(a) == type(b)
    if type(a) == list:
        assert len(a) == len(b)
        return [l_sum(a[i], b[i]) for i in xrange(len(a))]
    return a + b

def l_div(a, b):
    if type(a) == list:
        return [l_div(i, b) for i in a]
    return a / float(b)

def apply_delta(a, b):
    for l in xrange(len(b)):
        for n in xrange(len(b[l])):
            nd = a[l+1][n]
            for i in xrange(len(nd.inputs)):
                nd.inputs[i][1] += b[l][n][i]

def read_data(rf_n):
    rf = open(rf_n, "r")
    data = rf.read()
    extracted = []
    for line in data.splitlines(False):
        raw_inp = line.split(" | ")[0]
        inp = [float(x) for x in raw_inp.split(" ")]
        raw_out = line.split(" | ")[1]
        out = [float(x) for x in raw_out.split(" ")]
        extracted.append((inp, out))
    rf.close()
    return extracted

from neural import *
from random import sample, randint

ext_data = read_data("Networks/io.txt")

nn = NeuralNetwork([5, 8, 8, 2])

nn.read_network("Networks/Backprop.txt")

for i in xrange(500):
    rr = randint(0, 500)
    nn.compute(ext_data[rr][0])
    print "Expected", ext_data[rr][1], ", got",
    nn.print_out()

    dw = None
    for i in sample(ext_data, 20):
        bp = nn.backprop(i[0], i[1], 0.5, False)
        if dw == None:
            dw = bp
        else:
            dw = l_sum(dw, bp)
    dw = l_div(dw, len(ext_data))

    apply_delta(nn.layers, dw)

    nn.compute(ext_data[rr][0])
    print "Expected", ext_data[rr][1], ", got",
    nn.print_out()

nn.print_network("Backprop.txt")

# print nn.backprop(ext_data[0][0], ext_data[0][1])