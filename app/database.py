from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
# Load .env file
# load_doteng(".env_file_name") # Loadding secific .env file


load_dotenv()

# connect string -> where is the database located that needs to be used
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# check if app is in production

# Get the online var and convert to int
print("new is online var", os.getenv('IS_ONLINE'))
IS_ONLINE = int(os.getenv('IS_ONLINE'))

if IS_ONLINE:
    print("Using an online database")
    SQLALCHEMY_DATABASE_URL = os.getenv('DB_URL')
else:
    print("Using local database")
    SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOSTNAME')}/{os.getenv('DATABASE_NAME')}"

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
