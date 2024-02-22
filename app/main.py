from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor
# Databases
from . import models
from .database import engine
from app.routers import posts, users, auth, votes


# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "*"
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "Hello World!"}

@app.get("/check", status_code=status.HTTP_200_OK)
def check():
    """Checks the heath of the API, if ok, returns OK"""
    return {"message": "OK"}

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

