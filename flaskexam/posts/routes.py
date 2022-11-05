from flask import Blueprint, redirect, url_for, flash, render_template, abort, request
# from flaskclass import db
# from flask_login import current_user, login_required
# from flaskclass.models import Post
# from flaskclass.posts.forms import PostForm 

posts=Blueprint('posts',__name__)
