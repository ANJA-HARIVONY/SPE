from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Service
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Identifiants invalides')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role != 'admin':
        flash('Accès non autorisé')
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        service_id = request.form.get('service_id')
        
        if User.query.filter_by(username=username).first():
            flash('Nom d\'utilisateur déjà utilisé')
            return redirect(url_for('auth.register'))
            
        user = User(username=username, email=email, role=role, service_id=service_id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Utilisateur créé avec succès')
        return redirect(url_for('main.dashboard'))
        
    services = Service.query.all()
    return render_template('auth/register.html', services=services) 