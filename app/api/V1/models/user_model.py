from passlib.hash import pbkdf2_sha256 as sha256

class User():
    user_id = 1
    users = []

    def __init__(self, email, password, username, role, phone):
        self.username = username
        self.email = email
        self.password =password
        self.role = role
        self.phone = phone

    def create_user(self):
        user = dict(
            email = self.email,
            password = self.password,
            username = self.username,
            role = self.role,
            phone = self.phone
        )
        self.users.append(user)
        return user

    def find_by_email(self, email):
        found_email = [email for email in User.users if email['email'] == email]
        return found_email
    
    def get_all_users(self):
        return User.users

    def del_users(self):
        User.users.clear()
        del User.users[:]

    def generate_hash(self, password):
        return sha256.hash(password)

    def verify_hash(self, password, hash):
        return sha256.verify(password, hash)

    
