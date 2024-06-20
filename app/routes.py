from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from .logic import Logic

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        success, message = Logic.add_new_user(username, password, email)
        if success:
            flash(message, 'success')
            return render_template('login.html', message=message)
        else:
            flash(message, 'danger')
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
    return render_template('login.html')

