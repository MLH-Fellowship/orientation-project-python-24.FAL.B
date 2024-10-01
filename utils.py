""" Util functions for the Flask App."""
import re

def check_phone_number(phone_number):
    """ Checks if the phone number is valid and follows
        the international country code
    """
    # regular expression for international numbers. 
    regex = re.compile(r'^\+\d{1,3}\d{1,14}$')

    if regex.match(phone_number):
        return True
    
    return False