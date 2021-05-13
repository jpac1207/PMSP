import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class ChartUtil:
    @staticmethod
    def heat_map(data, y_labels, x_labels, title, show=False):
        if len(data.shape) == 1:
            data = np.array([data])
        fig, ax = plt.subplots()
        sns.heatmap(
            data,
            ax=ax,
            xticklabels=x_labels,
            yticklabels=y_labels,
            annot=True,
            cmap="YlGnBu",
            cbar=False,
            annot_kws={"rotation": 90},
            fmt="g",
        )
        ax.set_title(title)
        if show:
            plt.show()

    @staticmethod
    def multiple_heat_maps(data, y_labels, x_labels, title):
        number_of_segments = len(data)
        fig = plt.figure()
        for i in range(0, number_of_segments):
            ax = fig.add_subplot(number_of_segments, 1, i + 1)
            #print(data)
            #print("---------------------")
            sns.heatmap(
                data[i],
                ax=ax,
                xticklabels=x_labels,
                yticklabels=y_labels,
                annot=True,
                cmap="YlGnBu",
                cbar=False,
                annot_kws={"rotation": 90},
                fmt="g",
            )
            if(i == 0):
                ax.set_title(title)

        plt.show()

