"""
Initialize default categories in the database
Run this script after starting the backend to populate categories
"""
from app.core.database import SessionLocal
from app.models import Category

# Default categories for West Africa
CATEGORIES = [
    {"name": "Véhicules", "slug": "vehicules", "icon": "🚗", "description": "Voitures, motos, pièces auto", "order": 1},
    {"name": "Immobilier", "slug": "immobilier", "icon": "🏠", "description": "Vente, location, colocations", "order": 2},
    {"name": "Emploi & Services", "slug": "emploi-services", "icon": "💼", "description": "Offres d'emploi, services à domicile", "order": 3},
    {"name": "Mode & Beauté", "slug": "mode-beaute", "icon": "👗", "description": "Vêtements, chaussures, accessoires", "order": 4},
    {"name": "Maison & Jardin", "slug": "maison-jardin", "icon": "🏡", "description": "Meubles, électroménager, décoration", "order": 5},
    {"name": "Électronique", "slug": "electronique", "icon": "📱", "description": "Téléphones, ordinateurs, TV, audio", "order": 6},
    {"name": "Loisirs", "slug": "loisirs", "icon": "🎮", "description": "Sports, instruments, livres, jeux", "order": 7},
    {"name": "Matériel Pro", "slug": "materiel-pro", "icon": "🔧", "description": "Équipements et outils professionnels", "order": 8},
]

# Subcategories
SUBCATEGORIES = {
    "vehicules": [
        {"name": "Voitures", "slug": "voitures", "order": 1},
        {"name": "Motos", "slug": "motos", "order": 2},
        {"name": "Pièces détachées", "slug": "pieces-detachees", "order": 3},
    ],
    "immobilier": [
        {"name": "Vente", "slug": "vente", "order": 1},
        {"name": "Location", "slug": "location", "order": 2},
        {"name": "Colocations", "slug": "colocations", "order": 3},
    ],
    "electronique": [
        {"name": "Téléphones", "slug": "telephones", "order": 1},
        {"name": "Ordinateurs", "slug": "ordinateurs", "order": 2},
        {"name": "TV & Audio", "slug": "tv-audio", "order": 3},
    ],
}


def init_categories():
    db = SessionLocal()
    
    try:
        # Check if categories already exist
        existing = db.query(Category).first()
        if existing:
            print("✅ Categories already initialized")
            return
        
        print("🔄 Initializing categories...")
        
        # Create main categories
        category_map = {}
        for cat_data in CATEGORIES:
            category = Category(**cat_data)
            db.add(category)
            db.commit()
            db.refresh(category)
            category_map[cat_data["slug"]] = category.id
            print(f"  ✓ Created category: {cat_data['name']}")
        
        # Create subcategories
        for parent_slug, subcats in SUBCATEGORIES.items():
            parent_id = category_map.get(parent_slug)
            if parent_id:
                for subcat_data in subcats:
                    subcat = Category(**subcat_data, parent_id=parent_id)
                    db.add(subcat)
                    db.commit()
                    print(f"    ✓ Created subcategory: {subcat_data['name']}")
        
        print("✅ Categories initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing categories: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_categories()
