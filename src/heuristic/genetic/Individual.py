import numpy as np
from random import randint

class Individual:
    def __init__(self, number_of_segments, segments_routines, window_size, x = np.array([])):       
        self.x = x
        self.cost = 0
        self.number_of_segments = number_of_segments
        self.segments_routines = segments_routines
        self.window_size = window_size
        self.max_routines = None
        self.init_individual()

    def init_individual(self):   
        max_routines = max(list(map(lambda x: len(x), self.segments_routines)))
        self.max_routines = max_routines
        if(self.x.size == 0):          
            self.x = np.zeros(
                shape=(self.number_of_segments, self.max_routines, self.window_size)
            )

            for i in range(0, self.number_of_segments):
                for j in range(0, len(self.segments_routines[i])):
                    start_position = randint(0, self.segments_routines[i][j].interval_in_weeks - 1)
                    #print('[{0},{1}]'.format(0, self.segments_routines[i][j].interval_in_weeks - 1))
                    #print(start_position)
                    for k in range(0, self.segments_routines[i][j].frequency):
                        self.x[i][j][start_position] = 1
                        start_position = start_position + self.segments_routines[i][j].interval_in_weeks
                #print(self.x)
    def to_string(self):
        return self.x

