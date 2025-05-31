from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Dossier, Historique, Service
from datetime import datetime

bp = Blueprint('dossiers', __name__, url_prefix='/dossiers')

@bp.route('/')
@login_required
def index():
    dossiers = Dossier.query.order_by(Dossier.date_creation.desc()).all()
    return render_template('dossiers/index.html', dossiers=dossiers)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        reference = request.form.get('reference')
        reference_spe = request.form.get('reference_spe')
        date_creation = datetime.strptime(request.form.get('date_creation'), '%Y-%m-%d')
        objet = request.form.get('objet')
        titulaire = request.form.get('titulaire')
        destinataire = request.form.get('destinataire')
        pays = request.form.get('pays')
        observation = request.form.get('observation')
        
        dossier = Dossier(
            reference=reference,
            reference_spe=reference_spe,
            date_creation=date_creation,
            objet=objet,
            titulaire=titulaire,
            destinataire=destinataire,
            pays=pays,
            observation=observation,
            statut='En cours',
            service_id=current_user.service_id
        )
        
        db.session.add(dossier)
        
        # Création de l'entrée dans l'historique
        historique = Historique(
            dossier=dossier,
            action='Création du dossier',
            description=f'Dossier créé par {current_user.username}',
            user_id=current_user.id,
            service_id=current_user.service_id
        )
        
        db.session.add(historique)
        db.session.commit()
        
        flash('Dossier créé avec succès')
        return redirect(url_for('dossiers.view', id=dossier.id))
        
    return render_template('dossiers/create.html')

@bp.route('/<int:id>')
@login_required
def view(id):
    dossier = Dossier.query.get_or_404(id)
    historique = Historique.query.filter_by(dossier_id=id).order_by(Historique.date_action.desc()).all()
    services = Service.query.filter(Service.id != dossier.service_id).all()  # Exclure le service actuel
    return render_template('dossiers/view.html', dossier=dossier, historique=historique, services=services)

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    dossier = Dossier.query.get_or_404(id)
    
    if request.method == 'POST':
        dossier.date_creation = datetime.strptime(request.form.get('date_creation'), '%Y-%m-%d')
        dossier.objet = request.form.get('objet')
        dossier.titulaire = request.form.get('titulaire')
        dossier.destinataire = request.form.get('destinataire')
        dossier.pays = request.form.get('pays')
        dossier.observation = request.form.get('observation')
        dossier.reference_spe = request.form.get('reference_spe')
        dossier.statut = request.form.get('statut')
        
        historique = Historique(
            dossier=dossier,
            action='Mise à jour du dossier',
            description=f'Dossier mis à jour par {current_user.username}',
            user_id=current_user.id,
            service_id=current_user.service_id
        )
        
        db.session.add(historique)
        db.session.commit()
        
        flash('Dossier mis à jour avec succès')
        return redirect(url_for('dossiers.view', id=dossier.id))
        
    return render_template('dossiers/update.html', dossier=dossier)

@bp.route('/<int:id>/transfer', methods=['POST'])
@login_required
def transfer(id):
    if current_user.role not in ['admin', 'chef']:
        flash('Accès non autorisé')
        return redirect(url_for('dossiers.view', id=id))
        
    dossier = Dossier.query.get_or_404(id)
    service_id = request.form.get('service_id')
    observation_transfert = request.form.get('observation_transfert')
    
    if not service_id:
        flash('Veuillez sélectionner un service de destination')
        return redirect(url_for('dossiers.view', id=id))
    
    if not observation_transfert:
        flash('Veuillez saisir la référence SPE')
        return redirect(url_for('dossiers.view', id=id))
    
    service = Service.query.get_or_404(service_id)
    if service.id == dossier.service_id:
        flash('Le dossier est déjà dans ce service')
        return redirect(url_for('dossiers.view', id=id))
    
    dossier.service_id = service_id
    historique = Historique(
        dossier=dossier,
        action='Transfert du dossier',
        description=f'Dossier transféré vers le service {service.nom} par {current_user.username} (Obs: {observation_transfert})',
        user_id=current_user.id,
        service_id=service_id
    )
    
    db.session.add(historique)
    db.session.commit()
    
    flash('Dossier transféré avec succès')
    return redirect(url_for('dossiers.view', id=dossier.id)) 