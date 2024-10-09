# pylint: disable=R0913

'''
Models for the Resume API. Each class is related to
'''

from dataclasses import dataclass
from typing import List

@dataclass
class User:
    '''
    User Class
    '''
    name: str
    phone_number: str
    email_address: str

@dataclass
class Experience:
    '''
    Experience Class
    '''
    title: str
    company: str
    start_date: str
    end_date: str
    description: str
    logo: str


@dataclass
class Education:
    '''
    Education Class
    '''
    course: str
    school: str
    start_date: str
    end_date: str
    grade: str
    logo: str


@dataclass
class Skill:
    '''
    Skill Class
    '''
    name: str
    proficiency: str
    logo: str

@dataclass
class Project:
    '''
    Project Class
    '''
    title: str
    description: str
    technologies: List[str]
    link: str