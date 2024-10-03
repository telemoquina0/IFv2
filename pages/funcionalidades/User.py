from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .funcsifv2 import funcsif
import dash

class Usuario(UserMixin):
    def __init__(self, name, password):
        self.id=name
        self.name = name
        self.password = password
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def get_id(self):
        return self.id
    def __repr__(self):
        return '<Usuario {}>'.format(self.name)
   


def get_user(name):
    p=funcsif()
    password= p.get_pw(name)
    if password is None:
        return None
    else:
        return Usuario(name,password)
    
restricted_page = {}

def require_login(page):
    for pg in dash.page_registry:
        if page == pg:
            restricted_page[dash.page_registry[pg]['path']] = True

def dame_sesion():
    if current_user.is_authenticated:
        return f'{current_user.name}'
    else:
        return "Sin sesión"

