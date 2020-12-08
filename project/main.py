from flask import Blueprint, render_template, request
from flask_login import login_required, current_user 
from . import db
import requests
import itertools

main = Blueprint('main', __name__)

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
    'x-rapidapi-key': "",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

@main.route('/')
def index(): 
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/recipes') 
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

@main.route('/recipe')
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
