'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill, User
from utils import check_phone_number
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

@app.route('/resume/experience', methods=['GET', 'POST', 'PUT'])
def experience():
    '''
    Handle experience requests
    '''
    if request.method == 'GET':
        return jsonify([item.__dict__ for item in data['experience']]), 200

    if request.method == 'POST':
        return jsonify({})

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
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify([item.__dict__ for item in data['education']]), 200

    if request.method == 'POST':
        return jsonify({})

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


@app.route('/resume/skill', methods=['GET', 'POST', 'PUT'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify([item.__dict__ for item in data['skill']]), 200

    if request.method == 'POST':
        return jsonify({})

    if request.method == 'PUT':
        body = request.get_json()
        new_skill_order = []
        for skill in body['data']:
            name = skill['name']
            proficiency = skill['proficiency']
            logo = skill['logo']
            new_skill_order.append(Skill(name, proficiency, logo))
        data['skill'] = new_skill_order

        return_data = [item.__dict__ for item in data['skill']]
        return jsonify(return_data), 200

    return jsonify({})
