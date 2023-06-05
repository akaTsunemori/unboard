from stub_database import users


class LoginError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


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

    def user_logon(self, email: str, password: str) -> None:
        if email not in users:
            raise LoginError('User does not exist in the database')
        if users[email][0] != password:
            raise LoginError('Wrong password')
        if users[email][1]:
            self.is_admin = True
            self.admin_student = 'admin'
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

