class ScheduleGenerator:
    def __init__(self, section, rooms, assigned_times, teachers):
        self.section = section
        self.rooms = rooms
        self.assigned_times = assigned_times
        self.teachers = teachers
        self.schedule = []
        self.last_used_room_index = {'Lecture': -1, 'TD': -1, 'TP': -1}

    def teacher_is_available(self, teacher_name, day):
        return any(teacher['name'] == teacher_name and day in teacher['availability'] for teacher in self.teachers)

    def find_suitable_teacher(self, module_name, day):
        qualified_teachers = [
            teacher for teacher in self.teachers
            if any(m['name'] in module_name for m in teacher['modules']) and day in teacher['availability']
        ]
        if not qualified_teachers:
            return None
        qualified_teachers.sort(key=lambda x: next((mod['priority'] for mod in x['modules'] if mod['name'] in module_name), float('inf')))
        return qualified_teachers[0]['name'] if qualified_teachers else None


    def room_is_available(self, room_name, day, start_time, end_time):
        return all(not (start_time < t['end'] and end_time > t['start']) for t in self.assigned_times.get((room_name, day), []))

    def find_time_slot(self, session_type):
        suitable_rooms = [room for room in self.rooms if room['type'] == session_type]
        room_count = len(suitable_rooms)
        start_index = (self.last_used_room_index[session_type] + 1) % room_count

        for i in range(room_count):
            room_index = (start_index + i) % room_count
            room = suitable_rooms[room_index]
            for availability in room['availability']:
                day = availability['day']
                for time in availability['time']:
                    if self.room_is_available(room['name'], day, time['start'], time['end']):
                        self.last_used_room_index[session_type] = room_index
                        return day, time['start'], time['end'], room
        return None, None, None, None


    def assign_session(self, moduleName, session_type, day, start_time, end_time, room):
        teacher = self.find_suitable_teacher(moduleName, day)
        if not teacher:
            self.schedule.append([day, f"{start_time} - {end_time}", room['name'], moduleName, session_type, "No teacher available"])
            return
        if self.room_is_available(room['name'], day, start_time, end_time):
            self.schedule.append([day, f"{start_time} - {end_time}", room['name'], moduleName, session_type, teacher])
            if (room['name'], day) not in self.assigned_times:
                self.assigned_times[(room['name'], day)] = []
            self.assigned_times[(room['name'], day)].append({'start': start_time, 'end': end_time})
        else:
            print(f"Failed to assign {moduleName} {session_type} on {day} from {start_time} to {end_time}")


    def schedule_lectures(self, module):
        for _ in range(module['lectures']):
            day, start_time, end_time, room = self.find_time_slot('Lecture')
            if day:
                self.assign_session(module['moduleName'], 'Lecture', day, start_time, end_time, room)

    def schedule_tds(self, module):
        if module.get('td', False):
            day, start_time, end_time, room = self.find_time_slot('TD')
            if day:
                self.assign_session(module['moduleName'], 'TD', day, start_time, end_time, room)

    def schedule_tps(self, module):
        if module.get('tp', False):
            day, start_time, end_time, room = self.find_time_slot('TP')
            if day:
                self.assign_session(module['moduleName'], 'TP', day, start_time, end_time, room)

    def generate_schedule(self):
        for module_group in self.section['modules']:
            for module in module_group['modules']:
                self.schedule_lectures(module)
                self.schedule_tds(module)
                self.schedule_tps(module)
        return self.schedule