import warnings
warnings.simplefilter("ignore", UserWarning)

from scenic.simulators.sumo.simulator import SumoSimulator
import traci

def main():
    config = {
            "gui" : False,
            # "gui" : True,

            # Quiet Mode
            "--no-warnings" : "",
            "--no-step-log" : "",

            # Traci Connection
            "--num-clients" : 1,
            "--remote-port" : 5522,

            # GUI Options
            "--delay" : 50,
            "--start" : "",
            "--quit-on-end" : "",

            #Collisions
            "--collision.action" : "warn",
            "--collision.check-junctions": "", 
            "--collision.stoptime": 50,

            # RNG
            "--seed" : 333,
            
            # Step length
            "--default.action-step-length" : 0.5,
            "--step-length" : 0.5,
        }
    
    map_fn = "/home/gossq/git-projects/scenic-sumo-most/examples/sumo/maps/CurvyRoad.net.xml"
    scene_fn = "/home/gossq/git-projects/scenic-sumo/examples/sumo/scenes/traffic-light.scenic"
    simulator = SumoSimulator(map_fn, scene_fn, config)

    sim = simulator.createSimulation()

    traci.close()
    return

main()