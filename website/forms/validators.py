from wtforms.validators import ValidationError
from db import session

class Unique(object):
    """ My own validator that checks field uniqueness """
    def __init__(self, table: any, table_column: str,
                 message="Contain of this field must be unique, your information already busy."):
        self.table = table
        self.table_column = table_column
        self.message = message

    def __call__(self, form, field):
        if self.table_column == "email":
            is_busy = session.query(self.table).filter_by(email=field.data).first() if field else None
        elif self.table_column == "name":
            is_busy = session.query(self.table).filter_by(name=field.data).first() if field else None
        elif self.table_column == "title":
            is_busy = session.query(self.table).filter_by(title=field.data).first() if field else None
        if is_busy:
            raise ValidationError(self.message)


class AuthorizationEmail(object):
    """ My own validator that checks if there is a user in table with entered username """
    def __init__(self, table:any, message="Wrong email. If you aren't registered, click on button \"Sign Up\"."):
        self.table = table
        self.message = message

    def __call__(self, form, field):
        email_existence = session.query(self.table).filter_by(email=field.data).first() if field else None
        if not email_existence:
            raise ValidationError(self.message)


class AuthorizationPassword(object):
    """ My own validator that checks matching of entered password to password in database """
    def __init__(self, table, message="Wrong password! Try again."):
        self.table = table
        self.message = message

    def __call__(self, form, field):
        email = form.email.data
        email_existence = session.query(self.table).filter_by(email=email).first() if field else None
        if email_existence:
            users = session.query(self.table).all()
            for user in users:
                if user.email == email:
                    if user.password != field.data:
                        raise ValidationError(self.message)
                    return None
