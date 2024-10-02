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

def test_experience_post_success():
    """
    Test the successful creation of a new experience entry.
    """
    new_experience = {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "start_date": "January 2023",
        "end_date": "Present",
        "description": "Full stack development",
        "logo": "tech-corp-logo.png"
    }
    response = app.test_client().post('/resume/experience',
                           json=new_experience)
    assert response.status_code == 201
    for key, value in response.json.items():
        assert new_experience[key] == value

def test_experience_post_missing_fields():
    """
    Test the unsuccessful creation of a new experience entry because of missing fields.
    """
    incomplete_experience = {
        "title": "Data Engineer",
        "company": "Google"
    }
    response = app.test_client().post('/resume/experience', 
                           json=incomplete_experience)
    assert response.status_code == 400
    assert 'error' in response.json

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

def test_post_education_success():
    """
    Test the successful creation of a new education entry.
    """
    new_education = {
        "course": "Master's in Computer Science",
        "school": "Tech University",
        "start_date": "September 2022",
        "end_date": "June 2024",
        "grade": "3.8 GPA",
        "logo": "tech-uni-logo.png"
    }
    response = app.test_client().post('/resume/education', 
                            json=new_education,
                            content_type='application/json')
    assert response.status_code == 201
    for key, value in response.json.items():
        assert new_education[key] == value

def test_post_education_missing_fields():
    """
    Test the unsuccessful creation of a new education entry because of missing fields.
    """
    incomplete_education = {
        "course": "PhD in Computer Science",
        "school": "Cornell University"
    }
    response = app.test_client().post('/resume/education', 
                            json=incomplete_education,
                            content_type='application/json')
    assert response.status_code == 400
    assert 'error' in response.json

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

def test_post_skill_success():
    """
    Test the successful creation of a new post entry.
    """
    new_skill = {
        "name": "JavaScript",
        "proficiency": "3-4 Years",
        "logo": "js-logo.png"
    }
    response = app.test_client().post('/resume/skill', 
                            json=new_skill,
                            content_type='application/json')
    assert response.status_code == 201
    for key, value in response.json.items():
        assert new_skill[key] == value

def test_post_skill_missing_fields():
    """
    Test the unsuccessful creation of a new skill entry because of missing fields.
    """
    incomplete_skill = {
        "name": "JavaScript"
    }
    response = app.test_client().post('/resume/skill', 
                            json=incomplete_skill,
                            content_type='application/json')
    assert response.status_code == 400
    assert 'error' in response.json