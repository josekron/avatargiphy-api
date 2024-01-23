def test_avatar_api(client):
    response = client.get('/avatars/')
    assert response.status_code == 200
    assert response.json['avatars'] is not None

