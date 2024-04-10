class ScheduleGenerator:
    def __init__(self, section, rooms):
        self.section = section
        self.rooms = rooms
        self.schedule = []
        self.assigned_times = {}

    def room_is_available(self, room_name, day, start_time):
        if (room_name, day, start_time) in self.assigned_times:
            return False
        return True

    def assign_session(self, moduleName, session_type, day, start_time, end_time, room):
        if self.room_is_available(room['name'], day, start_time):
            self.schedule.append([day, f"{start_time} - {end_time}", room['name'], moduleName, session_type])
            self.assigned_times[(room['name'], day, start_time)] = True

    def find_time_slot(self, room, session_type):
        for availability in room['availability']:
            for time in availability['time']:
                if self.room_is_available(room['name'], availability['day'], time['start']):
                    return availability['day'], time['start'], time['end']
        return None, None, None

    def generate_schedule(self):
        for module_group in self.section['modules']:
            for module in module_group['modules']:
                for _ in range(module['lectures']):
                    day, start_time, end_time = self.find_time_slot(self.rooms[0], 'Lecture')
                    if day:
                        self.assign_session(module['moduleName'], 'Lecture', day, start_time, end_time, self.rooms[0])
                if module.get('td', False):
                    day, start_time, end_time = self.find_time_slot(self.rooms[1], 'TD')
                    if day:
                        self.assign_session(module['moduleName'], 'TD', day, start_time, end_time, self.rooms[1])
                if module.get('tp', False):
                    day, start_time, end_time = self.find_time_slot(self.rooms[1], 'TP')
                    if day:
                        self.assign_session(module['moduleName'], 'TP', day, start_time, end_time, self.rooms[1])
        return self.schedule