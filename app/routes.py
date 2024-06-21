from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User
from .logic import Logic

main = Blueprint('main', __name__)


@main.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', user=user)


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


@main.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully", 'success')
    return redirect(url_for('main.home'))

