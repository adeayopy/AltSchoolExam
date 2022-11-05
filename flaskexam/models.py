from flaskexam import db, login_manager,app
from datetime import datetime
from flask_login import UserMixin
import jwt
import datetime as dt

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
