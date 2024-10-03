import dash_bootstrap_components as dbc
from dash import html, get_asset_url, Input, Output, State, clientside_callback, dcc
from .funcionalidades.funcsifv2 import funcsif
from .funcionalidades.myfunc import escribir_log
from .funcionalidades.User import dame_sesion
from flask_login import current_user

def dame_icono(user):
    escribir_log('info', dame_sesion()+': función dame_icono')
    p=funcsif()
    p.inicializar(user)
    especie=p.get_attr("especie")
    if especie=="SOLE":
        return "lenguado blanco.png", 26
    else:
        return "rodaballo blanco.png", 48
    

def get_sidebar(active_item=None):
    escribir_log('info', dame_sesion()+': función get_sidebar')
    if current_user.is_authenticated:
        user=current_user.name
    else:
        user="Default"
    imagen, alto=dame_icono(user)
    nav = html.Nav(id="sidebar", className="active", children=[
        html.Div(className="custom-menu", children=[
            html.Button([
                html.I(className="fa fa-bars"),
                html.Span("Toggle Menu", className="sr-only")
            ], type="button", id="sidebarCollapse", className="btn btn-primary")
        ]),
        html.Div(className="flex-column p-4 nav nav-pills", children=[
            html.A([
                html.Img(src=get_asset_url(path=imagen), alt='', width=48, height=alto, className='mx-2'),
                html.Span("IF v2.0", className='fs-4'),
            ], className='d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none', href='/'),
            html.Hr(),
            dbc.NavItem(dbc.NavLink("Login", href="/", className='text-white', active=True if active_item=='pages.home' else False)),
            dbc.NavItem(dbc.NavLink("Logout", href="/logout", className='text-white', active=True if active_item=='pages.logout' else False)),
            dbc.NavItem(dbc.NavLink("Settings", href="/settings", className='text-white', active=True if active_item=='pages.settings' else False)),
            dbc.NavItem(dbc.NavLink("Evolución de generaciones", href="/gen_evol", className='text-white', active=True if active_item=='pages.gen_evol' else False)),
            dbc.NavItem(dbc.NavLink("Evolución de tallas", href="/tallas_evol", className='text-white', active=True if active_item=='pages.tallas_evol' else False)),
            dbc.NavItem(dbc.NavLink("Resultado", href="/resultado", className='text-white', active=True if active_item=='pages.resultado' else False)),
            dbc.NavItem(dbc.NavLink("Diferencial de despesques", href="/diff_despesques", className='text-white', active=True if active_item=='pages.diff_despesques' else False))
        ])
    ])
    return nav

def banner():
    escribir_log('info', dame_sesion()+': función banner')
    banner= dbc.Row(
                [dbc.Col(),dbc.Col([html.Img(src=get_asset_url(path="SSF_LOGO_NEG 2.jpg"), alt='SSF logo',className="banner-image",
                        height='20px', width='53px')])],
            justify='end')
    return banner


def layout():
    layout_login = html.Div([
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    html.H1("Bienvenido al IF versión 2.0",className='text-center'),
                                    html.Form(
                                    [   
                                        html.H3("Por favor, identifíquese para acceder:", id="h1",className='text-center'),
                                        dcc.Input(placeholder="Usuario", type="text", id="uname-box", name='username',persistence="session"),
                                        dcc.Input(placeholder="Contraseña", type="password", id="pwd-box", name='password'),
                                        dbc.Button("Login", n_clicks=0, type="submit",className='me-2', id="login-button", style={'background-color':'#F2A900','border-color': '#F2A900'}),
                                        html.Div(children="", id="output-state")
                                    ], method='POST',id="formulario")],style={'textAlign':'center','width': '100%','margin':'auto'},
                                width=6),
                            ], justify="center"),
                        ],className="vstack gap-3")
    if current_user.is_authenticated:
        user=current_user.name
        layout_logout= html.Div([dbc.Row([
                                    dbc.Col([html.Br(),
                                            html.H1("Bienvenido al IF versión 2.0"),
                                            html.Br(),
                                            html.P(f"Está loguedado como el usuario {user}", className='text-center'),
                                            html.Br()],width=6)], justify="center"),
                            ],style={"justifyContent": "center"},className="vstack gap-3")

    if current_user.is_authenticated:
        layout_components=layout_logout
    else:
        layout_components=layout_login
    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container([banner()], fluid=True),
            dbc.Container(layout_components, fluid='md')
        ], className='content')
    ]

    return layout

clientside_callback(
    """
    function(yes, name){
        if (name === 'active') {
            return '';
        } else if (name === '') {
            return 'active';
        }
    }
    """,
    Output('sidebar', 'className'),
    Input('sidebarCollapse', 'n_clicks'),
    State('sidebar', 'className')
)


