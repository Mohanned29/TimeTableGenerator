from m_schedule_generator import ScheduleGenerator

class ScheduleManager:
    def __init__(self, sections, rooms, teachers):
        self.sections = sections
        self.rooms = rooms
        self.teachers = teachers
        self.global_room_usage = {}

    def generate_schedules_for_all(self):
        schedules = {}
        for section in self.sections:
            generator = ScheduleGenerator(section, self.rooms, self.teachers, self.global_room_usage)
            schedules[section['name']] = generator.generate_schedule()
        return schedules
