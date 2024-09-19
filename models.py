from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from datetime import datetime


db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-recipe_reviews.user",)

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String())

    recipe_reviews = db.relationship('RecipeReview', backref="user")

    def _repr_(self):
        return f'<User: {self.username}>'
    

    @hybrid_property
    def password_hash(self):
        raise AttributeError ("Not Allowed")
    

    @password_hash.setter

    def password_hash(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash,password.encode("utf-8"))
    

