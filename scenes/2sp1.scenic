from scenic.simulators.sumo.model import *
from scenic.core.distributions import *

model scenic.simulators.sumo.model

"""Uses allnetworksedit.net.xml"""

# In SUMO speed is in meters per second. But we imagine speed in Kilometers
# per second, so we must convert from KPH to MPS.

kph2mps = 1/3.6
mps2kph = 3.6
lanes = [1,2]
ego_lane = random.choice(lanes)
npc1_lane = random.choice(lanes)
ego_dist = Range(189,189)

ego = Car at 0 @ 0,          # Always start ego at 0 & 0
    with name "ego",         # The ego must be named ego
    with route ["E2", "E3"], # A route is required
    with track True,         # Follow the EGO in the GUI
    with color [0,0,255,255],# Set RGBA color to Blue
    with lane ego_lane,
    with distance ego_dist,
    with speed 0 * kph2mps,
    with changeSpeed [50*kph2mps, 10]
    
npc1 = Car at 0 @ 2, # Other actors should be 2 units away from each other
    with name "npc1",
    with route ["-E0", "E3"],
    with color [255,0,0,255], # Red
    with distance Range(-100,-10) + ego_dist,
    with speed Range(10,50) * kph2mps,
    with laneChange [DiscreteRange(1,2), 0]

ped1 = Pedestrian at 0 @ 4,
    with name "ped1",
    with route ["-E3","E2"],
    with color [255,255,0,255], #yellow
    with departTime Range(0,0.1),
    with distance Range(200,200.36),
    with egoWaitAtXing True

param ego_speed = ego.speed * mps2kph
param departTime_ped = ped1.departTime
param npc1_speed = npc1.speed * mps2kph
