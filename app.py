from flask import Flask, request, jsonify
from main import generate_schedules

app = Flask(__name__)

@app.route('/generate_schedule', methods=['POST'])
def receive_and_process_schedule():
    data = request.get_json()
    sections = data['sections']
    rooms = data['rooms']
    schedules = generate_schedules(sections, rooms)
    return jsonify(schedules)

@app.route('/')
def home():
    return "Flask app is running!"


if __name__ == '__main__':
    app.run(debug=True)