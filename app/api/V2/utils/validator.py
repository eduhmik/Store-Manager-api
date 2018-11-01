import random
import re

class Password():
    """method to validate a password"""
    def check_is_valid(self, pwd):
        for char in pwd:
            if char.isdigit() and char.islower() and char.isupper() and len(pwd) in range(6, 13):
                return True
            return 'invalid'
        

class Email():
    """method to validate an email"""
    def is_valid_email(self,email):
        match = re.match(
            r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            return {"message": "Enter a valid email address"}
        return email