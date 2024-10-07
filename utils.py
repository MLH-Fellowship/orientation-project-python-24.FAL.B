
'''
Utility Methods File
'''
import os
import google.generativeai as genai
from dotenv import load_dotenv
import re


load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def get_suggestion(description, type):
    """
    give suggestions for description section using gemini (free alternative to openai's chatgpt api)
    """
    prompt=""
    if type == "education":
        prompt = f"Improve the following education 
                  experience description for resume: {description}" 
    elif type == "experience":
        prompt = f"Improve the following professional 
                  experience description for resume: {description}"

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text



def check_phone_number(phone_number):
    """ Checks if the phone number is valid and follows
        the international country code
    """
    regex = re.compile(r'^\+\d{1,3}\d{1,14}$')
    return bool(regex.match(phone_number))

