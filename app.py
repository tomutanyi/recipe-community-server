from flask import Flask, make_response, jsonify, request, session
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, RecipeListing, RecipeReview

app = Flask(__name__)

app.config['SECRET_KEY'] = 'zxcvbnm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True

CORS(app)
migrate = Migrate(app, db)
api = Api(app)
db.init_app(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()

class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)

    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        new_user.password_hash = generate_password_hash(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify(new_user.to_dict()), 201)

api.add_resource(Users, '/users', endpoint='users')

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['person_id'] = user.id
            return make_response(jsonify(user.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "Invalid Email or Password"}), 401)

api.add_resource(Login, '/login', endpoint='login')

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        email = data["email"]
        password = data["password"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return make_response(
                jsonify({"error": "Username or email already exists"}), 409
            )

        new_user = User(
            username=username,
            email=email
        )
        new_user.password_hash = generate_password_hash(password)
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify(new_user.to_dict()), 201)

api.add_resource(Signup, "/signup")

class CheckSession(Resource):
    def get(self):
        user_id = session.get('person_id')
        if user_id:
            user_signed_in = User.query.filter_by(id=user_id).first()
            if user_signed_in:
                return make_response(jsonify(user_signed_in.to_dict()), 200)
            else:
                return make_response(jsonify({"error": "User not found"}), 404)
        else:
            return make_response(jsonify({"error": "User not signed in"}), 401)

api.add_resource(CheckSession, '/session', endpoint='session')
    

class Logout(Resource):
    def delete(self):
        if session.get('person_id'):
            session.pop('person_id', None)
            return make_response(jsonify({"message": "User logged out successfully"}), 200)
        else:
            return make_response(jsonify({"error": "User must be logged in to log out"}), 401)

api.add_resource(Logout, '/logout', endpoint='logout')


class UserByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
        return make_response(jsonify(user.to_dict()), 200)

api.add_resource(UserByID, '/users/<int:id>', endpoint='user_id')


class GetAllRecipe(Resource):
    def get(self):
        recipes = RecipeListing.query.all()
        if recipes:
            recipes_list = [recipe.to_dict() for recipe in recipes]
            return make_response(jsonify(recipes_list), 200)
        return make_response(jsonify({"Message": "No recipes at the moment", "status": 404}), 404)

    def post(self):
        try:
            data = request.get_json()
            new_recipe = RecipeListing(
                name=data['name'],
                image_link=data['image_link'],
                ingredients=data['ingredients'],
                instructions=data['instructions'],
                dietary_type=data['dietary_type']
            )
            db.session.add(new_recipe)
            db.session.commit()
            return make_response(jsonify({"Message": "Recipe added successfully", "status": 201}), 201)
        except Exception as e:
            return make_response(jsonify({"Message": f"Error adding recipe: {str(e)}", "status": 400}), 400)

api.add_resource(GetAllRecipe, '/recipes', endpoint='recipes')
