import json
import os
import sqlite3
from pathlib import Path

# Chemin de la base, modifiable avec une variable d'environnement (utile pour les tests)
DB_PATH = os.getenv("DB_PATH", "series.db")
DONNEES_INITIALES = Path(__file__).parent / "data" / "series.json"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # pour accéder aux colonnes par leur nom
    return conn


def get_db():
    """Dépendance FastAPI : ouvre une connexion pour la requête puis la ferme."""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db(avec_donnees=True):
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL UNIQUE,
            genre TEXT NOT NULL,
            annee INTEGER NOT NULL,
            statut TEXT NOT NULL DEFAULT 'en_cours',
            nb_saisons INTEGER,
            synopsis TEXT
        )
        """
    )

    # On remplit la table seulement si elle est vide
    nb = conn.execute("SELECT COUNT(*) FROM series").fetchone()[0]
    if nb == 0 and avec_donnees:
        with open(DONNEES_INITIALES, encoding="utf-8") as f:
            series = json.load(f)
        conn.executemany(
            """
            INSERT INTO series (titre, genre, annee, statut, nb_saisons, synopsis)
            VALUES (:titre, :genre, :annee, :statut, :nb_saisons, :synopsis)
            """,
            series,
        )

    conn.commit()
    conn.close()
