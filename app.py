from flask import Flask, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_login import LoginManager, current_user, UserMixin
from datetime import datetime
import requests
import itertools 

app = Flask(__name__)
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
    'x-rapidapi-key': "",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager = LoginManager()

from app import db
db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/Login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
       return render_template("user.html")
    else:
       return render_template("login.html")
   
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        return render_template("user.html")
    else:
        return render_template("index.html")

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
    findRecipes = "recipes/search"
    if (str(request.args['recipe']).strip() != ""):
        query = {"query":request.args['recipe'],"number":"10","offset":"0","instructionsRequired":"true","addRecipeNutrition":"true"}
        response = requests.request("GET", url + findRecipes, headers=headers, params=query).json()
        results = response['results']        
        return render_template('recipes.html', recipes=results)

@app.route('/recipe')
def recipe():
    # recipe details
    recipe_id = request.args['id']
    recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
    recipe_details = requests.request("GET", url + recipe_info_endpoint + "?includeNutrition=true", headers=headers).json()

    print(recipe_details)

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
