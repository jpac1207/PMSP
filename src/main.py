from factory.MaintenanceRoutineFactory import MaintenanceRoutineFactory
from util.ChartUtil import ChartUtil
from util.Utilities import Utilities
from strategy.Budai import Budai

T = 104  # planning horizon
GROUP_ACTIVITIES = False

def main():
    routines = MaintenanceRoutineFactory.get_signaling_plans()
    index = 0
    for routine in routines:
        routine.frequency = int(T / routine.interval_in_weeks)
        routine.index = index
        index = index + 1
    #print(list(map(lambda x: x.to_string(), routines)))    
    MaintenanceRoutineFactory.print_list(routines)
    #Utilities.reduce_routines(routines)
    
    response = Budai(routines, T, GROUP_ACTIVITIES).max_to_min()   
    work_labels = (list(map(lambda x: "{0}:{1} ({2})".format(x.equipment, x.plan_type[0:11], x.time_in_minutes), routines)))
    time_labels = (['t' + str(i) for i in range(1, T + 1)])
    ChartUtil.heat_map(response[0], work_labels, time_labels, "Distribuição das Atividades: (Custo: {0} minutos)".format(response[3]))
    ChartUtil.heat_map(response[1], ['Custo de Manutenção'], time_labels, "Distribuição das Atividades: (Custo: {0} minutos)".format(response[3]), True)    
    
if __name__ == "__main__":
    main()
