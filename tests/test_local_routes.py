
from .database_test_setup import *

def test_check(client):
    response = client.get("/check")
    # print(dir(response))
    # print(response.url)
    # print(response.links)
    # print(response.is_success)

    assert response.status_code == 200
    assert response.json() == {"message": "OK"}

def test_root_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}
