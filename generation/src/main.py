from pyanvil import world
from pyanvil import editor
from schema import schema
import load

myWorld = world.World('saves/save')
networkData = load.read_neural_net_file('../training/example.newt')

schema.network(networkData).write(myWorld, (0, 60, 0))

# s1 = editor.Schema([
#     [
#         [' A ', ' A ', ' A ', ' A ', ' A '],
#     ]
# ], {
#     ' A ': 'minecraft:stone'
# })

# s2 = editor.Schema([
#     [
#         [' B ', ' B ', ' B '],
#         [' B ', ' B ', ' B '],
#         [' B ', ' B ', ' B '],
#     ],
#     [
#         [' B ', ' B ', ' B '],
#         [' B ', ' B ', ' B '],
#         [' B ', ' B ', ' B '],
#     ],
#     [
#         [' B ', ' B ', ' B '],
#         [' B ', ' B ', ' B '],
#         [' B ', ' B ', ' B '],
#     ],
#     [
#         ['   ', ' B ', ' B '],
#         [' B ', '   ', ' B '],
#         [' B ', ' B ', '   '],
#     ],
# ], {
#     ' B ': 'minecraft:dirt'
# })

# print(s1)
# print(s2)
# print(s2.join(s1, (1, 2, -1), True))

myWorld.close('saves/save2')
