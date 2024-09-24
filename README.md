# Recipe Community API

This is a Flask-based RESTful API for a recipe community application. The API allows users to create accounts, login, view recipes, post reviews for recipes, and manage their reviews. It also provides endpoints for retrieving recipe listings, user data, and reviews.

## Features
- User registration and login
- Create, edit, and delete reviews for recipes
- Retrieve recipes and reviews
- Filter recipes by dietary type (vegetarian, vegan, non-vegetarian)

## Setup Instructions

### Clone the repository:

git clone https://github.com/your-repository/recipe-community-server.git

cd recipe-community-server

python3 -m venv venv

## Activate the virtual environment:

`pipenv install && pipenv shell`

**Run database migrations:**

`flask db upgrade`

**Start the Flask server:**

`flask run`

The application will run locally on http://127.0.0.1:5000.

## API Endpoints

### User Management

POST /signup

Register a new user.

Request Body:

```
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

POST /login

Login a user.

Request Body:

```
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

GET /users

Retrieve all users.

GET /users/<user_id>

Retrieve details of a specific user.

### Recipe Management

GET /recipes

Retrieve all recipes.

POST /recipes

Add a new recipe.

Request Body:

```
{
  "name": "Spaghetti Bolognese",
  "image_link": "http://image.url",
  "ingredients": "Pasta, Tomato, Meat",
  "instructions": "Cook pasta, mix with sauce...",
  "dietary_type": "Non-vegetarian"
}
```

GET /recipes/<recipe_id>

Retrieve details of a specific recipe.

### Review Management

GET /reviews

Retrieve all reviews.

POST /reviews

Post a review for a recipe.

Request Body:

```{
  "user_id": 1,
  "recipe_listing_id": 2,
  "rating": 5,
  "commentary": "Delicious!"
}
```

PATCH /reviews/<review_id>
Edit a review.

Request Body:

```{
  "user_id": 1,
  "rating": 4,
  "commentary": "Great but could be better"
}
```

DELETE /reviews/<review_id>

Delete a review.

User Reviews

GET /users/<user_id>/reviews

Retrieve all reviews posted by a specific user.

Recipe Reviews

GET /recipes/<recipe_id>/reviews

Retrieve all reviews for a specific recipe.

## Technologies used

1. Flask
2. SQLite
3. Python


### Author:

Tom Omele Mutanyi






