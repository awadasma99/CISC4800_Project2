from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import login_required, current_user 
from . import db
from .forms import EditProfileForm, SaveRecipe
import requests
import itertools
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
    'x-rapidapi-key': "KEY",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

def filter_recipes(recipe): 
    if not recipe["instructions"]: 
        return False 
    else:
        return True

@main.route('/')
def index(): 
    randomRecipes = "recipes/random"
    querystring = {"number":"32"}
    vegetarian_querystring = {"number":"32","tags":"vegetarian"}
    vegan_querystring = {"number":"32","tags":"vegan"}

    response = requests.request("GET", url + randomRecipes, headers=headers, params=querystring).json()
    vegetarian_response = requests.request("GET", url + randomRecipes, headers=headers, params=vegetarian_querystring).json()
    vegan_response = requests.request("GET", url + randomRecipes, headers=headers, params=vegan_querystring).json()

    filtered_results = filter(filter_recipes, response['recipes'])
    filtered_vegetarian_results = filter(filter_recipes, vegetarian_response['recipes'])
    filtered_vegan_results = filter(filter_recipes, vegan_response['recipes'])

    first_sixteen = list(filtered_results)
    first_sixteen_vegetarian = list(filtered_vegetarian_results)
    first_sixteen_vegan = list(filtered_vegan_results)

    return render_template('index.html', recipes=first_sixteen[0:16], vegetarian_recipes=first_sixteen_vegetarian[0:16], vegan_recipes=first_sixteen_vegan)

@main.route('/profile')
@login_required
def profile():
    user = current_user.name
    return render_template('profile.html', user=user)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        
        if not check_password_hash(current_user.password, form.old_password.data):
            flash('Incorrect Password: Please try again.')
            return render_template('editprofile.html', title='Edit Profile', form=form)
        else:
            current_user.password = generate_password_hash(form.new_password.data, method='sha256')
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('main.profile'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.name.data = current_user.name
        db.session.commit()
    return render_template('editprofile.html', title='Edit Profile', form=form)

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

        # find summaries 
        summaries = [] 
        for result in results: 
            recipe_id = result['id']
            getSummaries = "recipes/{0}/summary".format(recipe_id)
            
            summary = requests.request("GET", url + getSummaries, headers=headers).json()
            summaries.append(summary['summary']) 

        return render_template('recipes.html', recipes=results, summaries=summaries)

@main.route('/recipe', methods=['GET', 'POST'])
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

    form = SaveRecipe()
    if form.is_submitted():
        flash('Recipe has been saved!')
        this_recipe = recipe_id
        recipe_title = recipe_details['title']

        info = [this_recipe, recipe_title]
        # current_user.saved_recipes.append(this_recipe)
        current_user.saved_recipes.append(info)
        
    return render_template('recipe.html', recipe=recipe_details, instructions=analyzed_instructions, similarRecipes=similar_recipes, nutrition=nutrition, form=form)
