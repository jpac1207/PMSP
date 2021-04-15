class MaintenanceEvent:

    def __init__(self, init_date, init_km, end_km, init_hour, work_duration, init_line, end_line, description, work_type):
        self.init_date = init_date
        self.init_km = float(init_km)
        self.end_km = float(end_km)
        self.init_hour = init_hour
        self.work_duration = MaintenanceEvent.str_time_in_minutes(
            work_duration)
        self.init_line = init_line
        self.end_line = end_line
        self.description = description
        self.work_type = work_type

    def to_string(self):
        return ("[Init Date: {}, Init KM: {}, End KM: {}, Init Hour: {}, Work Duration: {}, Init Line: {},"
                "End Line: {}, Work Type: {}, Description: {}]").format(self.init_date, self.init_km,
                                                                        self.end_km, self.init_hour, self.work_duration,
                                                                        self.init_line, self.end_line, self.work_type, self.description)

    @ staticmethod
    def str_time_in_minutes(str_time):
        parts = str_time.split(':')
        print(parts)
        return int(parts[0]) + int(parts[1])
