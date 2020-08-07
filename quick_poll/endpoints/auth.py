from flask import current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
import jwt

basic_auth = HTTPBasicAuth()
@basic_auth.verify_password
def verify_password(username, password):
    if not current_app.config.get("QUICKPOLL_SIMPLE_AUTH", True):
        return False

    if username != "" and username != None:
        return User(
            id = username,
            username = username,
            roles = ["editor"]
        )
    return False

@basic_auth.get_user_roles
def get_user_roles(user):
    return user.roles

basic_token_auth = HTTPTokenAuth('Bearer')
@basic_token_auth.verify_token
def verify_token(token):
    public_key = current_app.config.get("QUICKPOLL_PUBLIC_KEY")
    algorithm = current_app.config.get("QUICKPOLL_ALGORITHM", "RS512")

    if not public_key:
        return False

    try:
        data = jwt.decode(token, public_key, algorithm=algorithm)
    except:
        try:
            print(jwt.get_unverified_header(token))
            print(jwt.decode(token, verify = False))
        except:
            pass

        return False

    try:
        return User(
            id = data["id"],
            username = data.get("username"),
            roles = data.get("roles", [])
        )
    except:
        return False

@basic_token_auth.get_user_roles
def get_user_roles(user):
    return user.roles

class User():
    def __init__(self, id: str, username: str, roles: [str]):
        self.id = id or ""
        self.username = username or ""
        self.roles = roles or []

auth = MultiAuth(basic_auth, basic_token_auth)