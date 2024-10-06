import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session


"""
your project’s title: Mealprep Planner
your name: Ngoc Hwang Philipp Huynh
your GitHub and edX usernames; bobocs50
your city and country; Potsdam Germany
and, the date you have recorded this video: 6.10.2024
"""




#Configure application
app = Flask(__name__)

#SQLite database
db = SQL("sqlite:///data.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        #Get fronend input
        meal_name = request.form.get("meal_name")
        servings = request.form.get("servings")

        ingredients = request.form.getlist('ingredients[]')
        quantities = request.form.getlist('quantities[]')
        units = request.form.getlist('units[]')

        #INSERT meals
        db.execute("INSERT INTO meals (meal_name, servings) VALUES(?, ?)",
                   meal_name.lower(), int(servings))

        #Get meal id
        meal_id = db.execute("SELECT last_insert_rowid() AS id")[0]["id"]

        #INSERT ingredients
        for i in range(len(ingredients)):
            db.execute("INSERT INTO ingredients (meal_id, ingredient_name, quantity, unit) VALUES(?, ?, ?, ?)",
                       meal_id, ingredients[i].lower(), int(quantities[i]), units[i].lower())

        return redirect("/")


    return render_template("index.html")


@app.route("/select", methods=["GET", "POST"])
def select():

    meals_list = []
    filtered_serving = []

    #get meals
    meals_names = db.execute("SELECT meal_name FROM meals")
    #iterrate through dict and put into list outside of if block
    for meal in meals_names:
            meal_title = meal["meal_name"].title()
            meals_list.append(meal_title)

    if request.method == "GET":
        return render_template("select.html", meals=meals_list)




    elif request.method == "POST":
        #get meal and portions
        selected_meals = request.form.getlist("selected_meals")
        selected_servings = request.form.getlist("selected_servings")

        #filter out whitespace
        for serving in selected_servings:
            if serving.strip():
                filtered_serving.append(int(serving))

        #scale the meals

        current_meal = 0

        for meal in selected_meals:

            #find the id of the meal
            id = db.execute("SELECT id FROM meals WHERE meal_name = ?", meal.lower())[0]["id"]

            #get the ingredients dict for that id
            ingredients= db.execute("SELECT quantity FROM ingredients WHERE meal_id = ?", id)

            # Extract quantities into a list
            quantities = [ingredient["quantity"] for ingredient in ingredients]

            #interate through each ingredient and multiply for portion and put into list
            updated_quantities = []

            for quantity in quantities:
                new_quantity = quantity * filtered_serving[current_meal]
                updated_quantities.append(new_quantity)

            #INSERT meals into meals_new
            db.execute("INSERT INTO meals_new (meal_name, servings, meal_id) VALUES(?, ?, ?)",
                       selected_meals[current_meal].lower(), filtered_serving[current_meal], id)

            #GET ingredients and unit
            ingredients = db.execute("SELECT ingredient_name FROM ingredients WHERE meal_id = ?", id)
            units = db.execute("SELECT unit FROM ingredients WHERE meal_id = ?", id)

            #put them into lists
            updated_ingredients = [ingredient["ingredient_name"].lower() for ingredient in ingredients]
            updated_units = [unit["unit"] for unit in units]

            #INSERT ingredients into ingredients_new
            for i in range(len(ingredients)):
                db.execute("INSERT INTO ingredients_new (meal_id, ingredient_name, quantity, unit) VALUES(?, ?, ?, ?)",
                        id, updated_ingredients[i].lower(), int(updated_quantities[i]), updated_units[i].lower())






            #PUT INGREDIENTS, QUANTITY AND UNIT INTO GROCERY LIST
            grocery_list = db.execute("SELECT ingredient_name, quantity FROM grocery_list")

            #LISTS
            existing_ingredients = []
            existing_quantities = []

            #add into list
            for i in grocery_list:
                existing_ingredients.append(i["ingredient_name"].lower())
                existing_quantities.append(i["quantity"])


            #iterate trough each ingredient
            for i, ingredient in enumerate(updated_ingredients):

                if ingredient in existing_ingredients:
                    #find index of the ingredient
                    index = existing_ingredients.index(ingredient)
                    #add up quantities
                    new_quantity = existing_quantities[index] + updated_quantities[i]
                    #update database
                    db.execute("UPDATE grocery_list SET quantity = ? WHERE ingredient_name = ?",
                    new_quantity, ingredient)

                else:
                    db.execute("INSERT INTO grocery_list (ingredient_name, quantity, unit) VALUES(?,?,?)",
                        ingredient.lower(), updated_quantities[i], updated_units[i].lower())



            #Increment to move to next meal
            current_meal += 1

        return redirect("/recipe")

@app.route("/recipe", methods=["GET", "POST"])
def recipe():
    if request.method == "POST":
        # Handle button click here
        db.execute("DELETE FROM ingredients_new")
        db.execute("DELETE FROM meals_new")

        return redirect("/recipe")


    elif request.method == "GET":
        # Fetch meals with their IDs
        meals = db.execute("SELECT meal_id, meal_name, servings FROM meals_new")

        # Create a dictionary to store meals and their ingredients
        recipe_data = {}

        for meal in meals:
            #Get meal_id from meals_new
            meal_id = meal['meal_id']

            # Fetch ingredients from ingredients_new with ID
            ingredients = db.execute("SELECT ingredient_name, quantity, unit FROM ingredients_new WHERE meal_id = ?", meal_id)

            # Store meal info and its ingredients in the dictionary
            recipe_data[meal['meal_name']] = {
                'servings': meal['servings'],
                'ingredients': ingredients
            }

    return render_template("recipe.html", recipe_data=recipe_data)


@app.route("/planner", methods=["GET","POST"])
def planner():
    if request.method == "POST":
        # Handle button click here
        db.execute("DELETE FROM grocery_list")


        return redirect("/planner")
    elif request.method =="GET":
        grocery_list = db.execute("SELECT ingredient_name, quantity, unit FROM grocery_list")
        return render_template("planner.html", grocery_list=grocery_list)



