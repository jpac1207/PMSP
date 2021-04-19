import numpy as np

class Budai:
    def __init__(self, routines, window_size, group_activities=False):
        self.routines = routines
        self.window_size = window_size
        self.group_activities = group_activities
        self.x = np.array([])
        self.c = np.array([])
        self.init_variables()

    def init_variables(self):
        self.x = np.zeros((len(self.routines), self.window_size))
        self.c = np.zeros((len(self.routines), self.window_size))

    def insert_test_occurrences(self):
        self.add_occurrence(0, 0, self.routines[0].time_in_minutes)
        self.add_occurrence(0, 12, self.routines[0].time_in_minutes)
        self.add_occurrence(0, 24, self.routines[0].time_in_minutes)
        self.add_occurrence(0, 36, self.routines[0].time_in_minutes)

    def add_occurrence(self, row_index, collumn_index, cost):
        self.x[row_index][collumn_index] = 1
        self.c[row_index][collumn_index] = cost

    def cost(self):
        cost = 0
        for index in range(0, self.window_size):
            cost = cost + max(self.c[:, index])
        return cost

    def check_constraints(self):
        for index in range(0, len(self.routines)):
            routine = self.routines[index]
            occurrences = self.x[index]

            # First constraint
            maintenance_activities_first_cycle = [
                (i + 1)
                for i, x in enumerate(occurrences[0 : routine.interval_in_weeks - 1])
                if x == 1
            ]
            if len(maintenance_activities_first_cycle) != 1:
                return False

            # Second constraint
            maintenance_activities = [
                (i + 1) for i, x in enumerate(occurrences) if x == 1
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

    def get_first_avaliable_period(self, routine):
        for t in range(0, routine.interval_in_weeks - 1):
            start_window = t
            free_window = 0
            for s in range(0, routine.frequency):
                print(s)
                if 1 in (self.x[:, start_window]):
                    break
                else:
                    free_window = free_window + 1
                start_window = start_window + (routine.interval_in_weeks - 1)
            if free_window == routine.frequency:
                return t
        print("here")
        return -1

    def get_minor_cost_period(self, routine):
        costs = {}
        for s in range(0, routine.interval_in_weeks - 1):
            period = s
            for t in range(0, routine.frequency):
                self.add_occurrence(routine.index, period, routine.time_in_minutes)
                period = period + routine.interval_in_weeks - 1
            costs[s] = self.cost()
            # clear interval
            period = s
            for t in range(0, routine.frequency):
                self.add_occurrence(routine.index, period, 0)
                period = period + routine.interval_in_weeks - 1

        minor_cost = min(costs, key=costs.get)
        return minor_cost

    # O(n(n + p)T 2)
    def max_to_min(self):
        return self.frequency(True)

    # O(n(n + p)T 2)
    def min_to_max(self):
        return self.frequency(False)

    def frequency(self, reverse):
        sorted_routines = sorted(
            self.routines, key=lambda x: x.frequency, reverse=reverse
        )
        # first item
        period = 0
        for t in range(0, sorted_routines[0].frequency):
            self.add_occurrence(
                sorted_routines[0].index, period, sorted_routines[0].time_in_minutes
            )
            period = period + sorted_routines[0].interval_in_weeks - 1

        for routine in sorted_routines[1:]:
            period = (
                self.get_minor_cost_period(routine)
                if self.group_activities
                else self.get_first_avaliable_period(routine)
            )
            for t in range(0, routine.frequency):
                self.add_occurrence(routine.index, period, routine.time_in_minutes)
                period = period + routine.interval_in_weeks - 1
            # break
        return (self.x, self.c, self.check_constraints(), self.cost())
