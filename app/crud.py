"""Fonctions d'accès à la base de données pour les séries."""

import sqlite3

COLONNES = ["titre", "genre", "annee", "statut", "nb_saisons", "synopsis"]


def ligne_vers_dict(ligne):
    return dict(ligne) if ligne else None


def lister_series(conn):
    lignes = conn.execute("SELECT * FROM series ORDER BY titre").fetchall()
    return [dict(l) for l in lignes]


def get_serie(conn, serie_id):
    ligne = conn.execute("SELECT * FROM series WHERE id = ?", (serie_id,)).fetchone()
    return ligne_vers_dict(ligne)


def creer_serie(conn, donnees):
    """Renvoie la série créée, ou None si le titre existe déjà."""
    try:
        cur = conn.execute(
            """
            INSERT INTO series (titre, genre, annee, statut, nb_saisons, synopsis)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [donnees[c] for c in COLONNES],
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return None
    return get_serie(conn, cur.lastrowid)


def modifier_serie(conn, serie_id, donnees):
    """Met à jour seulement les champs présents dans `donnees`."""
    champs = [c for c in COLONNES if c in donnees]
    if champs:
        sql = "UPDATE series SET " + ", ".join(f"{c} = ?" for c in champs) + " WHERE id = ?"
        conn.execute(sql, [donnees[c] for c in champs] + [serie_id])
        conn.commit()
    return get_serie(conn, serie_id)


def supprimer_serie(conn, serie_id):
    cur = conn.execute("DELETE FROM series WHERE id = ?", (serie_id,))
    conn.commit()
    return cur.rowcount > 0


def titre_existe(conn, titre, sauf_id=None):
    ligne = conn.execute(
        "SELECT id FROM series WHERE LOWER(titre) = LOWER(?) AND id != ?",
        (titre, sauf_id or 0),
    ).fetchone()
    return ligne is not None
