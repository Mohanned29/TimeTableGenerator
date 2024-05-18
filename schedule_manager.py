from m_schedule_generator import ScheduleGenerator

class ScheduleManager:
    def __init__(self, years, rooms, teachers):
        self.years = years
        self.rooms = rooms
        self.teachers = teachers

    def generate_schedules_for_all(self):
        schedules = []
        for year_entry in self.years:
            year_number = year_entry['year']
            year_schedule = {
                "year": year_number,
                "specialite": []
            }
            for specialite_entry in year_entry['specialite']:
                speciality_name = specialite_entry['name']
                speciality_schedule = {
                    "name": speciality_name,
                    "sections": []
                }

                for section_data in specialite_entry['sections']:
                    section_name = section_data['name']

                    section_info = {
                        "name": section_name
                    }
                    generator = ScheduleGenerator(year_number, section_data, self.rooms, self.teachers)
                    section_schedule = generator.generate_schedule()
                    section_info["schedule"] = section_schedule
                    speciality_schedule["sections"].append(section_info)

                year_schedule["specialite"].append(speciality_schedule)

            schedules.append(year_schedule)

        return schedules
