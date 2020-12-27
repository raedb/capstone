import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor
from dotenv import load_dotenv

# using dotenv to unpack the environment variables
load_dotenv()

# read environment variables for JWT
ASSISTANT_JWT = "Bearer {}".format(os.environ.get('ASSISTANT_JWT'))
DIRECTOR_JWT = "Bearer {}".format(os.environ.get('DIRECTOR_JWT'))
PRODUCER_JWT = "Bearer {}".format(os.environ.get('PRODUCER_JWT'))


class CastingTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_casting"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        # Executed after each test
        pass

    # test and error tests for each enpoint
    def test_get_paginated_movies(self):
        res = self.client().get('/movies',
                                headers={"Authorization": (ASSISTANT_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_error_get_paginated_movies(self):
        res = self.client().get('/movies?page=5000',
                                headers={"Authorization": (ASSISTANT_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_get_paginated_actors(self):
        res = self.client().get('/actors',
                                headers={"Authorization": (ASSISTANT_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_error_get_paginated_actors(self):
        res = self.client().get('/actors?page=1000',
                                headers={"Authorization": (ASSISTANT_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/3',
                                   headers={"Authorization": (PRODUCER_JWT)})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
        self.assertEqual(movie, None)

    def test_error_delete_movie(self):
        res = self.client().delete('/movies/5000',
                                   headers={"Authorization": (PRODUCER_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_delete_actor(self):
        res = self.client().delete('/actors/3',
                                   headers={"Authorization": (DIRECTOR_JWT)})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))
        self.assertEqual(actor, None)

    def test_error_delete_actor(self):
        res = self.client().delete('/actors/5000',
                                   headers={"Authorization": (DIRECTOR_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_create_movie(self):
        res = self.client().post(
            '/movies',
            json={
                'title': 'created movie',
                'release_date': '1-2-2002'},
            headers={"Authorization": (PRODUCER_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_error_create_movie(self):
        res = self.client().post(
            '/movies/100',
            json={
                'title': 'error movie',
                'release_date': '02-02-2015'},
            headers={"Authorization": (PRODUCER_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_create_actor(self):
        res = self.client().post(
            '/actors',
            json={
                'name': 'created actor',
                'age': 25,
                'gender': 'Female'},
            headers={"Authorization": (DIRECTOR_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_error_create_actor(self):
        res = self.client().post(
            '/actors/100',
            json={
                'name': 'error actor',
                'age': 74,
                'gender': 'Female'},
            headers={"Authorization": (DIRECTOR_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_update_movie(self):
        res = self.client().patch('/movies/1',
                                  json={'release_date': '9-9-2009'},
                                  headers={"Authorization": (DIRECTOR_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_error_update_movie(self):
        res = self.client().patch('/movies/5000',
                                  json={'release_date': '7-7-2007'},
                                  headers={"Authorization": (DIRECTOR_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_update_actor(self):
        res = self.client().patch(
            '/actors/2',
            json={
                'age': 39},
            headers={"Authorization": (DIRECTOR_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_error_update_actor(self):
        res = self.client().patch(
            '/actors/5000',
            json={
                'age': 50},
            headers={"Authorization": (DIRECTOR_JWT)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
