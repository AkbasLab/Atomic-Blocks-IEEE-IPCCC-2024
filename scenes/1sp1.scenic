from scenic.simulators.sumo.model import *
from scenic.core.distributions import *

model scenic.simulators.sumo.model

"""Uses allnetworks.net.xml"""

# In SUMO speed is in meters per second. But we imagine speed in Kilometers
# per second, so we must convert from KPH to MPS.
kph2mps = 1/3.6
mps2kph = 3.6

ego = Car at 0 @ 0,          # Always start ego at 0 & 0
    with name "ego",         # The ego must be named ego
    with route ["E2", "E3"], # A route is required
    # with track True,         # Follow the EGO in the GUI
    with color [0,0,255,255],# Set RGBA color to Blue
    with departTime Range(10,25),
    with speed Range(10,50) * kph2mps # Set vehicle speed 10-50 kph
    #HOW TO EDIT EGO DISTANCE RANGE FROM CROSSING?
ped1 = Pedestrian at 0 @ 2,
        with name "ped1",
        with route ["-E3","E2"],
        with color [255,255,0,255],
        with departTime Range(0,0.1),
        with distance Range(200,200.36),
        with egoWaitAtXing True

param ego_speed = ego.speed * mps2kph
param departTime_ped = ped1.departTime
