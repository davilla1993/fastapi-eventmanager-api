# TASKS.md

## OBJECTIF

Développer une API publique de gestion d'événements culturels avec FastAPI, Pydantic v2 et PostgreSQL.

Le projet doit respecter l'architecture DDD Lite définie dans CLAUDE.md et PROJECT_RULES.md.

---

# PHASE 1 — INITIALISATION

## - [x] Tâche 1

Créer la structure du projet.

Livrables :

* app/
* modules/
* shared/
* infrastructure/
* tests/

Critère :

Le projet démarre correctement.

---

## - [x] Tâche 2

Configurer :

* FastAPI
* SQLAlchemy 2
* Alembic
* PostgreSQL
* Pydantic v2

Critère :

Connexion à PostgreSQL opérationnelle.

---

## - [x] Tâche 3

Configurer :

* Ruff
* Black
* MyPy
* Pytest

Critère :

Pipeline qualité fonctionnel.

---

# PHASE 2 — COUCHE SHARED

## - [x] Tâche 4

Créer BaseEntity.

Champs :

* id
* public_id
* created_at
* created_by
* updated_at
* updated_by
* deleted
* deleted_at
* deleted_by

Critère :

Toutes les entités héritent de BaseEntity.

---

## - [x] Tâche 5

Créer les exceptions métier communes.

Critère :

Exceptions centralisées.

---

## - [x] Tâche 6

Créer le système de pagination.

Critère :

Pagination réutilisable.

---

# PHASE 3 — TYPES PERSONNALISÉS

## - [x] Tâche 7

Implémenter :

* Slug
* URLImage
* CodePostalFR
* TelephoneE164
* IBAN

Critère :

Tous les validateurs fonctionnent.

---

## - [x] Tâche 8

Créer les serializers Pydantic v2.

Critère :

Sérialisation conforme.

---

## - [x] Tâche 9

Créer les tests unitaires des types.

Critère :

100 % des types testés.

---

## - [x] Tâche 10

Créer les tests Hypothesis.

Critère :

Tous les types couverts.

---

# PHASE 4 — AUTHENTIFICATION

## - [x] Tâche 11

Mettre en place JWT.

Critère :

Connexion fonctionnelle.

---

## - [x] Tâche 12

Créer les rôles :

* ADMIN
* ORGANIZER
* USER

Critère :

RBAC fonctionnel.

---

# PHASE 5 — MODULE ORGANIZERS

## - [x] Tâche 13

Créer l'entité Organizer.

Critère :

Migration générée.

---

## - [x] Tâche 14

Créer :

* Repository
* UseCases
* API

Critère :

CRUD complet.

---

# PHASE 6 — MODULE VENUES

## - [x] Tâche 15

Créer l'entité Venue.

Critère :

Migration générée.

---

## - [x] Tâche 16

Créer :

* Repository
* UseCases
* API

Critère :

CRUD complet.

---

# PHASE 7 — MODULE CATEGORIES

## - [x] Tâche 17

Créer l'entité Category.

Critère :

Migration générée.

---

## - [x] Tâche 18

Créer :

* Repository
* UseCases
* API

Critère :

CRUD complet.

---

# PHASE 8 — MODULE EVENTS

## - [ ] Tâche 19

Créer l'entité Event.

Critère :

Migration générée.

---

## - [ ] Tâche 20

Créer les schémas :

* Create
* Update
* Read
* ReadDetail

Critère :

Séparation stricte.

---

## - [ ] Tâche 21

Créer le polymorphisme :

* Concert
* Theatre
* Conference

Critère :

Discriminator Pydantic fonctionnel.

---

## - [ ] Tâche 22

Créer les UseCases.

Critère :

Aucune logique métier dans les routes.

---

## - [ ] Tâche 23

Créer les endpoints CRUD.

Critère :

CRUD complet.

---

## - [ ] Tâche 24

Créer les filtres avancés.

Filtres :

* catégorie
* organisateur
* ville
* date
* type d'événement

Critère :

Recherche fonctionnelle.

---

## - [ ] Tâche 25

Créer les tris.

Critère :

Tri ascendant et descendant.

---

## - [ ] Tâche 26

Créer la pagination.

Critère :

Pagination sur les listes.

---

# PHASE 9 — AUDIT ET LOGS

## - [ ] Tâche 27

Mettre en place les logs structurés.

Critère :

Logs JSON.

---

## - [ ] Tâche 28

Mettre en place l'audit.

Critère :

Traçabilité complète.

---

# PHASE 10 — DOCUMENTATION

## - [ ] Tâche 29

Ajouter des exemples OpenAPI.

Critère :

Swagger riche.

---

## - [ ] Tâche 30

Documenter tous les endpoints.

Critère :

Documentation complète.

---

# PHASE 11 — TESTS

## - [ ] Tâche 31

Tests unitaires.

Critère :

Couverture élevée.

---

## - [ ] Tâche 32

Tests d'intégration.

Critère :

Endpoints testés.

---

## - [ ] Tâche 33

Tests Hypothesis.

Critère :

Validation robuste.

---

# PHASE 12 — FINALISATION

## - [ ] Tâche 34

Dockeriser le projet.

Critère :

docker compose up fonctionne.

---

## - [ ] Tâche 35

Vérifier le respect du cahier des charges.

Critère :

100 % des exigences couvertes.

---

## - [ ] Tâche 36

Préparer la soutenance.

Critère :

Projet démontrable.
