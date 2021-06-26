import numpy as np

class MultiSegmentPmsp:
    def __init__(self):
        pass

    """
    @staticmethod
    def evaluate(individual):
        cost = 0
        for i in range(0, individual.number_of_segments):
            for j in range(0, individual.max_routines):
                for k in range(0, individual.window_size):
                    cost = cost +  (individual.x[i][j][k] * individual.segments_routines[i][j].time_in_minutes)
        return cost
    """

    @staticmethod
    def evaluate(individual):
        cost = 0
        for i in range(0, individual.number_of_segments):
            for j in range(0, individual.window_size):
                #print(individual.x[i][:, j])
                time_in_minutes_by_activity = np.array(list(map(lambda x: x.time_in_minutes, individual.segments_routines[i][:])))
                cost = cost + (
                    max(individual.x[i][:, j]
                    * time_in_minutes_by_activity)
                )
        return cost

    @staticmethod
    def check_constraints(individual):
        for i in range(0, individual.number_of_segments):
            # print('i:', i)
            activities_from_segment = individual.segments_routines[i]
            occurrences_from_segment = individual.x[i]
            for j in range(0, individual.max_routines):
                # print('j:', j)
                routine = activities_from_segment[j]
                occurrences = occurrences_from_segment[j]
                # First constraint
                maintenance_activities_first_cycle = [
                    (k + 1)
                    for k, x in enumerate(occurrences[0 : routine.interval_in_weeks])
                    if x == 1
                ]
                if len(maintenance_activities_first_cycle) != 1:
                    print(maintenance_activities_first_cycle)
                    print("here")
                    return False

                # Second constraint
                maintenance_activities = [
                    (k + 1) for k, x in enumerate(occurrences) if x == 1
                ]
                if len(maintenance_activities) != routine.frequency:
                    print("here2")
                    return False

                if len(maintenance_activities) > 0:
                    for mindex in range(1, len(maintenance_activities)):
                        if maintenance_activities[mindex] - maintenance_activities[
                            mindex - 1
                        ] != (routine.interval_in_weeks):
                            print("here3")
                            return False
        return True

