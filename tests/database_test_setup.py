from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
# Load .env file
# load_doteng(".env_file_name") # Loadding secific .env file
from app.database import get_db, Base 
import pytest
from alembic import command

load_dotenv()



SQLALCHEMY_DATABASE_URL = "postgresql://miclem:1234@localhost/fastapi_test"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
# Talk to the datbase
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

