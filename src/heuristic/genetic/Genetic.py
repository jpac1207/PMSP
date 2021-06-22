import random
import numpy as np

from util.Utilities import Utilities
from heuristic.genetic.Individual import Individual
from heuristic.genetic.MultiSegmentPmsp import MultiSegmentPmsp

LOG = False

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
        self.crossover_rate = 0.6
        self.mutation_rate = 0.1
        self.pop = []

    def run(self):
        minToMaxIndividuals = None
        self.pop = self.create_population()
        for i in range(0, self.number_of_iterations):
            self.crossover()
            self.mutation()
            minToMaxIndividuals = sorted(self.pop, key=lambda x: x.cost)
            # print("Costs: {}".format(list(map(lambda x: x.cost, minToMaxIndividuals))))
            print(
                "Best cost at iteration {}: {}".format(i, minToMaxIndividuals[0].cost)
            )
        return minToMaxIndividuals[0]

    def create_population(self):
        pop = []
        for i in range(0, self.number_of_individuals):
            individual = self.create_individual()
            pop.append(individual)
        return pop

    def create_individual(self, x=np.array([])):
        individual = Individual(
            self.number_of_segments, self.routines, self.window_size, x
        )
        individual.cost = MultiSegmentPmsp.evaluate(individual)
        valid = MultiSegmentPmsp.check_constraints(individual)
        # print(individual.cost)
        if not valid:
            print("INVALID INDIVIDUAL")
            individual.cost += 10000
        return individual

    def roulette(self, s):
        sum = 0
        r = random.uniform(0, s)
        for i in range(0, len(self.pop)):
            sum += self.pop[i].cost
            if sum > r:
                # print(i)
                return i
        return random.randint(0, self.number_of_individuals - 1)

    def crossover(self):
        s = sum(list(map(lambda x: x.cost, self.pop)))
        # print(s)
        for i in range(0, self.number_of_individuals):
            prob = random.uniform(0, 1)
            if prob < self.crossover_rate:
                first_index = self.roulette(s)
                individual = self.pop[first_index]
                second_index = 0
                while True:
                    second_index = self.roulette(s)
                    another_individual = self.pop[second_index]
                    if first_index != second_index:
                        break

                new_routines_schedule = np.zeros(
                    shape=(
                        self.number_of_segments,
                        individual.max_routines,
                        self.window_size,
                    )
                )
                for j in range(0, self.number_of_segments):
                    segment_number = j
                    cut_point = random.randint(
                        0, len(individual.segments_routines[segment_number]) - 1
                    )

                    if LOG:
                        print(
                            "Segment: {}; Cut point: {}".format(
                                segment_number, cut_point
                            )
                        )

                    for k in range(0, cut_point):
                        new_routines_schedule[segment_number][k] = individual.x[
                            segment_number
                        ][k]

                    for k in range(
                        cut_point, len(individual.segments_routines[segment_number])
                    ):
                        new_routines_schedule[segment_number][k] = another_individual.x[
                            segment_number
                        ][k]

                new_individual = self.create_individual(new_routines_schedule)
                if new_individual.cost < individual.cost:
                    self.pop[first_index] = new_individual
                elif new_individual.cost < another_individual.cost:
                    self.pop[second_index] = new_individual

    def mutation(self):
        for i in range(0, self.number_of_individuals):
            prob = random.uniform(0, 1)
            if prob < self.mutation_rate:
                # get an individual randomly
                individual = self.pop[i]
                segment_number = random.randint(
                    0, self.number_of_segments - 1
                )
                routine = random.randint(0, len(individual.segments_routines[segment_number]) -1)              
                maintenance_occurrences = [x for x, y in enumerate(individual.x[segment_number][routine]) if y == 1]
                first_occurrence = maintenance_occurrences[0]               
                position = 0
                while True:
                    position = random.randint(0, self.routines[segment_number][routine].interval_in_weeks - 1)
                    if (position != first_occurrence):
                        break             
                individual.x[segment_number][routine] = np.zeros(shape=(self.window_size))
                for k in range(0, self.routines[segment_number][routine].frequency):
                    individual.x[segment_number][routine][position] = 1
                    position = (
                        position
                        + self.routines[segment_number][routine].interval_in_weeks
                    )            
                individual.cost = MultiSegmentPmsp.evaluate(individual)
                valid = MultiSegmentPmsp.check_constraints(individual)               
                if not valid:
                    print("INVALID INDIVIDUAL")
                    individual.cost += 10000               
               


