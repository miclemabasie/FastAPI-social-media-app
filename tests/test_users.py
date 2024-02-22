from .database_test_setup import *
from app.models import User
from app.utils import custom_password_hash
from app.schemas import Token


def test_user_create(client):

    data = dict(username="miclem", email="miclem@mail.com", password="12345", password_repeat="12345")
    response = client.post("/users", json=data)
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == data.get("email")
    assert response.status_code == 201
    assert hasattr(new_user, "created_at")




def test_user_login(client, test_user):
    data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }

    response = client.post("/login", data=data) # using "data" cuz it's formdata
    login_data = Token(**response.json())
    assert hasattr(login_data, "access_token")
    assert hasattr(login_data, "token_type")
    assert login_data.token_type == "bearer"
    assert response.is_success == True
    assert response.status_code == 200

@pytest.mark.parametrize("username, password, status_code", [
    ("miclem@mail.com", "1234", 403),
    ("micle@mail.com", "12345", 403),
    ("micle@mail.com", "1234", 403),
    ("micle@mail.com", None, 422),
    (None, "12345", 422)
])
def test_incorrect_user_login(client, test_user, username, password, status_code):
    data = {
        "username": username,
        "password": password
    }

    response = client.post("/login", data=data) 

    assert response.status_code == status_code
    if response.status_code == 403:
        assert response.json().get("detail") == "Invalid Credentials"