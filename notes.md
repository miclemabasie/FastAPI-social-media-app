# FastAPI Library

## ORMs

We use ORMs so that we can manage the database using regular python syntax

## SQLALCHEMY

Sqlalchemy is one of the most popular python ORMs
It is a standalone library and has no association with FastAPI. it can be used with any other python web framework or any python based application [readmore](https://docs.sqlalchemy.org/)
Basic configuration for sqlalchey with fastapi

````from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connect string -> where is the database located that needs to be used
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "postgresql://miclem:1234@localhost/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Talk to the datbase
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()```
````

The above configuration is used to connect to a postgresql database

Net we need to specify our database tables in the form of python classes (Models)
In this case we define a model for the post table with all it's attributes

```
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, default=True)
```
