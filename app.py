from flask import Flask, request, jsonify, abort
from schedule_manager import ScheduleManager

app = Flask(__name__)

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    data = request.json
    if not data:
        abort(400, "Request body is missing or not in JSON format")
        
    try:
        rooms = data.get('rooms')
        teachers = data.get('teachers')
        sections = data.get('sections')

        if not rooms or not teachers or not sections:
            abort(400, "Required fields (rooms, teachers, sections) are missing")

        schedule_manager = ScheduleManager(sections, rooms, teachers)
        schedules = schedule_manager.generate_schedules_for_all()
        return jsonify(schedules), 200
    
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
