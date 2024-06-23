from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Test, Question
from .logic import Logic
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def home():
    user = session.get('user')

    if user:
        user_tests = Test.query.filter_by(created_by=user['id']).all()
        published_tests = Test.query.filter(Test.is_published, Test.created_by != user['id']).all()
        # Getting the creator for each published test
        for test in published_tests:
            test.author = Logic.get_user_by_id(test.created_by).username

    else:
        user_tests = []
        published_tests = Test.query.filter_by(is_published=True).all()
        # Getting the creator for each published test
        for test in published_tests:
            test.author = Logic.get_user_by_id(test.created_by).username

    return render_template('index.html', user=user, published_tests=published_tests, user_tests=user_tests)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        success, message = Logic.add_new_user(username, password, email, confirm_password)
        if success:
            flash(message, 'success')
            return redirect(url_for('main.login'))
        else:
            flash(message, 'danger')
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        success, user = Logic.verify_user(email, password)
        if success:
            session['user'] = {'username': user.username, 'email': user.email, 'id': user.id}
            flash("Login successful", 'success')
            return redirect(url_for('main.home'))
        else:
            flash(user, 'danger')
    return render_template('login.html')


@main.route('/add_test', methods=['GET', 'POST'])
def add_test():
    user = session.get('user')

    if not user:
        flash("You need to login first", 'danger')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        is_published = False
        success, message = Logic.add_new_test(name, time, is_published, user['id'])
        if success:
            flash(message, 'success')
            return redirect(url_for('main.home'))
        else:
            flash(message, 'danger')
    return render_template('add_test.html', user=user)


@main.route('/edit_test/<uuid:test_id>', methods=['GET', 'POST'])
def edit_test(test_id):
    user = session.get('user')

    test = Test.query.get(test_id)
    total_points = Logic.calculate_total_score(test_id)

    if not test:
        flash("Test not found", 'danger')
        return redirect(url_for('main.home'))

    if not user or test.created_by != user['id']:
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    if request.method == 'POST':
        test.name = request.form['name']
        test.time = request.form['time']
        db.session.commit()
        flash('Test updated successfully', 'success')
        return redirect(url_for('main.edit_test', test_id=test_id, total_points=total_points))
    return render_template('edit_test.html', test=test, total_points=total_points)


@main.route('/add_question/<uuid:test_id>', methods=['GET', 'POST'])
def add_question(test_id):
    user = session.get('user')
    current_test = Test.query.get(test_id)

    if not user or current_test.created_by != user['id']:
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    if request.method == 'POST':
        question_text = request.form['question']
        answer = request.form['answer']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        points = request.form['points']
        success, message = Logic.add_new_question(question_text, answer, option1, option2, option3, points, test_id)
        if success:
            flash(message, 'success')
            return redirect(url_for('main.edit_test', test_id=test_id))
        else:
            flash(message, 'danger')
    return render_template('add_question.html', test_id=test_id)


@main.route('/edit_question/<uuid:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    user = session.get('user')

    question = Question.query.get(question_id)
    if not question:
        flash("Error in finding the question", 'danger')
        return redirect(url_for('main.home'))

    current_test = Test.query.get(question.test_id)
    if not user or current_test.created_by != user['id']:
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    if request.method == 'POST':
        question.question = request.form['question']
        question.answer = request.form['answer']
        question.option1 = request.form['option1']
        question.option2 = request.form['option2']
        question.option3 = request.form['option3']
        question.points = request.form['points']
        db.session.commit()
        flash('Question updated successfully', 'success')
        return redirect(url_for('main.edit_test', test_id=question.test_id))

    return render_template('edit_question.html', question=question)


@main.route('/delete_question/<uuid:question_id>', methods=['POST'])
def delete_question(question_id):
    success, message, test_id = Logic.delete_question(question_id)
    if success:
        flash(message, 'success')
        return redirect(url_for('main.edit_test', test_id=test_id))
    else:
        flash(message, 'danger')
        return redirect(url_for('main.home'))


@main.route('/publish_test/<uuid:test_id>', methods=['POST'])
def publish_test(test_id):
    test = Test.query.get(test_id)
    if not test:
        flash("Test not found", 'danger')
        return redirect(url_for('main.home'))

    if test.is_published:
        flash("Test withdraw successfully", 'success')
    else:
        flash("Test published successfully", 'warning')

    test.is_published = not test.is_published
    db.session.commit()
    return redirect(url_for('main.home'))


@main.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully", 'success')
    return redirect(url_for('main.home'))
