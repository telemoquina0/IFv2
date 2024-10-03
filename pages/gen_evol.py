import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, callback,dcc, no_update
import os
from .funcionalidades.funcsifv2 import funcsif
from .funcionalidades.myfunc import escribir_log
from .funcionalidades.User import dame_sesion
import pandas as pd
import numpy as np
from flask_login import current_user
from .home import get_sidebar, banner


def layout():
    if current_user.is_authenticated:
        user=current_user.name
    else:
        return html.Div(["Haga ", dcc.Link("login", href="/"), " para operar"], className='text-center')
    p=funcsif()
    p.inicializar(user)
    default_campos_granjas = pd.read_csv(p.get_attr("path_default_campos_granjas"))['Granja'].to_list()
    default_campos_granjas=["Sin selección"]+default_campos_granjas
    layout= [
        get_sidebar(__name__),
        dbc.Container([banner()], fluid=True),
        dbc.Container([
            html.Div([
                dbc.Card([
                    dbc.Card(html.H4("Evolución de Generaciones", className='text-center'), color="info", inverse=True, style={"height": "6vh"},),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(width=4),
                            dbc.Col([
                                html.B("Seleccione una granja para plot", style={"margin-bottom":"2w"}),
                                dcc.Dropdown(id="granjas_plot_gen", options=[{'label': gr, 'value': gr} for gr in default_campos_granjas], value=default_campos_granjas[0]),
                            ],width=4),
                            dbc.Col(width=4),
                        ]),
                    ],style={"padding": "20px 20px 20px 20px","height": "100%"},)
                ]),
                dcc.Loading([
                    html.Div(id="contenedor_graficos_gen_evol")],
                    target_components={'contenedor_graficos_gen_evol':'children'},delay_show=1),#,delay_hide=1),
            ]),
        ], fluid='md')
    ]
    
    return layout


@callback(
    Output("contenedor_graficos_gen_evol", 'children'),
    Input('granjas_plot_gen','value'),
    State('contenedor_graficos_gen_evol', 'children'),
    prevent_initial_call=True,
    running=[(Output("granjas_plot_gen", "style"),
            {"visibility": "hidden"},
            {"visibility": "visible","column-count":"2"})]
)
def update_gen_evol(granja,niños):
    escribir_log('info', dame_sesion()+': callback update_gen_evol: gen_evol')
    if granja!="Sin selección":
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        if niños is None:
            numero_graficos_antiguos=0
        else:
            numero_graficos_antiguos=len(niños)
        for i in range(0,numero_graficos_antiguos):
            niños.pop()
        if os.path.exists(p.get_attr('path_masterDF')):
            masterDF=pd.read_csv(p.get_attr("path_masterDF"))
            historical_data=pd.read_csv(p.get_attr("path_historical_data"))
            n_gens_redondeado_par= int(np.ceil(len(masterDF['Gen'].unique())/2)*2)
            niños=[]
            lista_graficos=p.gen_evol_plot(master_DF = masterDF, historical_data = historical_data, granja = granja, 
                n_plots = n_gens_redondeado_par, max_historic_rows = 30000)
            numero_graficos_nuevos=len(lista_graficos)
            for j in range(0,numero_graficos_nuevos):
                new_graph = dcc.Graph(
                    figure=lista_graficos[j])
                niños.append(new_graph)
    
        if niños==[]:
            niños.append(html.P("No hay gráficos para mostrar", style={'textAlign': 'center'}))
        return niños
    return []



        
