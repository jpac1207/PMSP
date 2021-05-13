from heuristic.genetic.Individual import Individual
from heuristic.genetic.MultiSegmentPmsp import MultiSegmentPmsp

class Genetic:
    def __init__(self, number_of_individuals, number_of_segments, number_of_iterations, routines, window_size):
        self.number_of_individuals = number_of_individuals
        self.number_of_segments = number_of_segments
        self.number_of_iterations = number_of_iterations
        self.routines = routines
        self.window_size = window_size
    
    def run(self):
        pop = []
        for i in range(0, self.number_of_individuals):          
            individual = Individual(self.number_of_segments, self.routines, self.window_size)
            individual.cost = MultiSegmentPmsp.evaluate(individual)
            valid = MultiSegmentPmsp.check_constraints(individual)
            pop.append(individual)
            print(individual.cost)
            if(not valid):
                return individual

        return pop[0]


