class MultiSegmentPmsp:
    def __init__(self):
        pass
    @staticmethod
    def evaluate(individual):
        cost = 0
        for i in range(0, individual.number_of_segments):
            for j in range(0, individual.max_routines):
                for k in range(0, individual.window_size)
                    cost = cost +  (individual.x[i][j][k] * individual.segments_routines[i][j].time_in_minutes)
        return cost
        