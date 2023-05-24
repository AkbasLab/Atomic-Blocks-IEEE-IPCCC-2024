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
npc2_lane = random.choice(lanes)
ego_dist = 202.02

ego = Car at 0 @ 0,          # Always start ego at 0 & 0
    with name "ego",         # The ego must be named ego
    with route ["-E12", "E13"], # A route is required
    with track True,         # Follow the EGO in the GUI
    with color [0,0,255,255],# Set RGBA color to Blue
    with lane ego_lane,
    with distance ego_dist,
    with speed 0 * kph2mps,
    with changeSpeed [100*kph2mps, 150]

npc1 = Car at 0 @ 2, # Other actors should be 2 units away from each other
    with name "npc1",
    with route ["-E12", "-E11"],
    with color [255,0,0,255], # Red
    with distance Range(-50,-10) + ego_dist,
    with speed 30 * kph2mps,
    with speedMode 32,
    with lane ego_lane,
    with changeSpeed [Range(40,65)*kph2mps, 3]

npc2 = Car at 0 @ 4, # Other actors should be 4 units away from each other
    with name "npc2",
    with route ["-E14", "E13"],
    with color [0,255,0,255], # Green
    with distance 172.14,
    with lane npc2_lane,
    with speed 40 * kph2mps


param lane_npc2 = npc2.lane
param npc1_distance = npc1.distance
param npc1_changeSpeed = npc1.changeSpeed
