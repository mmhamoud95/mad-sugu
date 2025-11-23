# MadSugu - Plateforme de Petites Annonces

MadSugu est une application web complète de petites annonces et ventes en ligne, adaptée pour l'Afrique de l'Ouest, inspirée de Leboncoin.fr.

## 🚀 Stack Technique

- **Backend**: FastAPI (Python)
- **Frontend**: Svelte + SvelteKit
- **Styling**: Tailwind CSS
- **Base de données**: PostgreSQL avec SQLAlchemy
- **Authentification**: JWT tokens
- **Stockage**: Local storage (S3-compatible ready)
- **Cache**: Redis

## 📋 Fonctionnalités (Phase 1 - MVP)

### ✅ Implémenté

- ✅ Authentification utilisateur (inscription, connexion, JWT)
- ✅ Gestion des profils utilisateurs
- ✅ CRUD des annonces avec upload d'images
- ✅ Système de catégories et sous-catégories
- ✅ Recherche et filtres avancés (prix, localisation, catégorie, texte)
- ✅ Système de messagerie entre utilisateurs
- ✅ Système de favoris
- ✅ Design responsive (mobile-first)
- ✅ Optimisation des images
- ✅ API REST complète avec documentation Swagger

### ✅ Phase 2 - Implémenté

- ✅ Système d'évaluations et notes
- ✅ Alertes personnalisées
- ✅ Boost et mise en avant d'annonces
- ✅ Dashboard administrateur
- ✅ Notifications push
- ✅ PWA (Progressive Web App)
- ✅ Géolocalisation avancée
- ✅ Analytics et statistiques

### 🔄 À venir (Phase 3)

- [ ] Paiement Mobile Money (Orange Money, MTN, Moov)
- [ ] Support multilingue
- [ ] Email/SMS notifications
- [ ] Maps integration avancée

## 🏗️ Architecture

```
mad-sugu/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── api/         # Routes API
│   │   ├── core/        # Configuration et sécurité
│   │   ├── models/      # Modèles SQLAlchemy
│   │   ├── schemas/     # Schémas Pydantic
│   │   └── services/    # Services (upload, etc.)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # Application SvelteKit
│   ├── src/
│   │   ├── routes/     # Pages
│   │   └── lib/        # Composants, stores, utils
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml   # Configuration Docker
```

## 🛠️ Installation et Développement

### Prérequis

- Docker et Docker Compose
- Node.js 20+ (pour développement frontend sans Docker)
- Python 3.11+ (pour développement backend sans Docker)

### Démarrage rapide avec Docker

1. Cloner le repository :
```bash
git clone <repository-url>
cd mad-sugu
```

2. Copier les fichiers d'environnement :
```bash
cp backend/.env.example backend/.env
```

3. Démarrer tous les services :
```bash
docker-compose up -d
```

4. Accéder aux applications :
- Frontend : http://localhost:5173
- Backend API : http://localhost:8000
- Documentation API (Swagger) : http://localhost:8000/docs
- Documentation API (ReDoc) : http://localhost:8000/redoc

### Développement local (sans Docker)

#### Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos configurations

# Démarrer le serveur
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev
```

## 📦 Initialisation de la Base de Données

### Créer des catégories par défaut

Utilisez l'API pour créer les catégories :

```bash
curl -X POST "http://localhost:8000/api/v1/categories/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Véhicules",
    "slug": "vehicules",
    "icon": "🚗",
    "description": "Voitures, motos, pièces auto"
  }'
```

Catégories suggérées :
- 🚗 Véhicules (vehicules)
- 🏠 Immobilier (immobilier)
- 💼 Emploi & Services (emploi-services)
- 👗 Mode & Beauté (mode-beaute)
- 🏡 Maison & Jardin (maison-jardin)
- 📱 Électronique (electronique)
- 🎮 Loisirs (loisirs)
- 🔧 Matériel professionnel (materiel-pro)

## 🔐 Sécurité

- Mots de passe hashés avec bcrypt
- Authentification JWT
- Validation des données avec Pydantic
- Protection contre les injections SQL (SQLAlchemy ORM)
- CORS configuré
- Rate limiting (à implémenter en production)
- Validation des fichiers uploadés

## 📝 API Documentation

La documentation interactive de l'API est disponible à :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

### Endpoints principaux

#### Authentification
- `POST /api/v1/auth/register` - Inscription
- `POST /api/v1/auth/login` - Connexion (form data)
- `POST /api/v1/auth/login-json` - Connexion (JSON)

#### Utilisateurs
- `GET /api/v1/users/me` - Profil actuel
- `PUT /api/v1/users/me` - Modifier profil
- `GET /api/v1/users/{user_id}` - Profil utilisateur

#### Annonces
- `GET /api/v1/annonces/` - Liste avec filtres
- `GET /api/v1/annonces/{id}` - Détails
- `POST /api/v1/annonces/` - Créer
- `PUT /api/v1/annonces/{id}` - Modifier
- `DELETE /api/v1/annonces/{id}` - Supprimer
- `POST /api/v1/annonces/{id}/images` - Upload images

#### Catégories
- `GET /api/v1/categories/` - Liste
- `GET /api/v1/categories/{id}` - Détails
- `POST /api/v1/categories/` - Créer
- `PUT /api/v1/categories/{id}` - Modifier

#### Messages
- `GET /api/v1/messages/` - Liste
- `GET /api/v1/messages/conversations` - Conversations
- `POST /api/v1/messages/` - Envoyer
- `PUT /api/v1/messages/{id}/read` - Marquer lu

#### Favoris
- `GET /api/v1/favorites/` - Liste
- `POST /api/v1/favorites/{annonce_id}` - Ajouter
- `DELETE /api/v1/favorites/{annonce_id}` - Retirer
- `GET /api/v1/favorites/check/{annonce_id}` - Vérifier

#### Reviews (Phase 2)
- `POST /api/v1/reviews/` - Créer un avis
- `GET /api/v1/reviews/user/{user_id}` - Avis d'un utilisateur
- `PUT /api/v1/reviews/{id}` - Modifier un avis
- `DELETE /api/v1/reviews/{id}` - Supprimer un avis

#### Alerts (Phase 2)
- `POST /api/v1/alerts/` - Créer une alerte
- `GET /api/v1/alerts/` - Mes alertes
- `PUT /api/v1/alerts/{id}` - Modifier une alerte
- `DELETE /api/v1/alerts/{id}` - Supprimer une alerte

#### Notifications (Phase 2)
- `GET /api/v1/notifications/` - Liste des notifications
- `PUT /api/v1/notifications/{id}/read` - Marquer comme lu
- `PUT /api/v1/notifications/mark-all-read` - Tout marquer comme lu

#### Boost (Phase 2)
- `GET /api/v1/boost/prices` - Prix des boosts
- `POST /api/v1/boost/` - Booster une annonce
- `POST /api/v1/boost/{id}/urgent` - Marquer urgent

#### Analytics (Phase 2)
- `POST /api/v1/analytics/views` - Tracker une vue
- `GET /api/v1/analytics/summary` - Résumé analytics
- `GET /api/v1/analytics/user/{id}` - Analytics utilisateur

#### Geolocation (Phase 2)
- `GET /api/v1/geolocation/nearby` - Recherche à proximité
- `GET /api/v1/geolocation/cities` - Villes populaires
- `GET /api/v1/geolocation/heatmap` - Données heatmap

#### Admin (Phase 2)
- `GET /api/v1/admin/stats/dashboard` - Stats dashboard
- `GET /api/v1/admin/users` - Liste utilisateurs
- `PUT /api/v1/admin/annonces/{id}/approve` - Approuver annonce

📘 **Documentation complète**: Voir [PHASE2_FEATURES.md](PHASE2_FEATURES.md)

## 🌍 Adaptations pour l'Afrique de l'Ouest

- **Devise**: FCFA (format français)
- **Langue**: Français (support multilingue prévu)
- **Mobile-first**: Interface optimisée pour mobile
- **Images optimisées**: Formats WebP, compression
- **Paiements**: Mobile Money (à implémenter)
- **Localisation**: Quartiers et zones spécifiques

## 🧪 Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

## 🚀 Déploiement

### Production avec Docker

```bash
# Build et démarrer
docker-compose -f docker-compose.prod.yml up -d

# Migrations de base de données
docker-compose exec backend alembic upgrade head
```

### Variables d'environnement en production

Assurez-vous de configurer :
- `SECRET_KEY` : Clé secrète forte et aléatoire
- `DATABASE_URL` : URL de la base de données PostgreSQL
- `BACKEND_CORS_ORIGINS` : Origines autorisées
- Identifiants Mobile Money (Phase 2)
- Configuration SMTP pour emails (Phase 2)

## 📄 License

Ce projet est sous licence MIT.

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📧 Contact

Pour toute question ou suggestion, veuillez ouvrir une issue sur GitHub.

---

Développé avec ❤️ pour l'Afrique de l'Ouest