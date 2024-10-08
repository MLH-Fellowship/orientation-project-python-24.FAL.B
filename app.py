'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill

app = Flask(__name__)

data = {
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
