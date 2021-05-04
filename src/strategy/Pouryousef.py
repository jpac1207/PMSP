import numpy as np

class Pouryousef:
    def __init__(self, segments_count, routines, window_size, group_activities=False):
        self.segments_count = segments_count
        self.routines = routines
        self.window_size = window_size
        self.group_activities = group_activities
        self.x = None
        self.c = None       
        self.init_variables()
        self.insert_data()
        print(self.check_constraints())
        #print(self.cost())

    def init_variables(self):
        max_routines = max(list(map(lambda x: len(x), self.routines)))        
        self.x = np.zeros(shape=(self.segments_count, max_routines, self.window_size))
        self.c = np.zeros(shape=(self.segments_count, self.window_size))       
        #print(self.x)
        #print(self.x.shape)

    def insert_data(self):
        for i in range(0, self.segments_count):
            for j in range(0, len(self.routines[i])):               
                self.add_occurrence(i, j, 1, 10)
            #self.add_occurrence(i, 0, 1, 10)

    def add_occurrence(self, segment, row_index, collumn_index, cost):
        self.x[segment][row_index][collumn_index] = 1
        self.c[segment][collumn_index] = self.c[segment][collumn_index] + cost

    def delete_occurrence(self, segment, row_index, collumn_index, time_to_descrease):
        self.x[segment][row_index][collumn_index] = 0
        self.c[segment][collumn_index] = self.c[segment][collumn_index] - time_to_descrease

    def cost(self):
        cost = 0
        for i in range(0, self.segments_count):
            for j in range(0, self.window_size):
                cost = cost + self.c[i][j]
        return cost
    
    def verify_first_and_second_constraint(self):
         
        for i in range(0, self.segments_count):
            activities_from_segment = self.routines[i]
            occurrences_from_segment = self.x[i]            
            for j in range(0, len(activities_from_segment)):             
                routine = activities_from_segment[j]
                occurrences = occurrences_from_segment[j]
                # First constraint
                maintenance_activities_first_cycle = [
                    (k + 1)
                    for k, x in enumerate(occurrences[0 : routine.interval_in_weeks - 1])
                    if x == 1
                ]
                if len(maintenance_activities_first_cycle) != 1:
                    return False
                # Second constraint
                maintenance_activities = [
                    (k + 1) for k, x in enumerate(occurrences) if x == 1
                ]
                if len(maintenance_activities) != routine.frequency:
                    return False
                if len(maintenance_activities) > 0:
                    for mindex in range(1, len(maintenance_activities)):
                        if maintenance_activities[mindex] - maintenance_activities[
                            mindex - 1
                        ] != (routine.interval_in_weeks - 1):
                            return False
        return True

    def check_constraints(self):
        
        return self.verify_first_and_second_constraint()
        
