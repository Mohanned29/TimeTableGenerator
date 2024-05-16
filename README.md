# Schedule Generator System

## System Architecture Overview

![Alt text](UML.png)

Ce projet est une solution de planification avancée spécialement conçue pour la Faculté d'Informatique. Ce projet vise à automatiser et à rationaliser la création des emplois du temps, répondant aux défis spécifiques de planification rencontrés par les établissements académiques.

The scheduling system is designed to manage and generate schedules for various academic sections within an institution. It utilizes several classes and methods interconnected to efficiently allocate rooms, teachers, and time slots for courses as specified in the JSON configuration.

## Module: m_schedule_generator.py

### I) Class: ScheduleGenerator

This class encapsulates the logic for generating schedules for a specific section.

#### Attributes

- **year:** The academic year for which the schedule is being generated.
- **section:** The academic section for which the schedule is being generated.
- **rooms:** List of available rooms for scheduling.
- **teachers:** List of available teachers including their teaching modules and availability.
- **schedule:** List that stores the generated schedule entries.
- **assigned_lectures:** Set that keeps track of already assigned lectures to avoid duplication.
- **assigned_group_sessions:** Set to track sessions assigned to specific groups to prevent overlap.
- **teacher_commitments:** Dictionary to track when and where each teacher is already scheduled.
- **room_availability:** Dictionary to track room availability.
- **time_slots:** Dictionary of available time slots for scheduling sessions.

#### Methods

1. **init_availability()**
   - **Purpose:** Initializes the availability for rooms and teachers.
   - **Explanation:** Sets up the availability for each room and teacher for all days of the week.

2. **find_suitable_teacher(module_name, day)**
   - **Purpose:** Finds a suitable teacher for a given module on a specific day.
   - **Parameters:**
     - **module_name:** The name of the module.
     - **day:** The day for which a teacher is needed.
   - **Returns:** The name of a suitable teacher, or None if no teacher is available.

3. **find_available_room(session_type, day)**
   - **Purpose:** Finds an available room for a session type on a specific day.
   - **Parameters:**
     - **session_type:** The type of session (Lecture, TD, TP).
     - **day:** The day for which a room is needed.
   - **Returns:** The name of an available room, or None if no room is available.

4. **assign_session(group, module, session_type, day)**
   - **Purpose:** Assigns a session to a group, module, and day, ensuring room and teacher availability.
   - **Parameters:**
     - **group:** The group for which the session is being assigned.
     - **module:** The module for which the session is being assigned.
     - **session_type:** The type of session (Lecture, TD, TP).
     - **day:** The day of the session.
   - **Explanation:** Checks room and teacher availability and assigns the session if possible.

5. **is_slot_available(slot, day)**
   - **Purpose:** Checks if a specific slot is available for any room and teacher on the given day.
   - **Parameters:**
     - **slot:** The time slot being checked.
     - **day:** The day being checked.
   - **Returns:** True if the slot is available, otherwise False.

6. **update_availability(room_name, teacher_name, day, slot)**
   - **Purpose:** Updates the availability of a room and teacher for a specific slot and day.
   - **Parameters:**
     - **room_name:** The name of the room.
     - **teacher_name:** The name of the teacher.
     - **day:** The day of the session.
     - **slot:** The time slot of the session.

7. **generate_schedule()**
   - **Purpose:** Generates the complete schedule for all modules in the section.
   - **Returns:** The generated schedule.
   - **Explanation:** Iterates through all module groups in the section and schedules lectures, TDs, and TPs for each module using the respective scheduling methods.

## Module: schedule_manager.py

### II) Class: ScheduleManager

This class manages the generation of schedules for multiple sections.

#### Attributes

- **years:** Contains information about all the academic years and their respective sections.
- **rooms:** Holds data about available rooms where sessions can be scheduled.
- **teachers:** Stores information about teachers available to conduct sessions.

#### Methods

- **__init__(self, years, rooms, teachers)**
   - **Purpose:** Initializes the ScheduleManager with years, rooms, and teachers.
   - **Parameters:**
     - **years:** Dictionary containing academic years and their respective sections.
     - **rooms:** List of available rooms for scheduling.
     - **teachers:** List of available teachers including their teaching modules and availability.

- **generate_schedules_for_all(self)**
   - **Purpose:** Generates schedules for all sections by creating a ScheduleGenerator instance for each section and generating schedules using the provided rooms and teachers.
   - **Returns:** A list of generated schedules for all years and sections.
   - **Explanation:** Iterates through each year and section, generates schedules using ScheduleGenerator, and compiles them into a final schedule.



## Components Interaction

1. **JSON Configuration:** Holds all the necessary data about sections, modules, teachers, and rooms. This data acts as the foundation for the scheduling operations.
2. **ScheduleManager Class:** Acts as the central control unit that manages the scheduling for all sections using the ScheduleGenerator instances. It accesses global resources like room and teacher availability and coordinates the scheduling activities across different sections to avoid conflicts.
3. **ScheduleGenerator Class:** Responsible for generating the schedule for a specific section. It interacts with the data layers to fetch teacher availability and room schedules. This class contains multiple methods to handle different scheduling tasks.
4. **Data Layer Interaction:** Both ScheduleManager and ScheduleGenerator interact heavily with the JSON-configured data to retrieve and update scheduling information. This includes checking the availability of rooms and teachers and updating schedules as sessions are assigned.
5. **Utility Methods:** Methods like find_suitable_teacher and find_available_room provide utility support by checking specific conditions that affect the scheduling decisions, ensuring that no overlaps or conflicts occur in the schedules.
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

- **Installation:** Ensure Python 3.x is installed along with Flask. Install other dependencies as listed in requirements.txt.
- **Execution:** Run the Flask application with `python app.py` and utilize the provided API endpoints to interact with the system.
