"""
Flask Application
"""
from flask import Flask, jsonify, request
from models import Experience, Education, Skill, Project
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


@app.route("/resume/experience", methods=["GET", "POST", 'PUT'])
def experience():
    """
    Handle experience requests
    """
    if request.method == "GET":
        return jsonify({"experience": list(data["experience"])}), 200

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
        return jsonify({"id": len(data["experience"]) - 1}), 201
            
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
        return_data = list(data['experience'])       
        return jsonify(return_data), 200

    return jsonify({"error": "Unsupported request method !"}), 405

@app.route('/resume/education', methods=['GET', 'POST', 'PUT'])
def education():
    """
    Handles education requests
    """

    if request.method == "GET":
        return jsonify({"education": list(data["education"])}), 200

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
        return jsonify({"id": len(data["education"]) - 1}), 201
      
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

        return_data = list(data['education'])
        return jsonify(return_data), 200
    return jsonify({}), 405



@app.route("/resume/skill", methods=["GET", "POST", 'PUT'])
def skill():
    """
    Handles Skill requests
    """

    if request.method == "GET":
        return jsonify({"skills": list(data["skill"])}), 200

    if request.method == "POST":
        new_skill = request.json
        skill_data = new_skill["data"][0]
        skill_instance = Skill(
            skill_data["name"],
            skill_data["proficiency"],
            skill_data["logo"]
        )
        data["skill"].append(skill_instance)
        return jsonify({"id": len(data["skill"]) - 1}), 201
      
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

    return jsonify({}), 405


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

        # Check if the id is within the range of the project list
        int_id = int(project_id)
        if int_id < 0 or int_id >= len(data['project']):
            raise ValueError("Project not found")

        return int_id

    def get_project(project_id):
        '''
        Get project by id
        '''
        if project_id is not None:
            try:
                project_id = validate_id(project_id)
                return jsonify(data['project'][project_id]), 200
            except ValueError as error:
                return jsonify({"error": str(error)}), 400

        return jsonify([
                        {**project, "id": str(index)}
                        for index, project in enumerate(data['project'])
                ]), 200

    def add_project(body):
        '''
        Add project
        '''
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

    def edit_project(project_id, body):
        '''
        Edit project
        '''
        try:
            project_id = validate_id(project_id)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        for key, value in body.items():
            if hasattr(data['project'][project_id], key):
                setattr(data['project'][project_id], key, value)
            else:
                return jsonify({"error": f"Invalid field: {key}"}), 400

        return jsonify({**data['project'][project_id].__dict__, "id": str(project_id)}), 200

    def delete_project(project_id):
        '''
        Delete project
        '''
        try:
            project_id = validate_id(project_id)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        del data['project'][project_id]
        return jsonify({}), 204

    if request.method == 'GET':
        project_id = request.args.get('id', None)
        return get_project(project_id)

    if request.method == 'POST':
        body = request.get_json()
        return add_project(body)

    if request.method == 'PUT':
        project_id = request.args.get('id', None)
        body = request.get_json()

        return edit_project(project_id, body)

    if request.method == 'DELETE':
        project_id = request.args.get('id', None)

        return delete_project(project_id)

    return jsonify({"error": "Unsupported request method"}), 405


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
