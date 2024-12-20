from schedule_generator import ScheduleGenerator
import logging

class ScheduleManager:
    def __init__(self, years, rooms, teachers):
        self.years = years
        self.rooms = rooms
        self.teachers = teachers
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_schedules_for_all(self):
        schedules = []
        try:
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
                        generator = ScheduleGenerator(
                            year=year_number, 
                            section=section_data, 
                            rooms=self.rooms, 
                            teachers=self.teachers
                        )
                        section_schedule = generator.generate_schedule()
                        optimized_schedule = generator.optimize_schedule(section_schedule)
                        
                        section_info["schedule"] = optimized_schedule
                        speciality_schedule["sections"].append(section_info)

                    year_schedule["specialite"].append(speciality_schedule)

                schedules.append(year_schedule)
            self.logger.info(f"Successfully generated schedules for {len(self.years)} years")
            
            return schedules

        except Exception as e:
            # Log any errors during schedule generation
            self.logger.error(f"Error generating schedules: {str(e)}")
            return []
