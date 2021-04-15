import pandas as pd
from model.MaintenanceRoutine import MaintenanceRoutine

class MaintenanceRoutineFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_signaling_plans():
        file = open('routine.csv', 'r', encoding='utf-8')
        file.readline()#remove header
        routines = []
        for line in file:
            fields = line.replace('\n', '').split(';')
            system = fields[0]
            equipment = fields[1]
            period = fields[2]
            tolerancy = fields[3]
            plan_type = fields[4]
            work_type = fields[5]
            times = fields[6]
            routines.append(MaintenanceRoutine(system, equipment, period, tolerancy, plan_type, work_type, times))
        return routines
        
