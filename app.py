from flask import Flask, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import requests
import itertools 

app = Flask(__name__)
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
    'x-rapidapi-key': "",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

client = MongoClient("localhost", 27017)
db = client['mydb']
print(db)
coll = db["users"]


@app.route("/Login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
       return render_template("user.html")
    else:
       return render_template("login.html")
   
@app.route("/Signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        name = ["name"]
        email = ["email"]
        password = ["password"]
        info = [{"name" : name, "email" : email, "password" : password}]
        user = coll.insert_one(info)
        return render_template("user.html")
    else:
        return render_template("signup.html")

@app.route("/logout")
def logout():
    return render_template("index.html")

@app.route("/user")
def user():
        return render_template("user.html")

def filter_recipes(recipe): 
    if not recipe["instructions"]: 
        return False 
    else:
        return True

@app.route('/')
def homepage():
    randomRecipes = "recipes/random"
    querystring = {"number":"50"}
    response = requests.request("GET", url + randomRecipes, headers=headers, params=querystring).json()

    filtered_results = filter(filter_recipes, response['recipes'])
    first_twelve = itertools.islice(filtered_results, 12)

    return render_template('index.html', recipes=first_twelve)

@app.route('/recipes') 
def recipes():
    findRecipes = "recipes/complexSearch"
    if (str(request.args['recipe']).strip() != ""):
        allergies = request.args['allergies']

        if (request.args['diet']):
            diet = request.args['diet']
        else:
            diet = ""

        query = {"query":request.args['recipe'],"number":"10","offset":"0","instructionsRequired":"true","addRecipeNutrition":"true","excludeIngredients":allergies,"diet":diet}
        response = requests.request("GET", url + findRecipes, headers=headers, params=query).json()
        results = response['results']        
        return render_template('recipes.html', recipes=results)

@app.route('/recipe')
def recipe():
    # recipe details
    recipe_id = request.args['id']
    recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
    recipe_details = requests.request("GET", url + recipe_info_endpoint + "?includeNutrition=true", headers=headers).json()

    # analyzed instructions 
    analyzed_instructions_endpoint = "recipes/{0}/analyzedInstructions".format(recipe_id)
    querystring = {"stepBreakdown":"true"}
    analyzed_instructions = requests.request("GET", url + analyzed_instructions_endpoint, headers=headers, params=querystring).json()

    # similar recipes
    similar_endpoint = "recipes/{0}/similar".format(recipe_id)
    similar_recipes = requests.request("GET", url + similar_endpoint, headers=headers).json()

    # nutrition info 
    nutrition = recipe_details['nutrition']['nutrients'] 

    return render_template('recipe.html', recipe=recipe_details, instructions=analyzed_instructions, similarRecipes=similar_recipes, nutrition=nutrition)

if __name__ == '__main__':
    app.run(debug=True)
