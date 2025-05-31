# Système de Gestion des Dossiers SPE

Une application web Flask pour la gestion des dossiers de la SPE (Service des Pensions et Épargnes).

## Fonctionnalités

- 🔐 Authentification des utilisateurs avec différents rôles (admin, chef, agent)
- 📁 Gestion des dossiers (création, modification, transfert)
- 🏢 Gestion des services
- 👥 Gestion des utilisateurs
- 📊 Tableau de bord avec statistiques
- 📝 Historique des actions
- 🔄 Transfert de dossiers entre services
- 📱 Interface responsive

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

## Installation

1. Cloner le dépôt :

```bash
git clone [URL_DU_REPO]
cd SPE
```

2. Créer et activer l'environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate  # Sur Unix/macOS
# ou
.venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Initialiser la base de données :

```bash
python utilitaire_unit.py
```

## Configuration

1. Créer un fichier `.env` à la racine du projet avec les variables suivantes :

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=votre_clé_secrète
```

2. Lancer l'application :

```bash
flask run
```

## Structure du Projet

```
SPE/
├── .venv/                  # Environnement virtuel
├── instance/              # Dossier pour les fichiers d'instance
├── migrations/            # Migrations de la base de données
├── routes/               # Routes de l'application
│   ├── auth.py          # Authentification
│   ├── dossiers.py      # Gestion des dossiers
│   ├── main.py          # Routes principales
│   └── services.py      # Gestion des services
├── templates/            # Templates HTML
│   ├── auth/            # Templates d'authentification
│   ├── dossiers/        # Templates des dossiers
│   ├── main/            # Templates principaux
│   └── services/        # Templates des services
├── .gitignore           # Fichiers ignorés par Git
├── api.py               # API REST
├── app.py              # Point d'entrée de l'application
├── config.py           # Configuration
├── create_admin.py     # Script de création d'admin
├── extensions.py       # Extensions Flask
├── models.py           # Modèles de données
├── requirements.txt    # Dépendances Python
└── utilitaire_unit.py  # Utilitaires
```

## Utilisation

1. Se connecter avec les identifiants administrateur :

   - Nom d'utilisateur : admin
   - Mot de passe : admin123

2. Créer des services et des utilisateurs

3. Commencer à gérer les dossiers

## Rôles et Permissions

- **Administrateur** : Accès complet à toutes les fonctionnalités
- **Chef de service** : Gestion des dossiers de son service et transfert
- **Agent** : Gestion des dossiers de son service

## Contact

Pour toute question ou assistance, contactez :

- Email : rilonyainafanasina@gmail.com

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
