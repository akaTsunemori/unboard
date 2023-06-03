from flask import Flask, render_template, request
from os import listdir
from random import choice


app = Flask(__name__)
images = [i for i in listdir('static/images/anime') if i.endswith('.png') or i.endswith('.webp')]


@app.route('/')
def home():
    image = choice(images)
    return render_template('home.html', anime_image = image)

@app.route('/about')
def about():
    image = choice(images)
    return render_template('about.html', anime_image = image)

@app.route('/classes')
def classes():
    image = choice(images)
    return render_template('classes.html', anime_image = image)

@app.route('/ranking')
def ranking():
    image = choice(images)
    return render_template('ranking.html', anime_image = image)

@app.route('/login', methods=['GET', 'POST'])
def login():
    image = choice(images)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password) # Now I have the inputs from email and passwd
    return render_template('login.html', anime_image = image)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    image = choice(images)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        print(name, email, password) # Now I have the inputs from name, email and passwd
    return render_template('signup.html', anime_image = image)

if __name__ == '__main__':
    app.run(debug=True)
