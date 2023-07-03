from threading import Timer
from database_handler import DatabaseHandler


class LoginHandler:
    def __init__(self) -> None:
        self.is_admin = False
        self.is_logged = False
        self.hide_logged_status='hidden'
        self.hide_signup_button=''
        self.hide_logged_panel = 'hidden'
        self.login_logout = 'Login'
        self.admin_student = 'student'
        self.user_email=''
        self.login_redirect = '/login'
        self.database_handler = DatabaseHandler()
        self.warning = ''

    def user_logon(self, email: str, password: str) -> None:
        if email == 'admin@unb.br' and password == 'admin':
            self.is_admin = True
            self.admin_student = 'admin'
        login_sucess = self.database_handler.login(email, password)
        if not login_sucess:
            self.warning = 'Login failure! Check that you\'ve entered valid information.'
            Timer(2.5, self.__reset_warning).start()
            return
        self.warning = ''
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
        self.admin_student = 'Student'
        self.user_email=''
        self.login_redirect = '/login'
        self.warning = ''

    def user_signup(self, email: str, name: str, password: str, profile_pic) -> None:
        signup_sucess = self.database_handler.signup(email, name, password, profile_pic)
        if not signup_sucess:
            self.warning = 'Sign up failure! Check that you\'ve entered valid information.'
            Timer(2.5, self.__reset_warning).start()
            return
        self.warning = ''

    def __reset_warning(self) -> None:
        self.warning = ''

