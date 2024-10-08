'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill, User
from utils import check_phone_number, correct_spelling
app = Flask(__name__)

data = {
    "user": [
        User("Jackie Stewart",
             "+4478322678",
             "jack@resume.com")
    ],
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png"),
        Experience("Intern",
                   "A Nice Company",
                   "October 2021",
                   "December 2021",
                   "Writing Scripts",
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


@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
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

@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle experience requests
    '''
    if request.method == 'GET':
        return jsonify({"experience": [exp.__dict__ for exp in data["experience"]]})

    if request.method == 'POST':
        new_experience = request.json
        experience_instance = Experience(
            new_experience["title"],
            new_experience["company"],
            new_experience["start_date"],
            new_experience["end_date"],
            new_experience["description"],
            new_experience["logo"]
        )
        data["experience"].append(experience_instance)
        return jsonify({"id": len(data["experience"]) - 1})

    return jsonify({})

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({"education": [edu.__dict__ for edu in data["education"]]})

    if request.method == 'POST':
        new_education = request.json
        education_instance = Education(
            new_education["course"],
            new_education["school"],
            new_education["start_date"],
            new_education["end_date"],
            new_education["grade"],
            new_education["logo"]
        )
        data["education"].append(education_instance)
        return jsonify({"id": len(data["education"]) - 1})

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({"skills": [skill.__dict__ for skill in data["skill"]]})

    if request.method == 'POST':
        new_skill = request.json
        skill_instance = Skill(new_skill["name"], new_skill["proficiency"], new_skill["logo"])
        data["skill"].append(skill_instance)
        return jsonify({"id": len(data["skill"]) - 1})

    return jsonify({})

@app.route('/resume/spellcheck', methods=['POST'])
def spellcheck():
    '''
    Corrects the spelling of a text
    '''
    body = request.get_json()
    try:
        text = body['text']
        corrected_text = correct_spelling(text)

        return jsonify({"before": text, "after": corrected_text}), 200
    except KeyError:
        return jsonify({"error": "Missing text parameter"}), 400
