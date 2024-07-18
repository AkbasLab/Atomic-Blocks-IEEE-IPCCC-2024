from scenic.simulators.sumo.model import *
from scenic.core.distributions import *

model scenic.simulators.sumo.model

"""Uses allnetworksedit.net.xml"""

# In SUMO speed is in meters per second. But we imagine speed in Kilometers
# per second, so we must convert from KPH to MPS.

kph2mps = 1/3.6
mps2kph = 3.6
lanes = [1,2]
ego_lane = 1
ego_dist = 100

ego = Car at 0 @ 0,          # Always start ego at 0 & 0
    with name "ego",         # The ego must be named ego
    with route ["-E15", "E16"], # A route is required
    with track True,         # Follow the EGO in the GUI
    with lane ego_lane,
    with distance ego_dist,
    with speed 20 * kph2mps,
    with color [0,0,255,255] # Set RGBA color to Blue
npc1 = Car at 0 @ 2, # Other actors should be 2 units away from each other
    with name "npc1",
    with route ["-E15", "E16"],
    with color [255,0,0,255], # Red
    with distance ego_dist+1,
    with lane 2,
    with laneChange [1, 10],
    with speed 30 * kph2mps
npc2 = Car at 0 @ 4, # Other actors should be 4 units away from each other
    with name "npc2",
    with route ["-E15", "E16"],
    with color [0,255,0,255], # Green
    with distance ego_dist-Range(10,70),
    with speedMode 32,
    with lane ego_lane,
    with speed 20 * kph2mps,
    with changeSpeed [Range(70,100)*kph2mps, 49]
ped1 = Pedestrian at 0 @ 6,
    with name "ped1",
    with route ["-E15", "E15"],
    with color [255,255,0,255], #yellow
    with departTime 47,
    with distance 377.12

Traf1 = TrafficLight at 0 @ 8,
    with name "J19",
    with state ["rrrrrGGGGgrrrrrGGGggrrrrrG","rrrrgGGGGgrrrrrGGGggrrrrrG"],
    with duration [100,50]



param npc2_distance = npc2.distance
param npc2_changeSpeed = npc2.changeSpeed[0]
