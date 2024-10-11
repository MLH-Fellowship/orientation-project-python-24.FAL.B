"""
Flask Application
"""

from flask import Flask, jsonify, request
from models import Experience, Education, Skill, User
from utils import get_suggestion, check_phone_number, correct_spelling


app = Flask(__name__)

data = {
    "user": [User("Jackie Stewart", "+4478322678", "jack@resume.com")],
    "experience": [
        Experience(
            "Software Developer",
            "A Cool Company",
            "October 2022",
            "Present",
            "Writing Python Code",
            "example-logo.png",
        ),
        Experience(
            "Intern",
            "A Nice Company",
            "October 2021",
            "December 2021",
            "Writing Scripts",
            "example-logo.png",
        ),
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


@app.route("/resume/user", methods=["GET", "POST", "PUT"])
def user():
    """
    Handles User information
    """

    # defining sub function to reduce number of returns
    def get_users():
        return jsonify([user.__dict__ for user in data["user"]]), 200

    def add_user(body):
        # retrieve user's information.
        name = body["name"]
        phone_number = body["phone_number"]
        email = body["email_address"]
        # store the new user information.
        if not check_phone_number(phone_number):
            return jsonify({"error": "Incorrect phone number !"}), 400
        new_user = User(name, phone_number, email)
        data["user"].append(new_user)
        return jsonify(new_user.__dict__), 201

    # edit the user information.
    def edit_user(body):
        name = body["name"]
        phone_number = body["phone_number"]
        email = body["email_address"]
        for i, user_ in enumerate(data["user"]):
            if user_.email_address == email:
                if not check_phone_number(phone_number):
                    return jsonify({"error": "Incorrect phone number !"}), 400
                data["user"][i] = User(name, phone_number, email)
                return jsonify(data["user"][i].__dict__), 200
        return jsonify({"error": "User not found !"}), 404

    if request.method == "GET":
        return get_users()
    if request.method == "POST":
        body = request.get_json()
        return add_user(body)
    if request.method == "PUT":
        body = request.get_json()
        return edit_user(body)
    return jsonify({"error": "Unsupported request method !"}), 405


@app.route("/resume/experience", methods=["GET", "POST", 'PUT'])
def experience():
    """
    Handle experience requests
    """
    if request.method == 'GET':
        return jsonify(
            {"experience": [exp.__dict__ for exp in data["experience"]]})

    if request.method == "POST":
        new_experience = request.json
        new_exp = new_experience["data"][0]
        experience_instance = Experience(
            new_exp["title"],
            new_exp["company"],
            new_exp["start_date"],
            new_exp["end_date"],
            new_exp["description"],
            new_exp["logo"],
        )
        data["experience"].append(experience_instance)
        return jsonify({"id": len(data["experience"]) - 1})

    if request.method == 'PUT':
        body = request.get_json()
        new_experience_order = []
        for exp in body['data']:
            title = exp['title']
            company = exp['company']
            start_date = exp['start_date']
            end_date = exp['end_date']
            description = exp['description']
            logo = exp['logo']

            new_experience_order.append(
                Experience(title, company, start_date, end_date, description, logo)
                )
        data['experience'] = new_experience_order

        return_data = [item.__dict__ for item in data['experience']]
        return jsonify(return_data), 200

    return jsonify({"error": "Unsupported request method !"}), 405

@app.route('/resume/education', methods=['GET', 'POST', 'PUT'])
def education():
    """
    Handles education requests
    """
    if request.method == 'GET':
        return jsonify(
            {"education": [edu.__dict__ for edu in data["education"]]})

    if request.method == "POST":
        new_education = request.json
        new_edu = new_education["data"][0]
        education_instance = Education(
            new_edu["course"],
            new_edu["school"],
            new_edu["start_date"],
            new_edu["end_date"],
            new_edu["grade"],
            new_edu["logo"],
        )
        data["education"].append(education_instance)
        return jsonify({"id": len(data["education"]) - 1})

    if request.method == 'PUT':
        body = request.get_json()
        new_education_order = []
        for edu in body['data']:
            course = edu['course']
            school = edu['school']
            start_date = edu['start_date']
            end_date = edu['end_date']
            grade = edu['grade']
            logo = edu['logo']
            new_education_order.append(Education(course, school, start_date, end_date, grade, logo))
        data['education'] = new_education_order

        return_data = [item.__dict__ for item in data['education']]
        return jsonify(return_data), 200
    return jsonify({})


@app.route("/resume/skill", methods=["GET", "POST", 'PUT'])
def skill():
    """
    Handles Skill requests
    """

    if request.method == "GET":
        return jsonify({"skills": [skill.__dict__ for skill in data["skill"]]})

    if request.method == "POST":
        new_skill = request.json
        skill_data = new_skill["data"][0]
        skill_instance = Skill(
            skill_data["name"],
            skill_data["proficiency"],
            skill_data["logo"]
        )
        data["skill"].append(skill_instance)
        return jsonify({"id": len(data["skill"]) - 1})

    if request.method == 'PUT':
        body = request.get_json()
        new_skill_order = []
        for _skill in body['data']:
            name = _skill['name']
            proficiency = _skill['proficiency']
            logo = _skill['logo']
            new_skill_order.append(Skill(name, proficiency, logo))
        data['skill'] = new_skill_order

        return_data = [item.__dict__ for item in data['skill']]
        return jsonify(return_data), 200

    return jsonify({})


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
    return jsonify({"suggestion": suggestion})
