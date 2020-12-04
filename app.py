from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

import requests
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

headers = {
    'x-rapidapi-key': "8d518c5534mshba4a11ab4c1cb0ep1c69d1jsn4c0415dbddd7",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

findRecipes = "recipes/search"

db = SQLAlchemy(app)
class users(db.Model):
    email = db.Column("email", db.String(100), primary_key= True)
    password = db.Column("password", db.String(100))

    def __int__(self, email, password):
        self.email = email
        self.password = password

@app.route('/')
def homepage():
    return render_template('index.html')
   
@app.route("/Login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return render_template("user.html")
    else:
        return render_template("login.html")

# @app.route('/search')
# def searchRecipes():
#    return render_template('search_page.html')

@app.route('/recipes') 
def recipe_results():
    if (str(request.args['ingredients']).strip() != ""):
        query = {"query":request.args['ingredients'],"number":"10","offset":"0","instructionsRequired":"true"}
        response = requests.request("GET", url + findRecipes, headers=headers, params=query).json()
        results = response['results']        
        return render_template('recipes.html', recipes=results)

@app.route('/recipe')
def recipe():
    # recipe details
    recipe_id = request.args['id']
    recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
    recipe_details = requests.request("GET", url + recipe_info_endpoint, headers=headers).json()

    # analyzed instructions 
    analyzed_instructions_endpoint = "recipes/{0}/analyzedInstructions".format(recipe_id)
    querystring = {"stepBreakdown":"true"}
    analyzed_instructions = requests.request("GET", url + analyzed_instructions_endpoint, headers=headers, params=querystring).json()

    # return render_template('recipe.html', recipe=recipe_details, instructions=analyzed_instructions[0]['steps'])
    return render_template('recipe.html', recipe=recipe_details, instructions=analyzed_instructions)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
