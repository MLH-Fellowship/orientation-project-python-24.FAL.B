'''
Tests in Pytest
'''

import os
import json
import tempfile
import pytest
from app import app

from utils import load_data
from unittest.mock import patch


def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"

def test_user():
    '''
    Tests the /resume/user route. 
    '''
    # test GET request.
    response = app.test_client().get('/resume/user')
    assert response.status_code == 200
    assert isinstance(response.json, list)

    # test POST request with valid user information
    response = app.test_client().post('/resume/user', json={
        'name': 'John Doe',
        'phone_number': '+1234567890',
        'email_address': 'johndoe@example.com'
    })
    assert response.status_code == 201
    assert response.json['name'] == 'John Doe'
    assert response.json['phone_number'] == '+1234567890'
    assert response.json['email_address'] == 'johndoe@example.com'

    # test PUT request with invalid email address
    response = app.test_client().put('/resume/user', json={
        'name': 'Ola Doe',
        'phone_number': '+0987654321',
        'email_address': 'invalid-email'
    })
    assert response.status_code == 404
    assert response.json['error'] == 'User not found !'

    # test PUT request with valid email address
    response = app.test_client().put('/resume/user', json={
        'name': 'Ola Doe',
        'phone_number': '+0987654321',
        'email_address': 'johndoe@example.com'
    })
    assert response.status_code == 200
    assert response.json['name'] == 'Ola Doe'
    assert response.json['phone_number'] == '+0987654321'
    assert response.json['email_address'] == 'johndoe@example.com'

def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    response = app.test_client().get('/resume/experience')
    assert response.json["experience"][item_id] == example_experience


def test_education():
    '''
    Add a new education and then get all educations. 
    
    Check that it returns the new education in that list
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']

    response = app.test_client().get('/resume/education')
    assert response.json["education"][item_id] == example_education


def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json["skills"][item_id] == example_skill


@pytest.mark.parametrize('text, expected', [
    ('thiss is an exmple of spell chcking.',
        'this is an example of spell checking.'),
    ('I look forwrd to receving your response.',
        'I look forward to receiving your response.'), 
    ('plese let me knw if you need anythng else.',
        'please let me know if you need anything else.'),
    ("an apsirng softwar engneer,",
        "an aspiring software engineer,"),
    ('this is oppen-suorce project.',
        'this is open-source project.'),
    ('jldjldkwedwedweadncew',
        'jldjldkwedwedweadncew'),
    ('123', '123'),
    ('', '')
])
def test_correct_spelling(text, expected):
    '''
    Test the correct_spelling function
    '''
    response = app.test_client().post('/resume/spellcheck', json={'text': text})
    assert response.status_code == 200
    assert response.json['after'] == expected
    
@pytest.fixture
def setup_teardown():
    '''
    Setup temporary file to test load_data
    '''
    # Create a temporary directory and file for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file_path = os.path.join(temp_dir, 'test_resume.json')
        test_data = {
            "user": [
                {
                    "name": "Jackie Stewart",
                    "phone_number": "+4478322678",
                    "email_address": "jack@resume.com"
                }
            ],
            "experience": [
                {
                    "title": "Software Developer",
                    "company": "A Cool Company",
                    "start_date": "October 2022",
                    "end_date": "Present",
                    "description": "Writing Python Code",
                    "logo": "example-logo.png"
                }
            ],
            "education": [
                {
                    "degree": "Computer Science",
                    "institution": "University of Tech",
                    "start_date": "September 2019",
                    "end_date": "July 2022",
                    "grade": "80%",
                    "logo": "example-logo.png"
                }
            ],
            "skill": [
                {
                    "name": "Python",
                    "experience": "1-2 Years",
                    "logo": "example-logo.png"
                }
            ]
        }
        with open(test_file_path, 'w') as file:
            json.dump(test_data, file)

        yield test_file_path, test_data

def test_load_data(setup_teardown):
    '''
    Test the load_data util function
    '''
    test_file_path, test_data = setup_teardown

    # Test if the load_data function successfully loads the data
    data = load_data(test_file_path)
    assert data == test_data

    # Test if the load_data function handles file not found
    non_existent_file = os.path.join(tempfile.gettempdir(), 'non_existent_file.json')
    data = load_data(non_existent_file)
    assert data is None

    # Test if the load_data function handles invalid JSON
    invalid_json_file = os.path.join(tempfile.gettempdir(), 'invalid_resume.json')
    with open(invalid_json_file, 'w') as file:
        file.write('{invalid_json}')

    data = load_data(invalid_json_file)
    assert data is None

    if os.path.exists(invalid_json_file):
        os.remove(invalid_json_file)
        
# testcases for ai suggested improved descriptions
@patch('app.get_suggestion')
def test_get_description_suggestion(mock_get_suggestion):
    '''
    Test the /suggestion route with valid inputs
    '''
    mock_get_suggestion.return_value = "Improved description"

    response = app.test_client().post('/suggestion', json={
        'description': 'This is a sample description.',
        'type': 'experience'
    })

    assert response.status_code == 200
    assert response.json['suggestion'] == 'Improved description'


def test_get_description_suggestion_missing_fields():
    '''
    Test the /suggestion route with missing fields
    '''
    # Missing 'type'
    response = app.test_client().post('/suggestion', json={
        'description': 'This is a sample description.'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Description and type are required'

    # Missing 'description'
    response = app.test_client().post('/suggestion', json={
        'type': 'experience'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Description and type are required'

