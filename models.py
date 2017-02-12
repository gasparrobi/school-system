from peewee import *
from flask_login import UserMixin
import datetime


# Configure your database connection here
# database name = should be your username on your laptop

db = PostgresqlDatabase('schoolsystem', user='codezero',password='codezero',host='46.101.4.131')



class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class School(BaseModel):
    name = CharField()


class User(BaseModel, UserMixin):
    login = CharField()
    password = CharField()
    role = CharField()

class Applicant(BaseModel):
    applicant_id = CharField(unique=True, null=True)
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    application_date = DateTimeField(default=datetime.datetime.now().date())
    city = CharField()
    status = CharField(default="applied")
    school = ForeignKeyField(School, related_name="applicants", null=True)
    user = ForeignKeyField(User, related_name='applicant', unique=True, null=False)


class City(BaseModel):
    city_name = CharField()
    location = ForeignKeyField(School, related_name="location")


class Mentor(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    school = ForeignKeyField(School, related_name="mentors")
    user_id = ForeignKeyField(User, related_name='mentor', unique=True, null=False)


class InterviewSlot(BaseModel):
    start = DateTimeField()
    end = DateTimeField()
    reserved = BooleanField()
    assigned_mentor = ForeignKeyField(Mentor, related_name="slot")

    class Meta:
        indexes = (
            # create a unique one from/to/date
            (('start', 'end', 'assigned_mentor'), True),
        )


class Interview(BaseModel):
    applicant = ForeignKeyField(Applicant, related_name="interview")
    slot = ForeignKeyField(InterviewSlot, related_name='interview')
