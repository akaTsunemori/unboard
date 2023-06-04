from flask import Flask, render_template, request, redirect
from os import listdir
from random import choice

from login_handler import LoginHandler


# Main app
app = Flask(__name__)

# Login handler
lh = LoginHandler()

# Get random anime images from the anime dir
images = [i for i in listdir('static/images/anime') if i.endswith('.png') or i.endswith('.webp')]


@app.route('/')
def home():
    image = choice(images)
    return render_template('home.html',
        anime_image=image,
        hide_logged_status=lh.hide_logged_status,
        hide_signup_button=lh.hide_signup_button,
        user_email=lh.user_email,
        dynamic_login=lh.dynamic_login,
        login_redirect=lh.login_redirect)


@app.route('/about')
def about():
    image = choice(images)
    return render_template('about.html',
        anime_image=image,
        hide_logged_status=lh.hide_logged_status,
        hide_signup_button=lh.hide_signup_button,
        user_email=lh.user_email,
        dynamic_login=lh.dynamic_login,
        login_redirect=lh.login_redirect)


@app.route('/classes')
def classes():
    image = choice(images)
    return render_template('classes.html',
        anime_image=image,
        hide_logged_status=lh.hide_logged_status,
        hide_signup_button=lh.hide_signup_button,
        user_email=lh.user_email,
        dynamic_login=lh.dynamic_login,
        login_redirect=lh.login_redirect)


@app.route('/ranking')
def ranking():
    image = choice(images)
    return render_template('ranking.html',
        anime_image=image,
        hide_logged_status=lh.hide_logged_status,
        hide_signup_button=lh.hide_signup_button,
        user_email=lh.user_email,
        dynamic_login=lh.dynamic_login,
        login_redirect=lh.login_redirect)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if lh.is_logged:
        return redirect('/')
    image = choice(images)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        lh.user_logon(email)
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


if __name__ == '__main__':
    app.run(debug=True)
