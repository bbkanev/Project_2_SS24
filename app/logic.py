from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Test, Question, Attempt
from datetime import datetime

import random
import re


class Logic:
    @staticmethod
    def add_new_user(username, password, email, confirm_password):
        # Check if password and confirm password match
        if password != confirm_password:
            return False, "Passwords do not match"

        # Validate password
        is_valid_password, message = Logic.validate_password(password)
        if not is_valid_password:
            return False, message

        # Validate email
        is_valid_email, message = Logic.validate_email(email)
        if not is_valid_email:
            return False, message

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return False, "This email already exists"
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return True, "User registered successfully"

    @staticmethod
    def verify_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return True, user
        return False, "Invalid email or password"

    @staticmethod
    def validate_password(password):
        # Minimum length of 8 characters
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        # Contains both uppercase and lowercase characters
        if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password):
            return False, "Password must contain both uppercase and lowercase characters"

        # Contains at least one numerical digit
        if not re.search(r"\d", password):
            return False, "Password must contain at least one numerical digit"

        # Contains at least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"

        return True, "Password is valid"

    @staticmethod
    def validate_email(email):
        # Regex pattern for validating an Email
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, email):
            return False, "Invalid email address"
        return True, "Email is valid"

    @staticmethod
    def add_new_test(name, time, is_published, created_by):
        new_test = Test(name=name, time=time, is_published=is_published, created_by=created_by)
        db.session.add(new_test)
        db.session.commit()
        return True, "Test added successfully"

    @staticmethod
    def add_new_question(question, answer, option1, option2, option3, points, test_id):
        new_question = Question(question=question, answer=answer, option1=option1, option2=option2, option3=option3,
                                points=points, test_id=test_id)
        db.session.add(new_question)
        db.session.commit()
        return True, "Question added successfully"

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def calculate_total_score(test_id):
        questions = Question.query.filter_by(test_id=test_id).all()
        total_score = sum([question.points for question in questions])
        return total_score

    @staticmethod
    def delete_question(question_id):
        question = Question.query.get(question_id)
        test_id = question.test_id
        if question:
            db.session.delete(question)
            db.session.commit()
            return True, "Question deleted successfully", test_id
        return False, "Question not found"

    @staticmethod
    def shuffle_options(question):
        options = [question.answer, question.option1, question.option2, question.option3]
        options = [option for option in options if option]  # Remove any None values
        random.shuffle(options)
        return options

    @staticmethod
    def save_attempt(test_id, user_id, finish_time, time_taken, score, max_score):
        new_attempt = Attempt(test_id=test_id, user_id=user_id, finish_time=finish_time,
                              time_taken=time_taken, score=score)
        db.session.add(new_attempt)
        db.session.commit()
        return True, f"Test submitted successfully! Your score is {score}/{max_score}', 'success'"

    @staticmethod
    def calculate_time_taken(start_time_str):
        if start_time_str:
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
            finish_time = datetime.utcnow()
            time_taken = (finish_time - start_time).total_seconds()
        else:
            finish_time = datetime.utcnow()
            time_taken = None
        return finish_time, time_taken

    @staticmethod
    def get_leaderboard(attempts):
        best_attempts = {}
        for attempt in attempts:
            if attempt.user_id not in best_attempts or (attempt.score > best_attempts[attempt.user_id].score) or (
                    attempt.score == best_attempts[attempt.user_id].score and attempt.time_taken <
                    best_attempts[attempt.user_id].time_taken):
                best_attempts[attempt.user_id] = attempt

        results = list(best_attempts.values())

        return results