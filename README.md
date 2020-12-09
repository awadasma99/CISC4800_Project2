# CISC 4800 - Project2

To run this, make sure you have everything installed (details below). 

Run the app by running `flask run` in the command line. Ensure that you're in the `project` folder. You may get an error related to env variables, which you can set by running the following: 
* `export FLASK_APP=project`
* `export FLASK_DEBUG=1`

When you run `flask run` again, you should be given a message on terminal saying something along the lines of "running on server http://127.0.0.1:5000/". Take that link and paste it into your browser, and you should be met with the search page.

Note: you will also need an API key, which needs to be entered in the `main.py` file.

________________

Before you make changes to any python files, you're going to want to create a Python environment. You can do so by running the following commands: 
* `python3 -m venv auth`
* `source auth/bin/activate`

You may also have to configure the database. You can do this by opening up a Python REPL (run `python` in your command line, and it should open up). From there, enter the following: 
* `from project import db, create_app`
* `db.create_all(app=create_app())`

Exit the REPL using Command + D. 

Installation Details
----------------------------------

Make sure you have Python installed on your device, as well as the following libraries: 
* `pip install flask flask-sqlalchemy flask-login`
* `pip install requests` 

---------------------------------
