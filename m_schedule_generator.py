import random

class ScheduleGenerator:
    def __init__(self, rooms, days, times, courses, sections):
        self.rooms = rooms
        self.days = days
        self.times = times
        self.courses = courses
        self.sections = sections
        self.global_room_schedule = {}
        self.session_to_room_type_map = {
            'lecture': 'Amphi',
            'TD': 'TD Room',
            'TP': 'TP Room'
        }
        self.initialize_availability()



    def initialize_availability(self):
        self.room_availability = {}
        for room_type, room_list in self.rooms.items():
            for room_info in room_list:
                room_name = room_info['name']
                self.room_availability[room_name] = {
                    'availability': set((day, time) for day, time in room_info['availability']),
                    'sessions': [],
                }
        self.section_availability = {}
        for section, details in self.sections.items():
            self.section_availability[section] = set((d, t) for d in self.days for t in self.times)



    def is_section_available(self, section, day, time):
        return (day, time) in self.section_availability[section]



    def find_available_room(self, session_type, day, time, global_room_schedule):
        room_type = self.session_to_room_type_map.get(session_type)
        if not room_type:
            print(f"No valid room type mapping found for session type: {session_type}")
            return None
        for room_info in self.rooms.get(room_type, []):
            room_name = room_info['name']
            if (room_name, day, time) not in global_room_schedule:
                print(f"Room {room_name} of type {room_type} is available for {session_type} on {day} at {time}")
                return room_name
        print(f"No available room found for {session_type} on {day} at {time} within type {room_type}")
        return None



    def schedule_session(self, course_name, session_type, section, day, time, room, global_room_schedule):
        if room and (room, day, time) not in global_room_schedule:
            global_room_schedule[(room, day, time)] = f"{section} - {course_name} - {session_type}"
            print(f"Successfully scheduled {course_name} {session_type} for {section} on {day} at {time} in {room}")
            return True
        else:
            print(f"Failed to book {room} for {course_name} {session_type} on {day} at {time} due to conflict or unavailability.")
            return False



    def generate_schedule(self, global_room_schedule):
        all_schedules = {}

        for section_key, section_details in self.sections.items():
            section_schedule = []
            for course_name, session_types in self.courses.items():
                for session_type, is_required in session_types.items():
                    if is_required:
                        session_scheduled = False
                        random.shuffle(self.days)
                        random.shuffle(self.times)
                        for day in self.days:
                            for time in self.times:
                                if session_scheduled:
                                    break
                                if self.is_section_available(section_key, day, time):
                                    room = self.find_available_room(session_type, day, time, global_room_schedule)
                                    if room:
                                        success = self.schedule_session(course_name, session_type, section_key, day, time, room, global_room_schedule)
                                        if success:
                                            section_schedule.append([day, time, room, course_name, session_type])
                                            session_scheduled = True
                                            break
                        if not session_scheduled:
                            print(f"Unable to schedule {session_type} for {course_name} in section {section_key}. Check room and time slot availability.")
            
            #Schedule lectures specifically
            for course_name, session_types in self.courses.items():
                lectures = int(session_types.get('lectures', 0))
                for _ in range(lectures):
                    session_scheduled = False
                    random.shuffle(self.days)
                    random.shuffle(self.times)
                    for day in self.days:
                        for time in self.times:
                            if session_scheduled:
                                break
                            if self.is_section_available(section_key, day, time):
                                room = self.find_available_room('lecture', day, time, global_room_schedule)
                                if room:
                                    success = self.schedule_session(course_name, 'lecture', section_key, day, time, room, global_room_schedule)
                                    if success:
                                        section_schedule.append([day, time, room, course_name, 'lecture'])
                                        session_scheduled = True
                                        break
                    if not session_scheduled:
                        print(f"Unable to schedule lecture for {course_name} in section {section_key}. Check room and time slot availability.")

            all_schedules[section_key] = section_schedule

        return all_schedules