import random
import numpy as np

from heuristic.common.Individual import Individual
from heuristic.common.MultiSegmentPmsp import MultiSegmentPmsp


class Differential:
    def __init__(
        self,
        number_of_individuals,
        number_of_segments,
        number_of_iterations,
        routines,
        window_size,
        leader = None
    ):
        self.number_of_individuals = number_of_individuals
        self.number_of_segments = number_of_segments
        self.number_of_iterations = number_of_iterations
        self.routines = routines
        self.window_size = window_size
        self.leader = leader
        self.crossover_rate = 0.5     
        self.pop = []           

    def run(self):
        minToMaxIndividuals = None
        best_individuals_by_iteration = []
        self.pop = self.create_population()
        for i in range(0, self.number_of_iterations):
            donators = self.mutation()
            self.crossover(donators)
            minToMaxIndividuals = sorted(self.pop, key=lambda x: x.cost)
            '''
            print(
                "Best cost at iteration {}: {}".format(i, minToMaxIndividuals[0].cost)
            )
            '''
            best_individuals_by_iteration.append(minToMaxIndividuals[0].cost)
        return (minToMaxIndividuals[0], best_individuals_by_iteration)

    def mutation(self):
        donators = []
        for i in range(0, self.number_of_individuals):
            first_position = i if self.leader == None else self.leader
            first_individual = self.pop[first_position]

            second_position = None
            second_individual = None
            while True:
                second_position = random.randint(0, self.number_of_individuals - 1)
                if second_position != first_position:
                    break
            second_individual = self.pop[second_position]

            third_position = None
            third_individual = None
            while True:
                third_position = random.randint(0, self.number_of_individuals - 1)
                if (
                    third_position != second_position
                    and third_position != first_position
                ):
                    break
            third_individual = self.pop[third_position]

            new_routines_schedule = np.zeros(
                shape=(
                    self.number_of_segments,
                    first_individual.max_routines,
                    self.window_size,
                )
            )
            local_donators = [first_individual, second_individual, third_individual]           
            for j in range(0, self.number_of_segments):
                donator_count = random.randint(0, len(local_donators) - 1)
                for k in range(0, first_individual.max_routines):
                    new_routines_schedule[j][k] = local_donators[donator_count].x[j][k]
                    if donator_count == 2:
                        donator_count = 0
                    else:
                        donator_count = donator_count + 1

            donator = self.create_individual(new_routines_schedule)
            donators.append(donator)
        return donators

    def crossover(self, donators):
        for i in range(0, self.number_of_individuals):
            donator = donators[i]
            target = self.pop[i]
            new_routines_schedule = np.zeros(
                shape=(self.number_of_segments, donator.max_routines, self.window_size)
            )
            for j in range(0, self.number_of_segments):
                trial = random.uniform(0, 1)
                if trial > self.crossover_rate:
                    new_routines_schedule[j] = target.x[j]
                else:
                    new_routines_schedule[j] = donator.x[j]
            candidate = self.create_individual(new_routines_schedule)           
            if candidate.cost < target.cost:
                self.pop[i] = candidate
            '''
            elif donator.cost < target.cost:
                self.pop[i] = donator
            '''

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
