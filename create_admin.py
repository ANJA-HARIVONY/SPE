from app import app, db
from models import User, Service

def create_admin():
    with app.app_context():
        # Créer un service par défaut
        service = Service(nom="Administration", description="Service administratif")
        db.session.add(service)
        db.session.commit()

        # Créer un utilisateur admin
        admin = User(
            username="admin",
            email="admin@example.com",
            role="admin",
            service_id=service.id
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Utilisateur admin créé avec succès!")

if __name__ == "__main__":
    create_admin() 