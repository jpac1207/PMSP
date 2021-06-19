from factory.MaintenanceRoutineFactory import MaintenanceRoutineFactory
from util.ChartUtil import ChartUtil
from util.Utilities import Utilities
from strategy.Budai import Budai
from strategy.Pouryousef import Pouryousef

from heuristic.genetic.Genetic import Genetic

T = 52  # planning horizon
GROUP_ACTIVITIES = False
NUMBER_OF_INDIVIDUALS = 2
NUMBER_OF_SEGMENTS = 1

NUMBER_OF_ITERATIONS = 1

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
    
    best = Genetic(
        NUMBER_OF_INDIVIDUALS, NUMBER_OF_SEGMENTS, NUMBER_OF_ITERATIONS, multiple_routines, T
    ).run()
    work_labels = list(
        map(
            lambda x: "{0}:{1} [{2};{3};{4}]".format(
                x.equipment, x.plan_type[0:11], x.time_in_minutes, x.frequency, x.interval_in_weeks
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
