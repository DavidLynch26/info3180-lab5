# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, TextAreaField
from flask_wtf.file import FileAllowed, FileRequired, FileField

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[InputRequired()])
    description = TextAreaField('Movie Description', validators=[InputRequired()])
    poster = FileField('Movie Poster', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png'], 'Images only!')])