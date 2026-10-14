from fastapi import FastAPI

app = FastAPI(title="API Catalogue de séries")


@app.get("/")
def accueil():
    return {"message": "API Catalogue de séries", "documentation": "/docs"}
