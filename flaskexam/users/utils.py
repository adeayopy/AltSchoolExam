import os, secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskclass import app, mail
# from flaskclass.users.routes import users


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    fname,fext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+fext
    picture_path=os.path.join(app.root_path, 'static/profilepicture',picture_fn)
    
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_email_reset(user):
    token=user.generate_confirmation_token()
    msg=Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body=f''' 
    To reset your passrod, visit:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request, ignore this email'''
    mail.send(msg)
    