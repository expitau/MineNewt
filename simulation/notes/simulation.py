import random
import math

STOCHASTIC_BITLENGTH = 10000


class Neuron:
    def __init__(self, size):
        self.S = 0
        self.size = size

    def stActivation(self, bInputs):
        # print([x.toNum() for x in bInputs])

        if (len(bInputs) != self.size):
            raise Exception(
                f"Incorrect size of bInputs passed to activation function (expected {self.size} but received {len(bInputs)})")

        s = list(bInputs)
        # print(s, self.S)
        for j in range(self.size):
            b = s[j]
            if b == 0:
                self.S -= 1
            else:
                self.S += 1
        if self.S >= self.size:
            self.S = self.size
        if self.S <= -self.size:
            self.S = -self.size

        if self.S >= 0:
            return 1
        else:
            return 0


class Stochastic:
    def __init__(self, value, size=10000):
        self.size = size
        self.value = value

    @classmethod
    def fromNum(cls, p, size=10000):
        value = 0
        for i in range(size):
            if random.random() < (p / 2 + 0.5):
                value = value << 1 | 1
            else:
                value = value << 1
        return cls(value, size)

    @classmethod
    def fromStr(cls, s):
        size = len(s)
        value = 0
        for i in range(len(s)):
            if s[i] == "1":
                value = value & 1
            value <<= 1
        return cls(value, size)

    def toNum(self):
        x = 0
        s = self.value
        # print(f"S = {s}")
        for i in range(self.size):
            x += s & 1
            s >>= 1
        # print(f"x = {x}")
        # print(f"size = {self.size}")
        return (x / self.size - 0.5) * 2

    def at(self, i):
        if i >= self.size:
            raise IndexError("Stochastic overflow")
        return (self.value >> i) & 1

    def __str__(self):
        out = ""
        for i in range(self.size):
            out = str(self.at(i)) + out
        return out

    def __len__(self) -> int:
        return self.size


def stProduct(bA, bB):
    if (bA != 0 and bA != 1):
        raise Exception(f"bA not binary (received {bA})")
    if (bB != 0 and bB != 1):
        raise Exception(f"bB not binary (received {bB})")
    return 1 - (bA ^ bB)


def stWeight(bA, p):
    if (bA != 0 and bA != 1):
        raise Exception(f"bA not binary (received {bA})")
    return 1 - (bA ^ (1 if random.random() < (p / 2 + 0.5) else 0))


def getActivation(weights, stL):
    neuron = Neuron(len(stL))
    prod = 0
    for i in range(STOCHASTIC_BITLENGTH):
        b = neuron.stActivation([stWeight(stL[x].at(i), weights[x]) for x in range(len(stL))])
        # b = neuron.stActivation(stWeight(stInputs[0].at(i), 0.5),
        #                         stWeight(stInputs[1].at(i), -0.5),
        #                         stWeight(stInputs[2].at(i), -0.25),
        #                         stWeight(stInputs[3].at(i), 0.25),
        #                         stWeight(stInputs[4].at(i), 0.1),
        #                         stWeight(stInputs[5].at(i), -0.1)
        #                         )
        prod <<= 1
        prod = prod | b
    out = Stochastic(prod, STOCHASTIC_BITLENGTH)
    return out


inputs = [0.8, -0.5, 0.2, -0.9, 0.1, 0.7]
network = [6, 4, 2]
weights = [
    [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]],
    [[-0.1, -0.2, -0.3, -0.4], [0.1, 0.2, 0.3, 0.4]]
]

stInputs = [Stochastic.fromNum(x, STOCHASTIC_BITLENGTH) for x in inputs]

layers = [[(stInputs[y] if x == 0 else 0) for y in range(network[x])]
          for x in range(len(network))]
for layerN in range(1, len(network)):
    for nodeN in range(network[layerN]):
        layers[layerN][nodeN] = getActivation(
            weights[layerN - 1][nodeN], layers[layerN - 1])
print([[st.toNum() for st in layer] for layer in layers])

