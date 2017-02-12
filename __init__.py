from flask import Flask, render_template, request, url_for, redirect, flash, abort
from peewee import *
import applicant_methods
import mentor_methods
import interview_methods
import forms
import pushover
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

try:
    from forms import *
except Exception:
    from .forms import *
try:
    from models import *
except Exception:
    from .models import *
try:
    from interview_methods import *
except Exception:
    from .interview_methods import *

try:
    from applicant_methods import *
except Exception:
    from .applicant_methods import *

try:
    from mentor_methods import *
except Exception:
    from .mentor_methods import *

try:
    from pushover import *
except Exception:
    from .pushover import *


def user_list():
    array = []
    array.append(('Username', 'Password', 'Applicant name'))
    for item in User.select():
        if len(item.applicant) != 0:
            array.append((item.login, item.password, item.applicant[0].first_name))
        else:
            array.append((item.login, item.password))

    return array


def create_user(form):
    user = User.create(login=form.login.data, password=form.password.data, role='applicant')
    applicant = Applicant.create(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                                 city=str(form.city.data).lower(), user=user.id)

    Applicant_methods.assign_id_to_applicant(applicant)
    Applicant_methods.assign_school_to_applicant(applicant)
    interview_methods.assign_interview(applicant)
    msg = "{} {} just registered as an applicant! - codezero".format(applicant.first_name, applicant.last_name)
    pushover.send_pushover(msg)


def filter_redirect(choice, query):
            if choice == "last_name":
                return "filter_by_last_name"
            elif choice == "first_name":
                return "filter_by_first_name"
            elif choice == "school":
                return "filter_by_school"
            elif choice == "status":
                return "filter_by_status"


app = Flask(__name__)
app.secret_key = 'aosjndajndjansdojnasd.asdadas.d.d.1'

class_list = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(User.id == user_id)
    except DoesNotExist:
        return None


""" LOGIN - INDEX PAGE"""


@app.route('/', methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    form2 = forms.RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class

        try:
            user = User.get(form.username.data == User.login)
        except DoesNotExist:
            flash('Invalid username or password.')
            return render_template('login.html', form=form, form2=form2)
        if user.password == form.password.data:
            login_user(user)
        else:
            flash('Invalid password.')
            return render_template('login.html', form=form, form2=form2)

        # next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #    return Flask.abort(400)
        if current_user.role == 'admin':
            return redirect(url_for('homepage'))
        elif current_user.role == 'applicant':
            return redirect(url_for('user_page'))
        elif current_user.role == 'mentor':
            return redirect(url_for('mentor_page'))
        else:
            return redirect(url_for('user_page'))
    elif request.method == "POST" and form2.validate_on_submit():
        if form2.validate_on_submit():
            flash("You have successfully registered", "success")
            create_user(form2)
            return redirect(url_for("login"))
    return render_template("login.html", form=form, form2=form2)


""" ADMIN HOMEPAGE """


@app.route('/admin', methods=["GET", "POST"])
@login_required
def homepage():
    if current_user.role != 'admin':
        abort(404)
    Applicants = Applicant.select()
    Mentors = Mentor.select()
    list_length = int(len(Applicants))
    list_length2 = int(len(Mentors))
    form = forms.FilterApplicantForm()

    if request.method == "GET":
        return render_template(
                                "index2.html",
                                form=form,
                                Applicants=Applicants,
                                Mentors=Mentors,
                                list_length=list_length,
                                list_length2=list_length2
                                )

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER APPLICANTS BY FIRST NAME """


@app.route('/filter_by_first_name/<query>', methods=["GET", "POST"])
@login_required
def filter_by_first_name(query):
    if current_user.role != 'admin':
        abort(404)
    Applicants = Applicant.select().where(Applicant.first_name.contains(query))
    Mentors = Mentor.select()
    list_length = int(len(Applicants))
    list_length2 = int(len(Mentors))
    form = forms.FilterApplicantForm()
    if request.method == "GET":
        return render_template(
                                "index2.html",
                                Applicants=Applicants,
                                Mentors=Mentors,
                                list_length=list_length,
                                list_length2=list_length2,
                                form=form
                                )
    
    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER APPLICANTS BY LAST NAME """
@app.route('/filter_by_last_name/<query>', methods=["GET", "POST"])
@login_required
def filter_by_last_name(query):
    if current_user.role != 'admin':
        abort(404)
    Applicants = Applicant.select().where(Applicant.last_name.contains(query))
    Mentors = Mentor.select()
    list_length = int(len(Applicants))
    list_length2 = int(len(Mentors))
    form = forms.FilterApplicantForm()
    if request.method == "GET":
        return render_template(
                                "index2.html",
                                Applicants=Applicants,
                                Mentors=Mentors,
                                list_length=list_length,
                                list_length2=list_length2,
                                form=form
                                )
    
    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER APPLICANTS BY SCHOOL """
@app.route('/filter_by_school/<query>', methods=["GET", "POST"])
@login_required
def filter_by_school(query):
    if current_user.role != 'admin':
        abort(404)
    Applicants = Applicant.select().where(Applicant.school.name.contains(query))
    Mentors = Mentor.select()
    list_length = int(len(Applicants))
    list_length2 = int(len(Mentors))
    form = forms.FilterApplicantForm()
    if request.method == "GET":
        return render_template(
                                "index2.html",
                                Applicants=Applicants,
                                Mentors=Mentors,
                                list_length=list_length,
                                list_length2=list_length2,
                                form=form
                                )
    
    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" FILTER APPLICANTS BY FIRST STATUS """
@app.route('/filter_by_status/<query>', methods=["GET", "POST"])
@login_required
def filter_by_status(query):
    if current_user.role != 'admin':
        abort(404)
    Applicants = Applicant.select().where(Applicant.status.contains(query))
    Mentors = Mentor.select()
    list_length = int(len(Applicants))
    list_length2 = int(len(Mentors))
    form = forms.FilterApplicantForm()
    if request.method == "GET":
        return render_template(
                                "index2.html",
                                Applicants=Applicants,
                                Mentors=Mentors,
                                list_length=list_length,
                                list_length2=list_length2,
                                form=form
                                )

    elif request.method == "POST" and form.validate_on_submit():
        query = request.form.get('name')
        choice = request.form.get('options')
        url = filter_redirect(choice, query)
        return redirect(url_for(url, query=query))


""" DELETE APPLICANT """
@app.route('/delete_applicant/<app_id>', methods=["GET", "POST"])
@login_required
def delete_applicant(app_id):
    if current_user.role != 'admin':
        abort(404)
    user = Applicant.select().where(Applicant.applicant_id == app_id).get()
    if request.method == "GET":
        return "Delete is not configured yet. \
                Instead you are seeing {} {}'s \
                applicant_id: {} and role: {}".format(
                                                        user.first_name, 
                                                        user.last_name, 
                                                        user.applicant_id, 
                                                        user.user.role)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for("login"))


@app.route('/user', methods=["GET", "POST"])
@login_required
def user_page():
    return render_template("user.html", user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        if current_user.role != 'admin':
            return redirect(url_for("user_page"))
        else:
            return redirect(url_for("homepage"))
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You have successfully registered", "success")
        create_user(form)
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route('/mentor', methods=["GET", "POST"])
@login_required
def mentor_page():
    if current_user.is_authenticated:
        if current_user.role != 'mentor':
            abort(404)
    else:
        abort(404)
    mentor = Mentor.get(user_id=current_user.id)
    interviewlots = InterviewSlot.select().where(InterviewSlot.assigned_mentor == mentor.id)
    interviews = Interview.select().join(InterviewSlot).where(InterviewSlot.assigned_mentor == mentor.id)
    num_of_intvws = len(interviews)
    form = forms.AddInterviewSlot()
    if form.validate_on_submit():
        InterviewSlot.create(start=form.start.data, end=form.end.data, reserved=False, assigned_mentor=mentor.id)
        return redirect(url_for("mentor_page"))
    return render_template("mentor_site.html", interviewlots=interviewlots, interviews=interviews, form=form, mentor = mentor, num_of_intvws=num_of_intvws)


@app.route('/mentors', methods=["GET", "POST"])
@login_required
def mentors():
    LISTA = mentor_methods.get_list()
    list_length = int(len(LISTA))
    if request.method == "GET":
        return render_template("mentors.html", LISTA=LISTA, list_length=list_length, class_list=class_list)


@app.route('/users', methods=["GET", "POST"])
@login_required
def users():
    LISTA = user_list()
    list_length = int(len(LISTA))
    if request.method == "GET":
        return render_template("users.html", LISTA=LISTA, list_length=list_length, class_list=class_list)

@app.route('/interview', methods=["GET", "POST"])
@login_required
def interview():
    interviews = interview_methods.get_interviews()
    list_length = int(len(interviews))
    if request.method == "GET":
        return render_template("interviews.html", interviews=interviews, list_length=list_length, class_list=class_list)

@app.route('/try', methods=["GET", "POST"])
def tryy():
    if request.method == "GET":
        return render_template("try.html")


if __name__ == "__main__":
    app.run(debug=True)