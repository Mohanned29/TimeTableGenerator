import itertools

class ScheduleGenerator:
    def __init__(self, section, rooms):
        self.section = section
        self.rooms = {room['name']: room for room in rooms}
        self.schedule = []

    def find_available_room(self, session_type):
        for room_name, room_details in self.rooms.items():
            if session_type.lower() in room_details['type'].lower():
                return room_name
        return None

    def generate_schedule(self):
        for module_group in self.section['modules']:
            for module in module_group['modules']:
                moduleName = module['moduleName']
                self.assign_sessions(moduleName, 'Lecture', module['lectures'])
                if module.get('td', False):
                    self.assign_sessions(moduleName, 'TD', 1)  #assuming 1 TD session per module psq 3yit
                if module.get('tp', False):
                    self.assign_sessions(moduleName, 'TP', 1)  #assuming 1 TP session per module psq 3yit
        return self.schedule

    def assign_sessions(self, moduleName, session_type, count):
        for _ in itertools.repeat(None, count):
            room = self.find_available_room(session_type)
            if room:
                self.schedule.append({'module': moduleName, 'session_type': session_type, 'room': room})
            else:
                print(f"No available room found for {session_type} session of {moduleName}")

