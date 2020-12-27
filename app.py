# import os
from flask import Flask, jsonify, request, abort, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor, setup_db
from auth import requires_auth, AuthError


ITEMS_PER_PAGE = 20

# paginating


def pagination(request, selection, type):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    if(type == 'movies'):
        movies = [movie.print() for movie in selection]
        return movies[start:end]
    elif(type == 'actors'):
        actors = [actor.print() for actor in selection]
        return actors[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # initializing CORS to enable cross-domain requests
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Acess-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Acess-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def get_root():
        return jsonify({
            "success": True
        })

    @app.route('/login')
    def login():
        return redirect("https://fsnd-rmb.us.auth0.com/authorize?audience=image&response_type=token&client_id=tJwIaCeImPAmE7CeZhQ760FZq1ppMuGk&redirect_uri=http://localhost:8080/")

    @app.route('/logoff')
    def logoff():
        return redirect("https://fsnd-rmb.us.auth0.com/v2/logout?client_id=tJwIaCeImPAmE7CeZhQ760FZq1ppMuGk&returnTo=http://localhost:8080/")

    # get all the movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(token):
        movies = Movie.query.order_by(Movie.title).all()
        current_movies = pagination(request, movies, 'movies')

        if(len(current_movies) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'movies': current_movies,
            'total_movies': len(movies)
        }), 200

    # display all the actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(token):
        actors = Actor.query.order_by(Actor.name).all()
        current_actors = pagination(request, actors, 'actors')

        if(len(current_actors) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'actors': current_actors,
            'total_actors': len(actors)
        }), 200

    # create a movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(token):
        body = request.json

        if body is None:
            abort(400)

        # if the fields are not in the body then  abort due to bad request
        if not('title' in body and 'release_date' in body):
            abort(400)

        new_title = body.get('title')
        new_release_date = body.get('release_date')

        # Create and insert a new movie
        new_movie = Movie(title=new_title, release_date=new_release_date)
        new_movie.insert()

        # Return the newly created movie
        return jsonify({
            'success': True,
            'movies': [Movie.query.get(new_movie.id).print()]
        })

    # create an actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(token):
        body = request.json

        if body is None:
            abort(400)

        # if the fields are not in the body then  abort due to bad request
        if not('name' in body and 'age' in body and 'gender' in body):
            abort(400)

        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')

        # Create and insert a new actor
        new_actor = Actor(name=new_name, age=new_age, gender=new_gender)
        new_actor.insert()

        # Return the newly created actor
        return jsonify({
            'success': True,
            'actors': [Actor.query.get(new_actor.id).print()]
        })

    # delete a movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(token, movie_id):

        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if(movie is None):
            abort(404)

        # delete and re-list
        try:

            movie.delete()
            movies = Movie.query.order_by(Movie.id).all()
            current_movies = pagination(request, movies, 'movies')

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'movies': current_movies,
                'total_movies': len(movies)
            }), 200

        except Exception:
            abort(422)

    # delete an actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(token, actor_id):

        actor = Actor.query.filter_by(id=actor_id).one_or_none()

        if(actor is None):
            abort(404)

        try:
            # delete then re-list
            actor.delete()
            actors = Actor.query.order_by(Actor.id).all()
            current_actors = pagination(request, actors, 'actors')

            return jsonify({
                'success': True,
                'deleted': actor_id,
                'actors': current_actors,
                'total_actors': len(actors)
            }), 200

        except Exception:
            abort(422)

    # update a movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(token, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()

        if movie is None:
            abort(404)

        body = request.get_json()

        # get the updates
        try:
            if('title' in body):
                movie.title = body['title']
            if('release_date' in body):
                movie.release_date = body['release_date']
        except Exception:
            abort(400)

        # update movie
        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.print()
        }), 200

    # update an actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(token, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()

        if actor is None:
            abort(404)

        body = request.get_json()

        # get the updates
        try:
            if('name' in body):
                actor.name = body['name']
            if('age' in body):
                actor.age = body['age']
            if('gender' in body):
                actor.gender = body['gender']
        except Exception:
            abort(400)

        # update actor
        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.print()
        }), 200

    @app.errorhandler(AuthError)
    def authentication_eror(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal server error"
        }), 500

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
