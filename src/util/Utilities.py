import math
import copy

from factory.MaintenanceRoutineFactory import MaintenanceRoutineFactory

class Utilities:
    def __init__(self):
        pass
    @staticmethod
    def lcm(a, b):        
        return abs(a*b) // math.gcd(a, b)   
    @staticmethod
    def is_coprime(x, y):
        return math.gcd(x, y) == 1
    @staticmethod
    def reduce_routines(routines):
        MaintenanceRoutineFactory.print_list(routines)
        for i in range(0, len(routines)):
            for j in range(i+1, len(routines)):
                print(routines[i].description, routines[i].interval_in_weeks)
                print(routines[j].description, routines[j].interval_in_weeks)
                print(Utilities.lcm(routines[i].interval_in_weeks, routines[j].interval_in_weeks))
    
    @staticmethod
    def multiple_copies_from_routines(n, routines):
        copies = []
        for i in range(0, n):
            copies.append(copy.deepcopy(routines))
        return copies



