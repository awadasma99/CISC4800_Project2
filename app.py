from flask import Flask, render_template, request, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from flask_pymongo import PyMongo
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, current_user, logout_user,login_required, login_user
import requests
import itertools
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
    'x-rapidapi-key': "8d518c5534mshba4a11ab4c1cb0ep1c69d1jsn4c0415dbddd7",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

log = LoginManager(app)
log.login_view = "login"
client = MongoClient("localhost", 27017)
db = client['mydb']
coll = db["users"]

class User:
    def __init__(self, name, email, password):
        self.email = email
        self.name = name
        self.password = password

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @log.user_loader
    def load_user(self):
        usr = mongo.db.Users.find_one({"name": self.name})
        if not usr:
            return None
        return User(name=usr["name"], email=usr["email"], password=usr["password"])

class Login(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')

class Signup(FlaskForm):
    name = StringField('email', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Signup')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if current_user.is_authenticated:
        return render_template("user.html")
    if form.validate_on_submit():
         user = mongo.db.Users.find_one({"email": form.email.data})
         if user and User.check_password(user['Password'], form.password.data):
            login_user(user)
            return render_template("user.html")
    else:
        flash("Invalid username or password")
        return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
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
