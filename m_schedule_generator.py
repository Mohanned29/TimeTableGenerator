import random

class ScheduleGenerator:
    def __init__(self, section, rooms, teachers):

        self.section = section
        self.rooms = rooms
        self.teachers = teachers
        self.schedule = []  #hedi will store the final schedule li ytaficha fel response
        self.assigned_lectures = set()  #track les cours li dernahom deja to avoid double booking
        self.assigned_group_sessions = {}  #track td and tp li dernahom deja to avoid double booking

    def find_suitable_teacher(self, module_name, day):
        #tfiltri teachers who are available on the given day and can teach the module (ex : garici -> analyse -> monday)
        qualified_teachers = [
            teacher for teacher in self.teachers
            if any(m['name'] == module_name for m in teacher['modules']) and day in teacher['availability']
        ]
        #ida mkch teachers available, return a placeholder string : "No teacher available"
        if not qualified_teachers:
            return "No teacher available"
        #sort the qualified teachers by their priority for the module ( apr apr )
        qualified_teachers.sort(key=lambda x: next((mod['priority'] for mod in x['modules'] if mod['name'] == module_name), float('inf')))
        return qualified_teachers[0]['name']

    def find_available_room(self, session_type, day):
        #list te3 rooms that match the session type (lecture , td , tp) and are available on the specified day
        suitable_rooms = [room for room in self.rooms if room['type'] == session_type and day in room['availability']]
        #using random , khyr room:
        return random.choice(suitable_rooms)['name'] if suitable_rooms else None

    def assign_session(self, group, module, session_type, day):

        #check for previous booking to avoid double booking
        if session_type == 'Lecture' and module['moduleName'] in self.assigned_lectures:
            return
        if group and (module['moduleName'], session_type, group) in self.assigned_group_sessions:
            return

        #find an available room and a teacher , assinging la seance
        room_name = self.find_available_room(session_type, day)
        if not room_name:
            return  #exit if no room is available w hedi mtsrach ida kanet data kbira

        teacher = self.find_suitable_teacher(module['moduleName'], day)
        if teacher == "No teacher available":
            return  #exit if no teacher is available

        #zid la seance details to the schedule list bch tafichiha f response
        self.schedule.append({
            'day': day,
            'room': room_name,
            'moduleName': module['moduleName'],
            'session_type': session_type,
            'teacher': teacher,
            'group': group
        })

        #mark la seance as assigned to prevent future double booking
        if session_type == 'Lecture':
            self.assigned_lectures.add(module['moduleName'])
        if group:
            self.assigned_group_sessions[(module['moduleName'], session_type, group)] = True

    def generate_schedule(self):
        #define the days of the week where classes can be scheduled
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Saturday", "Sunday"]
        for module_group in self.section['modules']:
            for module in module_group['modules']:
                #schedule one lecture for each module and pas plus if not already scheduled
                for day in days_of_week:
                    if module['moduleName'] not in self.assigned_lectures:
                        self.assign_session(None, module, 'Lecture', day)
                        break  #if we schedule one lecture than nhbso (khdmt beli chaque module 3ndo cour wahed)

                #same for td and tp
                for group in self.section['groups']:
                    if module.get('td', False):
                        for day in days_of_week:
                            if (module['moduleName'], 'TD', group) not in self.assigned_group_sessions:
                                self.assign_session(group, module, 'TD', day)
                                break  #hbs after scheduling one session par groupe

                    if module.get('tp', False):
                        for day in days_of_week:
                            if (module['moduleName'], 'TP', group) not in self.assigned_group_sessions:
                                self.assign_session(group, module, 'TP', day)
                                break

        return self.schedule  #return the complete schedule
