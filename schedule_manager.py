from m_schedule_generator import ScheduleGenerator

class ScheduleManager:
    def __init__(self, years, rooms, teachers):
        self.years = years
        self.rooms = rooms
        self.teachers = teachers

    def generate_schedules_for_all(self):
        schedules = {}
        for year_name, year_data in self.years.items():
            year_schedule = {}
            sections = year_data.get('sections', [])
            for section_data in sections:
                generator = ScheduleGenerator(year_name, section_data, self.rooms, self.teachers)
                year_schedule[section_data['name']] = generator.generate_schedule()
            schedules[year_name] = year_schedule
        return schedules
