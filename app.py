'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill
from typing import List, Dict, Any
from dataclasses import asdict

app = Flask(__name__)

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}

def validate_fields(required_fields: List[str], request_data: Dict[str, Any]) -> tuple:
    '''
    Validate that all the required fields are present in the request data
    '''
    missing_fields = [field for field in required_fields if field not in request_data]
    if missing_fields: 
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, ""

@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})

@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle experience requests
    '''
    if request.method == 'GET':
        return jsonify()

    if request.method == 'POST':
        request_data = request.get_json()
        required_fields = ["title", "company", "start_date", "end_date", "description", "logo"]
        is_valid, error_mssg = validate_fields(required_fields, request_data)

        if not is_valid: 
            return jsonify({"error": error_mssg}), 400
        
        try: 
            new_experience = Experience(**request_data)
            data["experience"].append(new_experience)
            return jsonify(asdict(new_experience)), 201
        except TypeError as e: 
            return jsonify({"error": str(e)}), 400

    return jsonify({}), 405

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        request_data = request.get_json()
        required_fields = ["course", "school", "start_date", "end_date", "grade", "logo"]
        is_valid, error_mssg = validate_fields(required_fields, request_data)
        
        if not is_valid:
            return jsonify({"error": error_mssg}), 400
        try: 
            new_education = Education(**request_data)
            data["education"].append(new_education)
            return jsonify(asdict(new_education)), 201
        except TypeError as e:
            return jsonify({"error": str(e)}), 400

    return jsonify({}), 405


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        request_data = request.get_json()
        required_fields = ["name", "proficiency", "logo"]
        is_valid, error_mssg = validate_fields(required_fields, request_data)
        
        if not is_valid:
            return jsonify({"error": error_mssg}), 400
        try: 
            new_skill = Skill(**request_data)
            data["skill"].append(new_skill)
            return jsonify(asdict(new_skill)), 201
        except TypeError as e:
            return jsonify({"error": str(e)}), 400

    return jsonify({}), 405
