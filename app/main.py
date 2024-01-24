from fastapi import FastAPI, status
from psycopg2.extras import RealDictCursor
# Databases
from . import models
from .database import engine
from app.routers import posts, users, auth


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/check", status_code=status.HTTP_200_OK)
def index():
    """Checks the heath of the API, if ok, returns OK"""
    return {"message": "OK"}

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

