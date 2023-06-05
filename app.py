from flask import Flask, render_template, request, redirect
from os import listdir
from random import choice


# Project modules
from login_handler import LoginHandler


# Main app
app = Flask(__name__)

# Login handler
lh = LoginHandler()

# Get random anime images from the anime dir
images = [i for i in listdir('static/images/anime') if i.endswith('.png') or i.endswith('.webp')]


# Utility for calling flask's render_template function
def render_template_util(page: str) -> str:
    image = choice(images)
    return render_template(page,
        anime_image=image,
        hide_logged_status=lh.hide_logged_status,
        hide_signup_button=lh.hide_signup_button,
        hide_logged_panel=lh.hide_logged_panel,
        admin_student=lh.admin_student,
        user_email=lh.user_email,
        login_logout=lh.login_logout,
        login_redirect=lh.login_redirect)


# Conventional routes
@app.route('/')
def home():
    return render_template_util('home.html')


@app.route('/about')
def about():
    return render_template_util('about.html')


@app.route('/classes')
def classes():
    return render_template_util('classes.html')


@app.route('/ranking')
def ranking():
    return render_template_util('ranking.html')


@app.route('/admin')
def admin():
    return render_template_util('admin.html')


@app.route('/student')
def student():
    return render_template_util('student.html')


# Login, logout and signup routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if lh.is_logged:
        return redirect('/')
    image = choice(images)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        lh.user_logon(email, password)
        print(email, password) # Now I have the inputs from email and passwd
        return redirect('/')
    return render_template('login.html', anime_image = image)


@app.route('/logout')
def logout():
    lh.user_logout()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if lh.is_logged:
        return redirect('/')
    image = choice(images)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        print(name, email, password) # Now I have the inputs from name, email and passwd
    return render_template('signup.html', anime_image = image)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
