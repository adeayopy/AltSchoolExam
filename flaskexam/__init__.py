import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app=Flask(__name__)
app.config['SECRET_KEY']='e3952e788e587da94f5aab5c3747dabf'
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:////home/adeayo/Documents/AltSchool/AltSchoolExam/flaskexam/site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='users.login'
login_manager.login_message_category='info'
app.config['MAIL_SERVER']="smtp.gmail.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('EMAIL')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASSWORD')

mail=Mail(app)

from flaskexam.users.routes import users
from flaskexam.posts.routes import posts
from flaskexam.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
