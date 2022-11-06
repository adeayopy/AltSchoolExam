from flask import Blueprint, render_template, request
from flaskexam.models import Post

main=Blueprint('main',__name__)

@main.route('/')
@main.route("/home")
def home():
    page=request.args.get('page',1, type=int)
    # with main.app_context():
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', posts=posts)

