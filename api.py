from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from extensions import db
from models import User, Service, Dossier, Historique
from datetime import datetime

api = Blueprint('api', __name__, url_prefix='/api')

# Routes pour les utilisateurs
@api.route('/users', methods=['GET'])
@login_required
def get_users():
    if current_user.role != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'service_id': user.service_id
    } for user in users])

@api.route('/users/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    if current_user.role != 'admin' and current_user.id != id:
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'service_id': user.service_id
    })

# Routes pour les services
@api.route('/services', methods=['GET'])
@login_required
def get_services():
    services = Service.query.all()
    return jsonify([{
        'id': service.id,
        'nom': service.nom,
        'description': service.description,
        'users_count': len(service.users),
        'dossiers_count': len(service.dossiers)
    } for service in services])

@api.route('/services/<int:id>', methods=['GET'])
@login_required
def get_service(id):
    service = Service.query.get_or_404(id)
    return jsonify({
        'id': service.id,
        'nom': service.nom,
        'description': service.description,
        'users': [{
            'id': user.id,
            'username': user.username,
            'role': user.role
        } for user in service.users],
        'dossiers': [{
            'id': dossier.id,
            'reference': dossier.reference,
            'objet': dossier.objet,
            'statut': dossier.statut
        } for dossier in service.dossiers]
    })

# Routes pour les dossiers
@api.route('/dossiers', methods=['GET'])
@login_required
def get_dossiers():
    if current_user.role == 'admin':
        dossiers = Dossier.query.all()
    else:
        dossiers = Dossier.query.filter_by(service_id=current_user.service_id).all()
    
    return jsonify([{
        'id': dossier.id,
        'reference': dossier.reference,
        'objet': dossier.objet,
        'titulaire': dossier.titulaire,
        'destinataire': dossier.destinataire,
        'statut': dossier.statut,
        'service_id': dossier.service_id,
        'date_creation': dossier.date_creation.isoformat()
    } for dossier in dossiers])

@api.route('/dossiers/<int:id>', methods=['GET'])
@login_required
def get_dossier(id):
    dossier = Dossier.query.get_or_404(id)
    if current_user.role != 'admin' and dossier.service_id != current_user.service_id:
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    return jsonify({
        'id': dossier.id,
        'reference': dossier.reference,
        'objet': dossier.objet,
        'titulaire': dossier.titulaire,
        'destinataire': dossier.destinataire,
        'statut': dossier.statut,
        'service_id': dossier.service_id,
        'date_creation': dossier.date_creation.isoformat(),
        'historique': [{
            'id': action.id,
            'action': action.action,
            'description': action.description,
            'date_action': action.date_action.isoformat(),
            'user_id': action.user_id,
            'service_id': action.service_id
        } for action in dossier.historique]
    })

@api.route('/dossiers', methods=['POST'])
@login_required
def create_dossier():
    data = request.get_json()
    
    dossier = Dossier(
        reference=data['reference'],
        objet=data['objet'],
        titulaire=data['titulaire'],
        destinataire=data['destinataire'],
        statut=data.get('statut', 'en_cours'),
        service_id=current_user.service_id
    )
    
    db.session.add(dossier)
    
    historique = Historique(
        dossier=dossier,
        action='Création du dossier',
        description=f'Dossier créé par {current_user.username}',
        user_id=current_user.id,
        service_id=current_user.service_id
    )
    
    db.session.add(historique)
    db.session.commit()
    
    return jsonify({
        'id': dossier.id,
        'reference': dossier.reference,
        'message': 'Dossier créé avec succès'
    }), 201

@api.route('/dossiers/<int:id>', methods=['PUT'])
@login_required
def update_dossier(id):
    dossier = Dossier.query.get_or_404(id)
    if current_user.role != 'admin' and dossier.service_id != current_user.service_id:
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    data = request.get_json()
    
    dossier.objet = data.get('objet', dossier.objet)
    dossier.titulaire = data.get('titulaire', dossier.titulaire)
    dossier.destinataire = data.get('destinataire', dossier.destinataire)
    dossier.statut = data.get('statut', dossier.statut)
    
    historique = Historique(
        dossier=dossier,
        action='Mise à jour du dossier',
        description=f'Dossier mis à jour par {current_user.username}',
        user_id=current_user.id,
        service_id=current_user.service_id
    )
    
    db.session.add(historique)
    db.session.commit()
    
    return jsonify({
        'id': dossier.id,
        'message': 'Dossier mis à jour avec succès'
    })

@api.route('/dossiers/<int:id>/transfer', methods=['POST'])
@login_required
def transfer_dossier(id):
    if current_user.role not in ['admin', 'chef']:
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    dossier = Dossier.query.get_or_404(id)
    data = request.get_json()
    
    if 'service_id' not in data:
        return jsonify({'error': 'service_id est requis'}), 400
    
    service = Service.query.get_or_404(data['service_id'])
    dossier.service_id = service.id
    
    historique = Historique(
        dossier=dossier,
        action='Transfert du dossier',
        description=f'Dossier transféré vers le service {service.nom} par {current_user.username}',
        user_id=current_user.id,
        service_id=service.id
    )
    
    db.session.add(historique)
    db.session.commit()
    
    return jsonify({
        'id': dossier.id,
        'message': 'Dossier transféré avec succès'
    })

# Routes pour l'historique
@api.route('/historique', methods=['GET'])
@login_required
def get_historique():
    if current_user.role == 'admin':
        historique = Historique.query.order_by(Historique.date_action.desc()).all()
    else:
        historique = Historique.query.filter_by(service_id=current_user.service_id).order_by(Historique.date_action.desc()).all()
    
    return jsonify([{
        'id': action.id,
        'dossier_id': action.dossier_id,
        'action': action.action,
        'description': action.description,
        'date_action': action.date_action.isoformat(),
        'user_id': action.user_id,
        'service_id': action.service_id
    } for action in historique]) 