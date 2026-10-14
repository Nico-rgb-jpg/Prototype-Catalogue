def test_accueil(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["documentation"] == "/docs"


# ---------- GET /series ----------

def test_lister_series(client):
    r = client.get("/series")
    assert r.status_code == 200
    assert len(r.json()) == 19
    assert r.headers["X-Total-Count"] == "19"


def test_lister_series_triees_par_titre(client):
    titres = [s["titre"] for s in client.get("/series?limit=100").json()]
    assert titres == sorted(titres)


def test_recherche_par_titre(client):
    r = client.get("/series", params={"titre": "BREAK"})
    assert [s["titre"] for s in r.json()] == ["Breaking Bad"]


def test_filtre_genre(client):
    r = client.get("/series", params={"genre": "animation"})
    assert len(r.json()) == 3
    assert all(s["genre"] == "Animation" for s in r.json())


def test_filtre_statut(client):
    r = client.get("/series", params={"statut": "annulee"})
    assert {s["titre"] for s in r.json()} == {"Firefly", "Mindhunter"}


def test_filtre_annees(client):
    r = client.get("/series", params={"annee_min": 2020, "annee_max": 2022})
    assert all(2020 <= s["annee"] <= 2022 for s in r.json())
    assert len(r.json()) == 3


def test_filtres_combines(client):
    r = client.get("/series", params={"genre": "Drame", "statut": "terminee"})
    assert len(r.json()) == 3


def test_tri_par_annee_decroissant(client):
    annees = [s["annee"] for s in client.get("/series?tri=annee&ordre=desc&limit=100").json()]
    assert annees == sorted(annees, reverse=True)


def test_pagination(client):
    page1 = client.get("/series?limit=5&offset=0").json()
    page2 = client.get("/series?limit=5&offset=5").json()
    assert len(page1) == 5 and len(page2) == 5
    assert not {s["id"] for s in page1} & {s["id"] for s in page2}


def test_parametres_invalides(client):
    assert client.get("/series?statut=inconnu").status_code == 422
    assert client.get("/series?tri=synopsis").status_code == 422
    assert client.get("/series?limit=500").status_code == 422


def test_aucun_resultat(client):
    r = client.get("/series", params={"titre": "zzzz"})
    assert r.status_code == 200
    assert r.json() == []


# ---------- GET /series/{id} ----------

def test_detail_serie(client):
    r = client.get("/series/1")
    assert r.status_code == 200
    assert r.json()["titre"] == "Breaking Bad"


def test_detail_serie_inexistante(client):
    r = client.get("/series/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Série introuvable"


# ---------- POST /series ----------

def test_ajouter_serie(client, nouvelle_serie):
    r = client.post("/series", json=nouvelle_serie)
    assert r.status_code == 201
    data = r.json()
    assert data["id"] == 20
    assert data["titre"] == "Stranger Things"
    # elle doit ensuite être retrouvable
    assert client.get(f"/series/{data['id']}").status_code == 200


def test_ajouter_serie_statut_par_defaut(client):
    r = client.post("/series", json={"titre": "Test", "genre": "Drame", "annee": 2020})
    assert r.status_code == 201
    assert r.json()["statut"] == "en_cours"


def test_ajouter_serie_titre_deja_pris(client, nouvelle_serie):
    nouvelle_serie["titre"] = "breaking bad"
    r = client.post("/series", json=nouvelle_serie)
    assert r.status_code == 409


def test_ajouter_serie_invalide(client):
    r = client.post("/series", json={"titre": "", "genre": "Drame", "annee": 1800, "statut": "bof"})
    assert r.status_code == 422
    champs_en_erreur = {e["loc"][-1] for e in r.json()["detail"]}
    assert champs_en_erreur == {"titre", "annee", "statut"}


def test_ajouter_serie_champ_manquant(client):
    r = client.post("/series", json={"titre": "Sans genre", "annee": 2020})
    assert r.status_code == 422


# ---------- PUT /series/{id} ----------

def test_remplacer_serie(client, nouvelle_serie):
    r = client.put("/series/1", json=nouvelle_serie)
    assert r.status_code == 200
    assert r.json()["titre"] == "Stranger Things"
    assert r.json()["id"] == 1


def test_remplacer_serie_inexistante(client, nouvelle_serie):
    assert client.put("/series/999", json=nouvelle_serie).status_code == 404


def test_remplacer_avec_titre_existant(client, nouvelle_serie):
    nouvelle_serie["titre"] = "Dark"
    assert client.put("/series/1", json=nouvelle_serie).status_code == 409


# ---------- PATCH /series/{id} ----------

def test_modifier_un_champ(client):
    r = client.patch("/series/4", json={"nb_saisons": 3})
    assert r.status_code == 200
    assert r.json()["nb_saisons"] == 3
    assert r.json()["titre"] == "The Last of Us"  # le reste ne change pas


def test_modifier_statut(client):
    r = client.patch("/series/4", json={"statut": "terminee"})
    assert r.json()["statut"] == "terminee"


def test_modifier_avec_titre_vide(client):
    assert client.patch("/series/1", json={"titre": None}).status_code == 422


def test_modifier_serie_inexistante(client):
    assert client.patch("/series/999", json={"genre": "Drame"}).status_code == 404


# ---------- DELETE /series/{id} ----------

def test_supprimer_serie(client):
    r = client.delete("/series/1")
    assert r.status_code == 204
    assert client.get("/series/1").status_code == 404
    assert client.get("/series").headers["X-Total-Count"] == "18"


def test_supprimer_serie_inexistante(client):
    assert client.delete("/series/999").status_code == 404


# ---------- GET /genres ----------

def test_lister_genres(client):
    r = client.get("/genres")
    assert r.status_code == 200
    genres = {g["genre"]: g["nombre"] for g in r.json()}
    assert genres["Drame"] == 4
    assert genres["Animation"] == 3
    assert sum(genres.values()) == 19
