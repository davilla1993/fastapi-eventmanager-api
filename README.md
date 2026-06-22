# Event Management API

API publique de gestion d'événements culturels — Projet d'évaluation finale  
**Master 1 Intelligence Artificielle & Big Data**

> **Démo en ligne**
> - Swagger UI : [https://events-api.gfolly.com/docs](https://events-api.gfolly.com/docs)
> - ReDoc : [https://events-api.gfolly.com/redoc](https://events-api.gfolly.com/redoc)
> - Health check : [https://events-api.gfolly.com/health](https://events-api.gfolly.com/health)

---

## Présentation

Plateforme REST permettant de gérer des **concerts**, **pièces de théâtre** et **conférences** avec une validation rigoureuse des données, une authentification JWT et un audit trail automatique.

### Stack technique

| Composant | Technologie |
|---|---|
| Framework | FastAPI 0.115+ |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2 (async) |
| Base de données | PostgreSQL |
| Migrations | Alembic |
| Driver async | asyncpg |
| Auth | JWT (python-jose) + bcrypt |
| Tests | pytest + pytest-asyncio + Hypothesis |
| Qualité | Ruff · Black · MyPy (strict) |

---

## Architecture

Le projet suit une architecture **DDD Lite** organisée en modules métier indépendants, chacun découpé en quatre couches :

```
app/
├── modules/
│   ├── iam/            # Authentification & gestion des rôles
│   ├── events/         # Événements (Concert, Théâtre, Conférence)
│   ├── organizers/     # Organisateurs
│   ├── venues/         # Salles et lieux
│   └── categories/     # Catégories thématiques
│
├── shared/             # Types, pagination, exceptions communes
│   ├── types/          # Types personnalisés Pydantic v2
│   ├── pagination/
│   └── exceptions/
│
└── infrastructure/     # Config, BDD, sécurité, logs
    ├── database/
    ├── security/
    └── logging/

tests/
├── unit/               # Tests unitaires (types, domain)
├── integration/        # Tests des endpoints HTTP
└── property/           # Tests property-based (Hypothesis)
```

### Règle de dépendances

```
api → application → domain
          ↑
    infrastructure
```

La couche `domain` ne dépend d'aucune autre couche.

---

## Fonctionnalités

### Types Pydantic v2 personnalisés

| Type | Validation |
|---|---|
| `Slug` | Chaîne URL-friendly : minuscules, chiffres, tirets |
| `CodePostalFR` | Exactement 5 chiffres |
| `TelephoneE164` | Format international E.164 (`+33612345678`) |
| `URLImage` | URL HTTPS avec extension `jpg`, `jpeg`, `png` ou `webp` |
| `IBAN` | IBAN européen validé (longueur + checksum) |

### Polymorphisme des événements

Un événement est discriminé par le champ `event_type` :

- **Concert** — champs `artist`, `genre`
- **Théâtre** — champs `director`, `cast_members`
- **Conférence** — champs `speaker`, `topic`

### Authentification & RBAC

| Rôle | Permissions |
|---|---|
| `USER` | Lecture de toutes les ressources publiques |
| `ORGANIZER` | USER + création/modification de ses événements, salles, profil |
| `ADMIN` | ORGANIZER + gestion des catégories, accès complet |

### Filtres avancés sur les événements

```
GET /api/v1/events?city=Paris&event_type=concert&price_max=50&tags=jazz,bebop&sort_by=start_at&sort_order=asc
```

### Audit trail

Chaque opération d'écriture est tracée : auteur, timestamp, action. Logs structurés JSON.

---

## Installation locale

### Prérequis

- Python ≥ 3.13
- PostgreSQL ≥ 15
- `uv` ou `pip`

### Étapes

```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd eventmanagement-project

# 2. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 3. Installer les dépendances
pip install -e ".[dev]"

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs (DATABASE_URL, SECRET_KEY)

# 5. Appliquer les migrations
alembic upgrade head

# 6. Lancer le serveur
uvicorn app.main:app --reload
```

L'API est disponible sur `http://localhost:8000`  
Documentation interactive : `http://localhost:8000/docs`

### Variables d'environnement

| Variable | Description | Exemple |
|---|---|---|
| `DATABASE_URL` | URL PostgreSQL async | `postgresql+asyncpg://user:pass@localhost:5432/eventdb` |
| `SECRET_KEY` | Clé secrète JWT (aléatoire, ≥ 32 chars) | `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ALGORITHM` | Algorithme JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Durée de vie du token | `30` |
| `DEBUG` | Mode debug | `false` |

---

## Déploiement Docker

```bash
# Copier les variables d'environnement
cp .env.example .env
# Éditer .env : renseigner SECRET_KEY (les autres ont des valeurs par défaut)

# Démarrer l'API + PostgreSQL
docker compose up --build
```

L'API est disponible sur `http://localhost:8000`. Les migrations sont appliquées automatiquement au démarrage.

Le `CMD` du Dockerfile exécute automatiquement `alembic upgrade head` avant de démarrer uvicorn.

---

## Exemples d'appels API

### 1. Créer un compte

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123",
    "full_name": "Carlo Admin"
  }'
```

### 2. Se connecter et récupérer un token

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password123"}'
```

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Créer une catégorie (ADMIN)

```bash
curl -X POST http://localhost:8000/api/v1/categories \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jazz", "slug": "jazz", "color": "#F59E0B"}'
```

### 4. Créer un concert (ORGANIZER / ADMIN)

```bash
curl -X POST http://localhost:8000/api/v1/events \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "concert",
    "title": "Jazz Festival Lome 2025",
    "slug": "jazz-festival-lome-2025",
    "start_at": "2025-07-14T20:00:00+02:00",
    "end_at": "2025-07-14T23:30:00+02:00",
    "city": "Lome",
    "price": "45.00",
    "capacity": 500,
    "venue_public_id": "<uuid>",
    "organizer_public_id": "<uuid>",
    "artist": "Ibrahim Maalouf",
    "genre": "Jazz contemporain"
  }'
```

### 5. Rechercher des événements avec filtres

```bash
curl "http://localhost:8000/api/v1/events?city=Lome&event_type=concert&price_max=50&tags=jazz&page=1&size=10"
```

---

## Tests

### Prérequis

Le fichier `.env` doit pointer vers une base PostgreSQL accessible et les migrations doivent être appliquées :

```bash
alembic upgrade head
```

### Commandes

```bash
# Tous les tests avec couverture (terminal)
pytest

# Lignes non couvertes détaillées
pytest --cov=app --cov-report=term-missing

# Rapport HTML navigable
pytest --cov=app --cov-report=html
# → ouvrir htmlcov/index.html dans le navigateur

# Rapport XML (CI / Codecov)
pytest --cov=app --cov-report=xml

# Par dossier
pytest tests/unit/
pytest tests/integration/
pytest tests/property/

# Un fichier précis avec sortie détaillée
pytest tests/integration/test_event_endpoints.py -v
```

Le seuil de couverture minimum est configuré à **80 %** dans `pyproject.toml`. En dessous de ce seuil, `pytest` retourne une erreur.

---

## Endpoints

| Méthode | Route | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | — | Créer un compte |
| `POST` | `/api/v1/auth/login` | — | Obtenir un token JWT |
| `GET` | `/api/v1/auth/me` | JWT | Profil connecté |
| `GET` | `/api/v1/events` | — | Lister les événements (filtres + pagination) |
| `POST` | `/api/v1/events` | ORGANIZER / ADMIN | Créer un événement |
| `GET` | `/api/v1/events/{id}` | — | Détail d'un événement |
| `PATCH` | `/api/v1/events/{id}` | ORGANIZER / ADMIN | Modifier un événement |
| `DELETE` | `/api/v1/events/{id}` | JWT | Supprimer un événement |
| `GET` | `/api/v1/venues` | — | Lister les salles |
| `POST` | `/api/v1/venues` | ORGANIZER / ADMIN | Créer une salle |
| `GET` | `/api/v1/venues/{id}` | — | Détail d'une salle |
| `PATCH` | `/api/v1/venues/{id}` | ORGANIZER / ADMIN | Modifier une salle |
| `DELETE` | `/api/v1/venues/{id}` | JWT | Supprimer une salle |
| `GET` | `/api/v1/organizers` | — | Lister les organisateurs |
| `POST` | `/api/v1/organizers` | ORGANIZER / ADMIN | Créer un organisateur |
| `GET` | `/api/v1/organizers/{id}` | — | Détail d'un organisateur |
| `PATCH` | `/api/v1/organizers/{id}` | JWT | Modifier un organisateur |
| `DELETE` | `/api/v1/organizers/{id}` | JWT | Supprimer un organisateur |
| `GET` | `/api/v1/categories` | — | Lister les catégories |
| `POST` | `/api/v1/categories` | ADMIN | Créer une catégorie |
| `GET` | `/api/v1/categories/{id}` | — | Détail d'une catégorie |
| `PATCH` | `/api/v1/categories/{id}` | ADMIN | Modifier une catégorie |
| `DELETE` | `/api/v1/categories/{id}` | ADMIN | Supprimer une catégorie |
| `GET` | `/health` | — | État du serveur |

Documentation OpenAPI complète : `/docs` (Swagger UI) · `/redoc` (ReDoc)

---

## Collection Postman

Une collection Postman complète est disponible dans `docs/EventManagement.postman_collection.json`.

Elle inclut les 24 routes organisées par module, avec :
- Sauvegarde automatique du token JWT après login
- Sauvegarde automatique des `public_id` après chaque création
- Tous les paramètres de filtres pré-configurés (désactivés par défaut)

---

## Auteur

**Folly S. Carlo GBOSSOU** — Master 1 Intelligence Artificielle & Big Data  
carlogbossou93@gmail.com