import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class ChartUtil:
    @staticmethod
    def heat_map(data, work_set, times_set, title):      
    
        fig, ax = plt.subplots(figsize=(20,15))       
        sns.heatmap(data, ax=ax, xticklabels=times_set, yticklabels=work_set, annot=True, linewidths=0.5, cmap="YlGnBu", cbar=False,)
        ax.set_title(title)
        plt.show()

