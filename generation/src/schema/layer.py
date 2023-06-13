import math

from editor import world
from editor import schema
from schema import adder, neuron

def outLineSegment(active=False):
    return schema.Schema(
        [
            [['   '], [' B '], [' B '], ['   '], ['   '], [' B '], [' B ']],
            [[' B '], ['Rr4'], ['Rr3'], [' B '], [' B '], [' - '], [' - ']],
            [['Rt ' if active else '   '], ['   '], ['   '], [' - '], [' - '], ['   '], ['   ']]],
        {' B ': 'minecraft:yellow_concrete',
         ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}),
         'Rr3': world.BlockState('minecraft:repeater', {'facing': 'west', 'delay': '3'}),
         'Rr4': world.BlockState('minecraft:repeater', {'facing': 'west', 'delay': '4'}),
         'Rt ': world.BlockState('minecraft:redstone_torch')})


def inLineSegment(flipDir=False):
    return schema.Schema(
        [[[' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ']],
         [[' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', 'Rrs4' if flipDir else 'Rrn4', 'Rrs3'
           if flipDir else 'Rrn3', ' - ']]],
        {' B ': 'minecraft:orange_concrete', ' - ': world.BlockState(
            'minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}),
         'Rrn3': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '3'}),
         'Rrn4': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '4'}),
         'Rrs3': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '3'}),
         'Rrs4': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '4'}), })



def multiplexer(inputSize, outputSize):
    print("Generating multiplexer...")

    res = schema.Schema(
        [[['   '] * adder.ADDER_LENGTH *
          outputSize] * adder.ADDER_WIDTH *
         inputSize] * 4, {})
    for i in range(inputSize):
        print(f"Generating input line ({i + 1}/{inputSize})")
        for j in range(
                max(inputSize, outputSize)):
            if j < inputSize:
                res = res.join(
                    outLineSegment(i == j),
                    (i * adder.ADDER_WIDTH,
                     0, j * adder.ADDER_LENGTH))
            res = res.join(
                inLineSegment(i > j),
                (i * adder.ADDER_WIDTH,
                 3, j * adder.ADDER_LENGTH))

    print("Done generating multiplexer")
    return res


def layer(inputSize, outputSize, layerData):
    print("Generating layer...")
    res = schema.Schema([[[]]], {})
    for i in range(outputSize):
        res = res.join(
            neuron.neuron(layerData[i][1:], layerData[i][0], max(5, round(2 + math.log2(inputSize + 1)))), (0, 0, -adder.ADDER_LENGTH))
    return res
