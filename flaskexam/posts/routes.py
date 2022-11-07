from flask import Blueprint, redirect, url_for, flash, render_template, abort, request
from flaskexam import db
from flask_login import current_user, login_required
from flaskexam.models import Post
from flaskexam.posts.forms import PostForm 

posts=Blueprint('posts',__name__)


@posts.route('/post/new',methods=['GET','POST'])
@login_required
# Functionality for new posts 
def new_post():
    form=PostForm() # Initialize postform
    if form.validate_on_submit():
        # write data from form to db
        post=Post(title=form.title.data, content=form.post_content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title="New Post", form=form, legend='New Post')

@posts.route('/post/<int:post_id>',methods=['GET','POST'])
@login_required
def post(post_id):
    # with posts.app_context():
    post=Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# Functionality to update post
@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        
        # print(form.title.data)
        # post.update(dict(title=form.title.data))
        post.content=form.post_content.data
        db.session.commit()

        flash('Your post has been updated','success')
        return redirect(url_for('posts.post',post_id=post.id))
    # Automatically populate field with data 
    elif request.method=='GET':
        form.title.data=post.title
        form.post_content.data=post.content
    return render_template('create_post.html', title="Update Post", form=form, legend='Update Post')

#  FUnctionality to delete post
@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    # Query post by id
    post=Post.query.get_or_404(post_id)
    # Vheck if it is the writer of the post performing the delete operation. Abort if not
    if post.author!=current_user:
        abort(403)
    # Delete post from sb
    with posts.app_context():
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted','success')
        return redirect(url_for('main.home'))
