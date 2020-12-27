import os
# from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
# import json

database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


#  Actor Model
class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    def get_name(self):
        return self.name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def print(self):
        return {
          'id': self.id,
          'name': self.name,
          'age': self.age,
          'gender': self.gender
        }

#  Movie Model


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date(), nullable=False)

    def get_title(self):
        return self.title

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def print(self):
        return {
          'id': self.id,
          'title': self.title,
          'release_date': self.release_date
        }
