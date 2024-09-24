from app import app, db
from models import User, RecipeListing, RecipeReview
from flask_bcrypt import Bcrypt
from faker import Faker
import random

bcrypt = Bcrypt(app)
fake = Faker()

def seed_users(num_users=10):
    users = []
    # Hash the password "123456"
    hashed_password = bcrypt.generate_password_hash("123456").decode('utf-8')
    
    usernames = ["alex", "sam", "jamie", "chris", "pat", "taylor", "jordan", "casey", "robin", "drew"]
    
    for username in usernames[:num_users]:  # Limit to num_users if needed
        email = f"{username}@gmail.com"
        # Use the hashed password instead of generating a random one
        new_user = User(username=username, email=email, password=hashed_password)
        users.append(new_user)
    
    db.session.bulk_save_objects(users)
    db.session.commit()


def seed_recipes():
    recipes_data = [
        {
            "name": "Spaghetti Aglio e Olio",
            "ingredients": "400g spaghetti, 4 garlic cloves, sliced, 1/2 cup olive oil, 1 tsp red pepper flakes, Salt, to taste, Fresh parsley, chopped, Grated Parmesan (optional)",
            "instructions": "Cook spaghetti in salted water until al dente. Reserve 1 cup of pasta water and drain the rest. In a pan, heat olive oil and sauté garlic until golden. Add red pepper flakes and cooked spaghetti to the pan. Toss to combine. Add reserved pasta water as needed for moisture. Season with salt and garnish with parsley and Parmesan.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154212/recipe-community/11-recipes-small-size/9094_tfrvka.jpg",
            "dietary_type": "Vegetarian"
        },
        {
            "name": "Chicken Tacos",
            "ingredients": "500g chicken breast, diced, 1 tbsp olive oil, 1 tsp cumin, 1 tsp paprika, Salt and pepper, to taste, Corn tortillas, Toppings: avocado, cilantro, lime, salsa",
            "instructions": "Heat olive oil in a pan. Add chicken and season with cumin, paprika, salt, and pepper. Cook until chicken is browned and cooked through. Warm tortillas in another pan. Assemble tacos with chicken and desired toppings.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154211/recipe-community/11-recipes-small-size/5057_uelnjw.jpg",
            "dietary_type": "Non-Vegetarian"
        },
        {
            "name": "Vegetable Stir-Fry",
            "ingredients": "2 cups mixed vegetables (bell peppers, broccoli, carrots), 2 tbsp soy sauce, 1 tbsp sesame oil, 2 garlic cloves, minced, 1 tsp ginger, minced, Cooked rice, for serving",
            "instructions": "Heat sesame oil in a large pan. Add garlic and ginger, sautéing until fragrant. Add mixed vegetables and stir-fry for 5-7 minutes. Pour in soy sauce and toss to coat. Serve over cooked rice.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154211/recipe-community/11-recipes-small-size/2148739212_tvyup3.jpg",
            "dietary_type": "Vegan"
        },
        {
            "name": "Caprese Salad",
            "ingredients": "4 ripe tomatoes, sliced, 250g mozzarella, sliced, Fresh basil leaves, 3 tbsp olive oil, Balsamic vinegar (optional), Salt and pepper, to taste",
            "instructions": "Arrange tomato and mozzarella slices on a plate, alternating them. Tuck basil leaves between the slices. Drizzle with olive oil and balsamic vinegar. Season with salt and pepper.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154210/recipe-community/11-recipes-small-size/19739_andqr8.jpg",
            "dietary_type": "Vegetarian"
        },
        {
            "name": "Beef Stroganoff",
            "ingredients": "500g beef sirloin, sliced, 1 onion, chopped, 200g mushrooms, sliced, 2 cups beef broth, 1 cup sour cream, 2 tbsp flour, Salt and pepper, to taste, Egg noodles, for serving",
            "instructions": "Sauté onion and mushrooms in a pan until soft. Add beef and cook until browned. Sprinkle flour over beef and stir. Gradually add beef broth, cooking until thickened. Remove from heat and stir in sour cream. Season with salt and pepper. Serve over egg noodles.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154210/recipe-community/11-recipes-small-size/alex_g7by0u.jpg",
            "dietary_type": "Non-Vegetarian"
        },
        {
            "name": "Quinoa Salad",
            "ingredients": "1 cup quinoa, 2 cups water, 1 cup cherry tomatoes, halved, 1 cucumber, diced, 1/4 cup red onion, chopped, 1/4 cup feta cheese, crumbled, 3 tbsp olive oil, Juice of 1 lemon, Salt and pepper, to taste",
            "instructions": "Rinse quinoa and cook with water until fluffy. Let it cool. In a bowl, combine quinoa, tomatoes, cucumber, onion, and feta. Drizzle with olive oil and lemon juice. Season with salt and pepper.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154210/recipe-community/11-recipes-small-size/2148784869_b7pyoq.jpg",
            "dietary_type": "Vegetarian"
        },
        {
            "name": "Mushroom Risotto",
            "ingredients": "1 cup Arborio rice, 1 onion, chopped, 200g mushrooms, sliced, 4 cups vegetable broth, 1/2 cup white wine, 1/2 cup Parmesan cheese, grated, 2 tbsp butter, Salt and pepper, to taste",
            "instructions": "Sauté onion and mushrooms in butter until soft. Add Arborio rice and stir for 1-2 minutes. Pour in wine and let it absorb. Gradually add broth, stirring constantly until rice is creamy. Stir in Parmesan and season with salt and pepper.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154208/recipe-community/11-recipes-small-size/7397_dmeiu3.jpg",
            "dietary_type": "Vegetarian"
        },
        {
            "name": "Lentil Soup",
            "ingredients": "1 cup lentils, rinsed, 1 onion, chopped, 2 carrots, diced, 2 celery stalks, diced, 4 cups vegetable broth, 2 garlic cloves, minced, 1 tsp thyme, Salt and pepper, to taste",
            "instructions": "In a pot, sauté onion, carrots, and celery until soft. Add garlic and thyme, cooking for another minute. Stir in lentils and broth. Bring to a boil, then simmer until lentils are tender. Season with salt and pepper.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154203/recipe-community/11-recipes-small-size/17403_a5to6b.jpg",
            "dietary_type": "Vegan"
        },
        {
            "name": "Pancakes",
            "ingredients": "1 cup flour, 2 tbsp sugar, 1 tbsp baking powder, 1/2 tsp salt, 1 cup milk, 1 egg, 2 tbsp melted butter",
            "instructions": "In a bowl, mix flour, sugar, baking powder, and salt. In another bowl, whisk milk, egg, and melted butter. Combine with dry ingredients. Heat a pan and pour batter to form pancakes. Cook until bubbles form, then flip. Serve with syrup and berries.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154202/recipe-community/11-recipes-small-size/18809_yw6dtt.jpg",
            "dietary_type": "Vegetarian"
        },
        {
            "name": "Stuffed Bell Peppers",
            "ingredients": "4 bell peppers, halved and seeded, 1 cup cooked rice, 500g ground beef or turkey, 1 can diced tomatoes, 1 tsp Italian seasoning, 1 cup shredded cheese",
            "instructions": "Preheat oven to 375°F (190°C). In a pan, cook ground meat until browned. Add tomatoes, rice, and Italian seasoning. Fill bell pepper halves with the mixture and place in a baking dish. Top with cheese and bake for 30 minutes.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154201/recipe-community/11-recipes-small-size/18813_xftpy5.jpg",
            "dietary_type": "Non-Vegetarian"
        },
        {
            "name": "Egg Fried Rice",
            "ingredients": "2 cups cooked rice, 2 eggs, beaten, 1 cup mixed vegetables, 2 tbsp soy sauce, 2 green onions, sliced, 2 tbsp oil",
            "instructions": "Heat oil in a pan, scramble the eggs, and set aside. In the same pan, add vegetables and stir-fry for 3-5 minutes. Add rice and soy sauce, stirring well. Mix in scrambled eggs and green onions.",
            "image_link": "https://res.cloudinary.com/dzpurt5ec/image/upload/v1727154202/recipe-community/11-recipes-small-size/34705_ouqsf9.jpg",
            "dietary_type": "Vegetarian"
        }
    ]
    
    # Assuming Recipe is your SQLAlchemy model for storing the recipes
    for recipe in recipes_data:
        new_recipe = RecipeListing(
            name=recipe['name'],
            ingredients=recipe['ingredients'],
            instructions=recipe['instructions'],
            image_link=recipe['image_link'],
            dietary_type=recipe['dietary_type']
        )
        db.session.add(new_recipe)
    
    db.session.commit()


def seed_reviews():
    reviews_data = [
        # Spaghetti Aglio e Olio reviews
        ("Deliciously simple! The garlic and olive oil blend perfectly.", 5),
        ("A delightful balance of flavors; the parsley adds a nice touch.", 4),
        ("A go-to dish when I want something quick and satisfying.", 5),
        ("Perfectly cooked pasta with a hint of spice.", 4),
        # Chicken Tacos reviews
        ("Packed with flavor and easy to make—perfect for a quick dinner!", 5),
        ("The spices really elevate this dish—so tasty!", 4),
        ("Juicy chicken and fresh toppings—yum!", 5),
        ("A fiesta of flavors in every bite!", 5),
        # Vegetable Stir-Fry reviews
        ("A vibrant dish! The veggies were fresh and crunchy.", 5),
        ("A healthy option that doesn’t skimp on flavor.", 4),
        ("Quick to whip up and packed with vitamins.", 5),
        ("A colorful dish that’s fun to eat.", 4),
        # Caprese Salad reviews
        ("So refreshing! The combination of tomatoes and mozzarella is unbeatable.", 5),
        ("A perfect summer salad, so light and refreshing.", 4),
        ("So simple yet so flavorful; a real treat!", 5),
        ("Fresh ingredients that shine through; highly recommend!", 5),
        # Beef Stroganoff reviews
        ("Creamy and comforting, this dish is a must-try for beef lovers.", 5),
        ("Comfort food at its finest; the beef is so tender!", 5),
        ("Rich and creamy, it feels like a warm hug!", 5),
        ("Delicious comfort food that's hard to resist.", 5),
        # Quinoa Salad reviews
        ("Nutty and nutritious! A great way to use leftover quinoa.", 4),
        ("A great blend of textures and flavors—super filling!", 4),
        ("Nutritious and delicious; a great side dish.", 4),
        ("Healthy and filling; a great lunch option!", 5),
        # Mushroom Risotto reviews
        ("Rich and creamy, this risotto is a true indulgence.", 5),
        ("A labor of love that pays off with every creamy bite.", 5),
        ("Absolutely divine! A restaurant-quality dish at home.", 5),
        ("Creamy and flavorful; an elegant dish!", 5),
        # Lentil Soup reviews
        ("Hearty and satisfying! Perfect for a cold day.", 5),
        ("Flavorful and nourishing—definitely a repeat!", 4),
        ("A warming soup that’s both healthy and satisfying.", 5),
        ("A great way to warm up—flavorful and hearty!", 4),
        # Pancakes reviews
        ("Fluffy and sweet—just like breakfast should be!", 5),
        ("The perfect breakfast treat—light and fluffy!", 5),
        ("A breakfast classic that never disappoints!", 5),
        ("Always a hit with the family—fluffy and delightful!", 5),
        # Stuffed Bell Peppers reviews
        ("Colorful and delicious! A great way to sneak in veggies.", 4),
        ("Hearty and flavorful; a crowd-pleaser!", 5),
        ("Creative and delicious; kids love these!", 4),
        ("Full of flavor and nutrients; love these!", 5),
        # Egg Fried Rice reviews
        ("Quick and easy! A perfect way to use leftover rice.", 4),
        ("A great way to use up leftover ingredients—delicious!", 4),
        ("Quick and easy—perfect for busy nights.", 4),
        ("A quick, easy, and delicious meal option.", 4),
        # Chocolate Chip Cookies reviews
        ("The classic cookie, perfectly gooey and sweet!", 5),
        ("Warm, melty, and perfect with a glass of milk!", 5),
        ("Irresistibly soft and chewy—my favorite!", 5),
        ("The perfect treat for any occasion!", 5),
        # Vanilla Smoothie reviews
        ("Creamy and dreamy—great for a refreshing treat!", 4),
        ("So easy to make and a great way to start the day!", 5),
        ("A quick pick-me-up; love the creaminess!", 4),
        ("A refreshing blend that's perfect for breakfast.", 4),
    ]

    reviews = []
    for i, (commentary, rating) in enumerate(reviews_data):
        user_id = random.randint(1, 10)
        recipe_listing_id = (i // 4) + 1  # Assign 4 reviews per recipe
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
