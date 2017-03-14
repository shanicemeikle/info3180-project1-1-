"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from models import UserProfile
from werkzeug.utils import secure_filename
from time import strftime
from datetime import date, datetime

import time
#import uiud
import json
import os
from random import randint

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/secure-page/')
@login_required
def secure_page():
    """Render a secure page on our website that only logged in users can access."""
    return render_template('secure_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # if user is already logged in, just redirec them to our secure page
        # or some other page like a dashboard
        return redirect(url_for('secure_page'))

    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    # Login and validate the user.
    if request.method == 'POST' and form.validate_on_submit():
        # Query our database to see if the username and password entered
        # match a user that is in the database.
        username = form.username.data
        password = form.password.data

        user = UserProfile.query.filter_by(username=username, password=password)\
        .first()

        if user is not None:
            # If the user is not blank, meaning if a user was actually found,
            # then login the user and create the user session.
            # user should be an instance of your `User` class
            login_user(user)

            flash('Logged in successfully.', 'success')
            next = request.args.get('next')
            return redirect(url_for('secure_page'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

# route to register user
#@app.route('/forms', methods=['GET', 'POST'])
#def register():
#    form = RegistrationForm(request.form)
#    if request.method == 'POST' and form.validate():
#        user = UserProfile(form.lastname.data, form.lastname.data,
#                    form.age.data, form.bio.data, form.gender.data)
#        db.session.add(user)
#        db.session.commit()
#        flash('Thanks for registering')
 #      return redirect(url_for('home'))
    #return render_template('register.html', form=form)##

#route for creating user profile
@app.route('/profile', methods=['POST','GET'])
def profile():
    if request.method == 'POST':
        #generating userid
        userid = randint(100000,199999)
        
        #collecting form info
        f_name =request.form['fname']
        l_name =request.form['lname']
        user_name =request.form['username']
        age =request.form['age']
        gender = request.form['gender']
        biography = request.form['bio']
        
        #uploading of profie pic
        profile_image = request.files['file']
        if profile_image:
            file_folder = app.config['UPLOAD_FOLDER']
            filename = secure_filename(profile_image.filename)
            profile_image.save(os.path.join(file_folder, filename))
        #flash('File uploaded')
        
        #getting date created on
        created_on = datetime.now().strftime("%a, %d %b %Y")
        
        #inserting values into the database
        user = UserProfile(userid=userid,firstname=f_name,lastname=l_name,username=user_name,bio=biography,age=age,
        gender=gender,created_on=created_on, profile_image=profile_image.filename)
        db.session.add(user)
        db.session.commit()
        flash('Profile successfully added!!')
        return redirect(url_for('home'))
    return render_template('profile.html')
    
# route for viewing a list of all user profiles
@app.route('/profile_list2', methods=['GET', 'POST'])
def profile_list2():
    userlist=[]

    #get all profiles from database
    user = db.session.query(UserProfile).all()
    
    #checking for JSON only
    #if request.headers['Content-Type']=='application/json' or 
    if request.method == "POST":
        #create list of profiles in json format
        for user in user:
            userlist += [{'username':user.username, 'userid':user.userid}]

        return jsonify(user=userlist)
    elif request.method == 'GET':
        return render_template('profile_list2.html', user=user)

    return redirect(url_for('home'))

# route for viewing individual profile
@app.route('/profile/<userid>', methods=['GET', 'POST'])
def userprofile(userid):
    userjson={}
    #get specific profile from database
    user = UserProfile.query.filter_by(userid=userid).first()
    if request.headers.get('content-type') == 'application/json' or request.method == 'POST':
        #create json formatted data
        userjson={'userid':user.userid, 'first_name':user.firstname, 'last_name':user.lastname, 'username':user.username, 'profile_image':user.profile_image, 'gender':user.gender, 'age':user.age, 'created_on':user.created_on, 'bio':user.bio}
        return jsonify(userjson)

    elif request.method == 'GET' and user:
        return render_template('view_profile.html', user=user)

    return render_template('profile_list2.html')
    
###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
