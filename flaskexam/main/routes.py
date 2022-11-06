from flask import Blueprint, render_template, request
from flaskexam.models import Post

main=Blueprint('main',__name__)


@main.route('/')
@main.route("/home")
# Home route to display all posts. Uses pagination to display posts
def home():
    #  Query 'page' in url and set default page to 1
    page=request.args.get('page',1, type=int)
    # Query all posts with 5 pages per page in and descending order 
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', posts=posts)

