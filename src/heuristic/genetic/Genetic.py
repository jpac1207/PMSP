import random
from util.Utilities import Utilities
from heuristic.genetic.Individual import Individual
from heuristic.genetic.MultiSegmentPmsp import MultiSegmentPmsp


class Genetic:
    def __init__(
        self,
        number_of_individuals,
        number_of_segments,
        number_of_iterations,
        routines,
        window_size,
    ):
        self.number_of_individuals = number_of_individuals
        self.number_of_segments = number_of_segments
        self.number_of_iterations = number_of_iterations
        self.routines = routines
        self.window_size = window_size
        self.crossover_rate = 0.7

    def run(self):
        pop = self.create_population()
        #self.crossover(pop)
        return pop[0]

    def create_population(self):
        pop = []
        for i in range(0, self.number_of_individuals):
            individual = Individual(
                self.number_of_segments, self.routines, self.window_size
            )
            individual.cost = MultiSegmentPmsp.evaluate(individual)
            valid = MultiSegmentPmsp.check_constraints(individual)
            pop.append(individual)
            # print(individual.cost)
            if not valid:
                print("INVALID INDIVIDUAL")
                individual.cost += 10000
        return pop

    def crossover(self, pop):
        for i in range(0, self.number_of_individuals):
            prob = random.uniform(0, 1)
            if prob < self.crossover_rate:
                individual = pop[i]
                # pick a segment
                segment_number = random.randint(0, self.number_of_segments - 1)
                #print(segment_number)
                #print(individual.segments_routines[segment_number])
                #pick a routine
                routine_number = random.randint(0, len(individual.segments_routines[segment_number]) - 1)
                routine = individual.segments_routines[segment_number][routine_number]
                for j in range(0, len(individual.segments_routines[segment_number])):
                    if(j != routine_number):
                        print(Utilities.lcm(routine_number, j))
               

