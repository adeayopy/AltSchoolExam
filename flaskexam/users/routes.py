from flask import Blueprint, redirect, url_for, flash, request, render_template
# from flask_login import current_user,login_user, login_required, logout_user
# from flaskclass.users.forms import RegisterationForm, LoginForm, UpdateForm, RequestResetForm, ResetPasswordForm
# from flaskclass import db, bcrypt
# from flaskclass.users.utils import save_picture, send_email_reset
# from flaskclass.models import User, Post


users=Blueprint('users',__name__)
