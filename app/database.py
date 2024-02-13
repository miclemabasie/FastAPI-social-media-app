from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# Load .env file
# load_doteng(".env_file_name") # Loadding secific .env file


# connect string -> where is the database located that needs to be used
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
print(os.getenv("DB_URL"))
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:fBA*6EE6bBdAbDa*5B5AG*FA1ggc32c2@viaduct.proxy.rlwy.net:51086/railway"

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # used only for sqlite
    SQLALCHEMY_DATABASE_URL
)
# Talk to the datbase
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
