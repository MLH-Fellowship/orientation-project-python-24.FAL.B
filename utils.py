"""
Utility Methods File
"""
import os
import re
import json
from spellchecker import SpellChecker
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def get_suggestion(description, description_type):
    """
    give suggestions for description section using gemini (free alternative to openai's chatgpt api)
    """
    prompt = ""
    if description_type == "education":
        prompt = f"Improve the following education \
        experience description for resume: {description}"
    elif description_type == "experience":
        prompt = f"Improve the following professional \
         experience description for resume: {description}"

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text


def check_phone_number(phone_number):
    """Checks if the phone number is valid and follows
    the international country code
    """
    regex = re.compile(r"^\+\d{1,3}\d{1,14}$")
    return bool(regex.match(phone_number))


def correct_spelling(text: str):
    """Corrects the spelling of a text"""

    spell_checker = SpellChecker()
    word_pattern = r"\w+|[^\w\s]"

    misspelled = spell_checker.unknown(re.findall(word_pattern, text))
    corrected_text = text

    for word in misspelled:
        correction = spell_checker.correction(word)
        if correction:
            corrected_text = corrected_text.replace(word, correction)

    return corrected_text

def load_data(file_path):
    """ Loads the json file """
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            print(f"Successfully loaded data from {file_path}")
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return None
