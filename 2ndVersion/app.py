from flask import Flask, request, jsonify, abort
from schedule_manager import ScheduleManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    data = request.json
    if not data:
        abort(400, "Request body is missing or not in JSON format")
    
    try:
        # Validate input data
        required_fields = ['years', 'rooms', 'teachers']
        for field in required_fields:
            if field not in data or not data[field]:
                abort(400, f"Required field '{field}' is missing or empty")

        years = data['years']
        rooms = data['rooms']
        teachers = data['teachers']

        # Initialize and generate schedules
        schedule_manager = ScheduleManager(years, rooms, teachers)
        schedules = schedule_manager.generate_schedules_for_all()

        # Log successful schedule generation
        logger.info(f"Successfully generated schedules for {len(years)} years")

        return jsonify(schedules), 200
    
    except KeyError as e:
        logger.error(f"Key error during schedule generation: {str(e)}")
        return jsonify({"error": f"Missing key in request data: {str(e)}"}), 400
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error during schedule generation: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
