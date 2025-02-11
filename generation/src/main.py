from editor import world
from schema import network
import load
from tensorflow.keras.models import load_model

myWorld = world.World('saves/input')
model = load_model('../.models/tictoe.keras')
networkData = load.read_neural_net_from_keras(model)

network.network(networkData).write(myWorld, (0, 60, 0))

myWorld.close('saves/output')
