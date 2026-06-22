from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.logging.request_middleware import RequestLoggingMiddleware
from app.infrastructure.logging.setup import setup_logging
from app.modules.categories.api.controllers.category_controller import (
    router as category_router,
)
from app.modules.events.api.controllers.event_controller import router as event_router
from app.modules.iam.api.controllers.auth_controller import router as auth_router
from app.modules.organizers.api.controllers.organizer_controller import (
    router as organizer_router,
)
from app.modules.venues.api.controllers.venue_controller import router as venue_router
from app.settings import settings
from app.shared.exceptions import AppException, app_exception_handler

setup_logging(level="INFO")

_DESCRIPTION = """
## API publique de gestion d'événements culturels

Plateforme permettant de gérer des **concerts**, **pièces de théâtre** et **conférences**
avec validation rigoureuse des données via des types Pydantic v2 personnalisés.

### Fonctionnalités principales

- 🎭 **Événements polymorphes** : Concert, Théâtre, Conférence (discriminator Pydantic)
- 🏛️ **Salles** (Venues) avec localisation et capacité
- 🎪 **Organisateurs** liés à des comptes utilisateurs
- 🏷️ **Catégories** avec couleur hexadécimale
- 🔐 **Authentification JWT** avec RBAC (ADMIN, ORGANIZER, USER)
- 🔍 **Filtres avancés** sur les événements (ville, date, prix, tags, type)
- 📑 **Pagination** sur toutes les listes
- 📋 **Audit trail** automatique sur les opérations d'écriture

### Types personnalisés

| Type | Description |
|---|---|
| `Slug` | Identifiant URL-friendly (ex: `jazz-festival-2025`) |
| `CodePostalFR` | Code postal français 5 chiffres |
| `TelephoneE164` | Numéro E.164 (ex: `+22890123456`) |
| `URLImage` | URL HTTPS avec extension jpg/jpeg/png/webp |
| `IBAN` | IBAN européen validé |

### Authentification

Utiliser `POST /api/v1/auth/login` pour obtenir un token JWT,
puis l'inclure dans le header : `Authorization: Bearer <token>`
"""

_TAGS_METADATA = [
    {
        "name": "Auth",
        "description": "Inscription, connexion et profil utilisateur.",
    },
    {
        "name": "Events",
        "description": (
            "Gestion des événements culturels. Polymorphisme : **Concert**, "
            "**Théâtre**, **Conférence**. Filtres avancés, tri et pagination."
        ),
    },
    {
        "name": "Venues",
        "description": "Salles de spectacle et lieux d'accueil des événements.",
    },
    {
        "name": "Organizers",
        "description": "Organisateurs responsables des événements.",
    },
    {
        "name": "Categories",
        "description": "Catégories thématiques des événements (réservé ADMIN).",
    },
    {
        "name": "health",
        "description": "Vérification de l'état du serveur.",
    },
]

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=_DESCRIPTION,
    contact={
        "name": "Carlo — Master 1 IA BIG DATA",
        "email": "carlogbossou93@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=_TAGS_METADATA,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]

app.include_router(auth_router, prefix="/api/v1")
app.include_router(organizer_router, prefix="/api/v1")
app.include_router(venue_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(event_router, prefix="/api/v1")


@app.get("/health", tags=["health"], summary="État du serveur")
async def health_check() -> dict[str, str]:
    """Retourne le statut et la version de l'API."""
    return {"status": "ok", "version": settings.app_version}