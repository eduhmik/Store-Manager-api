from passlib.hash import pbkdf2_sha256 as sha256

class User():
    user_id = 1
    users = []
    password = ''

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
        User.users.append(user)
        return user
        
    @staticmethod
    def get_single_user(email):
        """Retrieve user details by email"""

        single_user = [user for user in User.users if user['email'] == email]
        if single_user:
            return single_user[0]
        return 'not found'


    def get_all_users(self):
        return User.users

    def del_users(self):
        User.users.clear()
        del User.users[:]

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
        
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    
