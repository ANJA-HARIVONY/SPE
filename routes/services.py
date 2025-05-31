from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Service

bp = Blueprint('services', __name__, url_prefix='/services')

@bp.route('/')
@login_required
def index():
    if current_user.role != 'admin':
        flash('Accès non autorisé')
        return redirect(url_for('main.dashboard'))
        
    services = Service.query.all()
    return render_template('services/index.html', services=services)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'admin':
        flash('Accès non autorisé')
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        nom = request.form.get('nom')
        description = request.form.get('description')
        
        service = Service(nom=nom, description=description)
        db.session.add(service)
        db.session.commit()
        
        flash('Service créé avec succès')
        return redirect(url_for('services.index'))
        
    return render_template('services/create.html')

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    if current_user.role != 'admin':
        flash('Accès non autorisé')
        return redirect(url_for('main.dashboard'))
        
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        service.nom = request.form.get('nom')
        service.description = request.form.get('description')
        
        db.session.commit()
        flash('Service mis à jour avec succès')
        return redirect(url_for('services.index'))
        
    return render_template('services/update.html', service=service)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    if current_user.role != 'admin':
        flash('Accès non autorisé')
        return redirect(url_for('main.dashboard'))
        
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    
    flash('Service supprimé avec succès')
    return redirect(url_for('services.index')) 