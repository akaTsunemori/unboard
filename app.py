from flask import Flask, render_template, request, redirect
from os import listdir
from random import choice


# Project modules
from login_handler import LoginHandler
from database_handler import DatabaseHandler


# Main app
app = Flask(__name__)

# Setup base64 encode filter to handle BLOB images
from base64 import b64encode
@app.template_filter('base64_encode')
def base64_encode(value):
    return b64encode(value).decode('utf-8')
app.jinja_env.filters['base64_encode'] = base64_encode

# Login and database handlers
database_handler = DatabaseHandler()
lh = LoginHandler(database_handler=database_handler)

# Get random anime images from the anime dir
images = [i for i in listdir('static/images/anime') if i.endswith('.png') or i.endswith('.webp')]


# Utility for calling flask's render_template function
def render_template_util(page: str, **kwargs) -> str:
    image = choice(images)
    return render_template(page,
        anime_image=image,
        hide_logged_status=lh.hide_logged_status,
        hide_signup_button=lh.hide_signup_button,
        hide_logged_panel=lh.hide_logged_panel,
        admin_student=lh.admin_student,
        user_email=lh.user_email,
        login_logout=lh.login_logout,
        login_redirect=lh.login_redirect,
        **kwargs)


# Conventional routes
@app.route('/')
def home():
    return render_template_util('home.html', warning=lh.warning)


@app.route('/about')
def about():
    return render_template_util('about.html')


@app.route('/disciplines', methods=['GET', 'POST'])
def disciplines():
    search_results = []
    if request.method == 'POST':
        if 'button_value' in request.form:
            button_value = request.form['button_value']
            return classes(selected_discipline=button_value)
        query = request.form.get('query') # Handle the search query
        if query:
            search_results = database_handler.search_discipline(query)
            if not search_results:
                search_results = [f'No results found for "{query}".']
    return render_template_util('disciplines.html', search_results=search_results)


@app.route('/classes', methods=['GET', 'POST'])
def classes(selected_discipline: str):
    query_classes = database_handler.get_classes(selected_discipline)
    return render_template_util('classes.html', classes=query_classes)


@app.route('/professors', methods=['GET', 'POST'])
def professors():
    search_results = []
    if request.method == 'POST':
        if 'button_value' in request.form:
            button_value = request.form['button_value']
            return classes(selected_discipline=button_value) # This should return to a page with reviews for the professor
        query = request.form.get('query') # Handle the search query
        if query:
            search_results = database_handler.search_professor(query)
            if not search_results:
                search_results = [f'No results found for "{query}".']
    return render_template_util('professors.html', search_results=search_results)


@app.route('/admin')
def admin():
    if not lh.is_logged:
        return redirect('/')
    return render_template_util('admin.html')


@app.route('/student')
def student():
    if not lh.is_logged:
        return redirect('/')
    user_name, user_profile_pic = database_handler.student_data(lh.user_email)
    return render_template_util('student.html', user_name=user_name, user_profile_pic=user_profile_pic)


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
        profile_picture = request.files['profile-picture']
        lh.user_signup(email, name, password, profile_picture)
        return redirect('/')
    return render_template('signup.html', anime_image = image)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
