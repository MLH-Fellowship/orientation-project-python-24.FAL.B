"""
Flask Application
"""

from flask import Flask, jsonify, request

from models import Experience, Education, Skill,User
from utils import get_suggestion,check_phone_number


app = Flask(__name__)

data = {
    "user": [
        User("Jackie Stewart",
             "+4478322678",
             "jack@resume.com")
    ],
    "experience": [
        Experience(
            "Software Developer",
            "A Cool Company",
            "October 2022",
            "Present",
            "Writing Python Code",
            "example-logo.png",
        )
    ],
    "education": [
        Education(
            "Computer Science",
            "University of Tech",
            "September 2019",
            "July 2022",
            "80%",
            "example-logo.png",
        )
    ],
    "skill": [Skill("Python", "1-2 Years", "example-logo.png")],
}


@app.route("/test")
def hello_world():
    """
    Returns a JSON test message
    """
    return jsonify({"message": "Hello, World!"})

@app.route('/resume/user', methods=['GET', 'POST', 'PUT'])
def user():
    '''
    Handles User information
    '''
    if request.method == 'GET':
        return jsonify([user.__dict__ for user in data['user']]), 200
    # retrieve user's information.
    body = request.get_json()
    name = body['name']
    phone_number = body['phone_number']
    email = body['email_address']

    # store the new user information.
    if request.method == 'POST':
        if not check_phone_number(phone_number):
            return jsonify({"error": "Incorrect phone number !"}), 400

        new_user = User(name, phone_number, email)
        data['user'].append(new_user)
        return jsonify(new_user.__dict__), 201

    # edit the user information.
    if request.method == 'PUT':

        for i, user in enumerate(data['user']):  # find the user in the data.
            if user.email_address == email:
                if not check_phone_number(phone_number):
                    return jsonify({"error": "Incorrect phone number !"}), 400

                data['user'][i] = User(name, phone_number, email) # update the user's info.
                return jsonify(data['user'][i].__dict__), 200

        return jsonify({"error": "User not found !"}), 404
    # add a default return statement for unsupported request methods
    return jsonify({"error": "Unsupported request method !"}), 405

@app.route("/resume/experience", methods=["GET", "POST"])
def experience():
    """
    Handle experience requests
    """
    if request.method == "GET":
        return jsonify()

    if request.method == "POST":
        return jsonify({})

    return jsonify({})


@app.route("/resume/education", methods=["GET", "POST"])
def education():
    """
    Handles education requests
    """
    if request.method == "GET":
        return jsonify({})

    if request.method == "POST":
        return jsonify({})

    return jsonify({})


@app.route("/resume/skill", methods=["GET", "POST"])
def skill():
    """
    Handles Skill requests
    """
    if request.method == "GET":
        return jsonify({})

    if request.method == "POST":
        return jsonify({})

    return jsonify({})


@app.route("/suggestion", methods=["POST"])
def get_description_suggestion():
    """
    Handles suggestion requests
    """
    description = request.json.get("description")
    type = request.json.get("type")
    if not description or not type:
        return jsonify({"error": "Description and type are required"}), 400
    suggestion = get_suggestion(description, type)
    return jsonify({"suggestion": suggestion})
