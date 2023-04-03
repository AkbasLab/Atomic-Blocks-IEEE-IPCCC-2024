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
npc1_lane = 2
ego_dist = Range(150,180)
npc1_dist = Range(147,148)

ego = Car at 0 @ 0,          # Always start ego at 0 & 0
    with name "ego",         # The ego must be named ego
    with route ["E4", "E5"], # A route is required
    # with track True,         # Follow the EGO in the GUI
    with color [0,0,255,255],# Set RGBA color to Blue
    with lane ego_lane,
    with distance ego_dist,
    with speed Range(30,50) * kph2mps # Set vehicle speed 30-50 kph

npc1 = Car at 0 @ 2, # Other actors should be 2 units away from each other
    with name "npc1",
    with route ["-E6", "-E4"],
    with color [255,0,0,255], # Red
    with lane npc1_lane,
    with distance npc1_dist,
    with speed Range(30,50) * kph2mps,
    with changeSpeed [0*kph2mps, 7]



param ego_speed = ego.speed * mps2kph
param npc1_speed = npc1.speed * mps2kph
param npc1_distance = npc1.distance
