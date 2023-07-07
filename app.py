from flask import Flask, render_template, request, redirect
from os import listdir
from random import choice
from base64 import b64encode


# Project modules
from login_handler import LoginHandler
from database_handler import DatabaseHandler
from global_vars import GlobalVars


# Main app
app = Flask(__name__)

# Setup base64 encode filter to handle BLOB images
@app.template_filter('base64_encode')
def base64_encode(value):
    return b64encode(value).decode('utf-8')
app.jinja_env.filters['base64_encode'] = base64_encode

# Login and database handlers
database_handler = DatabaseHandler()
lh = LoginHandler(database_handler=database_handler)
global_vars = GlobalVars()

# Get random anime images from the anime dir
images = [i for i in listdir('static/images/anime') if i.endswith('.png') or i.endswith('.webp')]


def render_template_util(page: str, **kwargs) -> str:
    '''
    Utility for calling flask's render_template function with fixed arguments,
    additional arguments are allowed.

    Returns a str, the same as flask's render_template function does.
    '''
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
            selected_discipline = request.form['button_value']
            global_vars.set_discipline(selected_discipline)
            return redirect('/classes')
        query = request.form.get('query') # Handle the search query
        if query:
            search_results = database_handler.search_discipline(query)
            if not search_results:
                search_results = [f'No results found for "{query}".']
    return render_template_util('disciplines.html', search_results=search_results)


@app.route('/classes', methods=['GET', 'POST'])
def classes():
    if request.method == 'POST':
        selected_class = request.form['button_value']
        global_vars.set_class(selected_class)
        return redirect('/reviews')
    selected_discipline = global_vars.get_discipline()
    query_classes = database_handler.get_classes(selected_discipline)
    global_vars.set_query_results(query_classes)
    query_classes = [(i[0], i[3], i[4], i[5]) for i in query_classes]
    return render_template_util('classes.html', classes=query_classes)


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    class_to_review      = global_vars.get_class()
    discipline_to_review = global_vars.get_discipline()
    professor_to_review  = global_vars.get_professor()
    if request.method == 'POST':
        if 'report_button' in request.form:
            to_report = eval(request.form['report_button'])
            if professor_to_review:
                student_email, prof_id = to_report[0], to_report[2]
                database_handler.report_professor_review(student_email, prof_id)
            elif class_to_review:
                student_email, class_id = to_report[0], to_report[2]
                database_handler.report_class_review(student_email, class_id)
        review = request.form.get('review')
        if review and class_to_review:
            student_email = lh.user_email
            id = [i[2] for i in global_vars.get_query_results()
                  if i[4] == global_vars.get_class()]
            if id:
                database_handler.review_class(student_email, *id, review)
        elif review and professor_to_review:
            student_email = lh.user_email
            id = [i[0] for i in global_vars.get_query_results()
                  if i[1] == global_vars.get_professor()]
            if id:
                database_handler.review_professor(student_email, *id, review)
    if professor_to_review:
        id = [i[0] for i in global_vars.get_query_results()
              if i[1] == global_vars.get_professor()]
        if id:
            reviews_list = database_handler.get_professorreviews(*id)
    else:
        id = [i[2] for i in global_vars.get_query_results()
              if i[4] == global_vars.get_class()]
        if id:
            reviews_list = database_handler.get_classreviews(*id)
    return render_template_util('reviews.html',
                is_logged=lh.is_logged,
                class_to_review=class_to_review,
                discipline_to_review=discipline_to_review,
                professor_to_review=professor_to_review,
                reviews_list=reviews_list)


@app.route('/professors', methods=['GET', 'POST'])
def professors():
    search_results = []
    if request.method == 'POST':
        if 'button_value' in request.form:
            selected_professor = request.form['button_value']
            global_vars.set_professor(selected_professor)
            return redirect('/reviews')
        query = request.form.get('query') # Handle the search query
        if query:
            search_results = database_handler.search_professor(query)
            global_vars.set_query_results(search_results)
            if not search_results:
                search_results = [f'No results found for "{query}".']
            else:
                search_results = [i[1] for i in search_results]
    return render_template_util('professors.html', search_results=search_results)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not lh.is_logged:
        return redirect('/')
    if not lh.is_admin:
        return redirect('/')
    if request.method == 'POST':
        if 'delete_button' in request.form:
            selected_row = request.form['delete_button']
        if 'ban_button' in request.form:
            selected_row = request.form['ban_button']
        if 'remove_report_button' in request.form:
            selected_row = request.form['remove_report_button']
        print(selected_row)
    professor_reviews_reports = [i for i in database_handler.get_professorreviews_reports() if i]
    class_reviews_reports = [i for i in database_handler.get_classreviews_reports() if i]
    return render_template_util('admin.html',
                professor_reviews_reports=professor_reviews_reports,
                class_reviews_reports=class_reviews_reports)


@app.route('/student', methods=['GET', 'POST'])
def student():
    if not lh.is_logged:
        return redirect('/')
    if request.method == 'POST':
        if 'edit-profile' in request.form:
            return redirect('/edit-profile')
        if 'button_delete' in request.form:
            row_to_delete = eval(request.form['button_delete'])
            if 'professor' in row_to_delete:
                database_handler.del_professor_review(lh.user_email, row_to_delete['professor'])
            elif 'review' in row_to_delete:
                class_id = [i[-1] for i in global_vars.get_query_results() if i == row_to_delete['review']]
                database_handler.del_class_review(lh.user_email, *class_id)
    student_email = lh.user_email
    user_name, user_profile_pic = database_handler.student_data(student_email)
    first_name = user_name.split()[0]
    personal_information = [user_name, student_email]
    professor_reviews = database_handler.student_professor_reviews(student_email)
    class_reviews = database_handler.student_class_reviews(student_email)
    global_vars.set_query_results(class_reviews)
    return render_template_util('student.html',
                user_name=first_name,
                user_profile_pic=user_profile_pic,
                personal_information=personal_information,
                professor_reviews=professor_reviews,
                class_reviews=class_reviews)


# Student profile authentication and information routes
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
    return render_template('login.html', anime_image=image)


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
        confirm_password = request.form['confirm-password']
        profile_picture = request.files['profile-picture']
        lh.user_signup(email, name, password, confirm_password, profile_picture)
        return redirect('/')
    return render_template('signup.html', anime_image=image)


@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if not lh.is_logged:
        return redirect('/')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        profile_picture = request.files['profile-picture']
        lh.user_edit(email, name, password, confirm_password, profile_picture)
        return redirect('/')
    return render_template_util('edit-profile.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
