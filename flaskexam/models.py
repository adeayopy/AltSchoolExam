from flaskexam import db, login_manager,app
from datetime import datetime
from flask_login import UserMixin
import jwt
import datetime as dt

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return User.query.get(int(user_id))

# User model
class User(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    firstname=db.Column(db.String(120), nullable=False)
    lastname=db.Column(db.String(120), nullable=False)
    image_file=db.Column(db.String(20), nullable=False,default='default.jpg')
 
    password=db.Column(db.String(60), nullable=False)
    # This attribute defines the relationship with the Post model
    # backref Looks like adding another column to the Post model
    # when we have a post we can use the author attribute to get the user who created the post
    # with lazy, we can get all posts created by a user all at once
    # ('Address',
    #                             backref=db.backref('author', lazy='joined'), 
    #                             lazy='dynamic')
    posts=db.relationship('Post', backref=db.backref('author', lazy='joined'), 
                                lazy='dynamic')

    # method to generate token for password reset
    def generate_confirmation_token(self, expiration=1800):
        reset_token = jwt.encode(
            {
                "confirm": self.id,
                "exp": dt.datetime.now(tz=dt.timezone.utc)
                       + dt.timedelta(seconds=expiration)
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token
    # method to verify/validate token
    @staticmethod
    def confirm(token):
        try:
            user_id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                leeway=dt.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None
        with app.app_context():
            use=user_id.get('confirm')
        return User.query.get(use)



    def __repr__(self) -> str:
        return f"User('{self.username}','{self.email}','{self.image_file}')"

# Post model 
class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    # Referencing tablename user and column name id
    # Different from the relationship in Post because we are refencing the class there
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
    def __repr__(self) -> str:
        return f"Post('{self.title}','{self.date_posted}')"
