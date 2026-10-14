from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app import crud
from app.database import get_db
from app.schemas import Serie, SerieCreate, SerieUpdate

router = APIRouter(prefix="/series", tags=["Séries"])


def serie_ou_404(conn, serie_id):
    serie = crud.get_serie(conn, serie_id)
    if serie is None:
        raise HTTPException(status_code=404, detail="Série introuvable")
    return serie


@router.get("", response_model=List[Serie], summary="Lister les séries")
def lister_series(conn=Depends(get_db)):
    return crud.lister_series(conn)


@router.get("/{serie_id}", response_model=Serie, summary="Détail d'une série")
def detail_serie(serie_id: int, conn=Depends(get_db)):
    return serie_ou_404(conn, serie_id)


@router.post("", response_model=Serie, status_code=status.HTTP_201_CREATED, summary="Ajouter une série")
def ajouter_serie(serie: SerieCreate, conn=Depends(get_db)):
    if crud.titre_existe(conn, serie.titre):
        raise HTTPException(status_code=409, detail="Une série avec ce titre existe déjà")
    return crud.creer_serie(conn, serie.model_dump(mode="json"))


@router.put("/{serie_id}", response_model=Serie, summary="Remplacer une série")
def remplacer_serie(serie_id: int, serie: SerieCreate, conn=Depends(get_db)):
    serie_ou_404(conn, serie_id)
    if crud.titre_existe(conn, serie.titre, sauf_id=serie_id):
        raise HTTPException(status_code=409, detail="Une série avec ce titre existe déjà")
    return crud.modifier_serie(conn, serie_id, serie.model_dump(mode="json"))


@router.patch("/{serie_id}", response_model=Serie, summary="Modifier une partie d'une série")
def modifier_serie(serie_id: int, serie: SerieUpdate, conn=Depends(get_db)):
    serie_ou_404(conn, serie_id)
    # exclude_unset : on ne garde que les champs envoyés par le client
    donnees = serie.model_dump(mode="json", exclude_unset=True)
    for champ in ["titre", "genre", "annee", "statut"]:
        if champ in donnees and donnees[champ] is None:
            raise HTTPException(status_code=422, detail=f"Le champ '{champ}' ne peut pas être vide")
    if "titre" in donnees and crud.titre_existe(conn, donnees["titre"], sauf_id=serie_id):
        raise HTTPException(status_code=409, detail="Une série avec ce titre existe déjà")
    return crud.modifier_serie(conn, serie_id, donnees)


@router.delete("/{serie_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer une série")
def supprimer_serie(serie_id: int, conn=Depends(get_db)):
    if not crud.supprimer_serie(conn, serie_id):
        raise HTTPException(status_code=404, detail="Série introuvable")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
