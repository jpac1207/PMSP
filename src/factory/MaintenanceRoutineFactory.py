import pandas as pd
from model.MaintenanceRoutine import MaintenanceRoutine


class MaintenanceRoutineFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_signaling_plans():
        file = open("routine.csv", "r", encoding="utf-8")
        file.readline()  # remove header
        routines = []
        for line in file:
            fields = line.replace("\n", "").split(";")          
            system = fields[0]
            equipment = fields[1]
            period = fields[2]
            tolerancy = fields[3]
            plan_type = fields[4]
            work_type = fields[5]
            time = fields[6]
            routines.append(
                MaintenanceRoutine(
                    system, equipment, period, tolerancy, plan_type, work_type, time
                )
            )
        return routines

    @staticmethod
    def print_list(routines):
        print('----------------------------------------------{0} Routines----------------------------------------------'.format(len(routines)))
        for r in routines:
            print(
                "[System: {0}; Equipment: {1}; Interval_Weeks: {2}; Tolerancy: {3}; Plan_Type: {4}; Description: {5};"
                "Time_Minutes: {6}; Frequency: {7}]".format(
                    r.system,
                    r.equipment,
                    r.interval_in_weeks,
                    r.tolerancy,
                    r.plan_type,
                    r.description,
                    r.time_in_minutes,
                    r.frequency,
                )
            )

