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
        self.user_email=''
        self.database_handler = database_handler
        self.alerts = alerts

    def user_logon(self, email: str, password: str) -> None:
        login_status, is_admin = self.database_handler.login(email, password)
        if not login_status:
            self.alerts.new_alert(
                "Login failure! Check that you've entered valid information.",
                'failure')
            return
        else:
            self.alerts.new_alert(
                f'Logged in with account {email}. Have fun!',
                'success')
        self.is_admin = is_admin
        self.is_logged = True
        self.user_email = email

    def user_logout(self, alert: str = None) -> None:
        self.is_admin = False
        self.is_logged = False
        self.user_email=''
        if not alert:
            self.alerts.new_alert(
                'Logged out.', 'warning')
        else:
            self.alerts.new_alert(
                alert, 'warning')

    def user_signup(self, email: str, name: str, password: str, confirm_password: str, course: str, id: int, profile_pic) -> None:
        if password != confirm_password:
            self.alerts.new_alert(
                '"Password" and "Confirm password" do not match!',
                'failure')
            return
        id_str = str(id)
        if not id_str.isnumeric():
            self.alerts.new_alert(
                'Registration ID can\'t contain letters!',
                'failure')
            return
        signup_success = self.database_handler.signup(email, name, password, False, course, id, profile_pic)
        if not signup_success:
            self.alerts.new_alert(
                'Sign up failure! Check that you\'ve entered valid information.',
                'failure')
        else:
            self.alerts.new_alert(
                'Sign up success! You can now login with your account.',
                'success')

    def manage_admin(self, email: str, confirm_email: str, is_admin: bool) -> None:
        if email != confirm_email:
            self.alerts.new_alert(
                'Emails do not match!',
                'failure')
            return
        promotion_status = self.database_handler.manage_admin(email, is_admin)
        if not promotion_status:
            self.alerts.new_alert(
                'Admin management failure! Check that you\'ve entered valid information.',
                'failure')
        else:
            self.alerts.new_alert(
                'Admin management done.',
                'warning')

    def user_edit(self, email: str, name: str, password: str, confirm_password: str, course: str, id: int, profile_pic) -> None:
        if password != confirm_password:
            self.alerts.new_alert(
                '"Password" and "Confirm password" do not match!',
                'failure')
            return False
        if id:
            id_str = str(id)
            if not id_str.isnumeric():
                self.alerts.new_alert(
                    'Registration ID can\'t contain letters!',
                    'failure')
                return False
        edit_success = self.database_handler.edit_personal_info(self.user_email, email, name, password, course, id, profile_pic)
        if not edit_success:
            self.alerts.new_alert(
                'Failure when editing profile! Check that you\'ve entered valid information.',
                'failure')
            return False
        return True