import random

class ScheduleGenerator:
    def __init__(self, section, rooms, teachers):
        self.section = section
        self.rooms = rooms
        self.teachers = teachers
        self.schedule = []
        self.assigned_lectures = set()
        self.assigned_group_sessions = {}
        self.teacher_commitments = {}
        self.time_slots = {
            1: "8:00 - 9:30",
            2: "9:40 - 11:10",
            3: "11:20 - 12:50",
            4: "13:00 - 14:30",
            5: "14:40 - 16:10"
        }

    def find_suitable_teacher(self, module_name, day, slot):
        qualified_teachers = [
            teacher for teacher in self.teachers
            if any(m['name'] == module_name for m in teacher['modules']) and day in teacher['availability']
        ]
        available_teachers = [
            t for t in qualified_teachers
            if (t['name'], day, slot) not in self.teacher_commitments
        ]
        if not available_teachers:
            return "No teacher available"
        available_teachers.sort(key=lambda x: next((mod['priority'] for mod in x['modules'] if mod['name'] == module_name), float('inf')))
        return available_teachers[0]['name']

    def find_available_room(self, session_type, day, available_rooms):
        suitable_rooms = [
            room for room in available_rooms
            if room['type'] == session_type and day in room['availability']
        ]
        return random.choice(suitable_rooms)['name'] if suitable_rooms else None

    def assign_session(self, group, module, session_type, day, available_rooms):
        slot = random.choice(list(self.time_slots.keys()))
        time = self.time_slots[slot]

        print(f"Attempting to schedule {session_type} for {module['moduleName']} on {day} slot {slot}")

        if session_type == 'Lecture' and module['moduleName'] in self.assigned_lectures:
            print("Lecture already assigned for this module.")
            return
        if group and (module['moduleName'], session_type, group) in self.assigned_group_sessions:
            print(f"{session_type} already assigned for this group.")
            return

        room_name = self.find_available_room(session_type, day, available_rooms)
        if not room_name:
            print("No available room.")
            return

        teacher = self.find_suitable_teacher(module['moduleName'], day, slot)
        if teacher == "No teacher available" or (teacher, day, slot) in self.teacher_commitments:
            print(f"No available teacher or teacher already booked: {teacher}")
            teacher = "No teacher available"
        else:
            self.teacher_commitments[(teacher, day, slot)] = True
            print(f"Teacher {teacher} booked for {day} slot {slot}")

        self.schedule.append({
            'day': day,
            'room': room_name,
            'moduleName': module['moduleName'],
            'session_type': session_type,
            'teacher': teacher,
            'group': group,
            'time': time,
            'slot': slot
        })

        if session_type == 'Lecture':
            self.assigned_lectures.add(module['moduleName'])
        if group:
            self.assigned_group_sessions[(module['moduleName'], session_type, group)] = True

        print(f"Session scheduled: {self.schedule[-1]}")



    def generate_schedule(self):
        days_of_week = ["lundi", "mardi", "mercredi", "jeudi", "dimanche", "samedi"]
        random.shuffle(days_of_week)

        for module_group in self.section['modules']:
            available_rooms = self.rooms[:]
            for module in module_group['modules']:
                random_day = random.choice(days_of_week)
                if module['moduleName'] not in self.assigned_lectures:
                    self.assign_session(None, module, 'Lecture', random_day, available_rooms)

                for group in self.section['groups']:
                    if module.get('td', False):
                        random_day1 = random.choice(days_of_week)
                        if (module['moduleName'], 'TD', group) not in self.assigned_group_sessions:
                            self.assign_session(group, module, 'TD', random_day1, available_rooms)

                    if module.get('tp', False):
                        random_day2 = random.choice(days_of_week)
                        if (module['moduleName'], 'TP', group) not in self.assigned_group_sessions:
                            self.assign_session(group, module, 'TP', random_day2, available_rooms)

        return self.schedule
