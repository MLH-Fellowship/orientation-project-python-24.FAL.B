'''
Tests in Pytest
'''

import os
from unittest.mock import patch
import json
import tempfile
import pytest
from app import app

from utils import load_data


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
        "data": [
            {
                "title": "Software Developer",
                "company": "A Cooler Company",
                "start_date": "October 2022",
                "end_date": "Present",
                "description": "Writing JavaScript Code",
                "logo": "example-logo.png"
            }
        ]
    }

    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    response = app.test_client().get('/resume/experience')
    print(response.json)
    assert response.json["experience"][item_id] == example_experience['data'][0]

    # test PUT request
    response = app.test_client().put('/resume/experience', json={"data": [
            {
                "title": "Software Developer",
                "company": "The Coolest Company",
                "start_date": "October 2024",
                "end_date": "Present",
                "description": "Writing Python Code",
                "logo": "example-logo.png"
            }
        ]})
    assert response.status_code == 200
    response_data = response.json[0]
    assert response_data['title'] == 'Software Developer'
    assert response_data['company'] == 'The Coolest Company'
    assert response_data['start_date'] == 'October 2024'
    assert response_data['end_date'] == 'Present'
    assert response_data['description'] == 'Writing Python Code'
    assert response_data['logo'] == 'example-logo.png'


def test_education():
    '''
    Add a new education and then get all educations. 
    
    Check that it returns the new education in that list
    '''
    example_education = {"data": [{
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }]}

    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']

    response = app.test_client().get('/resume/education')
    assert response.json["education"][item_id] == example_education['data'][0]

    response = app.test_client().put('/resume/education', json={
        "data": [
            {
                "course": "Updated Course",
                "school": "Updated University",
                "start_date": "September 2020",
                "end_date": "June 2023",
                "grade": "90%",
                "logo": "new-education-logo.png"
            }
        ]
    })
    assert response.status_code == 200
    response_data = response.json[0]
    assert response_data['course'] == 'Updated Course'
    assert response_data['school'] == 'Updated University'
    assert response_data['start_date'] == 'September 2020'
    assert response_data['end_date'] == 'June 2023'
    assert response_data['grade'] == '90%'
    assert response_data['logo'] == 'new-education-logo.png'


def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = { "data":[{
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }]
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json["skills"][item_id] == example_skill["data"][0]

    response = app.test_client().put('/resume/skill', json={
        "data": [
            {
                "name": "Python",
                "proficiency": "4-6 years",
                "logo": "new-logo.png"
            }
        ]
    })
    assert response.status_code == 200
    response_data = response.json[0]
    assert response_data['name'] == 'Python'
    assert response_data['proficiency'] == '4-6 years'
    assert response_data['logo'] == 'new-logo.png'



def test_get_project():
    '''
    Test the get_project function

    Check that it returns a list of projects
    '''
    response = app.test_client().get('/resume/project')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_add_project():
    '''
    Test the add_project function

    Check that it returns the new project
    Check that it returns an error when missing fields
    '''
    new_project = {
        'title': 'Sample Project',
        'description': 'A sample project',
        'technologies': ['Python', 'Flask'],
        'link': 'https://github.com/username/sample-project'
    }
    response = app.test_client().post('/resume/project', json=new_project)
    assert response.status_code == 201
    assert response.json == {**new_project, 'id': '1'}

    new_project.pop('title')
    response = app.test_client().post('/resume/project', json=new_project)
    assert response.status_code == 400
    assert response.json == {'error': 'Missing fields: title'}

def test_edit_project():
    '''
    Test the edit_project function

    Check that it returns the updated project
    Check that it returns an error when the project id is invalid
    '''
    new_project = {
        'title': 'Sample Project',
        'description': 'A sample project',
        'technologies': ['Python', 'Flask'],
        'link': 'https://github.com/username/sample-project'
    }
    new_project_id = app.test_client().post('/resume/project', json=new_project).json['id']
    new_project['title'] = 'New Project'
    new_project['description'] = 'A new project'
    new_project['technologies'] = ['Python', 'Flask', 'Docker']

    response = app.test_client().\
                    put('/resume/project', json=new_project, query_string={'id': new_project_id})

    assert response.status_code == 200
    assert response.json == {**new_project, 'id': new_project_id}

    response = app.test_client().\
                        put('/resume/project', json=new_project, query_string={'id': 'invalid-id'})
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid id'}

def test_delete_project():
    '''
    Test the delete_project function

    Check that it returns a 204 status code
    Check that it returns an error when the project id is invalid
    '''
    new_project = {
        'title': 'Sample Project',
        'description': 'A sample project',
        'technologies': ['Python', 'Flask'],
        'link': 'https://github.com/username/sample-project'
    }
    new_project_id = app.test_client().post('/resume/project', json=new_project).json['id']
    response = app.test_client().delete('/resume/project', query_string={'id': new_project_id})
    assert response.status_code == 204

    response = app.test_client().delete('/resume/project', query_string={'id': 'invalid-id'})
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid id'}

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


def test_load_data():
    '''
    Test the load_data function with various scenarios
    '''
    # Setup test data
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
    # Create a temporary file with test data
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        json.dump(test_data, temp_file)
        test_file_path = temp_file.name

    try:
        # Test 1: Check if load_data function successfully loads the data
        data = load_data(test_file_path)
        assert data == test_data, "Loaded data does not match test data"

        # Test 2: Check if load_data function handles file not found
        non_existent_file = os.path.join(tempfile.gettempdir(), 'non_existent_file.json')
        data = load_data(non_existent_file)
        assert data is None, "load_data should return None for non-existent file"

        # Test 3: Check if load_data function handles invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as invalid_file:
            invalid_file.write('{invalid_json}')
            invalid_json_file = invalid_file.name

        data = load_data(invalid_json_file)
        assert data is None, "load_data should return None for invalid JSON"

    finally:
        # Cleanup
        os.unlink(test_file_path)
        if 'invalid_json_file' in locals():
            os.unlink(invalid_json_file)


# Test cases for AI-suggested improved descriptions
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
