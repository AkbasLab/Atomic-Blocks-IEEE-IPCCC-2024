from scenic.simulators.sumo.model import *
from scenic.core.distributions import *

model scenic.simulators.sumo.model

"""Uses 3way.net.xml"""

# In SUMO speed is in meters per second. But we imagine speed in Kilometers
# per second, so we must convert from KPH to MPS.
kph2mps = 1/3.6
mps2kph = 3.6

ego = Car at 0 @ 0,          # Always start ego at 0 & 0
    with name "ego",         # The ego must be named ego
    with route ["E6", "E8"], # A route is required
    # with track True,         # Follow the EGO in the GUI
    with color [0,0,255,255],# Set RGBA color to Blue
    with speed Range(1,40) * kph2mps # Set vehicle speed 1-50 kph

npc1 = Car at 0 @ 2, # Other actors should be 2 units away from each other
    with name "npc1",
    with route ["-E7", "E8"],
    with color [255,0,0,255], # Red
    with speed Range(1,30) * kph2mps
npc2 = Car at 0 @ 4, # Other actors should be 4 units away from each other
        with name "npc2",
        with route ["-E8", "-E6"],
        with color [0,255,0,255], # Green
        with speed Range(1,30) * kph2mps
ped1 = Pedestrian at 0 @ 6,
        with name "ped1",
        with route ["-E7","-E8"],
        with color [255,255,0,255],
        with departTime Range(0,5),
        with distance Range(80,100),
        with egoWaitAtXing True
Traf1 = TrafficLight at 0 @ 8,
    with name "J8",
    with state ["GGgrrrgGGrGr","GGgrryyrrrrr"],
    with duration [2,5]
    



param ego_speed = ego.speed * mps2kph
param npc1_speed = npc1.speed * mps2kph
param npc2_speed = npc2.speed * mps2kph
param departTime_ped = ped1.departTime
