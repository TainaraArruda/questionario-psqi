from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User
from datetime import datetime
bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('quiz.index'))
        flash('Usuário ou senha inválidos', 'error')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        birthdate = request.form['birthdate']
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
        email = request.form['email']
        password = request.form['password']
        user = User(fullname=fullname, birthdate=birthdate, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')