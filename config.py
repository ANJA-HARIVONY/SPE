import os
from datetime import timedelta

class Config:
    # Configuration de base
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///spe.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration de la session
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Configuration des uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Configuration de l'application
    APP_NAME = "SPE - Suivi de Dossiers"
    ITEMS_PER_PAGE = 20
    
    # Configuration des rôles
    ROLES = {
        'admin': 'Administrateur',
        'chef': 'Chef de service',
        'agent': 'Agent'
    }
    
    # Configuration des statuts de dossier
    STATUTS = {
        'en_cours': 'En cours',
        'termine': 'Terminé',
        'archive': 'Archivé'
    }

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 