from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# Class to hold forms for posting content
class PostForm(FlaskForm):
    title=StringField('Title',
    validators=[DataRequired()])
    post_content=TextAreaField('Content',
    validators=[DataRequired()])
    submit=SubmitField('Post')

 