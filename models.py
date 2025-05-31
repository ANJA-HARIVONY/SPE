from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # admin, chef, agent
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    users = db.relationship('User', backref='service', lazy=True)
    dossiers = db.relationship('Dossier', backref='service', lazy=True)

class Dossier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), unique=True, nullable=False)
    reference_spe = db.Column(db.String(50), nullable=True)
    date_creation = db.Column(db.DateTime, nullable=False)
    objet = db.Column(db.String(200), nullable=False)
    titulaire = db.Column(db.String(100), nullable=False)
    destinataire = db.Column(db.String(100), nullable=False)
    pays = db.Column(db.String(100), nullable=False)
    observation = db.Column(db.Text, nullable=True)
    statut = db.Column(db.String(20), nullable=False)  # en_cours, termine, archive
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    historique = db.relationship('Historique', backref='dossier', lazy=True)

class Historique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dossier_id = db.Column(db.Integer, db.ForeignKey('dossier.id'), nullable=False)
    date_action = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    user = db.relationship('User', backref='actions')
    service = db.relationship('Service', backref='actions') 