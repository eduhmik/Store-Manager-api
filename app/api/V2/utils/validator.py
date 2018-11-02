import random
import re

class Password(object):
    @staticmethod
    def check_has_digit(self,pwd):
        for char in pwd:
            if char.isdigit():
                return True
    @staticmethod
    def check_has_lower(self,pwd):
        for char in pwd:
            if char.islower():
                return True
    @staticmethod
    def check_has_upper(self,pwd):
        for char in pwd:
            if char.isupper():
                return True
    @staticmethod
    def check_has_special_chars(self,pwd):
        special_chars = ['$', '#', '@']
        return [char for char in pwd if char in special_chars]
    @staticmethod
    def check_password_length(self,pwd):
        if len(pwd) in range(6, 13):
            return True
    @staticmethod
    def is_valid(self, pwd):
        bool = self.check_has_digit(pwd) and self.check_has_lower(pwd) and self.check_has_special_chars(pwd) and self.check_password_length(pwd) and self.check_has_upper(pwd)
        if bool:
            return 'validated'
        return 'invalid'
    @staticmethod
    def get_valid_passwords(self, pwds):
        validated_password = []
        for pwd in pwds:
            if self.is_valid(pwd):
                validated_password.append(pwd)
            return validated_password
        

class Email():
    """method to validate an email"""
    def is_valid_email(self, email):
        match = re.match(
            r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            return {"message": "Enter a valid email address"}
        return True