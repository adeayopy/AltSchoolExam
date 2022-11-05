from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SECRET_KEY']='e3952e788e587da94f5aab5c3747dabf'
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:////home/adeayo/Documents/AltSchool/flaskapp/flaskclass/site.db'
db=SQLAlchemy(app)

from flaskexam.users.routes import users
from flaskexam.posts.routes import posts
from flaskexam.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
