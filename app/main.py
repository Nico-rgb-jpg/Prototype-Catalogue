from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes import genres, series


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Création de la table (et des données d'exemple) au démarrage
    init_db()
    yield


app = FastAPI(
    title="API Catalogue de séries",
    description="API REST pour gérer un catalogue de séries : ajout, consultation, modification et suppression.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(series.router)
app.include_router(genres.router)


@app.get("/", tags=["Accueil"])
def accueil():
    return {"message": "API Catalogue de séries", "documentation": "/docs"}
