# CISC 4800 - Project 2

## Instructions

### Python 
* Make sure you have python installed. Run `python -V` to check the version.

### Python Environment 
* Navigate to CISC4800_Project2
* On Mac, run the following commands: 
    * `python3 -m venv auth`
    * `source auth/bin/activate` 
* On Windows, I think this should work: 
    * `python3 -m venv auth` 
    * `auth\Scripts\activate`

* You should now see (auth) near your computer name. This creates an auth folder which holds all required libraries for your project. (Don't push it to GitHub!) 
* Resource for setting up venv on different OS: https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3

### Installing Packages 
* Now, run the following:
    * `pip install flask flask-sqlalchemy flask-login`
    * `pip install requests`

### Set the Environment Variables
* On Mac, run the following: 
    * `export FLASK_APP=project`
    * `export FLASK_DEBUG=1`
* On Windows: 
    * `set FLASK_APP=project`
    * `set FLASK_DEBUG=1`

### Run the app	
* From CISC4800_Project2, you should be able to run the command:
    * `flask run`

### Configuring the database
* If a change is made to the database (i.e. adding a column), enter a Python REPL by typing `python`

* Then, run the following commands. Make sure you’re in CISC4800_Project2:
    * `from project import db, create_app, models`
    * `db.create_all(app=create_app())`
