import dash_bootstrap_components as dbc
from dash import html
from flask_login import current_user
from .home import get_sidebar, banner


def layout_texto():
    if current_user.is_authenticated:
        user=current_user.name
        return html.P(f"Está loguedado como el usuario {user}",className='text-center')
    else:
        return html.P(f"No está logueado",className='text-center')
    

def layout():
    
    layout_logout= html.Div([
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                         html.H1("Bienvenido a IF versión 2.0",className='text-center'),
                                         html.Br(),
                                         layout_texto(),
                                         html.A(dbc.Button("Logout", n_clicks=0, type="submit",className='me-2', id="logout-button", style={'background-color':'#F2A900','border-color': '#F2A900'}),href='/logout'),
                                         html.Br()],style={'textAlign':'center','width': '100%','margin':'auto'},width=6)],
                                         justify="center")
                        ],className="vstack gap-3")
    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container([banner()], fluid=True),
            dbc.Container(layout_logout, fluid='md')
        ], className='content')
    ]

    return layout


