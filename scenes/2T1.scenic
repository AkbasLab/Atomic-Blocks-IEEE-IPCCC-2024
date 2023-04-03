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
route2 = ["-E4","E5"]
egoR2 = random.choice(route2)
ego_speed = Range(30,50)*kph2mps
npc1_speedChange = ego_speed + Range(10,30)*kph2mps
npc1_lane = ego_lane
npc2_lane = random.choice(lanes)
npc2_dist = Range(180,188)
ego_dist = Range(147.3,148.8)

ego = Car at 0 @ 0,          # Always start ego at 0 & 0
    with name "ego",         # The ego must be named ego
    with route ["-E6", egoR2], # A route is required
    # with track True,         # Follow the EGO in the GUI
    with color [0,0,255,255],# Set RGBA color to Blue
    with lane ego_lane,
    with distance ego_dist,
    with speed ego_speed # Set vehicle speed 30-50 kph

npc1 = Car at 0 @ 2, # Other actors should be 2 units away from each other
    with name "npc1",
    with route ["-E6", egoR2],
    with color [255,0,0,255], # Red
    with lane npc1_lane,
    with distance Range(-100,-10) + ego_dist,
    with speed ego_speed,
    with changeSpeed [npc1_speedChange, range(0,5)]

npc2 = Car at 0 @ 4,
    with name "npc2",
    with route ["E4", "E5"],
    with lane npc2_lane,
    with distance npc2_dist,
    with color [255,255,0,255], #yellow
    with speed Range(30,50) * kph2mps



param ego_speed = ego.speed * mps2kph
param ego_lane = ego.lane
param npc1_speed = npc1.speed * mps2kph
param npc1_distance = npc1.distance
param npc2_speed = npc2.speed * mps2kph
param npc1_lane = npc1.lane
param npc2_lane = npc2.lane
