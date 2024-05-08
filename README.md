# Schedule Generator System

## System Architecture Overview

The scheduling system is designed to manage and generate schedules for various academic sections within an institution. It utilizes several classes and methods interconnected to efficiently allocate rooms, teachers, and time slots for courses as specified in the JSON configuration.

## Module: m_schedule_generator.py

### I) Class: ScheduleGenerator

This class encapsulates the logic for generating schedules for a specific section.

- **section:** The academic section for which the schedule is being generated.
- **rooms:** List of available rooms for scheduling.
- **teachers:** List of available teachers including their teaching modules and availability.
- **schedule:** List that stores the generated schedule entries.
- **assigned_lectures:** Set that keeps track of already assigned lectures to avoid duplication.
- **assigned_group_sessions:** Dictionary to track sessions assigned to specific groups to prevent overlap.
- **teacher_commitments:** Dictionary to track when and where each teacher is already scheduled.

#### Methods

1. **Method: teacher_is_available(teacher_name, day)**
   - **Purpose:** Checks if a given teacher is available on a specific day.
   - **Parameters:**
     - **teacher_name:** The name of the teacher to check availability for.
     - **day:** The day for which availability is being checked.
   - **Returns:** true if the teacher is available on the specified day, otherwise false.
   - **Explanation:** Iterates through the list of teachers to find if the provided teacher is available on the given day. If any teacher with a matching name and availability on the specified day is found, the method returns True; otherwise, it returns False.


2. **Method: room_is_available(room_name, day, start_time, end_time)**
   - **Purpose:** Checks if a given room is available for a session at a specified time slot.
   - **Parameters:**
     - **room_name:** The name of the room being checked for availability.
     - **day:** The day for which availability is being checked.
     - **start_time:** The start time of the session.
     - **end_time:** The end time of the session.
   - **Returns:** True if the room is available for the specified time slot, otherwise False.
   - **Explanation:** Retrieves the bookings for the specified room and day from the global room usage data. It then iterates through these bookings to check if there are any conflicting time slots. If no conflicts are found, the method returns True; otherwise, it returns False.


3. **Method: assign_session(moduleName, session_type, day, start_time, end_time, room)**
   - **Purpose:** Assigns a session to a specific time slot, room, and teacher.
   - **Parameters:**
     - **moduleName:** The name of the module for which the session is being assigned.
     - **session_type:** The type of session being assigned (Lecture, TD, TP).
     - **day:** The day of the session.
     - **start_time:** The start time of the session.
     - **end_time:** The end time of the session.
     - **room:** The room where the session is being assigned.
   - **Explanation:** Checks if the specified room is available for the given time slot. If it is, it finds a suitable teacher for the module and assigns the session to that teacher, updating the schedule and global room usage data accordingly. If the room is not available, it prints a failure message.


4. **Method: generate_schedule()**
   - **Purpose:** Generates the complete schedule for all modules in the section.
   - **Returns:** The generated schedule.
   - **Explanation:** Iterates through all module groups in the section and schedules lectures, TDs, and TPs for each module using the respective scheduling methods. Finally, it returns the complete schedule.

## Module: schedule_manager.py

### II) Class: ScheduleManager

This class manages the generation of schedules for multiple sections.

#### Attributes
- **sections:** Contains information about all the sections for which schedules need to be generated.
- **rooms:** Holds data about available rooms where sessions can be scheduled.
- **teachers:** Stores information about teachers available to conduct sessions.
- **global_room_usage:** Tracks the usage of rooms across all sections to prevent scheduling conflicts.

#### Methods
- **generate_schedules_for_all():** Generates schedules for all sections by creating a ScheduleGenerator instance for each section and generating schedules using the provided rooms and teachers.

## Components Interaction

1. **JSON Configuration:** Holds all the necessary data about sections, modules, teachers, and rooms. This data acts as the foundation for the scheduling operations.
2. **ScheduleManager Class:** Acts as the central control unit that manages the scheduling for all sections using the ScheduleGenerator instances. It accesses global resources like room and teacher availability and coordinates the scheduling activities across different sections to avoid conflicts.
3. **ScheduleGenerator Class:** Responsible for generating the schedule for a specific section. It interacts with the data layers to fetch teacher availability and room schedules. This class contains multiple methods to handle different scheduling tasks.
4. **Data Layer Interaction:** Both ScheduleManager and ScheduleGenerator interact heavily with the JSON-configured data to retrieve and update scheduling information. This includes checking the availability of rooms and teachers and updating schedules as sessions are assigned.
5. **Utility Methods:** Methods like teacher_is_available and is_time_slot_used_by_another_section provide utility support by checking specific conditions that affect the scheduling decisions, ensuring that no overlaps or conflicts occur in the schedules.
6. **Execution Flow:** The system initiates by creating an instance of ScheduleManager. ScheduleManager then iterates through each section and creates an instance of ScheduleGenerator for each. ScheduleGenerator uses its methods to generate a complete schedule for its section based on the available data and constraints. Results are compiled into the final schedule for all sections and can be further processed or displayed.


## Flask Application Integration

The scheduling system utilizes a Flask web application to provide a user-friendly interface for managing and viewing the generated schedules. Flask is a lightweight web framework that is particularly well-suited for small to medium web applications like this scheduling system.

### Structure of the Flask Application

- **app.py:** This is the main file that contains the Flask application setup, routes, and server logic.

### Key Features

- **User Interface:** Provides an interactive and easy-to-navigate interface for users to view and manage the schedules.
- **API Endpoints:** Flask routes handle requests to generate, update, or fetch schedules, interfacing with the scheduling system backend.
- **Data Visualization:** Integrates tools for visualizing schedules in a calendar view to facilitate easier understanding and management.



### Getting Started
**To set up and run the scheduling system:**

- **Installation**: Ensure Python 3.x is installed along with Flask. Install other dependencies as listed in requirements.txt.
- **Execution:** Run the Flask application with python app.py and utilize the provided API endpoints to interact with the system.