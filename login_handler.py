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
        self.hide_admin_panel = 'hidden'
        self.dynamic_login = 'Login'
        self.user_email=''
        self.login_redirect = '/login'

    def user_logon(self, email: str, password: str) -> None:
        if email not in users:
            raise LoginError('User does not exist in the database')
        if users[email][0] != password:
            raise LoginError('Wrong password')
        if users[email][1]:
            self.admin_logon()
        self.is_logged = True
        self.hide_logged_status=''
        self.hide_signup_button='hidden'
        self.dynamic_login = 'Logout'
        self.user_email = email
        self.login_redirect = '/logout'

    def admin_logon(self) -> None:
        self.is_admin = True
        self.hide_admin_panel = ''

    def user_logout(self) -> None:
        self.is_admin = False
        self.is_logged = False
        self.hide_logged_status='hidden'
        self.hide_signup_button=''
        self.hide_admin_panel = 'hidden'
        self.dynamic_login = 'Login'
        self.user_email=''
        self.login_redirect = '/login'

