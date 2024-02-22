def test_vote_post(authorized_client, test_create_post):
    data = {
        "post_id": 3,
        "dir": 1
    }
    response = authorized_client.post("/votes", json=data)

    assert response.status_code == 201


def test_vote_post_twice_not_working(authorized_client, test_create_post):
    response = authorized_client.post("/votes", json={"post_id": 2, "dir": 1})
    assert response.json().get("detail") == "Can't like the same post twice"
    assert response.status_code == 409
    