import dash
from dash import Dash, dcc, html #, DiskcacheManager, CeleryManager
import dash_bootstrap_components as dbc
from flask import Flask, request, redirect, session, url_for, Response
from flask_login import login_user, LoginManager, current_user, logout_user
from flask_session import Session
from pages.funcionalidades.funcsifv2 import funcsif
from pages import home, logout, tallas_evol, gen_evol, diff_despesques, resultado, settings
from pages.funcionalidades.User import get_user, require_login
from pages.funcionalidades.myfunc import escribir_log
import os



options = {'encoding': 'UTF-8'}

CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


## Diskcache
#if 'REDIS_URL' in os.environ:
#    # Use Redis & Celery if REDIS_URL set as an env variable
#    from celery import Celery
#    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
#    background_callback_manager = CeleryManager(celery_app)


#else:
#    # Diskcache for non-production apps when developing locally
#    import diskcache
#    cache = diskcache.Cache("./cache")
#    background_callback_manager = DiskcacheManager(cache)


server = Flask(__name__, instance_relative_config=True)


app = Dash(__name__,
        server=server,
        #background_callback_manager = background_callback_manager,
        use_pages=True,
        pages_folder='pages',
        assets_folder='static',
        suppress_callback_exceptions=True,
        external_scripts=[{
            'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js',
            'integrity': 'sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm',
            'crossorigin': 'anonymous'
        }],
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME,{
            'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css',
            'integrity': 'sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9',
            'crossorigin': 'anonymous',
            'rel': 'stylesheet'
        },
        {
            'href': 'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
            'rel': 'stylesheet'
        }]
    )

dash.register_page('pages.homepage',
    path='/',
    title='Login',
    name='Login',
    layout=home.layout)
dash.register_page('pages.logout',
    path='/logout',
    title='Logout',
    name='Logout',
    layout=logout.layout)
dash.register_page('pages.settings',
    path='/settings',
    title='Settings',
    name='Settings',
    layout=settings.layout)
dash.register_page('pages.gen_evol',
    path='/gen_evol',
    title='Evolución de generaciones',
    name='Evolución de generaciones',
    layout=gen_evol.layout)
dash.register_page('pages.tallas_evol',
    path='/tallas_evol',
    title='Evolución de tallas',
    name='Evolución de tallas',
    layout=tallas_evol.layout)
dash.register_page('pages.resultado',
    path='/resultado',
    title='Resultado',
    name='Resultado',
    layout=resultado.layout)
dash.register_page('pages.diff_despesques',
    path='/diff_despesques',
    title='Diferencial de despesques',
    name='Diferencial de despesques',
    layout=diff_despesques.layout)


@server.route('/', methods=['POST'])
def login_button_click():
    if request.form:
        username = request.form['username'].upper()
        password = request.form['password'].upper()
        user = get_user(username)
        if user is not None and user.check_password(password):
            login_user(user)
            session['username'] = username
            escribir_log('info', f"{session['username']} :{username} logueado")
            escribir_log('info',f"inicio de sesión: {session['username']} ")
            if 'url' in session:
                if session['url']:
                    url = session['url']
                    session['url'] = None
                    return redirect(url) ## redirect to target url
            return redirect('/settings') ## redirect to home
        escribir_log('info', "intento de conexión fallida")
        return  Response('<p>Usuario o contraseña incorrecta. Haga <a href="/">login</a> para operar</p>')
    #html.Div(["Usuario o contraseña incorrecta. Haga ", dcc.Link("login", href="/"), " para operar"], className='text-center') # En linux no vale

#Esta función se define después de registrar
#la página de logout para que el programa 
#no lo confunda
@server.route('/logout')
def logout():
    if current_user.is_authenticated:
        escribir_log('info', f"{session['username']} : {current_user.name} deslogueado")
        logout_user()
        #session.pop('username', None)
        session.clear()
    return redirect(url_for('/'))


# Updating the Flask Server configuration with Secret Key to encrypt the user session cookie
os.chdir(os.path.dirname(os.path.abspath(__file__))) #Hay que poner el directorio donde se encuentra main 
server.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))
server.config['SESSION_TYPE'] = 'filesystem' 
Session(server)

# Login manager object will be used to login / logout users
login_manager = LoginManager(server)
login_manager.init_app(server)
login_manager.login_view = "/"

@login_manager.user_loader
def load_user(user_name):
    p=funcsif()
    users=p.dame_usuarios(False).to_list()
    for user in users:
        if user==user_name:
            return get_user(user_name)
    return None



require_login('pages.settings')
require_login('pages.gen_evol')
require_login('pages.tallas_evol')
require_login('pages.resultado')
require_login('pages.diff_despesques')

p=funcsif()
p.crear_carpetas()

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=False)