from flask import Flask, request, jsonify, abort
from schedule_manager import ScheduleManager

app = Flask(__name__)

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    data = request.json
    if not data:
        abort(400, "Request body is missing or not in JSON format")
    
    try:
        years = data.get('years')
        rooms = data.get('rooms')
        teachers = data.get('teachers')

        if not years or not rooms or not teachers:
            abort(400, "Required fields (years, rooms, teachers) are missing")

        schedule_manager = ScheduleManager(years, rooms, teachers)
        schedules = schedule_manager.generate_schedules_for_all()
        return jsonify(schedules), 200
    
    except KeyError as e:
        return jsonify({"error": f"Missing key in request data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
