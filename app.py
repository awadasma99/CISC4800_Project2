from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import requests
import itertools 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
    'x-rapidapi-key': "API-KEY",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

db = SQLAlchemy(app)
class users(db.Model):
    email = db.Column("email", db.String(100), primary_key= True)
    password = db.Column("password", db.String(100))

    def __int__(self, email, password):
        self.email = email
        self.password = password

def filter_recipes(recipe): 
    if not recipe["instructions"]: 
        return False 
    else:
        return True

@app.route("/Login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return render_template("user.html")
    else:
        return render_template("login.html")

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
        query = {"query":request.args['recipe'],"number":"10","offset":"0","instructionsRequired":"true","addRecipeNutrition":"true","excludeIngredients":allergies}
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
    db.create_all()
    app.run(debug=True)
