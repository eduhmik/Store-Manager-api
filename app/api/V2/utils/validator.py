import random
import re

class Password():
    def __init__(self, pwd):
        self.pwd = pwd
    
    def check_has_digit(self,pwd):
        return any(char.isdigit() for char in pwd)
    
    def check_has_lower(self,pwd):
        return any(char.islower() for char in pwd)
    
    def check_has_upper(self,pwd):
        return any(char.isupper() for char in pwd)
    
    def check_has_special_chars(self,pwd):
        special_chars = ['$', '#', '@', '*', '&', '!', '%']
        return [char for char in pwd if char in special_chars]
    
    def check_password_length(self,pwd):
        if len(pwd) in range(6, 13):
            return True
    
    def is_valid(self, pwd):
        bool = self.check_has_digit(pwd) and self.check_has_lower(pwd) and self.check_has_special_chars(pwd) and self.check_password_length(pwd) and self.check_has_upper(pwd)
        if bool:
            return 'validated'
        return 'invalid'
    
        

class Email():
    """method to validate an email"""
    def is_valid_email(self, email):
        match = re.match(
            r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            return {"message": "Enter a valid email address"}
        return True


class Verify():
    def __init__(self, payload):
        self.payload = payload

    def is_empty(self, items):
        for item in items:
            if bool(item) is False:
                return True
        return False


    def is_whitespace(self, items):
        for item in items:
            if item.isspace() is True:
                return True
        return False


    def is_payload(self, items, length):
        for item in items:
            if item is None or not item:
                return False


    def is_product_payload(self, items):
        res = self.payload(items, 5)
        if res:
            return 'valid'
        return 'invalid'


    def is_sales_payload(self, items):
        res = self.payload(items, 4, ['product_name', 'quantity', 'total', 'seller'])
        return res


    def is_register_payload(self, items):
        res = self.payload(items, 5, ['username', 'email', 'phone', 'role', 'password'])
        return res


    def is_login_payload(self, items):
        res = self.payload(items, 2, ['email', 'password'])
        return res


        