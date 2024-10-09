'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Project, Skill, User
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
    ],
    "project": [
        Project(
                title="Sample Project",
                description="A sample project",
                technologies=["Python", "Flask"],
                link="https://github.com/username/sample-project"
        )
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
        return jsonify()

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})

@app.route('/resume/project', methods=['GET', 'POST', 'PUT', 'DELETE'])
def project():
    '''
    Handles Project requests
    '''
    def validate_id(project_id):
        '''
        Validates the id
        '''
        if project_id is None:
            raise ValueError("Missing id")

        if not project_id.isdigit():
            raise ValueError("Invalid id")

        # check if the id is within the range of the project list
        int_id = int(project_id)
        if int_id < 0 or int_id >= len(data['project']):
            raise ValueError("Project not found")

        return int_id

    if request.method == 'GET':
        project_id = request.args.get('id', None)

        if project_id is not None:
            try:
                project_id = validate_id(project_id)
                return jsonify(data['project'][project_id]), 200
            except ValueError as error:
                return jsonify({"error": str(error)}), 400

        return jsonify([
                        {**project.__dict__, "id": str(index)}
                        for index, project in enumerate(data['project'])
                ]), 200

    if request.method == 'POST':
        body = request.get_json()
        mandatory_fields = ['title', 'description', 'technologies', 'link']
        missing_fields = [field for field in mandatory_fields if field not in body]

        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        new_project = Project(
                            body['title'],
                            body['description'],
                            body['technologies'],
                            body['link']
                        )
        data['project'].append(new_project)

        return jsonify({**new_project.__dict__, "id": str(len(data['project']) - 1)}), 201

    if request.method == 'PUT':
        project_id = request.args.get('id', None)
        try:
            project_id = validate_id(project_id)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        body = request.get_json()
        for key, value in body.items():
            if hasattr(data['project'][project_id], key):
                setattr(data['project'][project_id], key, value)
            else:
                return jsonify({"error": f"invalid field: {key}"}), 400

        return jsonify({**data['project'][project_id].__dict__, "id": str(project_id)}), 200

    if request.method == 'DELETE':
        project_id = request.args.get('id', None)
        try:
            project_id = validate_id(project_id)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        del data['project'][project_id]
        return jsonify({}), 204

    return jsonify({"error": "Unsupported request method"}), 405

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
