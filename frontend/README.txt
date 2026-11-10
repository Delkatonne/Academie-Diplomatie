ACADEMIE DE DIPLOMATIE — FRONTEND

Les fichiers HTML de ce dossier sont des modèles Jinja rendus par Flask : ils ne s'ouvrent plus
en double-cliquant dessus. Lancez le serveur (python run.py) puis ouvrez http://127.0.0.1:5000

Contenu :
- index.html : page d'accueil
- formations.html : catalogue avec recherche et filtre (cartes de formation à remplacer par les vôtres)
- connexion.html, inscription.html : formulaires reliés à Flask (validation, CSRF)
- espace-apprenant.html : espace de l'apprenant (connexion requise)
- admin-tableau-de-bord.html : liste des utilisateurs (rôle admin)
- erreur.html : pages d'erreur
- _nav_actions.html, _flash.html, _macros.html : morceaux réutilisés par les pages
- css/style.css, js/app.js : styles et scripts

Pour ajouter une formation : dans formations.html, dupliquez un bloc <article class="course-card" ...>
et modifiez son texte, sa catégorie (data-category) et sa couleur de couverture (cover-blue, cover-green, cover-gold).
