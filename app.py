from flask import Flask, render_template, request

import requests
app = Flask(__name__)

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

headers = {
    'x-rapidapi-key': "8d518c5534mshba4a11ab4c1cb0ep1c69d1jsn4c0415dbddd7",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

findRecipes = "recipes/findByIngredients"

@app.route('/')
def searchRecipes():
    return render_template('search_page.html')

@app.route('/recipes') 
def recipe_results():
    if (str(request.args['ingredients']).strip() != ""):
        query = {"ingredients":request.args['ingredients'],"number":"5","ranking":"1","ignorePantry":"false"}
        response = requests.request("GET", url + findRecipes, headers=headers, params=query).json()
        return render_template('recipes.html', recipes=response)

@app.route('/recipe')
def recipe():
    recipe_id = request.args['id']
    recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
    recipe_details = requests.request("GET", url + recipe_info_endpoint, headers=headers).json()
    return render_template('recipe.html', recipe=recipe_details)

if __name__ == '__main__':
    app.run(debug=True)
