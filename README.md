# API Catalogue de séries

API REST développée avec **FastAPI** pour gérer un catalogue de séries TV.
Elle permet d'ajouter, consulter, modifier et supprimer des séries, avec des filtres sur le titre, le genre, l'année et le statut.

Projet réalisé dans le cadre de mon Bachelor à l'ESGI pour m'entraîner à la conception d'API.

> **Note :** je republie ce projet dans une nouvelle version. Les fichiers d'origine ont été perdus ou étaient devenus obsolètes, je l'ai donc repris et mis à jour.

## Technologies

- Python 3.10+
- FastAPI (routes, validation, documentation automatique)
- Pydantic (modèles de données et validation)
- SQLite (module `sqlite3` de Python, requêtes SQL écrites à la main)
- pytest (tests)

## Installation

```bash
git clone https://github.com/<pseudo>/api-catalogue-series.git
cd api-catalogue-series

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Lancement

```bash
uvicorn app.main:app --reload
```

L'API est disponible sur http://127.0.0.1:8000.
Au premier lancement, la base `series.db` est créée et remplie avec 19 séries d'exemple.

La documentation Swagger est accessible sur http://127.0.0.1:8000/docs : on peut tester toutes les routes directement depuis le navigateur.

## Routes

| Méthode | Route | Description |
|---|---|---|
| GET | `/series` | Liste des séries (avec filtres, tri et pagination) |
| GET | `/series/{id}` | Détail d'une série |
| POST | `/series` | Ajouter une série |
| PUT | `/series/{id}` | Remplacer une série |
| PATCH | `/series/{id}` | Modifier certains champs |
| DELETE | `/series/{id}` | Supprimer une série |
| GET | `/genres` | Liste des genres avec le nombre de séries |

### Filtres disponibles sur `GET /series`

| Paramètre | Exemple | Effet |
|---|---|---|
| `titre` | `?titre=break` | recherche partielle dans le titre |
| `genre` | `?genre=Drame` | genre exact (majuscules ignorées) |
| `statut` | `?statut=terminee` | `en_cours`, `terminee` ou `annulee` |
| `annee_min` / `annee_max` | `?annee_min=2015&annee_max=2020` | période de sortie |
| `tri` / `ordre` | `?tri=annee&ordre=desc` | tri par `titre`, `annee` ou `id` |
| `limit` / `offset` | `?limit=10&offset=10` | pagination (page 2 de 10 résultats) |

Le nombre total de résultats est renvoyé dans l'en-tête `X-Total-Count`.

### Exemple

```bash
curl -X POST http://127.0.0.1:8000/series \
  -H "Content-Type: application/json" \
  -d '{"titre": "Stranger Things", "genre": "Science-fiction", "annee": 2016, "statut": "terminee", "nb_saisons": 5}'
```

```json
{
  "titre": "Stranger Things",
  "genre": "Science-fiction",
  "annee": 2016,
  "statut": "terminee",
  "nb_saisons": 5,
  "synopsis": null,
  "id": 20
}
```

### Codes de réponse

- `200` : OK
- `201` : série créée
- `204` : série supprimée
- `404` : série introuvable
- `409` : une série avec ce titre existe déjà
- `422` : données invalides (champ manquant, année hors limites, statut inconnu…)

## Tests

```bash
python -m pytest
```

29 tests couvrent toutes les routes : cas normaux, filtres, pagination et cas d'erreur (404, 409, 422).
Chaque test utilise une base temporaire, la base principale n'est jamais modifiée.

## Organisation du code

```
app/
├── main.py          création de l'application, ajout des routes
├── database.py      connexion SQLite et création de la table
├── schemas.py       modèles Pydantic (validation des données)
├── crud.py          requêtes SQL
├── routes/
│   ├── series.py    routes /series
│   └── genres.py    route /genres
└── data/
    └── series.json  données d'exemple
tests/
├── conftest.py      fixtures pytest (client de test, base temporaire)
└── test_series.py
```

## Améliorations possibles

- Authentification (clé d'API ou JWT) pour protéger les routes d'écriture
- Ajouter les saisons et épisodes dans des tables séparées
- Passer à PostgreSQL et SQLAlchemy
