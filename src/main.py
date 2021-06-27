from numpy.core.fromnumeric import mean
from factory.MaintenanceRoutineFactory import MaintenanceRoutineFactory
from util.ChartUtil import ChartUtil
from util.Utilities import Utilities
from strategy.Budai import Budai
from strategy.Pouryousef import Pouryousef

from heuristic.genetic.Genetic import Genetic
from heuristic.differential.Differential import Differential

T = 52  # planning horizon
GROUP_ACTIVITIES = False
NUMBER_OF_INDIVIDUALS = 100
NUMBER_OF_SEGMENTS = 5
NUMBER_OF_ITERATIONS = 100

TEST_EXECUTIONS = 10


def main():
    routines = MaintenanceRoutineFactory.get_signaling_plans()
    index = 0
    for routine in routines:
        routine.frequency = int(T / routine.interval_in_weeks)
        routine.index = index
        index = index + 1

    # MaintenanceRoutineFactory.print_list(routines)
    # Utilities.reduce_routines(routines)

    multiple_routines = Utilities.multiple_copies_from_routines(
        NUMBER_OF_SEGMENTS, routines
    )

    best = None
    all_bests_by_iteration = []
    all_bests = []
    
    bestFromDE = None
    bestFromGA = None

    for i in range(0, TEST_EXECUTIONS):
        bestFromGA = None
        bestFromDE = None
        bestsFromExecution = []
        for j in range(0, NUMBER_OF_ITERATIONS):
            bestFromGA, best_costs_by_iterationInGa = Genetic(
                NUMBER_OF_INDIVIDUALS,
                NUMBER_OF_SEGMENTS,
                15,
                multiple_routines,
                T,
                bestFromDE
            ).run()

            bestFromDE, best_costs_by_iteration = Differential(
                NUMBER_OF_INDIVIDUALS,
                NUMBER_OF_SEGMENTS,
                15,
                multiple_routines,
                T,
                bestFromGA
            ).run()
            print(bestFromGA.cost, bestFromDE.cost)
            bestFromIteration = bestFromGA if bestFromGA.cost < bestFromDE.cost else bestFromDE
            bestsFromExecution.append(bestFromIteration)
           
            if(bestFromGA.cost < bestFromDE.cost):
                bestFromDE = bestFromGA
            elif (bestFromDE.cost < bestFromGA.cost):
                bestFromGA = bestFromDE
       
        all_bests_by_iteration.append(bestsFromExecution)
        bestFromExecution = sorted(bestsFromExecution, key=lambda x: x.cost)
        print("--> ", bestsFromExecution)
        all_bests.append(bestFromExecution)        
    
    '''
    for i in range(0, TEST_EXECUTIONS):
        print("----- EXECUTION {} -----".format(i))
        bestFromExecution, best_costs_by_iteration = Genetic(
            NUMBER_OF_INDIVIDUALS,
            NUMBER_OF_SEGMENTS,
            NUMBER_OF_ITERATIONS,
            multiple_routines,
            T,
        ).run()
        all_bests.append(bestFromExecution)
        all_bests_by_iteration.append(best_costs_by_iteration)
    '''
    '''    
    for i in range(0, TEST_EXECUTIONS):
        print("----- EXECUTION {} -----".format(i))
        bestFromExecution, best_costs_by_iteration = Differential(
            NUMBER_OF_INDIVIDUALS,
            NUMBER_OF_SEGMENTS,
            NUMBER_OF_ITERATIONS,
            multiple_routines,
            T,
        ).run()
        all_bests.append(bestFromExecution)
        all_bests_by_iteration.append(best_costs_by_iteration)
    '''  
    '''
    means = []
    for i in range(0, NUMBER_OF_ITERATIONS):
        all_bests_in_i_iteration = list(map(lambda x: x[i], all_bests_by_iteration))
        means.append(mean(all_bests_in_i_iteration))
    '''
    #best = sorted(all_bests, key=lambda x: x.cost)[0]
    print('----------------------------------')
    #print(list(map(lambda x: x.cost, all_bests)))
    #print(means)

    work_labels = list(
        map(
            lambda x: "{0}:{1} [{2};{3};{4}]".format(
                x.equipment,
                x.plan_type[0:11],
                x.time_in_minutes,
                x.frequency,
                x.interval_in_weeks,
            ),
            routines,
        )
    )
    time_labels = ["t" + str(i) for i in range(1, T + 1)]
    ChartUtil.multiple_heat_maps(
        best.x,
        work_labels,
        time_labels,
        "Distribuição das Atividades: (Custo: {0} minutos)".format(best.cost),
    )
    
    # Pouryousef(2, multiple_routines, T, GROUP_ACTIVITIES)

    """
    response = Budai(routines, T, GROUP_ACTIVITIES).max_to_min()   
    work_labels = (list(map(lambda x: "{0}:{1} ({2})".format(x.equipment, x.plan_type[0:11], x.time_in_minutes), routines)))
    time_labels = (['t' + str(i) for i in range(1, T + 1)])
    ChartUtil.heat_map(response[0], work_labels, time_labels, "Distribuição das Atividades: (Custo: {0} minutos)".format(response[3]))
    ChartUtil.heat_map(response[1], ['Custo de Manutenção'], time_labels, "Distribuição das Atividades: (Custo: {0} minutos)".format(response[3]), True)    
    """


if __name__ == "__main__":
    main()
