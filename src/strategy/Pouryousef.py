import numpy as np

class Pouryousef:
    def __init__(self, segments_count, routines, window_size, group_activities=False):
        self.segments_count = segments_count
        self.routines = routines
        self.window_size = window_size
        self.group_activities = group_activities
        self.x = np.zeros(shape=(self.segments_count, len(self.routines), self.window_size))
        self.c = np.zeros(shape=(self.segments_count, self.window_size))
        print(self.c)
        #self.init_variables()

    def init_variables(self):
        for i in range(0, self.segments_count):
            print(i)
            self.x = np.append(self.x, np.zeros((len(self.routines), self.window_size)), axis=0)
            self.c = np.append(self.c, np.zeros(self.window_size))
        print(self.x)
        print(self.x.shape)
