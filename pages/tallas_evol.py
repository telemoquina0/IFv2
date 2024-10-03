import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, callback, dcc, dash_table,callback_context
import pandas as pd
import os
from .funcionalidades.funcsifv2 import funcsif
from .funcionalidades.User import dame_sesion
from flask_login import current_user
from .home import get_sidebar, banner
import dash_daq as daq
from .funcionalidades.myfunc import escribir_log

#import jwt as jw
#from flask_dance.contrib.azure import azure

# no need to verify the token here, that was already done before
#id_claims = jw.decode(azure.token.get("id_token"), options={"verify_signature": False})
#name = id_claims.get("name")


def calculos_graficos(granjas, salvar, leyenda, user):
    p=funcsif()
    p.inicializar(user)
    if os.path.exists(p.get_attr("path_masterDF")) :
        masterDF=pd.read_csv(p.get_attr("path_masterDF"))
        #Para calcular el número de gráficos
        meses_sim=len(masterDF['FechaFin'].unique())
        opt=None
        if  os.path.exists(p.get_attr("path_distribucion_optima")) :
            ##### Distribucion optima solo para Rodaballo#########
            opt=  pd.read_csv(p.get_attr("path_distribucion_optima"))
            stock_opt =  pd.read_csv(p.get_attr("path_df_stock_opt"))
            opt = opt.groupby(['Granja','Fecha','Talla_500']).agg(BiomasaFinal_tn =('Biomasa', 'sum')).reset_index()
            opt['BiomasaFinal_tn']=opt['BiomasaFinal_tn']/1000
            opt_totales = opt.groupby(['Granja','Fecha']).agg(BiomasaFinal_tn_tot =('BiomasaFinal_tn', 'sum')).reset_index()
            opt=opt.merge(opt_totales, on=['Granja','Fecha'],how='left')
            opt['Por']=opt['BiomasaFinal_tn']/opt['BiomasaFinal_tn_tot']
            opt=opt.drop(columns=['BiomasaFinal_tn_tot'], axis=1)
            opt=opt.merge(stock_opt, on=['Granja'], how='left')
            opt['BiomasaFinal_tn'] = opt['Por'] * opt['Tones']
            #if p.get_attr("especie")=="TURBOT":
            opt['Talla_500'] = opt['Talla_500'].apply(lambda x: str(x).replace("j.3000", "j.3000 - 4000"))

        return p.my_plots_all_opt(data_to_plot = masterDF, granjas =granjas , opt=opt, n_plots = (meses_sim+1)*len(granjas), save = salvar,
                legend = leyenda)
    else:
        return None
    
def layout():
    if current_user.is_authenticated:
        user=current_user.name
    else:
        return html.Div(["Haga ", dcc.Link("login", href="/"), " para operar"], className='text-center')
    p=funcsif()
    p.inicializar(user)
    #######################################################TALLAS EVOLS#####################################################
    default_campos_granjas=pd.read_csv(p.get_attr("path_default_campos_granjas"))['Granja'].sort_values().to_list()
    especie=p.get_attr("especie")
    if especie =="SOLE":
        visible="hidden"
    else:
        visible="visible"
    df_stock_opt =  pd.read_csv(p.get_attr("path_df_stock_opt"))
    df_stock_opt=df_stock_opt.loc[df_stock_opt['Granja'].isin(default_campos_granjas)].sort_values(by=['Granja'])
    #Aqui no puedo actualizar los gráficos.


    layout= [
        get_sidebar(__name__),
        dbc.Container([banner()], fluid=True),
        dbc.Container([
            html.Div([
                dbc.Card([
                    dbc.Card(html.H4("Evolución de Tallas", className='text-center'), color="info", inverse=True, style={"height": "6vh"},),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.B("Seleccione las granjas para plot", style={"margin-bottom":"2w"}), 
                                dbc.Checklist(
                                    id='granjas_plot',
                                    options=[{'label': gr, 'value': gr} for gr in default_campos_granjas],
                                    value=default_campos_granjas,
                                    inline=False,
                                    style={"column-count":"2","borderColor": "#808080"},
                                    input_checked_style={
                                                            "backgroundColor": "#808080",
                                                            "borderColor": "#808080",
                                                        },
                                ),
                                html.Hr(),
                                html.Div([
                                    dbc.Button([html.I(className='fa fa-sync'),html.Div(" Plot", style=dict(paddignLeft='10w',display='inline-block'))], id='run_plot_tallas', className='sync',n_clicks=0, style={'background-color':'#F2A900','border-color': '#F2A900'}),
                                    daq.BooleanSwitch(
                                        label={'label':' Incluir leyenda',
                                                'style':{  #'font-family': 'Arial',
                                                    'font-size':15}},
                                        labelPosition='right',id='plt_leg',
                                        on=False, color="#FF0000",
                                        style=dict(display='inline-block')
                                    ),
                                    daq.BooleanSwitch(
                                        label={'label':' Guardar gráficos',
                                                'style':{  #'font-family': 'Arial',
                                                    'font-size':15}},
                                        labelPosition='right',id='guardar_graf',
                                        on=False, color="#FF0000",
                                        style=dict(display='inline-block')
                                    )
                                ],className="hstack gap-3",)
                            ],width=6),
                            dbc.Col([ "Introduzca el stock de referencia",
                                dash_table.DataTable(id='df_stock_opt',
                                    data=df_stock_opt.to_dict('records'),
                                    columns=[{'id': 'Granja','name': 'Granja','type': 'text','editable': False},
                                    {'id': 'Tones','name': 'Tones','type': 'numeric'}],editable=True, 
                                    style_header={'textAlign': 'center','fontWeight': 'bold'},
                                    style_cell={'textAlign': 'center'},style_table={'overflowX': 'auto','minWidth': '100%'}),
                            ],width=6, style={'display': 'block' ,"visibility": visible }),
                        ],justify="center"),
                    ], style={"padding": "20px 20px 20px 20px"}),
                ], style={'height':'100%'}),
                
                dcc.Loading([
                    html.Div(id="contenedor_graficos_talla"),],
                    target_components={'contenedor_graficos_talla':'children'},delay_show=1),#,delay_hide=1),
            ],),  
        ], fluid='md'),
    ]
    
    return layout


@callback(
    Output('df_stock_opt', 'data'),
    Input('df_stock_opt', 'data'),
    Input('granjas_plot', 'value'),
    prevent_initial_call=True
    #cuando se visualiza la pagina
)
def update_tabla(datos,granjas):
    escribir_log('info', dame_sesion()+": update_tabla: tallas_evol")
    user=current_user.name
    p=funcsif()
    p.inicializar(user)
    entrada=callback_context.triggered_id
    df_opt= pd.read_csv(p.get_attr("path_df_stock_opt"))
    if entrada=='df_stock_opt':
        newDF =pd.DataFrame(datos,columns=datos[0].keys())
        #Para evitar introducir vacíos 
        newDF['Tones']=pd.to_numeric(newDF['Tones'], errors='coerce')
        newDF= newDF.fillna(0)
    if entrada=='granjas_plot':
        #Mirar si está la línea en el fichero 
        #Si no está crear una nueva línea
        if not granjas:
            return []
        else:
            newDF=df_opt.loc[df_opt['Granja'].isin(granjas)].copy()
            for i in granjas:
                if newDF.loc[newDF['Granja']==i].empty:
                    newDF.loc[newDF.shape[0]]=[i,3500]
    df_opt=df_opt.loc[~df_opt['Granja'].isin(granjas)]
    df_opt=pd.concat([df_opt if not df_opt.empty else None, newDF if not newDF.empty else None]).sort_values(by=['Granja'])
    df_opt.to_csv( p.get_attr('path_df_stock_opt'), index = False)
    return newDF.sort_values(by=['Granja']).to_dict('records')

@callback(
    Output("contenedor_graficos_talla", 'children'),
    Input('run_plot_tallas','n_clicks'),
    State('granjas_plot', 'value'),
    State('plt_leg','on'),
    State("contenedor_graficos_talla", 'children'),
    State('guardar_graf','on'),
    prevent_initial_call=True,
    running=[
        (Output('run_plot_tallas','disabled'),True,False),
        (Output('plt_leg','disabled'),True,False),
        (Output('guardar_graf','disabled'),True,False),
        (Output("granjas_plot", "style"),
            {"visibility": "hidden"},
            {"visibility": "visible","column-count":"2"}),
        (Output("df_stock_opt", "style"),
            {"visibility": "hidden"},
            {"visibility": "visible"})
    ]
)
def dibujar_grafico(click, granjas, leyenda, niños, salvar):
    escribir_log('info', dame_sesion()+": dibujar_grafico: tallas_evol")
    user=current_user.name
    if click:
        if granjas==[]:
            if niños is None:
                numero_graficos_antiguos=0
            else:
                numero_graficos_antiguos=len(niños)
            for i in range(0,numero_graficos_antiguos):
                niños.pop()
            return niños
        lista_graficos=calculos_graficos(granjas=granjas,salvar=salvar, leyenda=leyenda, user=user)
        if lista_graficos is None:
            numero_graficos_nuevos=0
        else:
            numero_graficos_nuevos=len(lista_graficos)
        
        niños=[]
        for i in range(0,numero_graficos_nuevos):
            new_graph = dcc.Graph(
                figure=lista_graficos[i])
            niños.append(new_graph)
        if niños==[]:
            niños.append(html.P("No hay gráficos para mostrar", style={'textAlign': 'center'}))
    return niños
