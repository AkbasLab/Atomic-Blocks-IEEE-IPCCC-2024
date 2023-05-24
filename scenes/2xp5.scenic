from scenic.simulators.sumo.model import *
from scenic.core.distributions import *

model scenic.simulators.sumo.model

"""Uses 2xp5allnetworksedit.net.xml"""

# In SUMO speed is in meters per second. But we imagine speed in Kilometers
# per second, so we must convert from KPH to MPS.

kph2mps = 1/3.6
mps2kph = 3.6
lanes = [1,2]
ego_lane = random.choice(lanes)
npc1_lane = ego_lane

ego_dist = 180

ego = Car at 0 @ 0,          # Always start ego at 0 & 0
    with name "ego",         # The ego must be named ego
    with route ["-E12", "-E11"], # A route is required
    #with track True,         # Follow the EGO in the GUI
    with color [0,0,255,255],# Set RGBA color to Blue
    with lane ego_lane,
    with speed Range(20,50) * kph2mps,
    with distance ego_dist,
    with changeSpeed [5*kph2mps, 5] #decelaration due to ped1
npc1 = Car at 0 @ 2, # Other actors should be 2 units away from each other
    with name "npc1",
    with route ["-E12", "-E11"],
    with color [255,0,0,255], # Red
    with distance Range(-70,-10) + ego_dist,
    with lane npc1_lane,
    with speedMode 32,
    with speed Range(40,80) * kph2mps


ped1 = Pedestrian at 0 @ 4,
    with name "ped1",
    with route ["-E12","E12"],
    with color [255,0,255,255], #purple
    with departTime 0,
    with distance 202,
    with egoWaitAtXing True

param ego_speed = ego.speed * mps2kph
param ego_lane = ego.lane
param npc1_speed = npc1.speed * mps2kph
param npc1_distance = npc1.distance
