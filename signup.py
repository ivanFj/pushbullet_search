import re, cgi

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

def escape(txt):
    return cgi.escape(txt, quote=True)


def validate_signup(username = "", password = "", verify = "", email = ""):
    inserts = {'username_err':'', 'password_err':'', 'verify_err':'', 'email_err':'', 'username':'', 'email':''}

    if not valid_username(username):
        inserts['username_err'] = "That is not a valid username."
    if not valid_password(password):
        inserts['password_err'] = "That is not a valid password."
    else:
        if (password != verify):
            inserts['verify_err'] = "Your passwords did not match."
    if email and not valid_email(email):
            inserts['email_err'] = "That is not a valid email."

    is_valid = True

    for value in inserts.values():
        if value:
            is_valid = False
            break

    inserts['username'] = escape(username)
    inserts['email'] = escape(email)

    if is_valid:
        return (True, username)
    else:
        return (False, inserts)