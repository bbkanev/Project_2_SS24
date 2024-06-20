from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User


class Logic:
    @staticmethod
    def add_new_user(username, password, email):
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return False, "Username already exists"
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return True, "User registered successfully"


    def verify_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return True, "Login successful"
        return False, "Invalid username or password"