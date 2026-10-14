import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Chaque test utilise sa propre base temporaire, remplie avec les données d'exemple
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    with TestClient(app) as c:
        yield c


@pytest.fixture
def nouvelle_serie():
    return {
        "titre": "Stranger Things",
        "genre": "Science-fiction",
        "annee": 2016,
        "statut": "terminee",
        "nb_saisons": 5,
        "synopsis": "Des enfants enquêtent sur des phénomènes étranges dans leur ville.",
    }
