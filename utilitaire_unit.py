import os
import sys
import subprocess
from pathlib import Path

def supprimer_base_donnees():
    """Supprime le fichier de base de données s'il existe"""
    db_path = Path('instance/spe.db')
    if db_path.exists():
        try:
            os.remove(db_path)
            print("✅ Base de données supprimée avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression de la base de données: {e}")
            sys.exit(1)
    else:
        print("ℹ️ Aucune base de données trouvée")

def executer_create_admin():
    """Exécute le script create_admin.py"""
    try:
        subprocess.run([sys.executable, 'create_admin.py'], check=True)
        print("✅ Administrateur créé avec succès")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la création de l'administrateur: {e}")
        sys.exit(1)

def main():
    print("🔄 Réinitialisation de l'application...")
    
    # Supprimer la base de données
    supprimer_base_donnees()
    
    # Créer l'administrateur
    executer_create_admin()
    
    print("\n✨ Réinitialisation terminée avec succès!")
    print("Vous pouvez maintenant démarrer l'application avec 'flask run'")

if __name__ == '__main__':
    main() 