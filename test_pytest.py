'''
Tests in Pytest
'''
from app import app


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
    assert response.json[item_id] == example_experience


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
    assert response.json[item_id] == example_education


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
    assert response.json[item_id] == example_skill
