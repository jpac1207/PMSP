class MaintenanceRoutine:
    def __init__(
        self,
        system,
        equipment,
        interval_in_weeks,
        tolerancy,
        plan_type,
        description,
        time_in_minutes,
    ):
        self.system = system
        self.equipment = equipment
        self.interval_in_weeks = int(interval_in_weeks)
        self.tolerancy = int(tolerancy)
        self.plan_type = plan_type
        self.description = description
        self.time_in_minutes = int(time_in_minutes)
        self.frequency = None
        self.index = None

    def to_string(self):
        return (
            "|System: {0}; Equipment: {1}; Interval_Weeks: {2}; Tolerancy: {3}; Plan_Type: {4}; Description: {5};"
            "Time_Minutes: {6}; Frequency: {7}|".format(
                self.system,
                self.equipment,
                self.interval_in_weeks,
                self.tolerancy,
                self.plan_type,
                self.description,
                self.time_in_minutes,
                self.frequency,
            )
        )  