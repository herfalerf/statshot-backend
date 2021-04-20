from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("username", validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=4, max=25)])

class LoginForm(FlaskForm):
    """Form for validating user login"""

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])

class PrefsForm(FlaskForm):
    """Form for settings user preferences"""

    fav_team_id = int
