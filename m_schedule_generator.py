import random
class ScheduleGenerator:
    def __init__(self, section, rooms, teachers, global_room_usage):
        self.section = section
        self.rooms = rooms
        self.teachers = teachers
        self.schedule = []
        self.global_room_usage = global_room_usage
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
        bookings = self.global_room_usage.get((room_name, day), [])
        for booking in bookings:
            if start_time < booking['end'] and end_time > booking['start']:
                return False
        return True


    def find_time_slot(self, session_type):
        suitable_rooms = [room for room in self.rooms if room['type'] == session_type]
        #shuffle rooms b random bch potentially nbdaw from a different index each time bch we distribute room usage evenly
        random.shuffle(suitable_rooms)
        for room in suitable_rooms:
            for availability in room['availability']:
                day = availability['day']
                for time in availability['time']:
                    start_time = time['start']
                    end_time = time['end']
                    if self.room_is_available(room['name'], day, start_time, end_time):
                        #mark this room as used in this time slot globally
                        if (room['name'], day, start_time, end_time) not in self.global_room_usage:
                            self.global_room_usage[(room['name'], day, start_time, end_time)] = True
                            return day, start_time, end_time, room
        return None, None, None, None


    def is_time_slot_used_by_another_section(self, day, start, end):
        for schedule in self.all_schedules:
            for entry in schedule:
                if entry[0] == day and entry[1].split(" - ")[0] == start and entry[1].split(" - ")[1] == end:
                    return True
        return False


    def assign_session(self, moduleName, session_type, day, start_time, end_time, room):
        if self.room_is_available(room['name'], day, start_time, end_time):
            teacher = self.find_suitable_teacher(moduleName, day)
            if not teacher:
                teacher = "No teacher available"
            self.schedule.append([day, f"{start_time} - {end_time}", room['name'], moduleName, session_type, teacher])
            self.global_room_usage.setdefault((room['name'], day), []).append({'start': start_time, 'end': end_time})
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