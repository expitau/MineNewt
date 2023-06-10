from pyanvil import world
from pyanvil import editor
from schema import schema
import load

# Load the world folder relative to the current working dir
myWorld = world.World('../save')
networkData = load.read_neural_net_file('../training/example.newt')

schema.network([4, 4, 4], networkData).write(myWorld, (0, 60, 0))
# schema.clockLineSegment().write(myWorld, (0, 80, 0))

myWorld.close('../save2')
