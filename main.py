from schedule_manager import ScheduleManager

def generate_schedules_for_all(years, rooms, teachers):
    schedule_manager = ScheduleManager(years, rooms, teachers)
    schedules = schedule_manager.generate_schedules_for_all()
    return schedules
