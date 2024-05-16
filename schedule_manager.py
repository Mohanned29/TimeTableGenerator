from m_schedule_generator import ScheduleGenerator

class ScheduleManager:
    def __init__(self, years, rooms, teachers):
        self.years = years
        self.rooms = rooms
        self.teachers = teachers

    def generate_schedules_for_all(self):
        schedules = []
        for year_name, year_data in self.years.items():
            year_number = int(year_name.split(' ')[0].replace('th', '').replace('nd', '').replace('st', ''))
            year_schedule = {
                "year": year_number,
                "specialite": []
            }
            specialities = {}
            
            sections = year_data.get('sections', [])
            for section_data in sections:
                speciality = section_data.get('speciality', 'Unknown Speciality')
                if speciality not in specialities:
                    specialities[speciality] = {
                        "name": speciality,
                        "sections": []
                    }
                
                generator = ScheduleGenerator(year_name, section_data, self.rooms, self.teachers)
                section_schedule = generator.generate_schedule()
                section_info = {
                    "name": section_data['name'],
                    "schedule": section_schedule
                }
                specialities[speciality]["sections"].append(section_info)
            
            year_schedule["specialite"] = list(specialities.values())
            schedules.append(year_schedule)
        return schedules
