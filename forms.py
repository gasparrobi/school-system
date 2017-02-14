from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

try:
    from models import User, Applicant, City
except Exception:
    from .models import User, Applicant, City


# from models import User


def username_exists(form, field):
    if User.select().where(User.login == field.data).exists():
        raise ValidationError("User already exists")


def email_exists(form, field):
    if Applicant.select().where(Applicant.email == field.data).exists():
        raise ValidationError("Email already exists")


def city_exist(form, field):
    if City.select().where(City.city_name == str(field.data).lower()).exists() == False:
        raise ValidationError("There is no such city")


class AddInterviewSlot(Form):
    start = StringField(
        "Starting Date"
    )
    end = StringField(
        "End Date"
    )

class RegisterForm(Form):
    login = StringField(
        "Username",
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]+$',
                   message=("Username should be one word, letters, "
                            "numbers, and underscores only.")
                   ),
            username_exists
        ])

    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]+$',
                   message=("Username should be one word, letters, "
                            "numbers, and underscores only.")
                   )
        ])
    last_name = StringField(
        "Last name",
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]+$',
                   message=("Username should be one word, letters, "
                            "numbers, and underscores only.")
                   )
        ])
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])

    city = StringField(
        "City",
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]+$',
                   message=("Username should be one word, letters, "
                            "numbers, and underscores only.")
                   ),
            city_exist
        ])

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo("password2", message="Passwords must match")])
    password2 = PasswordField(
        "Confirm Password",
        validators=[DataRequired()])


class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class FilterApplicantForm(Form):
    name = StringField("name", validators=[DataRequired()])
    options = SelectField("options", choices=[
                                                ("first_name","Filter by First Name"), 
                                                ("last_name","Filter by Last Name"),
                                                ("school","Filter by School"),
                                                ("status","Filter by Status"),
                                                ])


class UpdateApplicantForm(Form):
    email = StringField("update_email", validators=[DataRequired()])












