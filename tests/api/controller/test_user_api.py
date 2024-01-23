def test_user_api_success(client):
    response = client.get('/users/search?name=Jose')
    assert response.status_code == 200
    assert response.json['users'] is not None
    assert len(response.json['users']) == 1
    assert response.json['users'][0]['name'] == 'Jose'
    assert response.json['users'][0]['username'] == 'joseahp'

    response = client.get('/users/search?username=joseahp')
    assert response.status_code == 200
    assert response.json['users'] is not None
    assert len(response.json['users']) == 1
    assert response.json['users'][0]['name'] == 'Jose'
    assert response.json['users'][0]['username'] == 'joseahp'


def test_user_api_no_parameters(client):
    response = client.get('/users/search')
    assert response.status_code == 400


def test_user_api_not_found(client):
    response = client.get('/users/search?name=Maria')
    assert response.status_code == 200
    assert response.json['users'] is not None
    assert len(response.json['users']) == 0


def test_user_update_avatar_success(client):
    response = client.get('/users/search?name=Jose')
    assert response.status_code == 200
    assert response.json['users'] is not None
    assert len(response.json['users']) == 1
    assert response.json["users"][0]["id"] == 1
    assert response.json['users'][0]['avatar_id'] != 'EDYuWKNkQJkZXIl6U4'

    response = client.put("/users/1/avatar", json={
        "avatar_id": "EDYuWKNkQJkZXIl6U4"
    })
    assert response.status_code == 200
    assert response.json['user'] is not None
    assert response.json["user"]["id"] == 1
    assert response.json["user"]["avatar_id"] == "EDYuWKNkQJkZXIl6U4"


def test_user_update_avatar_no_body(client):
    response = client.put("/users/100/avatar", json={
    })
    assert response.status_code == 400


def test_user_update_avatar_not_found(client):
    response = client.put("/users/1/avatar", json={
        "avatar_id": "test"
    })
    assert response.status_code == 410
    assert response.json['meta'] is not None


def test_user_update_avatar_user_not_found(client):
    response = client.put("/users/100/avatar", json={
        "avatar_id": "EDYuWKNkQJkZXIl6U4"
    })
    assert response.status_code == 404
