# Description

Flask app with an integration with the **Giphy API** with endpoints to return a list of gifs, update an user with a gif as avatar, and fetch a list of users by either partial username or name.

There's room for improvement, but this project was a take-home test with a time limit of 1.5 hours.

### Technologies

- **Python3**
- **Flask**
- **pytest**
- **SimpleCache** (simulate the database)
- **Docker**

### Running locally

- Add your Giphy API Token in `.env`.
- `pip install -r requirements.txt`
- `flask run`

### Running on Docker container

- Add your Giphy API Token in `.env`.
- `docker build -t avatargiphy-api .`
- `docker run -p 5000:5000 avatargiphy-api`

### Running Tests

- `python -m pytest`

### Endpoints

- **GET /avatars**

`curl -L http://127.0.0.1:5000/avatars`

- **GET /users/search?name=X&username=X**

`curl -L http://127.0.0.1:5000/users/search?name=Jose&username=joseahp`

- **PUT /users/<user_id>/avatar**

`curl -L -d '{"avatar_id":"EDYuWKNkQJkZXIl6U4"}' -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/users/1/avatar`
