import FreeSimpleGUI as sg
import os
import pandas as pd
from datetime import datetime
import logging
import traci
import operator
import re
import matplotlib.pyplot as plt

LOG_FILENAME = "log.txt"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

import warnings
warnings.simplefilter("ignore", UserWarning)

from scenic.simulators.sumo.simulator import SumoSimulator
import traci

class ScenicSUMOGui:
    def __init__(self):
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        self.stats_dir = "%s/stats" % self.file_dir

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
            "--start" : "",
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

        # self.generate_scores()
        # quit()

        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = self.window.read()
            self.event = event
            self.values = values
            
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break

            # Run Scenarios
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
            elif event == "run" or event =="test":
                self.window["run"].update(disabled=True)
                try:
                    self.run()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:
                    logging.exception("Exception caught at runtime...")
                    traci.close()
                    print("Run terminated, see log.txt for details!")
                    pass
                self.window["run"].update(disabled=False)
                pass

            # Scenario Statistics
            if event == "generate-scores":
                self.generate_scores()


                
        self.window.close()
        return
    
    def run(self):
        # print(self.config)
        # self.values = {
        #     "map-fn" : "map/allnetworksedit.net.xml",
        #     "scene-fn" : "scenes/2sp1.scenic",
        #     "out-dir" : "out",
        #     "n-tests" : 10_000,
        # }
        

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
    
    def generate_scores(self):
        # Load params and scores
        # params_fn = self.values["params-fn"]
        # scores_fn = self.values["scores-fn"]
        params_fn = "out\parameter and scores\PARAM2t120230425231600.tsv"
        scores_fn = "out\parameter and scores\SCORE2t120230425231600.tsv"
        params_df = pd.read_csv(params_fn, sep="\t")        
        scores_df = pd.read_csv(scores_fn, sep="\t")

        # Parse run id
        run_id = scores_fn.split("\\")[-1].lower()[5:-4]

        # Stat directory
        run_stat_dir = "%s/%s" % (self.stats_dir, run_id)
        if not os.path.exists(run_stat_dir):
            os.makedirs(run_stat_dir)
        
        # Build the TSC
        ops = {
            ">"  : operator.gt,
            ">=" : operator.ge,
            "<"  : operator.lt,
            "<=" : operator.lt,
            "==" : operator.eq,
            "and": operator.and_,
            "or" : operator.or_
        }

        f0 = self.values["tsc_feature_0"]
        c0 = self.values["tsc_comparator_0"]
        try:
            v0 = float(re.findall(r"\d+\.*\d*",self.values["tsc_value_0"])[0])
        except IndexError:
            return
        
        if self.values["tsc_includer_1"] == "":
            tsc = lambda s : ops[c0]( s[f0], v0)
        else:
            i1 = self.values["tsc_includer_1"]
            f1 = self.values["tsc_feature_1"]
            c1 = self.values["tsc_comparator_1"]
            try:
                v1 = float(re.findall(r"\d+\.*\d*",self.values["tsc_value_1"])[0])
            except IndexError:
                return
            tsc = lambda s : ops[i1]( ops[c0]( s[f0], v0), ops[c1]( s[f1], v1))
        
        # Get indices of score with parameters
        tsc_indices = scores_df[scores_df.apply(tsc, axis=1)].index
            

        # Scores over time
        tsc_indices_set = set(tsc_indices)
        tsc_count = []
        n = 0
        for i in range(len(scores_df.index)):
            if i in tsc_indices_set:
                n += 1
            tsc_count.append(n)
            continue
        
        # Make the plot
        # x = [i for i in range(len(tsc_count))]
        # y = tsc_count
        # plt.figure(figsize=(5,5))
        # ax = plt.axes()
        # ax.plot(x, y, color="black")
        # ax.set_xlabel("# Tests")
        # ax.set_ylabel("%s > 0" % score_id)
        # ax.set_title("Target Scenarios Located")
        # plt.tight_layout()
        # plt.savefig("%s/%s_over_time.png" % (self.out_dir, score_id))

        return

    def init_window(self):
        sg.theme("SystemDefault1")

        BROWSE_SIZE = 30

        # All the stuff inside your window.'
        tab_run_scenarios = [  
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
                # sg.Button("Cancel", key="cancel", disabled=True),
                # sg.Button("Test", key="test")
            ]
        ]

        tab_score_stats = [
            [
                sg.Push(), sg.Text("Parameters TSV:"), 
                sg.In(key="params-fn", size=BROWSE_SIZE, enable_events=True),
                sg.FileBrowse(
                    target="params-fn",
                    file_types = (("Tab Seperated Value", ("*.tsv")),),
                )
            ],
            [
                sg.Push(), sg.Text("Scores TSV:"), 
                sg.In(key="scores-fn", size=BROWSE_SIZE, enable_events=True),
                sg.FileBrowse(
                    target="scores-fn",
                    file_types = (("Tab Seperated Value", ("*.tsv")),),
                )
            ],
            [sg.Text("Target Score Classification")],
            self.tsc_row(0, True),
            self.tsc_row(1),
            [sg.Button("Generate", key="generate-scores")]
        ]

        layout = [[sg.TabGroup([[
            sg.Tab("Run Scenarios", tab_run_scenarios),
            sg.Tab("Score Statistics", tab_score_stats)
        ]])]]

        # Create the Window
        self.window = sg.Window('SCENIC-SUMO GUI', layout)
        return
    
    def tsc_row(self, key_id : int, first : bool = False) -> list:
        row = [   
            sg.Combo(
                values = ["", "and", "or"],
                readonly=True,
                size=3,
                default_value="",
                disabled=first,
                key="tsc_includer_%d" % key_id
            ),
            sg.Combo(
                values=["e_brake_partial", "e_brake_full", "e_stop", 
                    "collision", "ped_ego_wait_at_xing_event"],
                readonly=True,
                size=15,
                default_value="e_brake_partial",
                key = "tsc_feature_%d" % key_id
            ),
            sg.Combo(
                values=[">", ">=", "<", "<=", "=="],
                readonly=True,
                size=2,
                default_value=">",
                key = "tsc_comparator_%d" % key_id
            ),
            sg.Input("0", size=5, key="tsc_value_%d" % key_id)
        ]
        return row
    
if __name__ == "__main__":
    ScenicSUMOGui()