from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from sqlalchemy import String, Text

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-recipe_reviews.user",)

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    recipe_reviews = db.relationship('RecipeReview', backref="user")

    def __repr__(self):
        return f'<User: {self.username}>'

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks a password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)


class RecipeListing(db.Model, SerializerMixin):
    __tablename__ = "recipe_listing"

    serialize_rules = ("-recipe_reviews.recipe_listing",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image_link = db.Column(db.String(255))  # Increase the length
    ingredients = db.Column(db.Text)  # Use Text if it can be long
    instructions = db.Column(db.Text)  # Use Text for longer instructions
    dietary_type = db.Column(db.String(50))

    recipe_reviews = db.relationship('RecipeReview', backref='recipe_listing')

    def __repr__(self):
        return f'<Recipe: {self.name}, Ingredients: {self.ingredients}, Instructions: {self.instructions}, Diet: {self.dietary_type}>'


class RecipeReview(db.Model, SerializerMixin):
    __tablename__ = 'recipe_reviews'

    serialize_rules = ("-user.recipe_reviews", "-recipe_listing.recipe_reviews",)

    id = db.Column(db.Integer, primary_key=True)
    commentary = db.Column(db.String())
    rating = db.Column(db.Integer())
    date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    recipe_listing_id = db.Column(db.Integer(), db.ForeignKey('recipe_listing.id'))

    @hybrid_property
    def recipe_name(self):
        """Returns the name of the associated recipe."""
        return self.recipe_listing.name

    def __repr__(self):
        return f'<Review: Rating {self.rating}, Commentary: {self.commentary}, Recipe: {self.recipe_name}>'
