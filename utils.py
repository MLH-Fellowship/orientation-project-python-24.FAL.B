""" Util functions for the Flask App."""
import json
import re
from spellchecker import SpellChecker

def check_phone_number(phone_number):
    """ Checks if the phone number is valid and follows
        the international country code
    """
    regex = re.compile(r'^\+\d{1,3}\d{1,14}$')
    return bool(regex.match(phone_number))

def correct_spelling(text: str):
    """ Corrects the spelling of a text"""

    spell_checker = SpellChecker()
    word_pattern = r'\w+|[^\w\s]'

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
        with open(file_path, 'r') as file:
            data = json.load(file)
            print(f"Successfully loaded data from {file_path}")
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
