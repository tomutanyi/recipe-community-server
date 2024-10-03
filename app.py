from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, RecipeListing, RecipeReview

app = Flask(__name__)

app.config['SECRET_KEY'] = 'zxcvbnm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tom:password@localhost:5432/recipe_db'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, supports_credentials=True)
migrate = Migrate(app, db)
api = Api(app)
db.init_app(app)

class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)

    def post(self):
        data = request.get_json()
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return make_response(jsonify({"error": "Email already exists"}), 409)

        try:
            new_user = User(username=data['username'], email=data['email'])
            new_user.set_password(data['password'])
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify(new_user.to_dict()), 201)
        except Exception as e:
            return make_response(jsonify({"error": f"Error creating user: {str(e)}"}), 400)

api.add_resource(Users, '/users', endpoint='users')

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if user and user.check_password(data.get('password')):
            return make_response(jsonify(user.to_dict()), 200)
        return make_response(jsonify({"error": "Invalid Email or Password"}), 401)

api.add_resource(Login, '/login', endpoint='login')

class Signup(Resource):
    def post(self):
        data = request.get_json()
        existing_user = User.query.filter_by(email=data['email']).first()

        if existing_user:
            return make_response(jsonify({"error": "Email already exists"}), 409)

        try:
            new_user = User(username=data['username'], email=data['email'])
            new_user.set_password(data['password'])
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify(new_user.to_dict()), 201)
        except Exception as e:
            return make_response(jsonify({"error": f"Error during signup: {str(e)}"}), 400)

api.add_resource(Signup, "/signup")

class UserByID(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
        return make_response(jsonify(user.to_dict()), 200)

api.add_resource(UserByID, '/users/<int:user_id>', endpoint='user_id')

class GetAllRecipe(Resource):
    def get(self):
        recipes = RecipeListing.query.all()
        if not recipes:
            return make_response(jsonify({"Message": "No recipes at the moment"}), 404)

        recipes_list = [recipe.to_dict() for recipe in recipes]
        return make_response(jsonify(recipes_list), 200)

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
            return make_response(jsonify({"Message": "Recipe added successfully"}), 201)
        except Exception as e:
            return make_response(jsonify({"Message": f"Error adding recipe: {str(e)}"}), 400)

api.add_resource(GetAllRecipe, '/recipes', endpoint='recipes')

class RecipeByID(Resource):
    def get(self, recipe_id):
        recipe = RecipeListing.query.filter_by(id=recipe_id).first()
        if not recipe:
            return make_response(jsonify({"error": "Recipe not found"}), 404)
        return make_response(jsonify(recipe.to_dict()), 200)

api.add_resource(RecipeByID, '/recipes/<int:recipe_id>', endpoint='recipe_by_id')

class RecipeReviewsByRecipeID(Resource):
    def get(self, recipe_id):
        reviews = RecipeReview.query.filter_by(recipe_listing_id=recipe_id).all()
        if not reviews:
            return make_response(jsonify({"error": "No reviews found for this recipe"}), 404)

        reviews_list = [review.to_dict() for review in reviews]
        return make_response(jsonify(reviews_list), 200)

api.add_resource(RecipeReviewsByRecipeID, '/recipes/<int:recipe_id>/reviews', endpoint='recipe_reviews_by_id')

class UserReviews(Resource):
    def get(self, user_id):
        reviews = RecipeReview.query.filter_by(user_id=user_id).all()
        if not reviews:
            return make_response(jsonify({"error": "No reviews found for this user"}), 404)

        reviews_list = [review.to_dict() for review in reviews]
        return make_response(jsonify(reviews_list), 200)

api.add_resource(UserReviews, '/users/<int:user_id>/reviews', endpoint='user_reviews')

class AllReviews(Resource):
    def get(self):
        reviews = RecipeReview.query.all()
        if not reviews:
            return make_response(jsonify({"error": "No reviews found"}), 404)

        reviews_list = [review.to_dict() for review in reviews]
        return make_response(jsonify(reviews_list), 200)

api.add_resource(AllReviews, '/reviews', endpoint='all_reviews')

class PostReview(Resource):
    def post(self):
        data = request.get_json()

        if 'user_id' not in data:
            return make_response(jsonify({"error": "User ID is required"}), 400)

        required_fields = ['recipe_listing_id', 'rating', 'commentary']
        for field in required_fields:
            if field not in data:
                return make_response(jsonify({"error": f"Missing field: {field}"}), 400)

        try:
            new_review = RecipeReview(
                user_id=data['user_id'],
                recipe_listing_id=data['recipe_listing_id'],
                rating=data['rating'],
                commentary=data['commentary']
            )
            db.session.add(new_review)
            db.session.commit()
            return make_response(jsonify({"message": "Review posted successfully", "review": new_review.to_dict()}), 201)
        except Exception as e:
            return make_response(jsonify({"error": f"Error posting review: {str(e)}"}), 400)

api.add_resource(PostReview, '/reviews', endpoint='post_review')

class EditReview(Resource):
    def patch(self, review_id):
        data = request.get_json()

        review = RecipeReview.query.filter_by(id=review_id, user_id=data['user_id']).first()
        if not review:
            return make_response(jsonify({"error": "Review not found or unauthorized"}), 404)

        if 'rating' in data:
            review.rating = data['rating']
        if 'commentary' in data:
            review.commentary = data['commentary']

        db.session.commit()
        return make_response(jsonify({"message": "Review updated successfully", "review": review.to_dict()}), 200)

api.add_resource(EditReview, '/reviews/<int:review_id>', endpoint='edit_review')

class DeleteReview(Resource):
    def delete(self, review_id):
        review = RecipeReview.query.filter_by(id=review_id).first()
        if not review:
            return make_response(jsonify({"error": "Review not found"}), 404)

        db.session.delete(review)
        db.session.commit()
        return make_response(jsonify({"message": "Review deleted successfully"}), 200)

api.add_resource(DeleteReview, '/reviews/<int:review_id>', endpoint='delete_review')

if __name__ == '__main__':
    app.run(debug=True)
