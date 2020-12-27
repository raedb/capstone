# Capstone Project - Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
This api implements CRUD for Actor and Movie models

## Heroku Address
https://raed-casting.herokuapp.com/

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the root directory of this project and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

After installing the dependencies, from the application root directory, execute the bash file `setup.sh` to set
environment variables for auth0 and for database URL:

```bash
source setup.sh
```

To run locally, a postgeres database called "casting" has to be created
'''
createdb casting
'''

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Authentication
This application has 3 roles, each role has its assigned permissions.
End points have been provided to /login and /logoff.

### Assistant
it has 2 permissions: get:movies, get:actors
```
username: a@casting.sa
password: A@casting.sa
```

### Director
In addtion to Assistant role's permissions: post:actors, delete:actors, patch:actors, patch:movies
```
username: d@casting.sa
password: D@casting.sa
```

### Producer
In addtion to Assistant and Director roles' permissions: post:movies, delete:movies
```
username: p@casting.sa
password: P@casting.sa
```

## API Reference

### Endpoints

#### GET '/'
- returns success always. no authorization is needed.
'''
{
    "success": true
}
'''

### GET '/login'
- redirect user to auth0 login page

### GET '/logoff'
- log off the user from auth0


#### GET '/actors'
- Fetches a paginated list of actors, 20 per page.
- Returns: list of actors ordered by name, `success:true`, total actors.
```
{
    "actors": [
        {
            "age": 23,
            "gender": "female",
            "id": 1,
            "name": "actor1"
        },
        {
            "age": 43,
            "gender": "female",
            "id": 2,
            "name": "actor2"
        },
        {
            "age": 53,
            "gender": "male",
            "id": 3,
            "name": "actor3"
        }
    ],
    "success": true,
    "total_actors": 3
}
```

#### GET '/movies'
- Fetches a paginated list of movies, 20 per page.
- Returns: list of movies ordered by title, `success:true`, total movies.
```
{
{
    "movies": [
        {
            "id": 1,
            "release_date": "Sun, 23 May 1999 00:00:00 GMT",
            "title": "mvoie1"
        },
        {
            "id": 2,
            "release_date": "Sun, 23 May 1999 00:00:00 GMT",
            "title": "mvoie2"
        },
        {
            "id": 3,
            "release_date": "Sun, 23 May 1999 00:00:00 GMT",
            "title": "mvoie3"
        }
    ],
    "success": true,
    "total_movies": 3
}
```


#### POST '/actors'
- Create a new actor.
- Request Arguments: { name: String, age: Integer, gender: String }.
- Returns: An object with `success: True` and the new actor.
```
{
    "actors": [
        {
            "age": 65,
            "gender": "male",
            "id": 4,
            "name": "Sameer Ghanem"
        }
    ],
    "success": true
}
```

#### POST '/movies'
- Create a new movie.
- Request Arguments: { title: String, release_date: Date }.
- Returns: An object with `success: True` and the new movie.
```
{
    "movies": [
        {
            "id": 4,
            "release_date": "Fri, 06 Apr 1945 00:00:00 GMT",
            "title": "gone with the wind"
        }
    ],
    "success": true
}
```

#### Patch '/actors/<actor_id>'
- Update an actor by its id.
- Request Arguments (one or more): { name: String, age: Integer, gender: String }.
- Returns: An object with `success: True` and the updated actor.
```
{
    "actor": {
        "age": 23,
        "gender": "female",
        "id": 1,
        "name": "patched name"
    },
    "success": true
}
```

#### Patch '/movies/<movie_id>'
- Update a movie by its id.
- Request Arguments (one or more): { title: String, release_date: Date }.
- Returns: An object with `success: True` and the updated movie.
```
{
    "movie": {
        "id": 2,
        "release_date": "Sun, 23 May 1999 00:00:00 GMT",
        "title": "changed patch"
    },
    "success": true
}
```

#### DELETE '/actors/<actor_id>'
- Removes an actor from the database by its id.
- Returns: An object with `success: True`, the id of the deleted actor, re-list existing actors, and total actors.
```
{
    "actors": [
        {
            "age": 23,
            "gender": "female",
            "id": 1,
            "name": "patched name"
        },
        {
            "age": 53,
            "gender": "male",
            "id": 3,
            "name": "actor3"
        },
        {
            "age": 65,
            "gender": "male",
            "id": 4,
            "name": "Sameer Ghanem"
        }
    ],
    "deleted": 2,
    "success": true,
    "total_actors": 3
}
```

#### DELETE '/movies/<movie_id>'
- Removes a movie from the database by its id.
- Returns: An object with `success: True`, the id of the deleted movie, re-list existing movies, and total movies.
```
{
    "deleted": 1,
    "movies": [
        {
            "id": 2,
            "release_date": "Sun, 23 May 1999 00:00:00 GMT",
            "title": "changed patch"
        },
        {
            "id": 3,
            "release_date": "Sun, 23 May 1999 00:00:00 GMT",
            "title": "mvoie3"
        },
        {
            "id": 4,
            "release_date": "Fri, 06 Apr 1945 00:00:00 GMT",
            "title": "gone with the wind"
        }
    ],
    "success": true,
    "total_movies": 3
}
```

## Testing (locally)

Run the follwing commands to setup the test database and run the tests:
```
dropdb test_casting
createdb test_casting
psql test_casting < test_casting.psql
python test_app.py
```
A valid JWT for each role should be provided in .env file, where variable names: [role]_JWT