from schedule_manager import ScheduleManager

def generate_schedules_for_all(rooms, sections, teachers):
    schedule_manager = ScheduleManager(rooms, teachers)
    schedules = schedule_manager.generate_schedules_for_all(sections)
    return schedules
