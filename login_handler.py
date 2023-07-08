from database_handler import DatabaseHandler
from alerts import Alerts


class LoginHandler():
    '''
    I'm not using Flask's login handler since it uses SQLAlchemy and using it would mean
    the SQL queries would be implicit. This login handler is a very basic and messy way
    to do it, and even then, I could make this better if I had the time.
    '''
    def __init__(self, database_handler: DatabaseHandler, alerts: Alerts) -> None:
        self.is_admin = False
        self.is_logged = False
        self.hide_logged_status='hidden'
        self.hide_signup_button=''
        self.hide_logged_panel = 'hidden'
        self.login_logout = 'Login'
        self.admin_student = 'student'
        self.user_email=''
        self.login_redirect = '/login'
        self.database_handler = database_handler
        self.alerts = alerts

    def user_logon(self, email: str, password: str) -> None:
        if email == 'admin@unb.br' and password == 'admin':
            self.is_admin = True
            self.admin_student = 'admin'
        else:
            login_sucess = self.database_handler.login(email, password)
            if not login_sucess:
                self.alerts.new_alert(
                    "Login failure! Check that you've entered valid information.",
                    'warning')
                return
            else:
                self.alerts.new_alert(
                    f'Logged in with account {email}. Have fun!',
                    'success')
        self.is_logged = True
        self.hide_logged_status=''
        self.hide_signup_button='hidden'
        self.hide_logged_panel = ''
        self.login_logout = 'Logout'
        self.user_email = email
        self.login_redirect = '/logout'

    def user_logout(self) -> None:
        self.is_admin = False
        self.is_logged = False
        self.hide_logged_status='hidden'
        self.hide_signup_button=''
        self.hide_logged_panel = 'hidden'
        self.login_logout = 'Login'
        self.admin_student = 'student'
        self.user_email=''
        self.login_redirect = '/login'
        self.alerts.new_alert(
            'Logged out.', 'success')

    def user_signup(self, email: str, name: str, password: str, confirm_password, profile_pic) -> None:
        if password != confirm_password:
            self.alerts.new_alert(
                '"Password" and "Confirm password" do not match!',
                'warning')
            return
        signup_success = self.database_handler.signup(email, name, password, profile_pic)
        if not signup_success:
            self.alerts.new_alert(
                'Sign up failure! Check that you\'ve entered valid information.',
                'warning')
        else:
            self.alerts.new_alert(
                'Sign up success! You can now login with your account.',
                'success')


    def user_edit(self, email: str, name: str, password: str, confirm_password: str, profile_pic) -> None:
        if password != confirm_password:
            self.alerts.new_alert(
                '"Password" and "Confirm password" do not match!',
                'warning')
            return
        edit_success = self.database_handler.edit_personal_info(self.user_email, email, name, password, profile_pic)
        if not edit_success:
            self.alerts.new_alert(
                'Failure when editing profile! Check that you\'ve entered valid information.',
                'warning')
        else:
            self.alerts.new_alert(
                'Success editing profile!',
                'success')