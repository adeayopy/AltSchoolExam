from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import current_user,login_user, login_required, logout_user
from flaskexam.users.forms import RegisterationForm, LoginForm, UpdateForm, RequestResetForm, ResetPasswordForm
from flaskexam import db, bcrypt
from flaskexam.users.utils import save_picture, send_email_reset
from flaskexam.models import User, Post




users=Blueprint('users',__name__)

# Function to register user
@users.route("/register", methods=['GET','POST'])
def register():
    # If user is logged in, user should not access the register page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form=RegisterationForm()
    if form.validate_on_submit():
        # hash password using bcrypt
        hash_password=bcrypt.generate_password_hash(form.password.data).decode()
        # write from to db
        user=User(username=form.username.data, email=form.email.data, firstname=form.firstname.data, lastname=form.lastname.data,password=hash_password)
        db.session.add(user)
        db.session.commit()
        # flash message and redirect to homepage
        flash(f"Welcome {form.username.data}! You can now login",'success')
        return redirect(url_for("users.login"))
    return render_template('register.html', title="Register", form=form)

# FUnction to login user
@users.route("/login", methods=['GET','POST'])
def login():
    # Ensure a logged in user does not go back to the login page except if logged out
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
            # filter user details by email and validate password
            user=User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                
                login_user(user,remember=form.remember.data)
                # if there is a query in the url before login, get the query and lead user to that page after login
                next_page=request.args.get('next')
                flash(f"You have been logged in!",'success')
                return redirect(next_page) if next_page else redirect (url_for("main.home"))
            else:
                flash("Login unsuccessful. Check email and password","danger")
    return render_template('login.html', title="Login", form=form)

# Functionality to view and update account
@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form=UpdateForm()
    if form.validate_on_submit():
        # check if profile picture is part of the update
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        # update using data from form and save to db
        current_user.username=form.username.data
        current_user.email=form.email.data
        current_user.firstname=form.firstname.data
        current_user.lastname=form.lastname.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('users.account'))
    # Auto populate field with data from db if viewing page
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
        form.firstname.data=current_user.firstname
        form.lastname.data=current_user.lastname

    profile_picture=url_for('static', filename='profilepicture/'+current_user.image_file)
    return render_template('account.html', title="Account",profile_picture=profile_picture, form=form)

# FUnction to log user out
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Function to view all posts by a user
@users.route("/user/<string:username>")
def user_posts(username):
    page=request.args.get('page',1, type=int)

    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('user_posts.html', user=user, posts=posts)

@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    # Ensure users are logged out
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_email_reset(user)
        flash('An email has been sent for password reset','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    # Ensure users are logged out
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    with users.app_context():
        user=User.confirm(token=token)
    if user is None:
        flash('Invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    
    form=ResetPasswordForm()

    if form.validate_on_submit():
        hash_password=bcrypt.generate_password_hash(form.password.data).decode()
        user.password=hash_password
        db.session.commit()
        flash(f"Your password has been changed",'success')
        return redirect(url_for("users.login"))
    return render_template('reset_token.html', title='Reset Password', form=form)


# Function to view the account details of users who posted an item
@users.route("/info/<string:username>")
@login_required
def info(username):

    user=User.query.filter_by(username=username).first_or_404()
    profile_picture=url_for('static', filename='profilepicture/'+user.image_file)
    return render_template('info.html', title="Account Info",profile_picture=profile_picture, user=user)
