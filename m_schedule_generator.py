import random

class ScheduleGenerator:
    def __init__(self, year, section, rooms, teachers):
        self.year = year
        self.section = section
        self.rooms = rooms
        self.teachers = teachers
        self.schedule = []
        self.assigned_lectures = set()
        self.assigned_group_sessions = set()
        self.teacher_commitments = {}
        self.room_availability = {}
        self.time_slots = {
            1: "8:00 - 9:30",
            2: "9:40 - 11:10",
            3: "11:20 - 12:50",
            4: "13:00 - 14:30",
            5: "14:40 - 16:10"
        }
        self.init_availability()

    def init_availability(self):
        days_of_week = ["lundi", "mardi", "mercredi", "jeudi", "dimanche", "samedi"]
        for room in self.rooms:
            self.room_availability[room['name']] = {day: [True] * 5 for day in days_of_week}
        for teacher in self.teachers:
            self.teacher_commitments[teacher['name']] = {day: [True] * 5 for day in days_of_week}

    def find_suitable_teacher(self, module_name, day):
        qualified_teachers = [
            teacher for teacher in self.teachers
            if any(m['name'].lower() == module_name.lower() for m in teacher['modules']) and day in teacher['availability']
        ]
        random.shuffle(qualified_teachers)  # Shuffle to introduce randomness
        for teacher in qualified_teachers:
            if any(self.teacher_commitments[teacher['name']][day]):
                return teacher['name']
        return None

    def find_available_room(self, session_type, day):
        suitable_rooms = [
            room for room in self.rooms
            if room['type'].lower() == session_type.lower() and day in room['availability']
        ]
        random.shuffle(suitable_rooms)  # Shuffle to introduce randomness
        for room in suitable_rooms:
            if any(self.room_availability[room['name']][day]):
                return room['name']
        return None

    def assign_session(self, group, module, session_type, day):
        """Assign a session to a group, module, and day, ensuring room and teacher availability."""
        available_slots = [slot for slot, time in self.time_slots.items() if self.is_slot_available(slot, day)]
        if not available_slots:
            return

        slot = random.choice(available_slots)
        time = self.time_slots[slot]

        room_name = self.find_available_room(session_type, day)
        if not room_name:
            return

        teacher = self.find_suitable_teacher(module['moduleName'], day)
        if not teacher:
            teacher = "No teacher available"

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
        self.update_availability(room_name, teacher, day, slot)

    def is_slot_available(self, slot, day):
        """Check if a specific slot is available for any room and teacher on the given day."""
        return any(self.room_availability[room][day][slot - 1] for room in self.room_availability) and \
               any(self.teacher_commitments[teacher][day][slot - 1] for teacher in self.teacher_commitments)

    def update_availability(self, room_name, teacher_name, day, slot):
        """Update the availability of a room and teacher for a specific slot and day."""
        self.room_availability[room_name][day][slot - 1] = False
        if teacher_name != "No teacher available":
            self.teacher_commitments[teacher_name][day][slot - 1] = False

    def generate_schedule(self):
        days_of_week = ["lundi", "mardi", "mercredi", "jeudi", "dimanche", "samedi"]
        random.shuffle(days_of_week)

        for module_group in self.section['modules']:
            for module in module_group['modules']:
                random_day = random.choice(days_of_week)
                if module['moduleName'] not in self.assigned_lectures:
                    self.assign_session(None, module, 'Lecture', random_day)
                    self.assigned_lectures.add(module['moduleName'])

                for group in self.section['groups']:
                    if module.get('td', False):
                        random_day1 = random.choice(days_of_week)
                        if (module['moduleName'], 'TD', group) not in self.assigned_group_sessions:
                            self.assign_session(group, module, 'TD', random_day1)
                            self.assigned_group_sessions.add((module['moduleName'], 'TD', group))

                    if module.get('tp', False):
                        random_day2 = random.choice(days_of_week)
                        if (module['moduleName'], 'TP', group) not in self.assigned_group_sessions:
                            self.assign_session(group, module, 'TP', random_day2)
                            self.assigned_group_sessions.add((module['moduleName'], 'TP', group))

        return self.schedule
