from schedule_manager import ScheduleManager

def generate_schedules_for_all(data):
    rooms = data['rooms']
    sections = data['sections']
    schedule_manager = ScheduleManager(rooms)
    schedules = schedule_manager.generate_schedules_for_all(sections)
    return schedules
