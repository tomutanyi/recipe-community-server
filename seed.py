from app import app, db
from models import User, RecipeListing, RecipeReview
from flask_bcrypt import Bcrypt
from faker import Faker
import random

bcrypt = Bcrypt(app)
fake = Faker()

def seed_users(num_users=10):
    users = []
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.unique.email()
        password = fake.password()
        new_user = User(username=username, email=email, password=password)
        users.append(new_user)
    db.session.bulk_save_objects(users)
    db.session.commit()

def seed_recipes(num_recipes=15):
    recipes = []
    for _ in range(num_recipes):
        name = fake.sentence()
        image_link = fake.image_url()
        ingredients = fake.words(nb=random.randint(3, 8), unique=True)
        instructions = fake.sentence(nb_words=random.randint(10, 20))
        dietary_type = random.choice(['Vegetarian', 'Vegan', 'Non-Vegetarian'])
        recipes.append(RecipeListing(
            name=name,
            image_link=image_link,
            ingredients=', '.join(ingredients),
            instructions=instructions,
            dietary_type=dietary_type
        ))
    db.session.bulk_save_objects(recipes)
    db.session.commit()

def seed_reviews(num_reviews=20):
    reviews = []
    for _ in range(num_reviews):
        commentary = fake.sentence()
        rating = random.randint(1, 5)
        user_id = random.randint(1, 10)
        recipe_listing_id = random.randint(1, 15)
        reviews.append(RecipeReview(
            commentary=commentary,
            rating=rating,
            user_id=user_id,
            recipe_listing_id=recipe_listing_id
        ))
    db.session.bulk_save_objects(reviews)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        print('dropped tables and then created!')
        seed_users()
        print('seeded users')
        seed_recipes()
        print('created recipes!')
        seed_reviews()
        print("Database seeded!")
