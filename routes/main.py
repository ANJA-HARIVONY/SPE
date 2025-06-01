from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Dossier, Service, Historique
from sqlalchemy import desc

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    # Récupération des dossiers selon le rôle de l'utilisateur
    if current_user.role == 'admin':
        dossiers = Dossier.query.order_by(desc(Dossier.date_creation)).all()
    elif current_user.role == 'chef':
        dossiers = Dossier.query.filter_by(service_id=current_user.service_id).order_by(desc(Dossier.date_creation)).all()
    else:
        dossiers = Dossier.query.filter_by(service_id=current_user.service_id).order_by(desc(Dossier.date_creation)).all()
    
    # Statistiques
    total_dossiers = len(dossiers)
    dossiers_en_cours = len([d for d in dossiers if d.statut == 'en_cours'])
    dossiers_termines = len([d for d in dossiers if d.statut == 'termine'])
    
    return render_template('main/dashboard.html',
                         dossiers=dossiers,
                         total_dossiers=total_dossiers,
                         dossiers_en_cours=dossiers_en_cours,
                         dossiers_termines=dossiers_termines)

@bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')

@bp.route('/help')
def help():
    return render_template('help/index.html') 