'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill, User
from utils import check_phone_number, correct_spelling, load_data
app = Flask(__name__)

data = load_data('data/resume.json')

@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})

@app.route('/resume/user', methods=['GET', 'POST', 'PUT'])
def user():
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
    
    if request.method == 'PUT':
        # Find the user by email and update their information

        for i, user in enumerate(data['user']):
            if user['email_address'] == email:
                data['user'][i] = {
                    'name': name,
                    'phone_number': phone_number,
                    'email_address': email
                }
                return jsonify(data['user'][i]), 200

        return jsonify({"error": "User not found !"}), 404

    return jsonify({"error": "Unsupported request method"}), 405

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
