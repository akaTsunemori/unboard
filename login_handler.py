class LoginHandler:
    def __init__(self) -> None:
        self.is_logged = False
        self.hide_logged_status='hidden'
        self.hide_signup_button=''
        self.dynamic_login = 'Login'
        self.user_email=''
        self.login_redirect = '/login'

    def user_logon(self, email: str) -> None:
        self.is_logged = True
        self.hide_logged_status=''
        self.hide_signup_button='hidden'
        self.dynamic_login = 'Logout'
        self.user_email = email
        self.login_redirect = '/logout'

    def user_logout(self) -> None:
        self.is_logged = False
        self.hide_logged_status='hidden'
        self.hide_signup_button=''
        self.dynamic_login = 'Login'
        self.user_email=''
        self.login_redirect = '/login'
