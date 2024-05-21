import random
import logging

#not used yet , apr sahel
logging.basicConfig(level=logging.INFO)

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
            5: "14:40 - 16:10",
            6: "16:20 - 17:50"
        }
        self.init_availability()



    def init_availability(self):
        days_of_week = ["lundi", "mardi", "mercredi", "jeudi", "dimanche", "samedi"]
        for room in self.rooms:
            self.room_availability[room['name']] = {day: [True] * 6 for day in days_of_week}
        for teacher in self.teachers:
            self.teacher_commitments[teacher['name']] = {day: [True] * 6 for day in days_of_week}



    def find_suitable_teacher(self, module_name, day):
        qualified_teachers = [
            teacher for teacher in self.teachers
            if any(m['name'].lower() == module_name.lower() for m in teacher['modules']) and day in teacher['availability']
        ]
        random.shuffle(qualified_teachers)
        for teacher in qualified_teachers:
            if any(self.teacher_commitments[teacher['name']][day]):
                return teacher['name']
        return None



    def find_available_room(self, session_type, day):
        suitable_rooms = [
            room for room in self.rooms
            if room['type'].lower() == session_type.lower() and day in room['availability']
        ]
        random.shuffle(suitable_rooms)
        for room in suitable_rooms:
            if any(self.room_availability[room['name']][day]):
                return room['name']
        return None



    def is_slot_available(self, slot, day):
        return any(self.room_availability[room][day][slot - 1] for room in self.room_availability) and \
               any(self.teacher_commitments[teacher][day][slot - 1] for teacher in self.teacher_commitments)



    def is_slot_conflict(self, section_name, day, slot, session_type, group):
        for session in self.schedule:
            if session['day'] == day and session['slot'] == slot and session['section'] == section_name:
                if session['session_type'] == 'Lecture':
                    return True
                if session['group'] == group:
                    return True
                if session['session_type'] in ['TD', 'TP'] and session_type == 'Lecture':
                    return True
        return False



    def assign_session(self, section_name, group, module, session_type, day):
        available_slots = [slot for slot, time in self.time_slots.items() if self.is_slot_available(slot, day)]
        if not available_slots:
            return

        available_slots = [slot for slot in available_slots if not self.is_slot_conflict(section_name, day, slot, session_type, group)]
        if not available_slots:
            return

        slot = random.choice(available_slots)
        time = self.time_slots[slot]

        room_name = self.find_available_room(session_type, day)
        if not room_name:
            return

        teacher = self.find_suitable_teacher(module['name'], day)
        if not teacher:
            teacher = "No teacher available"

        self.schedule.append({
            'day': day,
            'room': room_name,
            'moduleName': module['name'],
            'session_type': session_type,
            'teacher': teacher,
            'group': group,
            'time': time,
            'slot': slot,
            'section': section_name
        })
        self.update_availability(room_name, teacher, day, slot)



    def update_availability(self, room_name, teacher_name, day, slot):
        self.room_availability[room_name][day][slot - 1] = False
        if teacher_name != "No teacher available":
            self.teacher_commitments[teacher_name][day][slot - 1] = False



    def generate_schedule(self):
        days_of_week = ["lundi", "mardi", "mercredi", "jeudi", "dimanche", "samedi"]
        random.shuffle(days_of_week)

        section_name = self.section['name']

        for module in self.section['modules']:
            random_day = random.choice(days_of_week)
            if module['name'] not in self.assigned_lectures:
                self.assign_session(section_name, None, module, 'Lecture', random_day)
                self.assigned_lectures.add(module['name'])

            for group in self.section['groups']:
                if module.get('td', False):
                    random_day1 = random.choice(days_of_week)
                    self.assign_session(section_name, group, module, 'TD', random_day1)

                if module.get('tp', False):
                    random_day2 = random.choice(days_of_week)
                    self.assign_session(section_name, group, module, 'TP', random_day2)

        return self.schedule
