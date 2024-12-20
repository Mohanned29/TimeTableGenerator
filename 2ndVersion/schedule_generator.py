import logging
from typing import List, Dict, Optional
from ortools.sat.python import cp_model
import random

class ScheduleGenerator:
    def __init__(self, year: int, section: Dict, rooms: List[Dict], teachers: List[Dict]):
        self.year = year
        self.section = section
        self.rooms = rooms
        self.teachers = teachers
        self.MAX_LATE_SLOTS = 2
        self.PREFERRED_END_SLOT = 4
        self.time_slots = {
            1: "8:00 - 9:30",
            2: "9:40 - 11:10", 
            3: "11:20 - 12:50",
            4: "13:00 - 14:30",
            5: "14:40 - 16:10",
            6: "16:20 - 17:50"
        }

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    def create_constraint_model(self):

      model = cp_model.CpModel()
      solver = cp_model.CpSolver()
      days = ["lundi", "mardi", "mercredi", "jeudi", "dimanche", "samedi"]
      variables = {
          'late_slots': [],
          'teacher_work_days': []
      }

      for module in self.section['modules']:
          for day in days:
              for slot in self.time_slots.keys():
                  for session_type in ['Lecture', 'TD', 'TP']:
                      var_name = f"{module['name']}_{day}_{slot}_{session_type}"
                      variables[var_name] = model.NewBoolVar(var_name)

      late_slots_var = model.NewIntVar(0, len(self.section['modules']), 'late_slots')
      model.Add(late_slots_var == sum(
          var for var_name, var in variables.items() 
          if 'late_slots' in var_name and var == 1
      ))
      model.Minimize(late_slots_var)
      
      status = solver.Solve(model)

      if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
          return self._extract_schedule(solver, variables)
      else:
          self.logger.error("Could not generate a feasible schedule")
          return []



    def _extract_schedule(self, solver, variables):
        schedule = []
        for module in self.section['modules']:
            lecture_session = self._extract_session(
                solver, 
                module, 
                session_type='Lecture', 
                group=None
            )
            if lecture_session:
                schedule.append(lecture_session)
            
            # Handle group sessions (TD/TP)
            for group in self.section['groups']:
                # TD Session
                if module.get('td', False):
                    td_session = self._extract_session(
                        solver, 
                        module, 
                        session_type='TD', 
                        group=group
                    )
                    if td_session:
                        schedule.append(td_session)
                
                # TP Session
                if module.get('tp', False):
                    tp_session = self._extract_session(
                        solver, 
                        module, 
                        session_type='TP', 
                        group=group
                    )
                    if tp_session:
                        schedule.append(tp_session)
        return schedule


    def _extract_session(self, solver, module, session_type, group):

      day = random.choice(["lundi", "mardi", "mercredi", "jeudi", "dimanche", "samedi"])

      teacher = self.find_suitable_teacher(module['name'], day)
      if not teacher:
          teacher = "No teacher available"

      room_name = self.find_available_room(session_type, day)
      if not room_name:
          return None

      slot = random.choice(list(self.time_slots.keys()))
      
      return {
          'day': day,
          'room': room_name,
          'moduleName': module['name'],
          'session_type': session_type,
          'teacher': teacher,
          'group': group,
          'time': self.time_slots[slot],
          'slot': slot,
          'section': self.section['name']
      }


    def generate_schedule(self):
        try:
            self._validate_input()
            schedule = self.create_constraint_model()
            return schedule

        except Exception as e:
            self.logger.error(f"Schedule generation failed: {e}")
            return []


    def _validate_input(self):
        required_keys = ['modules', 'groups']
        for key in required_keys:
            if key not in self.section:
                raise ValueError(f"Missing required section key: {key}")

        if not self.rooms or not self.teachers:
            raise ValueError("Rooms and teachers data are required")


    def analyze_schedule_quality(self, schedule):
        metrics = {
            'late_slots_count': 0,
            'teacher_workload': {},
            'section_distribution': {}
        }
        for session in schedule:

            if session['slot'] > self.PREFERRED_END_SLOT:
                metrics['late_slots_count'] += 1

            metrics['teacher_workload'][session['teacher']] = \
                metrics['teacher_workload'].get(session['teacher'], 0) + 1

            metrics['section_distribution'][session['section']] = \
                metrics['section_distribution'].get(session['section'], []) + [session['slot']]
        return metrics


    def optimize_schedule(self, schedule):
      metrics = self.analyze_schedule_quality(schedule)
      optimized_schedule = self._redistribute_late_slots(schedule, metrics)  
      return optimized_schedule


    def _redistribute_late_slots(self, schedule, metrics):
        if metrics['late_slots_count'] <= self.MAX_LATE_SLOTS:
            return schedule

        optimized_schedule = schedule.copy()

        late_sessions = sorted(
            [session for session in optimized_schedule if session['slot'] > self.PREFERRED_END_SLOT],
            key=lambda x: x['slot'], 
            reverse=True
        )

        for session in late_sessions:
            earlier_slots = [
                slot for slot in range(1, self.PREFERRED_END_SLOT + 1)
                if self._is_slot_available(optimized_schedule, session, slot)
            ]

            if earlier_slots:
                new_slot = min(earlier_slots)
                
                session['slot'] = new_slot
                session['time'] = self.time_slots[new_slot]

        new_metrics = self.analyze_schedule_quality(optimized_schedule)

        if new_metrics['late_slots_count'] > self.MAX_LATE_SLOTS:
            optimized_schedule = self._aggressive_slot_redistribution(optimized_schedule)

        return optimized_schedule


    def _is_slot_available(self, schedule, session, target_slot):
        conflicts = [
            existing_session for existing_session in schedule
            if (existing_session['day'] == session['day'] and 
                existing_session['slot'] == target_slot and
                (existing_session['section'] == session['section'] or 
                existing_session['teacher'] == session['teacher']))
        ]

        return len(conflicts) == 0


    def _aggressive_slot_redistribution(self, schedule):
      """
      More aggressive strategy for redistributing late slots
      """
      # Group sessions by module and section
      session_groups = {}
      for session in schedule:
          key = (session['moduleName'], session['section'], session['session_type'])
          if key not in session_groups:
              session_groups[key] = []
          session_groups[key].append(session)

      # Redistribute sessions across different days if possible
      days = ["lundi", "mardi", "mercredi", "jeudi", "dimanche", "samedi"]
      
      for group_key, group_sessions in session_groups.items():
          late_sessions = [s for s in group_sessions if s['slot'] > self.PREFERRED_END_SLOT]
          
          for late_session in late_sessions:
              # Try to find an alternative day with earlier slots
              for day in days:
                  if day != late_session['day']:
                      # Check if we can move the session to an earlier slot on a different day
                      alternative_slots = [
                          slot for slot in range(1, self.PREFERRED_END_SLOT + 1)
                          if self._is_slot_available(schedule, late_session, slot)
                      ]
                      
                      if alternative_slots:
                          late_session['day'] = day
                          late_session['slot'] = min(alternative_slots)
                          late_session['time'] = self.time_slots[late_session['slot']]
                          break

      return schedule
