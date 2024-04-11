from m_schedule_generator import ScheduleGenerator

class ScheduleManager:
    def __init__(self, rooms):
        self.rooms = rooms
        self.assigned_times = {}

    def generate_schedules_for_all(self, sections):
        schedules = {}
        for section in sections:
            generator = ScheduleGenerator(section, self.rooms, self.assigned_times)
            schedules[section['name']] = generator.generate_schedule()
        return schedules
