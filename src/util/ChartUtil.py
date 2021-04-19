import matplotlib.pyplot as plt
import numpy as np

class ChartUtil:
    @staticmethod
    def heat_map(data, work_set, times_set, title):
        fig, ax = plt.subplots()
        im = ax.imshow(data)
        
        ax.set_xticks(np.arange(len(times_set)))
        ax.set_yticks(np.arange(len(work_set)))
        ax.set_xticklabels(times_set)
        ax.set_yticklabels(work_set)
        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Loop over data dimensions and create text annotations.
        for i in range(len(work_set)):
            for j in range(len(times_set)):
                text = ax.text(j, i, data[i, j], ha="center", va="center", color="w")

        ax.set_title(title)
        #fig.tight_layout()
        plt.show()

