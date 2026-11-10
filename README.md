# Académie de Diplomatie

Plateforme de formation en Relations internationales, Diplomatie et Science politique.

## Technologies
- Python et Flask
- PostgreSQL avec Psycopg 3
- Flask-SQLAlchemy et Flask-Migrate
- Flask-Login et Flask-WTF (protection CSRF)

## Installation locale

1. Créer et activer l'environnement virtuel.
2. Installer les dépendances : `python -m pip install -r requirements.txt`
3. Copier `.env.example` vers `.env` : `copy .env.example .env`
4. Modifier `.env` localement avec une clé secrète et le mot de passe PostgreSQL.
5. Appliquer les migrations : `flask db upgrade`
6. Créer les rôles : `flask seed-roles`
7. Créer votre compte administrateur : `flask create-admin`
8. Lancer : `python run.py`

Ne jamais publier ou transmettre le fichier `.env`.

## Ce qui fonctionne
- Inscription (rôle « apprenant » attribué automatiquement), connexion, « Se souvenir de moi », déconnexion (POST + CSRF).
- Espace apprenant protégé (`/espace-apprenant`).
- Tableau de bord administrateur (`/admin/`) réservé au rôle `admin` : liste des utilisateurs.
- Pages d'erreur 400, 403, 404 et 500.
- Mots de passe hachés, redirection `next` limitée aux chemins internes, cookies HttpOnly/SameSite.

## Pages et routes
| URL | Description |
|---|---|
| `/` | Accueil |
| `/formations` | Catalogue (cartes à compléter à la main dans `frontend/formations.html`) |
| `/inscription`, `/connexion`, `/deconnexion` | Authentification |
| `/espace-apprenant` | Espace de l'apprenant (connexion requise) |
| `/admin/` | Administration (rôle `admin`) |

## Tests
`python -m pip install -r requirements-dev.txt` puis `python -m pytest`
(les tests utilisent SQLite en mémoire, aucune base PostgreSQL n'est nécessaire).

## Pas encore réalisé
- Modèle de formations, inscriptions aux cours et paiements (`app/routes/payments/` est vide) : les cartes du catalogue restent à saisir par vos soins.
- Mot de passe oublié et vérification de l'adresse e-mail (nécessitent un envoi d'e-mails).
- Limitation du nombre de tentatives de connexion (par exemple avec Flask-Limiter).

## Production
Mettre `FLASK_DEBUG=0` et `SESSION_COOKIE_SECURE=1` dans `.env`, et servir l'application avec un serveur WSGI (gunicorn, waitress) derrière HTTPS.
