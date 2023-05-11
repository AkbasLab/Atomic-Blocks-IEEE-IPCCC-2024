import pandas as pd
import sim_bug_tools.graphics as sbt_graphics
import matplotlib.pyplot as plt
import numpy as np
import os

# Error Scenario 2sp5, 
# The EGO changes lanes at 0 speed in 2sp1


class Graphics:
    def __init__(self):
        test_id = "20230426001936"
        self.test_id = test_id
        self.params_df = pd.read_csv("out/PARAM%s.tsv" % test_id, sep="\t")
        self.scores_df = pd.read_csv("out/SCORE%s.tsv" % test_id, sep="\t")

        self.out_dir = "box/%s" % test_id
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        # self.histogram_params(self.params_df)
        # print(self.scores_df.describe())
        # print(self.scores_df.columns)

        

        


        # for feat in self.scores_df.columns:
        #     if not "ped" in feat:
        #         self.score_stats(feat)
        return
    
    def score_stats(self, score_id : str):
        # find indices of scenes with events
        tsc_indices = self.scores_df[self.scores_df[score_id] > 0].index
        tsc_indices_set = set(tsc_indices)
        
        # Retrieve Scores
        scores = self.scores_df.iloc[tsc_indices][score_id]
        
        # Plot Scores Over Time
        tsc_count = []
        n = 0
        for i in range(len(self.scores_df.index)):
            if i in tsc_indices_set:
                n += 1
            tsc_count.append(n)
            continue

        # Make the plot
        x = [i for i in range(len(tsc_count))]
        y = tsc_count
        plt.figure(figsize=(5,5))
        ax = plt.axes()
        ax.plot(x, y, color="black")
        ax.set_xlabel("# Tests")
        ax.set_ylabel("%s > 0" % score_id)
        ax.set_title("Target Scenarios Located")
        plt.tight_layout()
        plt.savefig("%s/%s_over_time.png" % (self.out_dir, score_id))

        # Save Target scenario parameters
        df = self.params_df.iloc[tsc_indices] \
            .set_index(tsc_indices)
        df[score_id] = scores
        df.to_csv("%s/%s_target_scenarios.csv" % (self.out_dir, score_id))
        return
    
    def histogram_params(self, df : pd.DataFrame):
        plt.figure(figsize=(5,7))
        ax = plt.axes()
        ncol = int(np.ceil(len(df.columns)/2))
        df.hist(ax = ax, color="black", grid=False, bins=50, layout=(ncol,2))
        plt.tight_layout()
        plt.savefig("figures/hhh.png")
        return 

if __name__ == "__main__":
    Graphics()