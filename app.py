from flask import Flask, render_template, request
from os import listdir

app = Flask(__name__)

@app.route('/')
def home():
    image = [i for i in listdir('static/images') if i.endswith('.png')][0]
    return render_template('home.html', anime_image = image)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password) # Now I have the inputs from name, email and passwd
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        print(name, email, password) # Now I have the inputs from name, email and passwd
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
