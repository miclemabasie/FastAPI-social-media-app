from .database_test_setup import *
from app.utils import custom_password_hash
from jose import JWTError, jwt
from app.oauth2 import create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta, datetime


SQLALCHEMY_DATABASE_URL = "postgresql://miclem:1234@localhost/fastapi_test"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
# Talk to the datbase
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close() 

@pytest.fixture(scope="function")
def client(session):
    def overide_get_db():
        try:
            yield session
        finally:
            session.close()

    # using alembic to create tables during test
    # instead of sqlalchemy
    # command.upgrade("head")
    app.dependency_overrides[get_db] = overide_get_db
    yield TestClient(app)
    # command.downgrade("base")


@pytest.fixture
def test_user(client, session):
    data = {
        "username": "miclem",
        "email": "miclem1@mail.com",
        "password": "12345",
        "password_repeat": "12345"
    }
    response = client.post("/users", json=data)
    assert response.status_code == 201
    # update the response with the password
    res = response.json()
    res.update({"password": data["password"]})
    return res

# login fixture
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_create_post(authorized_client, test_user):
    print("Creating post")
    posts_data = [
        {
            "title": "Python for noobs",
            "content": "Introducing python for newbies",
            "owner_id": test_user["id"]
        },
        {
            "title": "PHP for noobs",
            "content": "Introducing PHP for newbies",
            "owner_id": test_user["id"]
        },
        {
            "title": "JAVA for noobs",
            "content": "Introducing Java for newbies",
            "owner_id": test_user["id"]
        },
        {
            "title": "Machine Learning for newbies",
            "content": "Introducing machine learning for newbies",
            "owner_id": test_user["id"]
        },
    ]
    for post in posts_data:
        response = authorized_client.post("/posts/", json=post)
    
    # Get one post to be voted on already
        
    post_res = authorized_client.post("/votes", json={"post_id": 2, "dir": 1})
