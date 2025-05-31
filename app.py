from flask import Flask
from datetime import datetime
import os
from extensions import db, login_manager

# Initialisation de l'application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
db.init_app(app)
login_manager.init_app(app)

# Import des modèles et des routes
from models import User, Dossier, Service, Historique
from routes import auth, main, dossiers, services
from api import api

# Enregistrement des blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(main.bp)
app.register_blueprint(dossiers.bp)
app.register_blueprint(services.bp)
app.register_blueprint(api)

# Création des tables de la base de données
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 