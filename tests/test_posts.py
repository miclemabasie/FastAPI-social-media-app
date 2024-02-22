from .database_test_setup import *
from app.models import User
from app.utils import custom_password_hash
from app.schemas import Token
from app.oauth2 import create_access_token

def test_get_all_users(authorized_client, test_create_post):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200


def test_get_post_by_id(authorized_client, test_create_post, test_user):
    response = authorized_client.get("/posts/1", )
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("owner").get("id") == test_user["id"]
    assert response.json().get("owner").get("email") == test_user["email"]
    assert response.json().get("owner").get("username") == test_user["username"]

def test_post_create_route(test_user, authorized_client):
    data = {
        "title": "Mastering Javascript",
        "content": "An indept guide to javascript for newbies",
        "owner_id": test_user["id"]
    }
    response = authorized_client.post("/posts", json=data)
    assert response.status_code == 201

def test_unauthorized_access_denied(test_user, client):
    response = client.get("/posts/1")

    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"

def test_post_not_found(authorized_client, test_create_post):
    response = authorized_client.get("/posts/7")
    assert response.json().get("detail") == "Post with id not found"
    assert response.status_code == 404


def test_post_default_published_true(authorized_client, test_user):
    data = {
        "title": "Linux Os",
        "content": "A deep dive into linux",
        "owner_id": test_user["id"]
    }
    response = authorized_client.post("/posts", json=data)
    assert response.status_code == 201
    assert response.json().get("published") == True


def test_unauthorized_user_create_post(client, test_user):
    data = {
        "title": "Linux Os",
        "content": "A deep dive into linux",
        "owner_id": test_user["id"]
    }
    response = client.post("/posts", json=data)
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"


def test_delete_post_success(authorized_client, test_create_post, test_user):
    response = authorized_client.delete("/posts/2")
    assert response.status_code == 204
    all_posts = authorized_client.get("/posts")
    assert len(all_posts.json()) == 3

def test_user_can_not_delete_anothers_post(test_user, client, test_create_post):
    data = dict(username="miclem", email="miclem@mail.com", password="12345", password_repeat="12345")
    response = client.post("/users", json=data)
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == data.get("email")
    assert response.status_code == 201
    assert hasattr(new_user, "created_at")

    # Log the user in
    token = create_access_token({"user_id": new_user.id})
    auth_client = client
    auth_client.headers = {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive', 'user-agent': 'testclient', 'authorization': f"Bearer {token}"}
    
    res = auth_client.delete("/posts/2")
    assert res.status_code == 403


def test_can_update_valid_post(authorized_client, test_create_post):
    data = {
        "title": "PHP for noobs, Revised Edition",
        "content": "Introducing PHP for newbies",
    }
    response = authorized_client.put("/posts/2", json=data)

    assert response.json().get("title") == "PHP for noobs, Revised Edition"
    assert response.status_code == 200
    assert response.json().get("content") == "Introducing PHP for newbies"
    
def test_can_not_update_not_existing_post(authorized_client):
    data = {
        "title": "PHP for noobs, Revised Edition",
        "content": "Introducing PHP for newbies",
    }
    response = authorized_client.put("/posts/2342342", json=data)
    assert response.status_code == 404
    assert response.json().get("detail") == "Post with given id not found"

