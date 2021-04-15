class Budai:
    def __init__(self, routines, window_size):
        self.routines = routines
        self.window_size = window_size
        self.x = []
        self.c = []
        self.init_variables()

    def init_variables(self):
        for routine in self.routines:
            self.x.append([0] * self.window_size)
            self.c.append([0] * self.window_size)
            break
        self.insert_test_occurrences()
        print(self.check_constraints())
        print(self.cost())

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
        for index in range(0, 1):
            cost = cost + sum([a * b for a, b in zip(self.x[index], self.c[index])])
        return cost

    def check_constraints(self):

        for index in range(0, 1):
            routine = self.routines[index]
            occurrences = self.x[index]
            print(occurrences)
            # first constraint
            if 1 not in occurrences[0 : routine.interval_in_weeks]:
                return False
            # second constraint
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

