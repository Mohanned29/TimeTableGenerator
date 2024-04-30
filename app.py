from flask import Flask, request, jsonify
from schedule_manager import ScheduleManager

app = Flask(__name__)

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    data = request.json
    try:
        rooms = data['rooms']
        teachers = data['teachers']
        sections = data['sections']

        schedule_manager = ScheduleManager(sections, rooms, teachers)
        schedules = schedule_manager.generate_schedules_for_all()
        return jsonify(schedules), 200
    except Exception as e:
        app.logger.error(f"error processing request: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
