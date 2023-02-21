import PySimpleGUI as sg
import os
import pandas as pd
from datetime import datetime

import warnings
warnings.simplefilter("ignore", UserWarning)

from scenic.simulators.sumo.simulator import SumoSimulator
import traci

class ScenicSUMOGui:
    def __init__(self):
        
        self.config = {
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
            # "--start" : "",
            "--quit-on-end" : "",

            # Logging
            "--error-log" : "error.txt",

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

        self.init_window()

        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = self.window.read()
            self.event = event
            self.values = values
            
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            elif event == "cb-gui":
                self.window["cb-start"].update(disabled=not values[event])
                self.config["gui"] = values["cb-gui"]
            elif event == "cb-start":
                self.config.pop("--start", None)
                if values["cb-start"]:
                    self.config["--start"] = ""
            elif event in ["map-fn", "scene-fn", "out-dir"]:
                if os.path.isfile(values["map-fn"]) \
                    and values["map-fn"].lower().endswith(".net.xml") \
                    and os.path.isfile(values["scene-fn"]) \
                    and values["scene-fn"].lower().endswith(".scenic") \
                    and os.path.isdir(values["out-dir"]):
                    self.window["run"].update(disabled=False)
                else:
                    self.window["run"].update(disabled=True)
            elif event == "run":
                self.window["run"].update(disabled=True)
                self.run()
                self.window["run"].update(disabled=False)
                pass
                
        self.window.close()
        return
    
    def run(self):
        

        map_fn = self.values["map-fn"]
        scene_fn = self.values["scene-fn"]
        out_dir = self.values["out-dir"]
        n_tests = self.values["n-tests"]
        
        simulator = SumoSimulator(map_fn, scene_fn, self.config)

        for n in range(1,n_tests+1):
            simulator.createSimulation()
            self.window["pb-runs"].update(n/n_tests)

        traci.close()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        out_dir.rstrip("/")
        out_dir.rstrip("\\")

        pd.DataFrame(
            [pd.Series(scene.params) for scene in simulator.scenes]
        ).to_csv(
            "%s/PARAM%s.tsv" % (out_dir,timestamp),
            sep = "\t",
            index = False
        )

        pd.DataFrame(
            [pd.Series(sim.score) for sim in simulator.sims]
        ).to_csv(
            "%s/SCORE%s.tsv" % (out_dir,timestamp),
            sep = "\t",
            index = False
        )

        self.window["pb-runs"].update(1.01)
        return
    
    def init_window(self):
        sg.theme("SystemDefault1")

        BROWSE_SIZE = 30

        # All the stuff inside your window.
        layout = [  
            [ 
                sg.Push(), sg.T('*.net.xml File:'), 
                sg.In(key="map-fn", size = BROWSE_SIZE, enable_events = True), 
                sg.FileBrowse(
                    target = "map-fn", 
                    file_types = (("SUMO Network","*.net.xml"),),
                )
            ], 
            [
                sg.Push(), sg.Text("Scenic File:"),
                sg.In(key="scene-fn", size = BROWSE_SIZE, enable_events = True),
                sg.FileBrowse(
                    target = "scene-fn",
                    file_types = (("Scenic Files", ("*.scenic")),),
                )
            ],
            [
                sg.Push(), sg.Text("Output Directory:"),
                sg.In(key="out-dir", size = BROWSE_SIZE, enable_events = True),
                sg.FolderBrowse(target = "out-dir")
            ],
            [
                sg.T("Tests to Run:"),
                sg.Spin(
                    [1,5,10,50,100,500,1000,5000,10_000,50_000,100_000],
                    initial_value = 1,
                    key = "n-tests",
                    size=6,
                    readonly = True
                ),
                sg.Checkbox("GUI", key="cb-gui", enable_events=True),
                sg.Checkbox("Start Simulation", default=True, disabled=True,
                            key="cb-start", enable_events=True) 
            ],
            [
                sg.ProgressBar(
                    1.01, 
                    orientation="h", 
                    size=(38,20), 
                    key="pb-runs"
                )
            ],
            [
                sg.Button("Run", key="run", disabled=True), 
                # sg.Button("Cancel", key="cancel", disabled=True)
            ]
        ]

        # Create the Window
        self.window = sg.Window('Window Title', layout)
        return
    
if __name__ == "__main__":
    ScenicSUMOGui()