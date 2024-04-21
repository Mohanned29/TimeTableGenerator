from m_schedule_generator import ScheduleGenerator

class ScheduleManager:
    def __init__(self, section, rooms, assigned_times, teachers):
        self.section = section
        self.rooms = rooms
        self.assigned_times = assigned_times
        self.teachers = teachers

    def generate_schedules_for_all(self, sections):
        schedules = {}
        for section in sections:
            generator = ScheduleGenerator(section, self.rooms, self.assigned_times, self.teachers)
            schedules[section['name']] = generator.generate_schedule()
        return schedules
