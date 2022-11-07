# Flask exam

## Introduction

The flaskexam program is a basic blog that allows different users to create, login and logout of their accounts. It also allows users to view profile and  posts by different users. Moreover, users can edit their own post.

## Requirements

python version  >=  3.8.10

To run program, clone repository, using `git clone https://github.com/adeayopy/AltSchoolExam`

Create virtual and activate environment using

Windows
`python3 -m venv \path\to\new\virtual\environment`
`\path\to\new\virtual\environment\Scripts\activate.bat`
 
Linux
`python3 -m venv /path/to/new/virtual/environment`
`source /path/to/new/virtual/environment/bin/activate`


Download required dependencies using 

`pip install -r requirements.txt`

To use the change password feature by users, ensure the environment variable name in __init__.py matches with your environment variable file or pass them as strings directly
`app.config['MAIL_USERNAME']=os.environ.get('EMAIL')`
`app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASSWORD')`

Run blog using 

`python run.py`

Follow instructions on terminal to access server
