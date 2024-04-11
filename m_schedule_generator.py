class ScheduleGenerator:
    def __init__(self, section, rooms, assigned_times):
        self.section = section
        self.rooms = rooms
        self.schedule = []
        self.assigned_times = assigned_times
        self.last_used_room_index = {'Lecture': -1, 'TD': -1, 'TP': -1}

    def room_is_available(self, room_name, day, start_time, end_time):
        for assigned_time in self.assigned_times.get((room_name, day), []):
            if start_time < assigned_time['end'] and end_time > assigned_time['start']:
                return False
        return True

    def assign_session(self, moduleName, session_type, day, start_time, end_time, room):
        if self.room_is_available(room['name'], day, start_time, end_time):
            self.schedule.append([day, f"{start_time} - {end_time}", room['name'], moduleName, session_type])
            if (room['name'], day) not in self.assigned_times:
                self.assigned_times[(room['name'], day)] = []
            self.assigned_times[(room['name'], day)].append({'start': start_time, 'end': end_time})

    def find_time_slot(self, session_type):
        suitable_rooms = [room for room in self.rooms if room['type'] == session_type]
        room_count = len(suitable_rooms)
        start_index = (self.last_used_room_index[session_type] + 1) % room_count

        for i in range(room_count):
            room_index = (start_index + i) % room_count
            room = suitable_rooms[room_index]
            for availability in room['availability']:
                for time in availability['time']:
                    if self.room_is_available(room['name'], availability['day'], time['start'], time['end']):
                        self.last_used_room_index[session_type] = room_index
                        return availability['day'], time['start'], time['end'], room
        return None, None, None, None

    def generate_schedule(self):
        for module_group in self.section['modules']:
            for module in module_group['modules']:
                for _ in range(module['lectures']):
                    day, start_time, end_time, room = self.find_time_slot('Lecture')
                    if day:
                        self.assign_session(module['moduleName'], 'Lecture', day, start_time, end_time, room)
                if module.get('td', False):
                    day, start_time, end_time, room = self.find_time_slot('TD')
                    if day:
                        self.assign_session(module['moduleName'], 'TD', day, start_time, end_time, room)
                if module.get('tp', False):
                    day, start_time, end_time, room = self.find_time_slot('TP')
                    if day:
                        self.assign_session(module['moduleName'], 'TP', day, start_time, end_time, room)
        return self.schedule
