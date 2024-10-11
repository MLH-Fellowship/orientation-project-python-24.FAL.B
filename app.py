"""
Flask Application
"""
from flask import Flask, jsonify, request
from models import Experience, Education, Skill
from utils import check_phone_number, correct_spelling, get_suggestion, load_data

app = Flask(__name__)

data = load_data('data/resume.json')


@app.route("/test")
def hello_world():
    """
    Returns a JSON test message
    """
    return jsonify({"message": "Hello, World!"})


@app.route("/resume/user", methods=["GET", "POST", "PUT"])
def user_route():
    """
    Handle GET, POST, and PUT requests for user data.
    GET: Retrieve all users
    POST: Create a new user
    PUT: Update an existing user
    """
    if request.method == 'GET':
        return jsonify(data['user']), 200

    body = request.get_json()
    if not body or not all(key in body for key in ['name', 'phone_number', 'email_address']):
        return jsonify({"error": "Missing required fields"}), 400

    name = body['name']
    phone_number = body['phone_number']
    email = body['email_address']
    if not check_phone_number(phone_number):
        return jsonify({"error": "Incorrect phone number"}), 400

    if request.method == 'POST':
        # Create a new user and add it to the data
        new_user = {
            'name': name,
            'phone_number': phone_number,
            'email_address': email
        }
        data['user'].append(new_user)
        return jsonify(new_user), 201

    # Handle PUT request
    for i, current_user in enumerate(data['user']):
        if current_user['email_address'] == email:
            data['user'][i] = {
                'name': name,
                'phone_number': phone_number,
                'email_address': email
            }
            return jsonify(data['user'][i]), 200

    return jsonify({"error": "User not found !"}), 404


@app.route("/resume/experience", methods=["GET", "POST"])
def experience():
    """
    Handle experience requests
    """

    if request.method == "GET":
        return jsonify({"experience": list(data["experience"])}), 200

    if request.method == "POST":
        new_experience = request.json
        experience_instance = Experience(
            new_experience["title"],
            new_experience["company"],
            new_experience["start_date"],
            new_experience["end_date"],
            new_experience["description"],
            new_experience["logo"],
        )
        data["experience"].append(experience_instance)
        return jsonify({"id": len(data["experience"]) - 1}), 201

    return jsonify({}), 405


@app.route("/resume/education", methods=["GET", "POST"])
def education():
    """
    Handles education requests
    """
    if request.method == "GET":
        return jsonify({"education": list(data["education"])}), 200

    if request.method == "POST":
        new_education = request.json
        education_instance = Education(
            new_education["course"],
            new_education["school"],
            new_education["start_date"],
            new_education["end_date"],
            new_education["grade"],
            new_education["logo"],
        )
        data["education"].append(education_instance)
        return jsonify({"id": len(data["education"]) - 1}), 201

    return jsonify({}), 405


@app.route("/resume/skill", methods=["GET", "POST"])
def skill():
    """
    Handles Skill requests
    """

    if request.method == "GET":
        return jsonify({"skills": list(data["skill"])}), 200

    if request.method == "POST":
        new_skill = request.json
        skill_instance = Skill(
            new_skill["name"], new_skill["proficiency"], new_skill["logo"]
        )
        data["skill"].append(skill_instance)
        return jsonify({"id": len(data["skill"]) - 1}), 201

    return jsonify({}), 405


@app.route("/resume/spellcheck", methods=["POST"])
def spellcheck():
    """
    Corrects the spelling of a text
    """
    body = request.get_json()
    try:
        text = body["text"]
        corrected_text = correct_spelling(text)

        return jsonify({"before": text, "after": corrected_text}), 200
    except KeyError:
        return jsonify({"error": "Missing text parameter"}), 400


@app.route("/suggestion", methods=["POST"])
def get_description_suggestion():
    """
    Handles suggestion requests
    """
    description = request.json.get("description")
    description_type = request.json.get("type")
    if not description or not description_type:
        return jsonify({"error": "Description and type are required"}), 400
    suggestion = get_suggestion(description, description_type)
    return jsonify({"suggestion": suggestion}), 200
