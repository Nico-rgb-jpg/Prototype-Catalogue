from typing import List

from fastapi import APIRouter, Depends

from app import crud
from app.database import get_db
from app.schemas import Genre

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("", response_model=List[Genre], summary="Lister les genres et leur nombre de séries")
def lister_genres(conn=Depends(get_db)):
    return crud.lister_genres(conn)
