from m_schedule_generator import ScheduleGenerator

def transform_sections_data(sections):
    # Since the sections data is an array containing dictionaries,
    # merge them into a single dictionary.
    merged_sections = {}
    for section in sections:
        merged_sections.update(section)
    return merged_sections

def transform_rooms_data(rooms):

    transformed_rooms = {}
    for room_category in rooms:
        for room_type, room_list in room_category.items():
            transformed_rooms[room_type] = [{
                'name': room['name'],
                'availability': [(avail[0], avail[1]) for avail in room['availability']]
            } for room in room_list]
    return transformed_rooms

def generate_schedules(sections, rooms):
    
    courses_data = {}

    sections_data = transform_sections_data(sections)
    rooms_data = transform_rooms_data(rooms)

    # Initialize schedule generator with transformed data.
    schedule_generator = ScheduleGenerator(
        rooms=rooms_data,
        days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        times=["8:00 - 09:30", "09:40 - 11:10", "11:20 - 12:50", "13:00 - 14:30", "14:40 - 16:10"],
        courses=courses_data,
        sections=sections_data
    )

    # Generate schedules
    global_room_schedule = {}  # This could be used if you're tracking room usage across multiple schedule generations
    schedules = schedule_generator.generate_schedule(global_room_schedule)

    return schedules