from m_schedule_generator import ScheduleGenerator

def generate_schedules_for_all(data):
    rooms = data['rooms']
    schedules = {section['name']: ScheduleGenerator(section, rooms).generate_schedule() for section in data['sections']}
    return schedules