from flask import Flask, render_template, request, redirect
from os import listdir
from random import choice
from base64 import b64encode


# Project modules
from login_handler import LoginHandler
from database_handler import DatabaseHandler
from global_vars import GlobalVars
from alerts import Alerts


# Main app
app = Flask(__name__)

# Setup base64 encode filter to handle BLOB images
@app.template_filter('base64_encode')
def base64_encode(value):
    return b64encode(value).decode('utf-8')
app.jinja_env.filters['base64_encode'] = base64_encode

# Login and database handlers
database_handler = DatabaseHandler()
alerts = Alerts()
lh = LoginHandler(database_handler=database_handler, alerts=alerts)
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
    alert, alert_type = alerts.get_alert()
    return render_template(page,
        anime_image=image,
        hide_logged_status=lh.hide_logged_status,
        hide_signup_button=lh.hide_signup_button,
        hide_logged_panel=lh.hide_logged_panel,
        admin_student=lh.admin_student,
        user_email=lh.user_email,
        login_logout=lh.login_logout,
        login_redirect=lh.login_redirect,
        alert=alert,
        alert_type=alert_type,
        **kwargs)


# Conventional routes
@app.route('/')
def home():
    return render_template_util('home.html')


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
        query = request.form.get('query')
        if query:
            search_results = database_handler.search_discipline(query)
            if not search_results:
                search_results = [f'No results found for "{query}".']
    return render_template_util('disciplines.html', search_results=search_results)


@app.route('/classes', methods=['GET', 'POST'])
def classes():
    if request.method == 'POST':
        selected_class_id, selected_class = eval(request.form['button_value'])
        global_vars.set_class(selected_class)
        global_vars.set_class_id(selected_class_id)
        return redirect('/reviews')
    selected_discipline = global_vars.get_discipline()
    query_classes = database_handler.get_classes(selected_discipline)
    global_vars.set_query_results(query_classes)
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
                student_email, prof_id = to_report[0], to_report[-1]
                database_handler.report_professor_review(student_email, prof_id)
                alerts.new_alert('Professor review reported', 'success')
            elif class_to_review:
                student_email, class_id = to_report[0], to_report[-1]
                database_handler.report_class_review(student_email, class_id)
                alerts.new_alert('Class review reported', 'success')
        review = request.form.get('review')
        evaluation = request.form.get('evaluation')
        if review and not lh.is_logged:
            alerts.new_alert('In order to review, you must be logged in.', 'warning')
        else:
            if review and class_to_review:
                student_email = lh.user_email
                id = global_vars.get_class_id()
                if id:
                    database_handler.review_class(student_email, id, review, evaluation)
                alerts.new_alert('Class review added', 'success')
            elif review and professor_to_review:
                student_email = lh.user_email
                id = [i[0] for i in global_vars.get_query_results()
                    if i[1] == global_vars.get_professor()]
                if id:
                    database_handler.review_professor(student_email, *id, review, evaluation)
                alerts.new_alert('Professor review added', 'success')
    if professor_to_review:
        id = [i[0] for i in global_vars.get_query_results()
              if i[1] == global_vars.get_professor()]
        if id:
            reviews_list = database_handler.get_professorreviews(*id)
    else:
        id = global_vars.get_class_id()
        if id:
            reviews_list = database_handler.get_classreviews(id)
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
        query = request.form.get('query')
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
        if 'new_admin_button' in request.form:
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm-password']
            lh.signup_admin(email, password, confirm_password)
        if 'remove_admin_button' in request.form:
            email = request.form['email']
            confirm_email = request.form['confirm-email']
            if email != confirm_email:
                alerts.new_alert('"Email" and "Confirm email" do not match!' , 'warning')
            else:
                database_handler.remove_user(email)
                alerts.new_alert(
                    'Admin and everything linked to him removed from the database', 'success')
        if 'delete_button' in request.form:
            selected_row = eval(request.form['delete_button'])
            if 'professor_review' in selected_row:
                selected_row = selected_row['professor_review']
                student_email, prof_id = selected_row[0], selected_row[-1]
                database_handler.del_professor_review(student_email, professor_id=prof_id)
                alerts.new_alert('Professor review deleted.', 'success')
            elif 'class_review' in selected_row:
                selected_row = selected_row['class_review']
                student_email, prof_id = selected_row[0], selected_row[-1]
                database_handler.del_class_review(student_email, class_id)
                alerts.new_alert('Class review deleted.', 'success')
        if 'ban_button' in request.form:
            selected_row = eval(request.form['ban_button'])
            student_email = selected_row[0]
            database_handler.remove_user(student_email)
            alerts.new_alert(
                'User and everything linked to him removed from the database', 'warning')
        if 'remove_report_button' in request.form:
            selected_row = eval(request.form['remove_report_button'])
            if 'professor_review' in selected_row:
                selected_row = selected_row['professor_review']
                student_email, prof_id = selected_row[0], selected_row[-1]
                database_handler.del_professorreview_report(student_email, prof_id)
                alerts.new_alert('Professor review report deleted.', 'success')
            elif 'class_review' in selected_row:
                selected_row = selected_row['class_review']
                student_email, class_id = selected_row[0], selected_row[-1]
                database_handler.del_classreview_report(student_email, class_id)
                alerts.new_alert('Class review report deleted.', 'success')
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
                alerts.new_alert('Professor review deleted.', 'success')
            elif 'review' in row_to_delete:
                class_id = [i[-1] for i in global_vars.get_query_results() if i == row_to_delete['review']]
                database_handler.del_class_review(lh.user_email, *class_id)
                alerts.new_alert('Class review deleted.', 'success')
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
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        lh.user_logon(email, password)
        return redirect('/')
    return render_template_util('login.html')


@app.route('/logout')
def logout():
    lh.user_logout()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if lh.is_logged:
        return redirect('/')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        profile_picture = request.files['profile-picture']
        lh.user_signup(email, name, password, confirm_password, profile_picture)
        return redirect('/')
    return render_template_util('signup.html')


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
