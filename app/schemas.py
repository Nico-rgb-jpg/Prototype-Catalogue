from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Statut(str, Enum):
    en_cours = "en_cours"
    terminee = "terminee"
    annulee = "annulee"


class SerieBase(BaseModel):
    titre: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=50)
    annee: int = Field(ge=1900, le=2100, description="Année de sortie de la première saison")
    statut: Statut = Statut.en_cours
    nb_saisons: Optional[int] = Field(default=None, ge=1)
    synopsis: Optional[str] = Field(default=None, max_length=1000)


class SerieCreate(SerieBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "titre": "Stranger Things",
                "genre": "Science-fiction",
                "annee": 2016,
                "statut": "terminee",
                "nb_saisons": 5,
                "synopsis": "Des enfants enquêtent sur la disparition de leur ami dans une petite ville des années 80.",
            }
        }
    }


class SerieUpdate(BaseModel):
    """Pour le PATCH : tous les champs sont optionnels."""

    titre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    genre: Optional[str] = Field(default=None, min_length=1, max_length=50)
    annee: Optional[int] = Field(default=None, ge=1900, le=2100)
    statut: Optional[Statut] = None
    nb_saisons: Optional[int] = Field(default=None, ge=1)
    synopsis: Optional[str] = Field(default=None, max_length=1000)


class Serie(SerieBase):
    id: int


class Genre(BaseModel):
    genre: str
    nombre: int
