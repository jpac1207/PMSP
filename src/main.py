from factory.MaintenanceRoutineFactory import MaintenanceRoutineFactory
from strategy.Budai import Budai

T = 52  # planning horizon


def main():
    routines = MaintenanceRoutineFactory.get_signaling_plans()
    for routine in routines:
        routine.frequency = int(T / routine.interval_in_weeks)
    print(list(map(lambda x: x.to_string(), routines)))
    Budai(routines, T)

if __name__ == "__main__":
    main()
