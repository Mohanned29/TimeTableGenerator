from flask import Flask, request, jsonify
from main import generate_schedules_for_all

app = Flask(__name__)

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    data = request.json
    try:
        schedules = generate_schedules_for_all(data)
        return jsonify(schedules), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
