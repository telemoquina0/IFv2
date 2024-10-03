import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output, State, callback_context, no_update, callback
import os
from .funcionalidades.myfunc import rnorm3, date_col_names, obtener_celda_distinta, escribir_log, dame_tallas,fechas_stolt_func_new
from .funcionalidades.funcsifv2 import funcsif
from .funcionalidades.User import dame_sesion
import numpy as np
from datetime import date
from dash.dash_table.Format import Format, Scheme
import pandas as pd
import time
from pathlib import Path
from zipfile import ZipFile
from shutil import rmtree
import base64
import datetime 
import io
import re
import plotly.figure_factory as ff
from flask_login import current_user
from .home import get_sidebar, banner
from io import StringIO
import dash_daq as daq
import string
import scipy


def layout():
    if current_user.is_authenticated:
        user=current_user.name
    else:
        return html.Div(["Haga ", dcc.Link("login", href="/"), " para operar"], className='text-center')
    readme_initial_text = "##################################\nFecha de realización : " + str(date.today()) + "\n##################################"

    p=funcsif()
    p.inicializar(user)
    config_especie=p.get_attr("especie")
        
    if config_especie == "TURBOT":
        campos_granjas = ['Cervo_P', 'Lira_P', 'Merexo_P', 'Couso_P', 'Oye_P', 'Palmeira_P', 'Quilmas_P', 'Vilan_P', 'Tocha_P', 'SSF', 'SSF_Iberia']
    elif config_especie == "SOLE":
        campos_granjas = ['Cervo Sole', 'Tocha Sole', 'Hafnir_P', 'Couso i+d', 'Anglet_P']#, 'SSF', 'SSF_Iberia']
    campos_granjas.sort()

    meses_max_sim = 18
    p.crear_estructura_if(campos_granjas, meses_max_sim)

    ##GRANJAS#################
    if os.path.exists(p.get_attr("path_default_campos_granjas")):
        default_campos_granjas = pd.read_csv(p.get_attr("path_default_campos_granjas"))['Granja']
    else:
        default_campos_granjas = pd.DataFrame({'Granja': campos_granjas})
        default_campos_granjas.to_csv(p.get_attr("path_default_campos_granjas"), index=False)
        default_campos_granjas=default_campos_granjas['Granja']

    #FECHA######################
    if os.path.exists(p.get_attr("path_default_fecha")):
        default_fecha = pd.to_datetime(pd.read_csv(p.get_attr("path_default_fecha")).loc[0,'date']).date()
        default_fecha=fechas_stolt_func_new(default_fecha)
        if pd.to_datetime(default_fecha).date()>datetime.datetime.today().date():
            default_fecha=fechas_stolt_func_new(pd.to_datetime(default_fecha).date()- datetime.timedelta(days=32))
    else:
        #Ha de ser el último día de mes
        default_fecha=pd.DataFrame({'date':[pd.to_datetime((datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)).strftime('%Y-%m-%d')).date()]})
        default_fecha.to_csv(pd.read_csv(p.get_attr("path_default_fecha")), index=False)
        default_fecha=default_fecha.loc[0,'date']

    #BOTONES: CONTINUAR Y TIPO GROWTH#################### 
    if os.path.exists(p.get_attr("path_d_growth_type")):
        material_switch =pd.read_csv(p.get_attr("path_d_growth_type"))
    else:
        material_switch=pd.DataFrame(data={"Button":["continue","d_growth_type"], "State":[False, False]})
        material_switch.to_csv(p.get_attr("path_d_growth_type"), index=False)
    flag_continua=material_switch.loc[material_switch['Button']=="continue","State"].to_list()[0]

    return [
            get_sidebar(__name__),
            dbc.Container([banner()], fluid=True),
            dbc.Container([dcc.Store(id='mem_fecha', data=pd.read_csv(p.get_attr("path_default_campos_granjas")).to_json(orient='split', date_format='iso')),
                           dcc.Store(id='mem_granjas', data=pd.read_csv(p.get_attr("path_default_campos_granjas")).to_json(orient='split', date_format='iso')),
                           dcc.Store(id='mem_update_tablas', data=pd.DataFrame(data={'trigger': [0]}).to_json(orient='split', date_format='iso')),
                           dcc.Store(id='mem_update', data=pd.DataFrame(data={'trigger':[0]}).to_json(orient='split', date_format='iso')),
                           dbc.Row([   
                                dbc.Col([  
                                    html.Div([ 
                                        dbc.Card(html.H4("General settings", className='text-center'), color="info", inverse=True, style={"height": "6vh"}),
                                        html.Div([ 
                                            dcc.Tabs(id='general_settings_tab', children=[ 
                                                dcc.Tab(label='General', children=[ 
                                                    dbc.Row([ 
                                                        dbc.Col([   
                                                            dbc.Row([html.B("Fecha inicio modelo", style={"margin-bottom":"2w"})]), 
                                                            dcc.DatePickerSingle(
                                                                id='date',
                                                                date=default_fecha,
                                                                display_format='YYYY-MM-DD',
                                                                first_day_of_week=1
                                                            ),
                                                            html.Br(),
                                                            html.Br(),
                                                            dbc.Row([  
                                                                dbc.Col([
                                                                    daq.BooleanSwitch(
                                                                        label={'label':' Continuar ultima simulación',
                                                                               'style':{  #'font-family': 'Arial',
                                                                                    'font-size':15}},
                                                                        labelPosition='right',id='flag',
                                                                        on=flag_continua, color="#FF0000"
                                                                    )
                                                                ]), 
                                                                dbc.Col([ 
                                                                    html.Div([dcc.Input(value=mostrar_etiqueta_inicio()[1],id='last_date_found', readOnly=True, size='26')], style={'display': 'block' ,"visibility": mostrar_etiqueta_inicio()[0] })
                                                                ]),
                                                            ]), 
                                                            html.Br(),
                                                            html.B("Meses a simular"),
                                                            html.Br(),
                                                            dcc.Input(id='meses_sim', type='number' ,value=meses_max_sim, min=1, max=meses_max_sim, step=1),
                                                            html.Br(),
                                                            html.Br(),
                                                            dcc.ConfirmDialog(
                                                                id='ventana-borrar-mes',
                                                                message='¿Está seguro de borrar el ultimo mes simulado?',
                                                                ),
                                                            dbc.Button([html.I(className='fa fa-undo'),html.Div("Borrar ultimo mes", style=dict(paddignLeft='10w',display='inline-block')),], id='borrar_ultimo_mes', className='undo',n_clicks=0, style={'background-color':'#F2A900','border-color': '#F2A900'})
                                                        ], width=6, style={"padding": "20px 20px 20px 20px"}), 
                                                        dbc.Col([ 
                                                            dcc.ConfirmDialog(
                                                                id='ventana-granjas',
                                                                message='Debe escoger, al menos, una  granja',
                                                                ),
                                                            dbc.Row([html.B("Seleccione las granjas que se simulan", style={"margin-bottom":"2w"}),]), 
                                                            dbc.Checklist(
                                                                id='granjas_sim',
                                                                options=[{'label': gr, 'value': gr} for gr in campos_granjas],
                                                                value=default_campos_granjas.to_list(),
                                                                inline=False,
                                                                style={"column-count":"2","borderColor": "#808080"},
                                                                input_checked_style={
                                                                                        "backgroundColor": "#808080",
                                                                                        "borderColor": "#808080",
                                                                                    }
                                                                
                                                            ),
                                                            html.Br(),
                                                            dcc.ConfirmDialog(
                                                                id='ventana-inicializar-tablas',
                                                                message='¿Está seguro de inicializar las tablas? Al inicializarlas se reiniciarán todos los settings',
                                                                ),
                                                            dbc.Button([html.I(className='fa fa-sync'),html.Div("inicializar tablas", style=dict(paddignLeft='10w',display='inline-block')),], id='inicializar_tablas', className='sync',n_clicks=0, style={'background-color':'#F2A900','border-color': '#F2A900'}),
                                                            html.Br(),html.Hr(),
                                                            dcc.ConfirmDialog(
                                                                id='ventana-errores-ejecucion',
                                                                message='',
                                                                ),
                                                            html.Div([
                                                                html.P(id="paragraph_id", children=[" "]),
                                                                html.Progress(id="progress_bar", style={"visibility": "hidden"}),
                                                            ]),
                                                            dbc.Button([html.I(className='fa fa-paper-plane'),html.Div("RUN", style=dict(paddignLeft='10w',display='inline-block')),], id='run_model', className='paper-plane', n_clicks=0, style={'background-color':'#F2A900','border-color': '#F2A900'}),
                                                        ], width=6, style={"padding": "20px 20px 20px 20px"}) 
                                                    ]),
                                                ]),
                                                dcc.Tab(label='Download settings', children=[
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.Br(),
                                                            dbc.Row([html.B("Nombre del setting", style={"margin-bottom":"3w"})]), 
                                                            dcc.Input(id='nombre_settings', type='text', value="", placeholder="Nombre del setting"),
                                                            html.Hr(),
                                                            html.Div([dbc.Button([html.I(className='fa fa-download'),
                                                                    html.Div("Download", style=dict(paddignLeft='10w',display='inline-block')),], id='save_set', className='download', style={'background-color':'#F2A900','border-color': '#F2A900'}),
                                                                    dcc.Download(id="download-text")])
                                                        ], width=5, style={"padding": "20px 20px 20px 20px"}),
                                                        dbc.Col([
                                                            html.Br(),
                                                            dbc.Row([html.B("Descripción", style={"margin-bottom":"3w"})]),
                                                            dcc.Textarea(
                                                                id='settings_desc',
                                                                value=readme_initial_text,
                                                                style={'width': '100%', 'height': 220}
                                                            )
                                                        ], width=7),
                                                    ]) 
                                                ]), 
                                                dcc.Tab(label='Upload settings', children=[
                                                    dbc.Row([
                                                        dbc.Row([html.Br(), html.Br()]),
                                                        html.P('Al actualizar los settings perderá los settings actuales. Puede guardarlos antes en la pestaña de Download settings.', style={'textAlign': 'center'}),
                                                        dbc.Col(width=5),
                                                        dbc.Col([ 
                                                            dcc.Upload(dbc.Button([html.I(className='fa fa-upload'),html.Div(". Upload IF_setting.zip", style=dict(paddignLeft='10w',display='inline-block')),], id='file_past_settings', className='upload', style={'background-color':'#F2A900','border-color': '#F2A900'}),
                                                                    id='upload-data'),#,disable_click=True),
                                                        ], width=7, style={"padding": "20px 20px 20px 20px", "vertical-align": "middle"}),
                                                        dbc.Col(width=5)
                                                    ]) 
                                                ])
                                            ]) 
                                        ], style={"padding": "20px 20px 20px 20px","height": "100%"}),
                                    ]),
                                    html.Br(),
                                    html.Div(layout_inputs(campos_granjas, meses_max_sim, default_fecha)),
                                    html.Br(),
                                    html.Div(layout_despesques(default_campos_granjas)),
                                    html.Br(),
                                    html.Div(layout_perdidas()),
                                    html.Br(),
                                    html.Div(layout_growth()),
                                ], width=12, className="vstack gap-3"),
                            ]),
                        ]) 
        ]


#Esquema de sets (variable que se almacena en la memoria)
# -mem_granjas (lista de granjas)
#-mem_fecha
#-mem_update_tablas
#-mem_update

def incluir_linea(df, tipo, columnas_no_meses, granja, especie="TURBOT"):
    columnas_ceros=df.columns[columnas_no_meses:]
    df=df.reset_index(drop=True)
    if tipo==1:
        if columnas_no_meses==1:
            linea=[granja]+[0]*len(columnas_ceros)
            Total=df.loc[df.shape[0]-1]
            df.loc[df.shape[0]-1]=linea
            df=df.sort_values(by=['Granja']).reset_index(drop=True)
            df.loc[df.shape[0]]=Total
        if columnas_no_meses==2:
            tallas=dame_tallas(especie)
            mis_tallas = [f"{a}.{b}" for a,b in zip(string.ascii_lowercase[0:len(tallas)], tallas)]
            for i in mis_tallas:
                linea=[granja, i]+[0]*len(columnas_ceros)
                Total=df.loc[df.shape[0]-1]
                df.loc[df.shape[0]-1]=linea
                df=df.sort_values(by=['Granja','Talla']).reset_index(drop=True)
                df.loc[df.shape[0]]=Total
    else:
        if tipo==2:
            if especie=="TURBOT":
                linea=[granja, 14, 15, 100]
            elif especie=="SOLE":
                linea=[granja, 14, 24, 100]
        if tipo==3:
            if especie=="TURBOT":
                linea=[granja, 1000, 12, 1000, 12]
            elif especie=="SOLE":
                linea=[granja, 1000, 12, 1000, 12]
        if tipo==4:
            linea=[granja, 100]
        df.loc[df.shape[0]]=linea
        df=df.sort_values(by=['Granja']).reset_index(drop=True)
    return df


#Funcion que filtra los df por las granjas y si hay granjas 
#nuevas seleccionadas, crea la línea con ceros.
#granjas es una lista
def actualizar_granjas_tablas(granjas):
    try:
        escribir_log('info', dame_sesion()+": función: actualizar_granjas_tablas")
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        #Leemos todos los df
        #alevines y alevines settings
        df_alevines=pd.read_csv(p.get_attr("path_df_alevines"))
        #Filtramos y vemos si están todas las granjas
        granjas_n=granjas+['Total']
        df_alevines=df_alevines.loc[df_alevines['Granja'].isin(granjas_n)]
        df_alevines_pm_cv=pd.read_csv(p.get_attr("path_df_alevines_pm_cv"))
        df_alevines_pm_cv=df_alevines_pm_cv.loc[df_alevines_pm_cv['Granja'].isin(granjas)]
        df_despesques = pd.read_csv(p.get_attr('path_df_despesques'))
        df_despesques = df_despesques.loc[df_despesques['Granja'].isin(granjas)]
        df_dispersion = pd.read_csv(p.get_attr('path_df_dispersion'))
        df_dispersion=df_dispersion.loc[df_dispersion['Granja'].isin(granjas)]
        df_edad_pescas = pd.read_csv(p.get_attr('path_df_edad_pescas'))
        df_edad_pescas=df_edad_pescas.loc[df_edad_pescas['Granja'].isin(granjas)]
        #M+S
        df_losses=pd.read_csv(p.get_attr('path_df_losses'))
        df_losses=df_losses.loc[df_losses['Granja'].isin(granjas_n)]
        df_reparto_mort = pd.read_csv(p.get_attr('path_df_reparto_mort'))
        df_reparto_mort=df_reparto_mort.loc[df_reparto_mort['Granja'].isin(granjas)]
        #Growth estimado
        df_desired_growth=pd.read_csv(p.get_attr('path_df_desired_growth'))
        df_desired_growth=df_desired_growth.loc[df_desired_growth['Granja'].isin(granjas_n)]
        #Stock optimo
        df_stock_optimo=pd.read_csv(p.get_attr('path_df_stock_opt'))
        df_stock_optimo=df_stock_optimo.loc[df_stock_optimo['Granja'].isin(granjas)]
        df_alevines.to_csv(p.get_attr("path_df_alevines"),index=False)
        df_alevines_pm_cv.to_csv(p.get_attr("path_df_alevines_pm_cv"),index=False)
        df_despesques.to_csv(p.get_attr("path_df_despesques"),index=False)
        df_dispersion.to_csv(p.get_attr("path_df_dispersion"),index=False)
        df_edad_pescas.to_csv(p.get_attr("path_df_edad_pescas"),index=False)
        df_losses.to_csv(p.get_attr("path_df_losses"),index=False)
        df_reparto_mort.to_csv(p.get_attr("path_df_reparto_mort"),index=False)
        df_desired_growth.to_csv(p.get_attr("path_df_desired_growth"),index=False)
        df_stock_optimo.to_csv(p.get_attr("path_df_stock_opt"),index=False)
        granjas_añadir=[]
        for i in granjas:
            if df_alevines.loc[df_alevines['Granja']==i].empty:
                granjas_añadir=granjas_añadir+[i]
        if len(granjas_añadir)>0:

            df_alevines_pm_cv=pd.read_csv(p.get_attr("path_df_alevines_pm_cv"))
            #Despesques, totales, dispersion, edad minima pescas
            df_despesques = pd.read_csv(p.get_attr('path_df_despesques'))
            df_dispersion = pd.read_csv(p.get_attr('path_df_dispersion'))
            df_edad_pescas = pd.read_csv(p.get_attr('path_df_edad_pescas'))
            #M+S
            df_losses=pd.read_csv(p.get_attr('path_df_losses'))
            df_reparto_mort = pd.read_csv(p.get_attr('path_df_reparto_mort'))
            #Growth estimado
            df_desired_growth=pd.read_csv(p.get_attr('path_df_desired_growth'))
            #Stock optimo
            df_stock_optimo=pd.read_csv(p.get_attr('path_df_stock_opt'))

            for i in granjas_añadir:
                df_alevines=incluir_linea(df_alevines,1,1,i)
                df_alevines_pm_cv=incluir_linea(df_alevines_pm_cv,2,1,i)
                df_despesques=incluir_linea(df_despesques,1,2,i,p.get_attr("especie"))
                df_dispersion =incluir_linea(df_dispersion,1,1,i,p.get_attr("especie"))
                df_edad_pescas =incluir_linea(df_edad_pescas,1,1,i,p.get_attr("especie"))
                df_losses=incluir_linea(df_losses,1,1,i,p.get_attr("especie"))
                df_reparto_mort = incluir_linea(df_reparto_mort,3,1,i,p.get_attr("especie"))
                df_desired_growth=incluir_linea(df_desired_growth,1,1,i,p.get_attr("especie"))
                df_stock_optimo=incluir_linea(df_stock_optimo,4,1,i,p.get_attr("especie"))
            
            df_alevines_pm_cv=df_alevines_pm_cv.loc[df_alevines_pm_cv['Granja'].isin(granjas)]

            df_despesques=df_despesques.loc[df_despesques['Granja'].isin(granjas_n)]
            df_dispersion=df_dispersion.loc[df_dispersion['Granja'].isin(granjas_n)]
            df_edad_pescas=df_edad_pescas.loc[df_edad_pescas['Granja'].isin(granjas_n)]
            df_losses=df_losses.loc[df_losses['Granja'].isin(granjas_n)]
            df_reparto_mort=df_reparto_mort.loc[df_reparto_mort['Granja'].isin(granjas)]
            df_desired_growth=df_desired_growth.loc[df_desired_growth['Granja'].isin(granjas_n)]
            df_stock_optimo=df_stock_optimo.loc[df_stock_optimo['Granja'].isin(granjas)]

            df_alevines.to_csv(p.get_attr("path_df_alevines"),index=False)
            df_alevines_pm_cv.to_csv(p.get_attr("path_df_alevines_pm_cv"),index=False)
            df_despesques.to_csv(p.get_attr("path_df_despesques"),index=False)
            df_dispersion.to_csv(p.get_attr("path_df_dispersion"),index=False)
            df_edad_pescas.to_csv(p.get_attr("path_df_edad_pescas"),index=False)
            df_losses.to_csv(p.get_attr("path_df_losses"),index=False)
            df_reparto_mort.to_csv(p.get_attr("path_df_reparto_mort"),index=False)
            df_desired_growth.to_csv(p.get_attr("path_df_desired_growth"),index=False)
            df_stock_optimo.to_csv(p.get_attr("path_df_stock_opt"),index=False)

    except Exception as e:
        escribir_log('critical',dame_sesion()+': Error {0}'.format(str(e)))
        escribir_log('critical',dame_sesion()+': Error en actualizar_granjas_tablas')

#Guarda la fecha en la memoria y en el fichero (tengo que hacerlo así para que si hay un corte sean coherentes la fecha y las columnas)
#Establezco los tabs de Total por granja en despesques, M+S en perdidas y growth estimado en crecimiento.
@callback(
    Output("growth_tab", "value"),
    Output("losses_tab", "value"),
    Output("despesques_tab", "value"),
    Output('mem_fecha','data'),
    Output('date','date',allow_duplicate=True),
    Input('date','date'),
    prevent_initial_call=True
)
def fecha_inicio_modelo(fecha):
    try:
        escribir_log('info', dame_sesion()+": callback: fecha_inicio_modelo")
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        default_fecha=pd.read_csv(p.get_attr("path_default_fecha"))
        fecha=fechas_stolt_func_new(fecha)
        if pd.to_datetime(fecha).date()>datetime.datetime.today().date():
            fecha=fechas_stolt_func_new(pd.to_datetime(fecha).date()- datetime.timedelta(days=32))
        default_fecha.loc[0,'date']=fecha
        default_fecha.to_csv(p.get_attr("path_default_fecha"), index=False)
        return 'growth_estimado','M_S','Por_Granja',default_fecha.to_json(orient='split', date_format='iso'),fecha
    except Exception as e:
        escribir_log('critical',dame_sesion()+'fecha_inicio_modelo: Error {0}'.format(str(e)))
        return no_update, no_update, no_update, no_update, no_update



###############inicializar tablas
#Visualizar ventana aviso inicializar tablas
@callback(
    Output('ventana-inicializar-tablas', 'displayed'),
    Input('inicializar_tablas', 'n_clicks'),
    prevent_initial_call=True
)
def aviso_inicializar_tablas(n_clicks):
    try:
        if n_clicks:
            escribir_log('info', dame_sesion()+": callback: aviso_inicializar_tablas")
            return True
    except Exception as e:
        escribir_log('critical',dame_sesion()+': aviso_inicializar_tablas ' +"Error {0}".format(str(e)))
        return no_update




#Inicializa las tablas
@callback(
    output=[Output('ventana-granjas', 'displayed'),
    Output('mem_granjas','data'),
    Output('mem_update_tablas', 'data'),
    Output('date','date'),
    Output('flag','on', allow_duplicate=True),
    Output("select_gr_despesques",'options',allow_duplicate=True),
    Output('select_gr_despesques','value',allow_duplicate=True),
    Output("losses_tab", "value", allow_duplicate=True),  #Para actualizar 'select_gr_dist_mort'
    Output("growth_tab", "value",allow_duplicate=True),
    Output("despesques_tab", "value", allow_duplicate=True)],        #Devuelvo uno cualquiera. Lo tengo para que se actualice
    
    inputs=dict(submit_n_clicks=Input('ventana-inicializar-tablas', 'submit_n_clicks')),
    state=dict(granjas=State('granjas_sim', 'value'),
    trigger=State('mem_update_tablas', 'data')),
    prevent_initial_call=True,
    #background=True,  # Indica que es un background callback
    running=[
        (Output("inicializar_tablas", "disabled"), True, False),
        (Output("run_model", "disabled"), True, False),
        (Output('borrar_ultimo_mes', 'disabled'),True, False),
        (Output("date", "disabled"), True, False),
        (
            Output("granjas_sim", "style"),
            {"visibility": "hidden"},
            {"visibility": "visible","column-count":"2"}
        ),
        (
            Output("progress_bar", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"}
        ),
    ],
    progress=[Output("progress_bar", "value"), Output("progress_bar", "max")]
)
def inicializar_tablas(submit_n_clicks,granjas, trigger):
    escribir_log('info', dame_sesion()+": callback: inicializar_tablas")
    try:
        user=current_user.name
        if submit_n_clicks:
            #Comprobar que al menos hay una granja
            granjas.sort()
            if len(granjas)==0:
                return True, no_update, no_update, no_update,no_update,no_update,no_update,no_update,no_update,no_update
            p=funcsif()
            p.inicializar(user)
            #Borro el directorio Temp y se vuelve a crear el directorio con los valores por defecto
            #y las granjas seleccionadas
            #Se borran los ficheros del directorio Temp y el directorio Temp
            
            for path in Path(os.path.join(p.get_attr("parent_dir"),p.get_attr("especie"),user, "Temp")).glob("**/*"):
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    rmtree(path)
            meses_sim_max=18
            p.crear_estructura_if(campos_granjas = granjas, meses_max_sim = meses_sim_max)
            
            default_campos_granjas=pd.DataFrame({'Granja': granjas})
            #default_campos_granjas.to_csv(p.get_attr("path_default_campos_granjas"),index=False)
            update_tablas_trigger=pd.read_json(StringIO(trigger), orient='split')
            update_tablas_trigger.loc[0,'trigger']+=1
            fecha=pd.read_csv(p.get_attr("path_default_fecha")).loc[0,'date']
            fecha=fechas_stolt_func_new(fecha)
            return no_update, default_campos_granjas.to_json(orient='split', date_format='iso'), update_tablas_trigger.to_json(orient='split', date_format='iso'), fecha, False, \
                granjas, granjas[0], 'Distribucion_M_S','ajustes_growth','Por_Granja'
        
        
        return no_update, no_update, no_update, no_update,no_update, no_update, no_update, no_update,no_update, no_update
    except Exception as e:
        escribir_log('critical', dame_sesion()+': inicializar_tablas ' +"Error {0}".format(str(e)))
        return no_update, no_update, no_update, no_update,no_update, no_update, no_update, no_update,no_update, no_update

####################Flag continuar##########################################

def mostrar_etiqueta_inicio():
    escribir_log('info', dame_sesion()+": función: mostrar_etiqueta_inicio")
    try:
        p=funcsif()
        if current_user.is_authenticated:
            user=current_user.name
            p.inicializar(user)
            material_switch = pd.read_csv(p.get_attr("path_d_growth_type"))
            flag=material_switch.loc[material_switch['Button'] == "continue",  "State"].values.item(0)
            if flag:
                if os.path.exists(p.get_attr('path_masterDF')):
                    df_master = pd.read_csv(p.get_attr('path_masterDF'))
                    last_date = df_master['FechaFin'].max()
                    return ["visible", f"Nueva fecha inicio: {last_date}"]
                
            return ["hidden",""]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': mostrar_etiqueta_inicio' +"Error {0}".format(str(e)))
    


#Etiqueta del flag de continuar, oculta la etiqueta en el caso de que no haya ultima
#simulación
@callback(
    Output("last_date_found", "value"),
    Output("last_date_found", "style"),
    Input('last_date_found', 'value'),
    prevent_initial_call=True
)
def visibilidad_last_date_found(mensaje):
    escribir_log('info', dame_sesion()+": callback: visibilidad_last_date_found")
    try:
        if mensaje=="No hay simulacion que continuar":
            time.sleep(1.5)
            return "", {"visibility": "hidden"}
        if mensaje=="":
            return no_update,  {"visibility": "hidden"}
        return no_update,  {"visibility": "visible"}
    except Exception as e:
        escribir_log('critical', dame_sesion()+': visibilidad_last_date_found' +"Error {0}".format(str(e)))
        return no_update, no_update
        

#Guarda el flag de continuar en el fichero
#y pone la etiqueta del flag de continuar
@callback(
    Output('last_date_found', 'style', allow_duplicate=True),
    Output('last_date_found', 'value', allow_duplicate=True),
    Output('flag','on',allow_duplicate=True),
    Input('last_date_found', 'value'),
    Input('flag','on'),
    Input('mem_update', 'data'),
    Input('mem_update_tablas','data'),
    prevent_initial_call=True
)
def etiqueta_last_date_found(etiqueta, flag,data_trigger, data_update_tablas_trigger):
    escribir_log('info', dame_sesion()+": callback: etiqueta_last_date_found")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        entrada=callback_context.triggered_id
        if entrada!="last_date_found":
            material_switch = pd.read_csv(p.get_attr("path_d_growth_type"))
            material_switch.loc[material_switch['Button'] == "continue",  "State"]=flag
            if flag:
                if os.path.exists(p.get_attr('path_masterDF')):
                    df_master = pd.read_csv(p.get_attr('path_masterDF'))
                    last_date = df_master['FechaFin'].max()
                    material_switch.to_csv(p.get_attr("path_d_growth_type"),index=False)
                    return {"visibility": "visible"}, f"Nueva fecha inicio: {last_date}", no_update
                else:
                    material_switch.loc[material_switch['Button'] == "continue",  "State"]=False
                    material_switch.to_csv(p.get_attr("path_d_growth_type"),index=False)
                    return {"visibility": "visible"}, "No hay simulacion que continuar", False
            else:
                material_switch.loc[material_switch['Button'] == "continue",  "State"]=False
                material_switch.to_csv(p.get_attr("path_d_growth_type"),index=False)
                return {"visibility": "hidden"}, f"", False
        else:
            if etiqueta=="No hay simulacion que continuar":
                time.sleep(1.5)
                return {"visibility": "hidden"}, no_update, False
        return {"visibility": "hidden"}, no_update, False
    except Exception as e:
        escribir_log('critical', dame_sesion()+': etiqueta_last_date_found ' +"Error {0}".format(str(e)))
        return no_update, no_update, no_update




   

#####################################################
#Callback para borrar ultimo mes-> ventana de aviso
@callback(
    Output('ventana-borrar-mes', 'displayed'),
    Input('borrar_ultimo_mes', 'n_clicks'),
    prevent_initial_call=True
)
def aviso_borrar_ultimo_mes(n_clicks):
    if n_clicks:
        escribir_log('info', dame_sesion()+": callback: aviso_borrar_ultimo_mes")
        return True

#Callback para borrar ultimo mes
@callback(
    Output('mem_update','data'),
    Input('ventana-borrar-mes', 'submit_n_clicks'),
    Input('mem_update','data'),
    prevent_initial_call=True)
def borrar_ultimo_mes(submit_n_clicks, trigger):
    escribir_log('info', dame_sesion()+": callback: borrar_ultimo_mes")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        if submit_n_clicks:
            p.borrar_ultimo_mes_func()
            update_trigger=pd.read_json(StringIO(trigger), orient='split')
            update_trigger.loc[0,'trigger']+=1
            return update_trigger.to_json(orient='split', date_format='iso')
        return no_update
    except Exception as e:
        escribir_log('critical', dame_sesion()+': borrar_ultimo_mes ' +"Error {0}".format(str(e)))
        return no_update
 # Update trigger
 #   update <- reactiveValues(trigger = 0)
 #   observeEvent(input$run_model, priority = -1, {
 #     update$trigger <- update$trigger + 1
 #   })
    



#######################################ejecucion
#Visualizar ventana de avisos/errores ejecucion
@callback(
    Output('ventana-errores-ejecucion', 'displayed'),
    Input('ventana-errores-ejecucion', 'message'),
    prevent_initial_call=True
)
def aviso_errores_ejecucion(message):
    escribir_log('info', dame_sesion()+": callback: aviso_errores_ejecucion")
    return True



 # Borro todos los outputs (¡NO lo hago!) pulso Run y continue == F
@callback(
    output=[Output('ventana-errores-ejecucion', 'message', allow_duplicate=True),
    Output("select_gr_despesques",'options',allow_duplicate=True),
    Output('select_gr_despesques','value',allow_duplicate=True),
    Output("despesques_tab", "value", allow_duplicate=True),        #Devuelvo lo mismo que entra. Lo tengo para que se actualice
    Output("losses_tab", "value", allow_duplicate=True),            #Para actualizar 'select_gr_dist_mort'
    Output("growth_tab", "value",allow_duplicate=True),
    Output('mem_update_tablas', 'data',allow_duplicate=True)],  
    inputs=dict(submit_n_clicks=Input('run_model', 'n_clicks')),
    state=dict(default_flag=State('flag', 'on'),
        fecha=State('date','date'),
        meses_sim=State("meses_sim","value"),
        granjas=State("granjas_sim","value"),
        panel=State("despesques_tab", "value"),
        trigger=State('mem_update_tablas', 'data')),
    prevent_initial_call=True,
    running=[
        (Output("run_model", "disabled"), True, False),
        (Output("inicializar_tablas", "disabled"), True, False),
        (Output("borrar_ultimo_mes", "disabled"), True, False),
        (Output("date", "disabled"), True, False),
        (
            Output("flag", "style"),
            {"visibility": "hidden"},
            {"visibility": "visible"}
        ),
        (
            Output("meses_sim", "style"),
            {"visibility": "hidden"},
            {"visibility": "visible"}
        ),
        (
            Output("granjas_sim", "style"),
            {"visibility": "hidden"},
            {"visibility": "visible","column-count":"2"}
        ),
        (Output("download-text","disabled"),True,False),
        (Output("upload-data","disabled"),True,False),
        (
            Output("progress_bar", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"}
        ),
    ],
    progress=[Output("progress_bar", "value"), Output("progress_bar", "max")]
)
def ejecutar(submit_n_clicks, default_flag, fecha, meses_sim, granjas,panel, trigger):
    
    escribir_log('info', dame_sesion()+": callback: ejecutar")
    try:
        if submit_n_clicks:
            if current_user.is_authenticated:
                user=current_user.name
                p=funcsif()
                p.inicializar(user)
                if not default_flag:
                    #Borro los resultados
                    #Se borran los ficheros del directorio Temp/outputs/csv y Temp/outputs/plots

                    for path in Path(p.get_attr("solo_path_csv")).glob("**/*"):
                        if path.is_file():
                            os.remove(path)
                    for path in Path(p.get_attr("solo_path_plots")).glob("**/*"):
                        if path.is_file():
                            os.remove(path)
                granjas.sort()
                default_campos_granjas = pd.DataFrame({'Granja': granjas})
                default_campos_granjas.to_csv(p.get_attr("path_default_campos_granjas"),index=False)
                default_campos_granjas=default_campos_granjas['Granja']
                actualizar_granjas_tablas(default_campos_granjas.to_list())
                update_tablas_trigger=pd.read_json(StringIO(trigger), orient='split')
                update_tablas_trigger.loc[0,'trigger']+=1
                curvas= pd.read_csv(p.get_attr("path_curvas"))
                all_alevines= p.import_format_func(path =p.get_attr("path_df_alevines"), val_name = "Num")
                pesos_medios_entrada_alev=pd.read_csv(p.get_attr("path_df_alevines_pm_cv"))
                pesos_medios_entrada_alev['CV']=pesos_medios_entrada_alev['CV']/100
                all_ventas= p.import_format_func(p.get_attr("path_df_despesques"), val_name='BiomasaVentas')
                all_mortalidad = p.import_format_func(path =p.get_attr("path_df_losses"), val_name = "Num")
                all_crecimientoD= p.import_format_func(path =p.get_attr("path_df_desired_growth"), val_name = "Tones")
                all_ajustes_edad= p.import_format_growth_aj_edad_func()
                all_ajustes_talla = p.import_format_growth_aj_talla_o_gen_func(type = "Talla")
                all_ajustes_gen = p.import_format_growth_aj_talla_o_gen_func(type = "Gen")
                all_ajustes_mort_gen = p.import_format_mort_aj_gen_func()
                
                all_acabar_gen =p.import_format_acabar_gen()
                all_dispersion_df =p.import_format_func(path = p.get_attr("path_df_dispersion"), val_name = "cv", from_por = True)
                all_edad_venta_df =p.import_format_func(path = p.get_attr("path_df_edad_pescas"), val_name = "Edad")
                all_reparto_mort = p.import_format_mort_dist()
                resultado=p.import_initial_data(continue_flag = default_flag,fecha = fecha)
                culling_edad = pd.read_csv(p.get_attr("path_default_culling_por"))["Edad"].to_list()[0]
                culling_por = pd.read_csv(p.get_attr("path_default_culling_por"))["Por"].to_list()[0]
                df_growth_type = pd.read_csv(p.get_attr("path_d_growth_type"))
                df_growth_type= df_growth_type.loc[df_growth_type['Button'] == "d_growth_type", "State"].values.item(0)
                validation = True
                my_txt = "La Fecha de inicio de ajuste debe ser menor a la final"
                if (isinstance(all_ajustes_edad,str) or isinstance(all_ajustes_talla,str) or isinstance(all_ajustes_gen,str)):
                    #si alguno de los 3 es una cadena significa que se ha devuelto Error Fechas
                    validation = False
                    return ["Error en fechas. Ajustes de crecimiento: "+my_txt, default_campos_granjas.to_list(), default_campos_granjas.to_list()[0],\
                             panel,'Distribucion_M_S','ajustes_growth',update_tablas_trigger.to_json(orient='split', date_format='iso') ]
                if isinstance(all_ajustes_mort_gen,str):
                    #significa que se ha devuelto Error Fechas
                    validation = False
                    return ["Error en fechas. Ajustes de mortalidad: "+my_txt, default_campos_granjas.to_list(), default_campos_granjas.to_list()[0], \
                            panel,'Distribucion_M_S','ajustes_growth',update_tablas_trigger.to_json(orient='split', date_format='iso')]
                if validation:
                        for loop in range(1,(meses_sim+1)) :
                            mes_loop = pd.to_datetime(resultado['FechaFin'].unique()[0]).month
                            ano_loop = pd.to_datetime(resultado['FechaFin'].unique()[0]).year
                            escribir_log('info', dame_sesion()+": ######################################")
                            escribir_log('info', dame_sesion()+f": Year: {ano_loop} / Month: {mes_loop}")
                            resultado=p.set_alevines(resultado_df = resultado, all_alevines_df =all_alevines,
                                    peces_x_tanque = 2500, pm_y_cv_df = pesos_medios_entrada_alev).copy()
                            escribir_log('info', dame_sesion()+": Alevines ------ OK")
                            resultado=p.set_ventas(resultado_df = resultado, all_ventas_df = all_ventas, all_dispersion_df = all_dispersion_df,
                                    all_edad_venta_df = all_edad_venta_df, all_acabar_gen = all_acabar_gen, continue_flag= default_flag, loop = loop)
                            escribir_log('info', dame_sesion()+": Pescas ------ OK")
                            
                            resultado=p.set_bajas(resultado_df = resultado, all_reparto_mort_df = all_reparto_mort, all_ajustes_mort_gen_df = all_ajustes_mort_gen, 
                                    culling_edad = culling_edad, culling_por = culling_por, all_mortalidad_df = all_mortalidad)
                            escribir_log('info', dame_sesion()+": Bajas ------ OK")
                            resultado=p.set_crecimiento(resultado_df = resultado, curvas_df = curvas,  all_crecimientoD_df = all_crecimientoD,  
                                    all_ajustes_edad_df = all_ajustes_edad,  all_ajustes_talla_df = all_ajustes_talla, 
                                    all_ajustes_gen_df = all_ajustes_gen, d_growth_type = df_growth_type)
                            escribir_log('info', dame_sesion()+": Crecimiento ------ OK")
                            resultado = p.set_next_and_write(resultado_df = resultado, continue_flag = default_flag, loop = loop)
                            escribir_log('info', dame_sesion()+": Fin")
                
                        p.set_resultado()
                       
                        for i in range(1, 6):
                            escribir_log('info', dame_sesion()+": ######################################")
                        escribir_log('info', dame_sesion()+": Resultado guardado")
                        return ["Fin", default_campos_granjas.to_list(), default_campos_granjas.to_list()[0],\
                                 panel,'Distribucion_M_S','ajustes_growth',update_tablas_trigger.to_json(orient='split', date_format='iso')]
                #return [no_update, default_campos_granjas.to_list(), default_campos_granjas.tolist()[0], default_campos_granjas.tolist(), default_campos_granjas.tolist()[0]]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': ejecutar ' +"Error {0}".format(str(e)))
        escribir_log('critical', dame_sesion()+': Hubo un error en la ejecución: considere cambiar la fecha de inicio (anterior a la actual) e incluir más granjas')   
        default_campos_granjas = pd.DataFrame({'Granja': granjas})
        return [no_update, default_campos_granjas.to_list(), default_campos_granjas.tolist()[0], panel, \
                'Distribucion_M_S','ajustes_growth',update_tablas_trigger.to_json(orient='split', date_format='iso')]
#############################    




#callback para la subida de settings.
#toma el fichero que se ha subido, lo descomprime y
#sustituir los settings
@callback(
        Output('flag','on', allow_duplicate=True),
        Output("growth_tab", "value",allow_duplicate=True),
        Output('mem_update_tablas', 'data', allow_duplicate=True),
        Output('granjas_sim', 'value'),
        Output('date', 'date', allow_duplicate=True), #se repite
        Output("select_gr_despesques",'options',allow_duplicate=True),
        Output('select_gr_despesques','value',allow_duplicate=True),
        Output("despesques_tab", "value", allow_duplicate=True),        #Devuelvo uno cualquiera. Lo tengo para que se actualice
        Output("losses_tab", "value", allow_duplicate=True),  #Para actualizar 'select_gr_dist_mort'
        Input('upload-data', 'contents'),
        State('mem_update_tablas','data'),
        prevent_initial_call=True,
    running=[(Output('upload-data','disable_click'),True,False)]
)
def upload_settings(content,tablas_trigger):
    escribir_log('info', dame_sesion()+": callback: upload_settings")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        # the content needs to be split. It contains the type and the real content
        content_type, content_string = content.split(',')
        # Decode the base64 string
        content_decoded = base64.b64decode(content_string)
        # Use BytesIO to handle the decoded content
        zip_str = io.BytesIO(content_decoded)
        # Now you can use ZipFile to take the BytesIO output
        zip_obj = ZipFile(zip_str, 'r')

        #Para extraer los ficheros me tengo que poner en el directorio correspondiente
        ruta=os.path.join(p.get_attr("parent_dir"),p.get_attr("especie"),user)
        os.chdir(ruta)
        #Se borran los ficheros del directorio Temp y el directorio Temp
        for path in Path(os.path.join(ruta,"Temp")).glob("**/*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                rmtree(path)
        
        with zip_obj:
            zip_obj.extractall()
        ruta=p.get_attr("parent_dir")
        os.chdir(ruta)

        default_campos_granjas = pd.read_csv(p.get_attr("path_default_campos_granjas"))['Granja'].sort_values()
        default_fecha=pd.to_datetime(pd.read_csv(p.get_attr("path_default_fecha")).loc[0,'date']).date()
        material_switch = pd.read_csv(p.get_attr("path_d_growth_type"))
        
        default_flag=material_switch.loc[material_switch["Button"]=="continue","State"].to_list()[0]
        
        update_tablas_trigger=pd.read_json(StringIO(tablas_trigger), orient='split')
        update_tablas_trigger.loc[0,'trigger']+=1
        
        return default_flag,  'growth_estimado', update_tablas_trigger.to_json(orient='split', date_format='iso'), default_campos_granjas.to_list(), default_fecha,default_campos_granjas.to_list(), default_campos_granjas.to_list()[0], 'Por_Granja','Distribucion_M_S'
    except Exception as e:
        escribir_log('critical', dame_sesion()+': upload_settings ' +"Error {0}".format(str(e)))
        escribir_log('error', dame_sesion()+': Hubo un error procesando el fichero zip')
        return no_update, no_update, no_update, no_update, no_update,default_campos_granjas.to_list(), default_campos_granjas.to_list()[0], no_update,'Distribucion_M_S'
      
###################################
#Descarga de settings
####Descarga un zip en downloads con todo el directorio Temp
@callback(
    Output("download-text", "data"), 
    Input("save_set", "n_clicks"),
    State('nombre_settings','value'),
    State("settings_desc", "value"),
    prevent_initial_call=True
)
def descarga(n_clicks, nombre_fichero, descripcion):
    escribir_log('info', dame_sesion()+": callback: descarga")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        if n_clicks:
            filename=f"{user}_{nombre_fichero or 'IF_settings'}_{date.today()}.zip"
            directorio_principal=p.get_attr('parent_dir') 
            def write_archive(BytesIO):
                os.chdir(os.path.join(directorio_principal,p.get_attr("especie"),user,))
                with open(os.path.join(directorio_principal,p.get_attr("especie"),user, "Temp", "INFO.txt"), "w") as fileConn:
                    fileConn.write(descripcion)
                files=[]
                for dp, dn, filenames in  os.walk(os.path.join(directorio_principal,p.get_attr("especie"),user,"Temp")):
                    for f in filenames:
                        files.append(os.path.join(dp,f))
                with ZipFile(BytesIO, 'w') as zipf: #filename, 'w') as zipf:
                    for f in files:
                        zipf.write(f, os.path.relpath(f))
                os.chdir(directorio_principal)
            return dcc.send_bytes(write_archive, filename)
        return no_update
    except Exception as e:
        escribir_log('critical', dame_sesion()+': descarga ' +"Error {0}".format(str(e)))
        return no_update



################################################INPUTS################################################
def layout_inputs(campos_granjas, meses_max_sim, default_fecha):
    try:
        df_alevines, df_alevines_pm_cv= inicializar_actualizar_inputs(campos_granjas, meses_max_sim, default_fecha)
        return [
            dbc.Card(html.H4("Inputs", className='text-center'), color="info", inverse=True, style={"height": "6vh"}),
            html.Div([
                dcc.Tabs(id='inputs_tab', children=[ 
                    dcc.Tab(label='Num', children=[
                        html.Br(),
                        dbc.Row([ 
                                dash_table.DataTable(id='df_alevines',
                                                    data=df_alevines.to_dict('records'),
                                                    columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja','Total'])} for i in df_alevines.columns],
                                                    style_cell={'textAlign': 'right'},
                                                    style_header={'textAlign': 'center','fontWeight': 'bold'},
                                                    style_cell_conditional=[{'if': {'column_id': 'Granja'},'textAlign': 'center'}],
                                                    fixed_columns={'headers':True, 'data':1},style_table={'overflowX': 'auto','minWidth': '100%'})
                        ])
                    ]),
                    dcc.Tab(label='Inputs settings', children=[ 
                        html.Br(),
                        dbc.Row([
                                dash_table.DataTable(id='df_alevines_pm_cv',
                                                    data=df_alevines_pm_cv.to_dict('records'),
                                                    columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja'])} for i in df_alevines_pm_cv.columns],
                                                    style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                                                    style_cell_conditional=[{'if': {'column_id': 'Granja'},'textAlign': 'center'}],
                                                    style_table={'overflowX': 'auto','minWidth': '100%'})  
                        ])
                    ]),
                ]),
            ], style={"padding": "20px 20px 20px 20px"}),
        ]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': layout_inputs' +"Error {0}".format(str(e)))

#Inicializa-actualiza las tablas de alevines y alevines pm
def inicializar_actualizar_inputs(campos_granjas, meses_max_sim, default_fecha):
    escribir_log('info', dame_sesion()+": funcion: inicializar_actualizar_inputs")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        # Alevines num
        if os.path.exists(p.get_attr("path_df_alevines")):
            df_alevines=pd.read_csv(p.get_attr('path_df_alevines'))
        else:
            df_alevines=p.creador_generico_handson_1(campos_granjas, meses_max_sim, default_fecha)
            df_alevines.to_csv(p.get_attr("path_df_alevines"),index=False)
        # Alevines Pm y CV
        if os.path.exists(p.get_attr("path_df_alevines_pm_cv")):
            df_alevines_pm_cv= pd.read_csv(p.get_attr('path_df_alevines_pm_cv'))
        else:
            df_alevines_pm_cv=p.creador_generico_handson_4(campos_granjas)
            df_alevines_pm_cv.to_csv(p.get_attr("path_df_alevines_pm_cv"),index=False)
        return df_alevines, df_alevines_pm_cv
    except Exception as e:
        escribir_log('critical', dame_sesion()+': inicializar_actualizar_inputs ' +"Error {0}".format(str(e)))


#Actualizacion de inputs_alevines
@callback(
    Output('df_alevines', 'data'),
    Output('df_alevines','columns'),
    Input('df_alevines', 'data'),
    Input('mem_update_tablas', 'data'),
    Input('date','date'),
    State('granjas_sim','value'),
    prevent_initial_call=True
)
def actualizar_inputs_alevines(datos, trigger_tablas, fecha, granjas):
    escribir_log('info', dame_sesion()+": callback: actualizar_inputs_alevines")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
    
        entrada=callback_context.triggered_id
        if entrada=='date':
            newDF =pd.read_csv(p.get_attr('path_df_alevines')) 
            month_names= date_col_names(pd.to_datetime(fecha).date(), newDF.shape[1] -2)
            new_names=[newDF.columns[0]]+month_names+[newDF.columns[newDF.shape[1]-1]]
            newDF.columns= new_names
        elif entrada=='df_alevines':
            newDF =pd.DataFrame(datos,columns=datos[0].keys())
            #Para evitar introducir vacíos
            for i in range(1, newDF.shape[1]):
                newDF[newDF.columns[i]]=pd.to_numeric(newDF[newDF.columns[i]], errors='coerce')
            newDF= newDF.fillna(0)
            #Recalculo la columna y fila total
            newDF['Total']= 0
            columnas_meses=newDF.columns[1:]
            newDF.loc[newDF['Granja'] == "Total",columnas_meses]=[0]*len(columnas_meses)
            newDF= newDF.fillna(0)
            newDF.loc[newDF['Granja']  == "Total",columnas_meses]= newDF[columnas_meses].sum(axis=0).to_list()
            newDF['Total'] = newDF[columnas_meses].sum(axis=1) #no se puede sumar la primera columna que es granja
        elif entrada=='mem_update_tablas': #Se ha disparado el trigger de actualizar tablas
            meses_max_sim=18
            newDF, alevines_pm= inicializar_actualizar_inputs(granjas, meses_max_sim, fecha)

        newDF.to_csv(p.get_attr('path_df_alevines'),index=False)
        columnas=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja','Total'])} for i in newDF.columns]
        return newDF.to_dict('records'),columnas
    except Exception as e:
        escribir_log('critical', dame_sesion()+': actualizar_inputs_alevines ' +"Error {0}".format(str(e)))
        return no_update, no_update
      

#Actualizacion de inputs alevines_pm_cv
@callback(
    Output('df_alevines_pm_cv','data'),
    Input('df_alevines_pm_cv', 'data'),
    Input('mem_update_tablas', 'data'),
    prevent_initial_call=True
)
def actualizar_inputs_alevines_pm(datos, tablas_trigger):
    escribir_log('info', dame_sesion()+": callback: actualizar_inputs_alevines_pm")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        entrada=callback_context.triggered_id
        if entrada=='df_alevines_pm_cv':
            newDF =pd.DataFrame(datos, columns=datos[0].keys())
            
            #Para evitar introducir vacíos
            for i in range(1, newDF.shape[1]):
                newDF[newDF.columns[i]]=pd.to_numeric(newDF[newDF.columns[i]], errors='coerce')
            newDF= newDF.fillna(0)
            newDF.to_csv( p.get_attr('path_df_alevines_pm_cv'), index=False)
        elif entrada=='mem_update_tablas':
            newDF=pd.read_csv(p.get_attr('path_df_alevines_pm_cv'))
        return newDF.to_dict('records')
    except Exception as e:
        escribir_log('critical', dame_sesion()+': actualizar_inputs_alevines_pm ' +"Error {0}".format(str(e)))
        return no_update


##############################################DESPESQUES##############################################
def layout_despesques(default_campos_granjas):
    try:
        resultado=inicializar_actualizar_despesques('Despesques',default_campos_granjas.to_list()[0])
        df_despesques=resultado[0]
        return [
                dbc.Card(html.H4("Despesques", className='text-center'), color="info", inverse=True, style={"height": "6vh"}),
                    html.Div([
                        dbc.Row([html.B("Seleccione la granja de venta", style={"margin-bottom":"2w"})]),
                        dcc.Dropdown(id="select_gr_despesques", options=[{'label': gr, 'value': gr} for gr in default_campos_granjas.tolist()], value=default_campos_granjas.to_list()[0]),
                        html.Hr(),
                        dash_table.DataTable(id='df_despesques',
                            data=df_despesques.to_dict('records'),
                            columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja','Talla'] else 'text'), 'editable': (i not in  ['Granja', 'Talla'])} for i in df_despesques.columns],
                            style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                            style_cell_conditional=[{'if': {'column_id': ('Granja','Talla')},'textAlign': 'center'}],
                            fixed_columns={'headers':True, 'data':2}, style_table={'overflowX': 'auto','minWidth': '100%'}),
                        html.Hr(),
                        dcc.Tabs(id='despesques_tab', children=[ 
                            dcc.Tab(label='Total por granja', id='Total_por_granja', value='Por_Granja'),
                            dcc.Tab(label='Total por talla', id='Total_por_talla', value='Por_Talla'),
                            dcc.Tab(label='Disponibilidad', id='Disponibilidad', value='Disponibilidad'),
                            dcc.Tab(label='Acabar Gen', id='Acabar_Gen', value='Acabar_Gen'),
                            dcc.Tab(label='Dispersión', id='Dispersion', value='Dispersion'),
                            dcc.Tab(label='Edad mínima pescas', id='Edad_minima_pescas', value='Edad_pescas')
                        ], value='Por_Granja'),
                        dcc.Loading([
                            html.Div(id="tab-content"),],
                            target_components={'tab-content':'children'},delay_show=100) #,delay_hide=1)
                    ], style={"padding": "20px 20px 20px 20px"})
                ]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': layout_despesques ' +"Error {0}".format(str(e)))


# Callback para actualizar el tab de
#despesques. Esta puesto así apara que tarde menos en 
#cargar la página de inicio
@callback(
    Output("tab-content", "children"),
    Input("despesques_tab", "value"), #Estaba puesto [] en el input
    Input('select_gr_despesques', 'value'),
    #prevent_initial_call=True
)
def render_tab_content(active_tab,granja):
    escribir_log('info', dame_sesion()+": callback: render_tab_content")
    try:
        resultado=inicializar_actualizar_despesques(active_tab,granja)
        if active_tab == 'Por_Granja':
            resumen_desp_por_granja=resultado[0]
            return [html.Br(),
                    dbc.Row([
                            dash_table.DataTable(id='resumen_desp_por_granja',
                            data=resumen_desp_por_granja.to_dict('records'),
                            columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja','Talla'] else 'text')} for i in resumen_desp_por_granja.columns],
                            style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                            style_cell_conditional=[{'if': {'column_id': ('Granja','Talla')},'textAlign': 'center'}],
                            fixed_columns={'headers':True, 'data':1}, style_table={'overflowX': 'auto','minWidth': '100%'})
                    ]),
            ]
        elif active_tab == 'Por_Talla':
            resumen_desp_por_talla=resultado[0]
            return [html.Br(),
                    dbc.Row([ 
                            dash_table.DataTable(id='resumen_desp_por_talla',
                            data=resumen_desp_por_talla.to_dict('records'),
                            columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja','Talla'] else 'text')} for i in resumen_desp_por_talla.columns],
                            style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                            style_cell_conditional=[{'if': {'column_id': ('Granja','Talla')},'textAlign': 'center'}],
                            fixed_columns={'headers':True, 'data':2}, style_table={'overflowX': 'auto','minWidth': '100%'})
                    ])
            ]
        elif active_tab =='Disponibilidad':
            df_dispo_granja=resultado[0]
            return [html.Br(),
                    dbc.Row([
                            html.P("*** Esta es la disponibilidad de la ultima simulacion. Si se modifican las ventas, edad de ventas o dispersion de un mes la disponibilidad de los meses posteriores no sera la que aquí consta. Habrá que lanzar el modelo de nuevo. "),
                            dash_table.DataTable(id="df_dispo_granja",
                            data=df_dispo_granja.to_dict('records'),
                            columns=[{'name': i, 'id': i, 'type':('numeric' if i not in ['Granja','Talla'] else 'text'),'format':{'specifier': '.1f'}} for i in df_dispo_granja.columns],
                            style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                            style_cell_conditional=[{'if': {'column_id': ('Granja','Talla')},'textAlign': 'center'}],
                            fixed_columns={'headers':True, 'data':2}, style_table={'overflowX': 'auto','minWidth': '100%'})
                    ])
            ]
        elif active_tab=='Acabar_Gen':
            df_acabar_gen=resultado[0]
            default_campos_granjas=resultado[1].sort_values()
            granja=default_campos_granjas.to_list()[0]
            default_fecha=resultado[2].to_list()[0]
            return [html.Br(),
                    dbc.Row([ 
                            dash_table.DataTable(id="df_acabar_gen",
                            data=df_acabar_gen.to_dict('records'), 
                            columns=[{
                                'id': 'Activar','name': 'Activar','type': 'text','presentation':'dropdown','editable':True,'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': 'False'}},
                                {'id': 'Granja','name': 'Granja','type': 'text','presentation': 'dropdown','editable':True,'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': granja}},
                                {'id': 'Gen','name': 'Gen','type': 'text','editable':True,'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': "24 1"}},
                                {'id': 'Mes','name': 'Mes','type': 'datetime','editable':True,'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': default_fecha}}],
                            dropdown={
                                'Activar': {'options': [{'label': i, 'value': i}for i in ['True','False']]},
                                'Granja': {'options': [{'label': i, 'value': i} for i in default_campos_granjas.tolist()]},
                            },
                            style_cell={'textAlign': 'center'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                            style_table={'minWidth': '100%'},tooltip ={i: {'value': "Generacion tal y como aparece en elastic. ej: 21 1",
                                'use_with': 'both' } for i in ["Gen"]},tooltip_delay=0, tooltip_duration=None,css=[{"selector": ".Select-menu-outer","rule": 'display : block !important'}]
                            )
                    ])
            ]
        elif active_tab == 'Dispersion':
            df_dispersion=resultado[0]
            return [html.Br(),
                    dbc.Row([ 
                            dash_table.DataTable(id="df_dispersion",
                            data=df_dispersion.to_dict('records'),
                            columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja'])} for i in df_dispersion.columns],
                            style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                            style_cell_conditional=[{'if': {'column_id': 'Granja'},'textAlign': 'center'}],
                            fixed_columns={'headers':True, 'data':1}, style_table={'overflowX': 'auto','minWidth': '100%'})
                    ])
            ]
        elif active_tab == 'Edad_pescas':
            df_edad_pescas=resultado[0]
            return [html.Br(),
                    dbc.Row([ 
                            dash_table.DataTable(id="df_edad_pescas",
                            data=df_edad_pescas.to_dict('records'),
                            columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja'])} for i in df_edad_pescas.columns],
                            style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                            style_cell_conditional=[{'if': {'column_id': 'Granja'},'textAlign': 'center'}],
                            fixed_columns={'headers':True, 'data':1}, style_table={'overflowX': 'auto','minWidth': '100%'})
                    ])
            ]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': render_tab_content ' +"Error {0}".format(str(e)))
        return no_update


#Inicializa-actualiza las tablas de despesques, etc
def inicializar_actualizar_despesques(tipo,granja):
    escribir_log('info', dame_sesion()+": funcion: inicializar_actualizar_despesques")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        default_campos_granjas=pd.read_csv(p.get_attr('path_default_campos_granjas'))['Granja'].sort_values()
        meses_max_sim=18
        default_fecha=pd.read_csv(p.get_attr('path_default_fecha'))['date']
        if tipo in ['Despesques','Por_Granja', 'Por_Talla']:
            if os.path.exists(p.get_attr("path_df_despesques")):
                df_despesques_total = pd.read_csv(p.get_attr('path_df_despesques'))
            else:
                df_despesques_total=p.creador_generico_handson_2(default_campos_granjas.to_list(), meses_max_sim, default_fecha.to_list()[0])
                df_despesques_total.to_csv(p.get_attr("path_df_despesques"),index=False)

            
            df_despesques=df_despesques_total.loc[df_despesques_total['Granja']==granja]
            if tipo=='Despesques':
                return [df_despesques]
        if tipo=='Por_Granja':
            if not df_despesques is None:
                col=df_despesques.columns
                #Despesques por granja
                resumen_desp_por_granja=pd.melt(df_despesques_total, id_vars=["Granja", "Talla"], var_name="Month", value_name='Biomasa').copy() 
                resumen_desp_por_granja['Talla']='Consol'
                resumen_desp_por_granja=resumen_desp_por_granja.groupby(['Granja', 'Talla','Month']).agg({'Biomasa': 'sum'}).reset_index()
                resumen_desp_por_granja= pd.pivot_table(resumen_desp_por_granja, index=['Granja', 'Talla'], columns='Month', values='Biomasa').reset_index().copy()
                resumen_desp_por_granja=resumen_desp_por_granja[col]
                resumen_desp_por_granja.loc[len(resumen_desp_por_granja)]=resumen_desp_por_granja.iloc[0]
                resumen_desp_por_granja.loc[len(resumen_desp_por_granja)-1,'Granja']='Total'
                resumen_desp_por_granja= resumen_desp_por_granja.fillna(0)
                columnas_meses=resumen_desp_por_granja.columns[2:]
                resumen_desp_por_granja.loc[resumen_desp_por_granja['Granja'] == "Total","Talla"]='-'
                resumen_desp_por_granja.loc[resumen_desp_por_granja['Granja'] == "Total",columnas_meses]= [0]*len(columnas_meses)
                resumen_desp_por_granja.loc[resumen_desp_por_granja['Granja']  == "Total",columnas_meses]= resumen_desp_por_granja[columnas_meses].sum(axis=0).to_list()
                resumen_desp_por_granja=resumen_desp_por_granja[col]
                return [resumen_desp_por_granja]
        if tipo=='Por_Talla':
            if not df_despesques is None:
                col=df_despesques.columns
                #Despesques por talla
                resumen_desp_por_talla=pd.melt(df_despesques_total, id_vars=["Granja", "Talla"], var_name="Month", value_name='Biomasa').copy()
                resumen_desp_por_talla['Granja']='Consol'
                resumen_desp_por_talla=resumen_desp_por_talla.groupby(['Talla','Granja', 'Month']).agg({'Biomasa': 'sum'}).reset_index()
                resumen_desp_por_talla= pd.pivot_table(resumen_desp_por_talla, index=['Granja', 'Talla'], columns='Month', values='Biomasa').reset_index().copy()
                resumen_desp_por_talla.loc[len(resumen_desp_por_talla)]=resumen_desp_por_talla.iloc[0]
                resumen_desp_por_talla.loc[len(resumen_desp_por_talla)-1, 'Granja']='Total'
                resumen_desp_por_talla= resumen_desp_por_talla.fillna(0)
                columnas_meses=resumen_desp_por_talla.columns[2:]
                resumen_desp_por_talla.loc[resumen_desp_por_talla['Granja'] == "Total","Talla"]='-'
                resumen_desp_por_talla.loc[resumen_desp_por_talla['Granja'] == "Total",columnas_meses]= [0]*len(columnas_meses)
                resumen_desp_por_talla.loc[resumen_desp_por_talla['Granja']  == "Total",columnas_meses]= resumen_desp_por_talla[columnas_meses].sum(axis=0).to_list()
                resumen_desp_por_talla=resumen_desp_por_talla[col]
                return [resumen_desp_por_talla]
        
        #Disponibilidad
        if tipo=='Disponibilidad':
            df_dispo_granja=p.obtener_tabla_disponibilidad(granja)
            if df_dispo_granja is None:
                df_dispo_granja=p.creador_generico_handson_2([granja], meses_max_sim, default_fecha.to_list()[0])
            return [df_dispo_granja]
        #Acabar Gen
        if tipo=='Acabar_Gen':
            if os.path.exists(p.get_attr("path_df_acabar_gen")):
                df_acabar_gen = pd.read_csv(p.get_attr('path_df_acabar_gen'))
            else:
                df_acabar_gen=p.creador_generico_handson_5(default_campos_granjas.to_list())
                df_acabar_gen.to_csv(p.get_attr("path_df_acabar_gen"),index=False)

            df_acabar_gen['Mes']=df_acabar_gen['Mes'].apply(lambda x: pd.to_datetime(x).date())
            df_acabar_gen['Activar'] =df_acabar_gen['Activar'].map(str)
            df_acabar_gen['Gen'] =df_acabar_gen['Gen'].map(str)
            df_acabar_gen['Gen']=df_acabar_gen['Gen'].replace(to_replace="nan", value="").copy()
            return [df_acabar_gen, default_campos_granjas, default_fecha]
        #Dispersión
        #Hay que actualizar con la fecha de default_fecha
        if tipo=='Dispersion':
            if os.path.exists(p.get_attr("path_df_dispersion")):
                df_dispersion = pd.read_csv(p.get_attr('path_df_dispersion'))
                month_names= date_col_names(pd.to_datetime(default_fecha.to_list()[0]).date(), df_dispersion.shape[1] -1)
                new_names=[df_dispersion.columns[0]]+month_names
                df_dispersion.columns= new_names
                df_dispersion.to_csv( p.get_attr('path_df_dispersion'), index = False)
            else:
                df_dispersion=p.creador_generico_handson_1(default_campos_granjas.to_list(), meses_max_sim, default_fecha.to_list()[0]) 
                df_dispersion.to_csv(p.get_attr("path_df_dispersion"),index=False)
            return [df_dispersion.copy()]
        #Edad pescas
        #Hay que actualizar con la fecha de default_fecha
        if tipo=='Edad_pescas':
            if os.path.exists(p.get_attr("path_df_edad_pescas")):
                df_edad_pescas = pd.read_csv(p.get_attr('path_df_edad_pescas'))
                month_names= date_col_names(pd.to_datetime(default_fecha.to_list()[0]).date(), df_edad_pescas.shape[1] -1)
                new_names=[df_edad_pescas.columns[0]]+month_names
                df_edad_pescas.columns= new_names
                df_edad_pescas.to_csv( p.get_attr('path_df_edad_pescas'), index = False)
            else:
                df_edad_pescas=p.creador_generico_handson_1(default_campos_granjas.to_list(), meses_max_sim, default_fecha.to_list()[0])
                df_edad_pescas.to_csv(p.get_attr("path_df_edad_pescas"),index=False)
            return [df_edad_pescas]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': inicializar_actualizar_despesques ' +"Error {0}".format(str(e)))



@callback(
    Output('df_despesques', 'data'),
    Output('df_despesques', 'columns'),
    Input('df_despesques', 'data'),
    Input('date','date'),
    Input("select_gr_despesques", 'value'),
    prevent_initial_call=True
)
def actualizar_inputs_despesques(datos, fecha, granja):
    escribir_log('info', dame_sesion()+": callback: actualizar_inputs_despesques")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        entrada=callback_context.triggered_id
        if entrada=='date':
            newDF_T =pd.read_csv(p.get_attr('path_df_despesques'))
            month_names= date_col_names(pd.to_datetime(fecha).date(), newDF_T.shape[1] -2)
            new_names=[newDF_T.columns[0], newDF_T.columns[1]]+month_names
            newDF_T.columns= new_names
            newDF_T.to_csv( p.get_attr('path_df_despesques'), index = False)
            newDF=newDF_T.loc[newDF_T['Granja']==granja].copy()
        elif entrada=='df_despesques':
            newDF =pd.DataFrame(datos,columns=datos[0].keys())
            #Para evitar introducir vacíos
            for i in range(2, newDF.shape[1]):
                newDF[newDF.columns[i]]=pd.to_numeric(newDF[newDF.columns[i]], errors='coerce')
        
            newDF= newDF.fillna(0)
            newDF_rest =pd.read_csv(p.get_attr('path_df_despesques')) 
            newDF_rest=newDF_rest.loc[newDF_rest['Granja']!=granja]
            newDF_T=pd.concat([newDF if not newDF.empty else None, newDF_rest if not newDF_rest.empty else None], ignore_index=True)
            newDF_T.to_csv( p.get_attr('path_df_despesques'), index = False)
            
        elif entrada=="select_gr_despesques":
            newDF_T=pd.read_csv(p.get_attr('path_df_despesques'))
            newDF=newDF_T.loc[newDF_T['Granja']==granja].copy()

        columnas=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja','Talla'] else 'text'), 'editable': (i not in  ['Granja', 'Talla'])} for i in newDF.columns]
        return newDF.to_dict('records'), columnas
    except Exception as e:
        escribir_log('critical', dame_sesion()+': actualizar_inputs_despesques ' +"Error {0}".format(str(e)))
        return no_update, no_update
    
@callback(
    
    Output('resumen_desp_por_granja', 'data'),
    Output('resumen_desp_por_granja', 'columns'),
    Input('df_despesques', 'data'),
    Input('df_despesques', 'columns'),
    Input('despesques_tab','value'),
    prevent_initial_call=True
)
def actualizar_inputs_despesques_por_granja(datos, columnas, tipo_tab):
    escribir_log('info', dame_sesion()+": callback: actualizar_inputs_despesques_por_granja")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        
        newDF_T =pd.read_csv(p.get_attr('path_df_despesques'))
        col=newDF_T.columns
        
        #Despesques por granja
        if tipo_tab=='Por_Granja':
            desp_por_granja=pd.melt(newDF_T, id_vars=["Granja", "Talla"], var_name="Month", value_name='Biomasa').copy() #df_despesques_total
            desp_por_granja['Talla']='Consol'
            desp_por_granja['Biomasa'] =desp_por_granja['Biomasa'].map(int)
            desp_por_granja=desp_por_granja.groupby(['Granja', 'Talla','Month']).agg({'Biomasa': 'sum'}).reset_index()
            desp_por_granja= pd.pivot_table(desp_por_granja, index=['Granja', 'Talla'], columns='Month', values='Biomasa').reset_index().copy()
            desp_por_granja=desp_por_granja[col]
            #Añado la fila de Total
            desp_por_granja.loc[desp_por_granja.shape[0]]=desp_por_granja.iloc[0]
            desp_por_granja.loc[desp_por_granja.shape[0]-1,'Granja']='Total'
            desp_por_granja= desp_por_granja.fillna(0)
            columnas_meses=desp_por_granja.columns[2:]
            desp_por_granja.loc[desp_por_granja['Granja'] == "Total","Talla"]='-'
            desp_por_granja.loc[desp_por_granja['Granja'] == "Total",columnas_meses]= [0]*len(columnas_meses)
            desp_por_granja.loc[desp_por_granja['Granja']  == "Total",columnas_meses]= desp_por_granja[columnas_meses].sum(axis=0).to_list()
            desp_por_granja=desp_por_granja[col]
            columnas1=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja','Talla'] else 'text')} for i in desp_por_granja.columns]
            return desp_por_granja.to_dict('records'), columnas1
        return [], []
    except Exception as e:
        escribir_log('critical', dame_sesion()+': actualizar_inputs_despesques_por_granja' +"Error {0}".format(str(e)))
        return no_update, no_update
    

@callback(
    Output('resumen_desp_por_talla', 'data'),
    Output('resumen_desp_por_talla', 'columns'),
    Input('df_despesques', 'data'),
    Input('df_despesques', 'columns'),
    Input('despesques_tab','value'),
    prevent_initial_call=True
)
def actualizar_inputs_despesques_por_talla(datos, columnas, tipo_tab):
    escribir_log('info', dame_sesion()+": callback: actualizar_inputs_despesques_por_talla")
    try:
        user=current_user.name
        #Despesques por talla
        if tipo_tab=='Por_Talla':
            p=funcsif()
            p.inicializar(user)
            newDF_T =pd.read_csv(p.get_attr('path_df_despesques'))
            col=newDF_T.columns
            desp_por_talla=pd.melt(newDF_T, id_vars=["Granja", "Talla"], var_name="Month", value_name='Biomasa').copy()#df_despesques_total
            desp_por_talla['Granja']='Consol'
            desp_por_talla['Biomasa'] =desp_por_talla['Biomasa'].map(int)
            desp_por_talla=desp_por_talla.groupby(['Talla','Granja', 'Month']).agg({'Biomasa': 'sum'}).reset_index()
            desp_por_talla= pd.pivot_table(desp_por_talla, index=['Granja', 'Talla'], columns='Month', values='Biomasa').reset_index().copy()
            #Añado la fila de Total
            desp_por_talla.loc[desp_por_talla.shape[0]]=desp_por_talla.iloc[0]
            desp_por_talla.loc[desp_por_talla.shape[0]-1, 'Granja']='Total'
            desp_por_talla= desp_por_talla.fillna(0)
            columnas_meses=desp_por_talla.columns[2:]
            desp_por_talla.loc[desp_por_talla['Granja'] == "Total","Talla"]='-'
            desp_por_talla.loc[desp_por_talla['Granja'] == "Total",columnas_meses]= [0]*len(columnas_meses)
            desp_por_talla.loc[desp_por_talla['Granja']  == "Total",columnas_meses]= desp_por_talla[columnas_meses].sum(axis=0).to_list()
            desp_por_talla=desp_por_talla[col]
            columnas1=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja','Talla'] else 'text')} for i in desp_por_talla.columns]
            return desp_por_talla.to_dict('records'), columnas1
        
        return [],[]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': actualizar_inputs_despesques_por_talla' +"Error {0}".format(str(e)))
        return no_update, no_update


###OJO: Dispersion NO tiene fila de Total
#No se puede actualizar por fecha
@callback(
    Output('df_dispersion', 'data'),
    Output('df_dispersion', 'columns'),
    Input('df_dispersion', 'data'),
    #Input('mem_fecha','data'),
    #Input('date','date'),
    State('despesques_tab','value'),
    prevent_initial_call=True
)
def actualizar_inputs_dispersion(datos, tipo_tab):
    escribir_log('info', dame_sesion()+": callback: actualizar_inputs_dispersion")
    try:
        user=current_user.name
        if tipo_tab=='Dispersion':
            p=funcsif()
            p.inicializar(user)
            entrada=callback_context.triggered_id
            if entrada=='df_dispersion':
            
                newDF =pd.DataFrame(datos,columns=datos[0].keys())
                #Para evitar introducir vacíos
                for i in range(1, newDF.shape[1]):
                    newDF[newDF.columns[i]]=pd.to_numeric(newDF[newDF.columns[i]], errors='coerce')
                newDF= newDF.fillna(0)
                newDF.to_csv(p.get_attr('path_df_dispersion'), index = False)
            df_dispersion=newDF.copy()
            columnas=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja'])} for i in df_dispersion.columns]
            return df_dispersion.to_dict('records'),columnas
        return [],[]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': actualizar_inputs_dispersion ' +"Error {0}".format(str(e)))
        return no_update, no_update
      
@callback(
    Output('df_edad_pescas', 'data'),
    Output('df_edad_pescas', 'columns'),
    Input('df_edad_pescas', 'data'),
    #Input('mem_fecha','data'),
    #Input('date','date'),
    Input('despesques_tab','value'),
    prevent_initial_call=True
)
def actualizar_inputs_edad_pescas(datos, tipo_tab):
    escribir_log('info', dame_sesion()+": callback: actualizar_inputs_edad_pescas")
    try:
        user=current_user.name
        if tipo_tab=='Edad_pescas':
            p=funcsif()
            p.inicializar(user)
            entrada=callback_context.triggered_id
            #if entrada=='date':
            #if entrada=='mem_fecha':
            #    fecha=pd.read_json(StringIO(dato_fecha), orient='split').loc[0,'date']
            #    newDF =pd.read_csv(p.get_attr('path_df_edad_pescas'))
            #    month_names= date_col_names(pd.to_datetime(fecha).date(), newDF.shape[1] -1)
            #    new_names=[newDF.columns[0]]+month_names
            #    newDF.columns= new_names
            #    newDF.to_csv( p.get_attr('path_df_edad_pescas'), index = False)
            if entrada=='df_edad_pescas':
                newDF =pd.DataFrame(datos,columns=datos[0].keys())
                #Para evitar introducir vacíos
                for i in range(1, newDF.shape[1]):
                    newDF[newDF.columns[i]]=pd.to_numeric(newDF[newDF.columns[i]], errors='coerce')
                newDF= newDF.fillna(0)
                newDF.to_csv( p.get_attr('path_df_edad_pescas'), index = False)
            df_edad_pescas=newDF.copy()
            columnas=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja'])} for i in df_edad_pescas.columns]
            return df_edad_pescas.to_dict('records'),columnas
        return [],[]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': actualizar_inputs_edad_pescas ' +"Error {0}".format(str(e)))
        return no_update, no_update

@callback(
    Output(component_id='df_acabar_gen', component_property='data'),
    Input('df_acabar_gen', 'data'),
    State('df_acabar_gen','data_previous'),
    State('granjas_sim','value'),
    State('date','date'),
    State('despesques_tab','value'),
    prevent_initial_call=True
)
def update_tabla_acabar_gen(datos, datos_previos,granjas, fecha, tipo_tab):
    escribir_log('info', dame_sesion()+": callback: update_tabla_acabar_gen")
    try:
        user=current_user.name
        if tipo_tab=='Acabar_Gen':
            p=funcsif()
            p.inicializar(user)
            newDF = pd.DataFrame(datos,columns=datos[0].keys())
            antiguoDF = pd.DataFrame(datos_previos,columns=datos_previos[0].keys())
            antiguoDF["Activar"] = antiguoDF["Activar"].map(str)
            newDF["Activar"] = newDF["Activar"].map(str)
            df_acabar_gen=pd.read_csv(p.get_attr('path_df_acabar_gen'))
            ###Validacion
            error=False
            if antiguoDF.shape==newDF.shape:
                Posicion=obtener_celda_distinta(newDF,antiguoDF)
                if not Posicion is None:
                    datonuevo=newDF.loc[Posicion[0],Posicion[1]]
                    if Posicion[1]=="Mes":
                        if datonuevo != datetime.datetime.strptime(datonuevo, "%Y-%m-%d").strftime('%Y-%m-%d'):
                            error=True
                        else:
                            #Hay que poner el día 1 del mes
                            datonuevo=pd.to_datetime(datonuevo).date().replace(day=1).strftime('%Y-%m-%d')
                            newDF.loc[Posicion[0],Posicion[1]]=datonuevo
                    elif Posicion[1]=="Gen":
                        if p.get_attr('especie')=="TURBOT":
                            if len(re.findall(r"^[2][0-9]\s[1-4]$",datonuevo))==0 or len(datonuevo)!=4:
                                error=True
                        elif p.get_attr('especie')=="SOLE":
                            if len(re.findall(r"^[2][0-9]\s[1-6]$",datonuevo))==0 or len(datonuevo)!=4:
                                error=True
                        
                        
            if not error:
                newDF=newDF.loc[newDF["Activar"]=="True"]
                df2=pd.DataFrame({'Activar':['False'], 'Granja':[granjas[0]], 'Gen':["24 1"], 'Mes':[pd.to_datetime(fecha).date().replace(day=1)]})
                newDF=pd.concat([newDF if not newDF.empty else None, df2 if not df2.empty else None], ignore_index=True)
                newDF=newDF.fillna(0)
                newDF.to_csv(p.get_attr('path_df_acabar_gen'), index = False)
                df_acabar_gen=newDF.copy() 

            df_acabar_gen["Activar"] = df_acabar_gen["Activar"].map(str)
            return df_acabar_gen.to_dict('records')
        return [],[]
    except Exception as e:
        escribir_log('critical',dame_sesion()+": update_tabla_acabar_gen "+"Error {0}".format(str(e)))
        df_acabar_gen["Activar"] = df_acabar_gen["Activar"].map(str)
        return df_acabar_gen.to_dict('records')




#####################OJO Disponibilidad no tiene totales pero en el del Quillo se los puso. Yo no lo hago porque solo presenta una granja de cada vez
#y está filtrado por la granja de select_gr_despesques

@callback(
    output=[Output('df_dispo_granja','data'),
    Output('df_dispo_granja','columns')],
    inputs=dict(
        #dato_fecha=Input('mem_fecha','data'),
        #fecha=Input('date','date'),
        granja=Input('select_gr_despesques','value')),
    state=dict(meses=State('meses_sim', 'value'),
        trigger=State('mem_update','data'),
        tipo_tab=State('despesques_tab','value'),
        fecha=State('date','date')),
    prevent_initial_call=True,
    #background=True,  # Indica que es un background callback

    running=[
        (Output("date", "disabled"), True, False),
        (Output("select_gr_despesques", "disabled"), True, False),
        (Output("inicializar_tablas", "disabled"), True, False),
        (Output("run_model", "disabled"), True, False),
        (Output('borrar_ultimo_mes', 'disabled'),True, False),
    ],
)
##########Nota
#dispersion_datos=Input('df_dispersion','data'),
#edad_pescas_datos=Input('df_edad_pescas', 'data')
#No pueden funcionar como entradas porque no están disponibles a la vez que la tabla de disponibilidad
def update_tabla_disponibilidad(granja,meses, trigger, tipo_tab,fecha):
    escribir_log('info', dame_sesion()+": callback: update_tabla_disponibilidad")
    try:
        user=current_user.name
        if tipo_tab=='Disponibilidad':
            p=funcsif()
            p.inicializar(user)
            df_dispo_granja=p.obtener_tabla_disponibilidad(granja)
            if df_dispo_granja is None:
                #fecha=pd.read_json(StringIO(dato_fecha), orient='split').loc[0,'date']
                df_dispo_granja=p.creador_generico_handson_2([granja], meses, fecha)

            columnas=[{'name': i, 'id': i, 'type':('numeric' if i not in ['Granja','Talla'] else 'text'),'format': {'specifier': '.1f'}} for i in df_dispo_granja.columns]
            return [df_dispo_granja.to_dict('records'),columnas]
        return [[],[]]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': update_tabla_disponibilidad ' +"Error {0}".format(str(e)))
        return [no_update, no_update]




###############################################PERDIDAS###############################################
               


def layout_perdidas():
    try:
        return [
            dbc.Card(html.H4("Losses", className='text-center'), color="info", inverse=True, style={"height": "6vh"}),
            html.Div([
                dcc.Tabs(id='losses_tab', children=[ 
                    dcc.Tab(label='M + S', id='m_s', value='M_S'),
                    dcc.Tab(label='Culling', id='culling', value='Culling'),
                    dcc.Tab(label='Distribución M+S', id='distribucion_m_s', value='Distribucion_M_S'),
                    dcc.Tab(label='Ajustes', id='ajustes', value='Ajustes')
                        ], value='M_S'),
                html.Div(id="tab-content-perdidas")
            ],style={"padding": "20px 20px 20px 20px"}),
        ]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': layout_perdidas ' +"Error {0}".format(str(e)))

def inicializar_actualizar_perdidas(tipo,granja=None):
    escribir_log('info', dame_sesion()+": callback: inicializar_actualizar_perdidas")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        default_campos_granjas=pd.read_csv(p.get_attr('path_default_campos_granjas'))['Granja'].sort_values()
        meses_max_sim=18
        default_fecha=pd.read_csv(p.get_attr('path_default_fecha'))['date'].to_list()[0]

        #Culling
        if tipo=='Culling':
            default_culling_por = np.where(os.path.exists(p.get_attr("path_default_culling_por")), pd.read_csv(p.get_attr('path_default_culling_por'))["Por"].to_list()[0], 1)
            default_culling_edad = np.where(os.path.exists(p.get_attr("path_default_culling_por")), pd.read_csv(p.get_attr('path_default_culling_por'))["Edad"].to_list()[0], 166)
            return [default_culling_por,default_culling_edad]
        #losses
        #Hay que actualizar la fecha
        if tipo=='M_S':
            if os.path.exists(p.get_attr("path_df_losses")):
                df_losses=pd.read_csv(p.get_attr('path_df_losses'))
                month_names= date_col_names(pd.to_datetime(default_fecha).date(), df_losses.shape[1] -2)
                new_names=[df_losses.columns[0]]+month_names+[df_losses.columns[df_losses.shape[1]-1]]
                df_losses.columns= new_names
                df_losses.to_csv(p.get_attr("path_df_losses"),index=False)
            
            else:
                df_losses=p.creador_generico_handson_1(default_campos_granjas.to_list(), meses_max_sim, default_fecha)
                df_losses.to_csv(p.get_attr("path_df_losses"),index=False)
            return [df_losses]
        #Reparto mortalidad
        if tipo=='Distribucion_M_S':
            if granja is None:
                granja=default_campos_granjas.to_list()[0]
            if os.path.exists(p.get_attr("path_df_reparto_mort")):
                df_reparto_mort = pd.read_csv(p.get_attr('path_df_reparto_mort'))
            else:
                df_reparto_mort=p.creador_generico_handson_6(default_campos_granjas.to_list())
                df_reparto_mort.to_csv(p.get_attr("path_df_reparto_mort"),index=False)
            df_reparto_mort=df_reparto_mort.loc[df_reparto_mort['Granja']==granja].reset_index().drop(columns=['index'], axis=1)
            pesos=rnorm3(n=1000, mean_1=df_reparto_mort.loc[0,'PesoMedio_1'], cv_1=df_reparto_mort.loc[0,'CV_1']/100, mean_2=df_reparto_mort.loc[0,'PesoMedio_2'], cv_2=df_reparto_mort.loc[0,'CV_2']/100)
        
            mean_pesos = int(round(np.mean(pesos),0))
            hist_data = [pesos]
            group_labels = ['']
            colors = ['#333F44']

            # Create distplot with curve_type set to 'normal'
            if (p.get_attr('especie'))=='TURBOT':
                rango=[0,4000]
            if (p.get_attr('especie'))=='SOLE':
                rango=[0,1500]
            figura = ff.create_distplot(hist_data, group_labels, colors=colors, show_hist=False, show_rug=False ).add_vline(x=mean_pesos,
                        line=dict(dash='dash')).update_layout(showlegend=False,title_text=f'Peso medio total: {mean_pesos}').update_xaxes(range = rango)
            return [default_campos_granjas,df_reparto_mort,figura]
        #Ajustes mortalidad
        if tipo=='Ajustes':
            if os.path.exists(p.get_attr("path_df_ajustes_mortalidad")):
                df_ajustes_mortalidad = pd.read_csv(p.get_attr('path_df_ajustes_mortalidad'))
            else:
                df_ajustes_mortalidad=p.creador_generico_handson_3(default_campos_granjas.to_list(), col_por_cul=True)
                df_ajustes_mortalidad.to_csv(p.get_attr("path_df_ajustes_mortalidad"),index=False)
            df_ajustes_mortalidad['Mes_inicio']=df_ajustes_mortalidad['Mes_inicio'].apply(lambda x: pd.to_datetime(x).date())
            df_ajustes_mortalidad['Mes_fin']=df_ajustes_mortalidad['Mes_fin'].apply(lambda x: pd.to_datetime(x).date())
            df_ajustes_mortalidad["Activar"] = df_ajustes_mortalidad["Activar"].map(str)
            df_ajustes_mortalidad["Por_Cull"] = df_ajustes_mortalidad["Por_Cull"].map(str)
            df_ajustes_mortalidad["Talla_Gen_Edad"] = df_ajustes_mortalidad["Talla_Gen_Edad"].map(str)
            df_ajustes_mortalidad['Talla_Gen_Edad']=df_ajustes_mortalidad['Talla_Gen_Edad'].replace(to_replace="nan", value="").copy()
            return [df_ajustes_mortalidad, default_fecha, default_campos_granjas]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': inicializar_actualizar_perdidas ' +"Error {0}".format(str(e)))


# Callback para actualizar el tab de
#perdidas. Esta puesto así apara que tarde menos en 
#cargar la página de inicio
@callback(
    Output("tab-content-perdidas", "children"),
    Input("losses_tab", "value"),
    #prevent_initial_call=True
)
def render_tab_content_perdidas(active_tab):
    escribir_log('info', dame_sesion()+": callback: render_tab_content_perdidas")
    try:
        resultado=inicializar_actualizar_perdidas(active_tab)
        if active_tab == 'M_S':
            df_losses=resultado[0]                 
            return[
                html.Br(),
                dbc.Row([ 
                        dash_table.DataTable(id='df_losses',
                                            data=df_losses.to_dict('records'),
                                            columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja','Total'])} for i in df_losses.columns],
                                            style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                                            style_cell_conditional=[{'if': {'column_id': 'Granja'},'textAlign': 'center'}],
                                            fixed_columns={'headers':True, 'data':1},style_table={'overflowX': 'auto','minWidth': '100%'})
                ])
            ]
        elif active_tab == 'Culling':
            default_culling_por=resultado[0]
            default_culling_edad=resultado[1]
            return [
                html.Br(),
                dbc.Row([
                    dbc.Col([
                    html.Br(),
                        html.B("En % del batch: "),
                        html.Br(),
                        dcc.Input(id='culling_por', type='number',value=default_culling_por, min=0, max=100, step=1),
                        html.Br(),
                        html.Br(),
                        html.B("Edad aproximada culling: "),
                        html.Br(),
                        dcc.Input(id='culling_edad', type='number',value=default_culling_edad, min=0, max=1000, step=1),
                        html.Br(),
                    ])
                ])
            ]
        elif active_tab=='Distribucion_M_S':
            default_campos_granjas=resultado[0].sort_values()
            df_reparto_mort=resultado[1]
            figura=resultado[2]
            return [
                html.Br(),
                dbc.Row([html.Br(),
                        dbc.Col([
                            dbc.Row([html.B("Seleccione la granja", style={"margin-bottom":"2w"})]),
                            dcc.Dropdown(id="select_gr_dist_mort", options=[{'label': gr, 'value': gr} for gr in default_campos_granjas.tolist()], value=default_campos_granjas.tolist()[0]),
                            html.Br(),
                            dbc.Row([
                                dash_table.DataTable(id='df_reparto_mort',
                                    data=df_reparto_mort.to_dict('records'),
                                    columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja'])} for i in df_reparto_mort.columns],
                                    style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                                    style_cell_conditional=[{'if': {'column_id': 'Granja'},'textAlign': 'center'}],
                                    fixed_columns={'headers':True, 'data':1},style_table={'overflowX': 'auto','minWidth': '100%'})
                            ]),
                        ],style={'margin':'auto'},width=7,),
                        dbc.Col([html.Br(),
                            dcc.Graph(id='plot_dist_mort',figure=figura)
                        ],width=5),
                ])
            ]
        elif active_tab=='Ajustes':
            df_ajustes_mortalidad=resultado[0]
            default_fecha=resultado[1]
            default_campos_granjas=resultado[2].sort_values()
            return [
                html.Br(),
                dbc.Row([ 
                    dash_table.DataTable(id='df_ajustes_mortalidad',
                        data=df_ajustes_mortalidad.to_dict('records'),
                        columns=[{
                            'id': 'Activar','name': 'Activar','type': 'text','presentation':'dropdown','editable':True,'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': "False"}},
                            {'id': 'Granja','name': 'Granja','type': 'text','presentation': 'dropdown','editable':True,'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': default_campos_granjas.tolist()[0]}},
                            {'id': 'Ajuste_por','name': 'Ajuste_por','type': 'text','editable':False,'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': "Gen"}},
                            {'id': 'Talla_Gen_Edad','name': 'Talla_Gen_Edad','type': 'text','editable':True, 'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': "24 1"}},
                            {'id': 'Mes_inicio','name': 'Mes_inicio','type': 'datetime','editable':True,'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': default_fecha}},
                            {'id': 'Mes_fin','name': 'Mes_fin','type': 'datetime','editable':True, 'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': default_fecha}},
                            {'id': 'Ajuste','name': 'Ajuste','type': 'numeric','format': Format(precision=2, scheme=Scheme.decimal_integer),'editable':True,'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': "0"}},
                            {'id': 'Por_Cull','name': 'Por_Cull','type': 'text','editable':True,'presentation':'dropdown','on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': "False"}} ],
                        dropdown={
                            'Activar': {'options': [{'label': i, 'value': i}for i in ['True','False']]},
                            'Granja': {'options': [{'label': i, 'value': i} for i in default_campos_granjas.tolist()]},
                            'Por_Cull': {'options': [{'label': i, 'value': i} for i in ['True','False']]}
                        },style_cell={'textAlign': 'center'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                        fixed_columns={'headers':True, 'data':1},style_table={'overflowX': 'auto','minWidth': '100%'},tooltip ={i: {'value': "Ej Gen: 21 3",
                            'use_with': 'both' } for i in ["Talla_Gen_Edad"]},tooltip_delay=0, tooltip_duration=None, css=[{"selector": ".Select-menu-outer","rule": 'display : block !important'}])
                ])
            ]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': render_tab_content_perdidas ' +"Error {0}".format(str(e)))
        return no_update
            


#####¡OJO! df_losses tiene fila y columna de total
@callback(
    Output('df_losses','data'),
    Output('df_losses','columns'),
    Input('df_losses','data'),
    Input('mem_fecha','data'),
    #Input('date','date'),
    prevent_initial_call=True
)
def update_df_losses(datos,dato_fecha):
    escribir_log('info', dame_sesion()+": callback: update_df_losses")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        entrada=callback_context.triggered_id
        #if entrada=='date':
        if entrada=='mem_fecha':
            fecha=pd.read_json(StringIO(dato_fecha), orient='split').loc[0,'date']
            newDF =pd.read_csv(p.get_attr('path_df_losses'))
            month_names= date_col_names(pd.to_datetime(fecha).date(), newDF.shape[1] -2)
            new_names=[newDF.columns[0]]+month_names+[newDF.columns[newDF.shape[1]-1]]
            newDF.columns= new_names
            newDF.to_csv( p.get_attr('path_df_losses'), index = False)
            
        if entrada=='df_losses': 
            newDF =pd.DataFrame(datos,columns=datos[0].keys())
            #Para evitar introducir vacíos
            for i in range(1, newDF.shape[1]):
                newDF[newDF.columns[i]]=pd.to_numeric(newDF[newDF.columns[i]], errors='coerce')
            newDF= newDF.fillna(0)
            #Recalculo el total (fila y columna)
            newDF['Total']= 0
            columnas_meses=newDF.columns[1:]
            newDF.loc[newDF['Granja'] == "Total",columnas_meses]= [0]*len(columnas_meses)
            newDF.loc[newDF['Granja']  == "Total",columnas_meses]= newDF[columnas_meses].sum(axis=0).to_list()
            newDF['Total'] = newDF[columnas_meses].sum(axis=1) #no se puede sumar la primera columna que es granja
            newDF= newDF.fillna(0)
            newDF.to_csv( p.get_attr('path_df_losses'), index = False)
        df_losses=newDF.copy()
        columnas=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja','Total'])} for i in df_losses.columns]
        return df_losses.to_dict('records'),columnas
    except Exception as e:
        escribir_log('critical', dame_sesion()+': update_df_losses ' +"Error {0}".format(str(e)))
        return no_update, no_update
         
                
@callback(
    Input("culling_por","value"),
    Input("culling_edad","value"),
    prevent_initial_call=True
)
def actualizar_culling(valor_culling_por,valor_culling_edad):
    escribir_log('info', dame_sesion()+": callback: actualizar_culling")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        
        entrada=callback_context.triggered_id
        newDF=pd.read_csv(p.get_attr("path_default_culling_por"))
        if entrada=="culling_por":
            newDF.loc[0,"Por"]=valor_culling_por
        else:
            newDF.loc[0,"Edad"]=valor_culling_edad
        newDF.to_csv(p.get_attr("path_default_culling_por"),index=False)
    except Exception as e:
        escribir_log('critical', dame_sesion()+': actualizar_culling ' +"Error {0}".format(str(e)))



                
@callback(
    Output('df_ajustes_mortalidad','data'),
    Input('df_ajustes_mortalidad','data'),
    State('df_ajustes_mortalidad', 'data_previous'),
    State('date','date'),
    State('granjas_sim','value'),
    prevent_initial_call=True
)
def update_ajustes_mortalidad(datos,datos_previos,fecha,granjas):
    escribir_log('info', dame_sesion()+": callback: update_ajustes_mortalidad")
    try:
        user=current_user.name
        if not datos_previos is None:
            p=funcsif()
            p.inicializar(user)
            newDF = pd.DataFrame(datos,columns=datos[0].keys())
            antiguoDF = pd.DataFrame(datos_previos,columns=datos_previos[0].keys())
            newDF["Activar"] = newDF["Activar"].map(str)
            df_ajustes_mortalidad=pd.read_csv(p.get_attr('path_df_ajustes_mortalidad'))
            ###Validacion
            error=False
            if antiguoDF.shape==newDF.shape:
                Posicion=obtener_celda_distinta(newDF,antiguoDF)
                if not Posicion is None:
                    datonuevo=newDF.loc[Posicion[0],Posicion[1]]
                    if Posicion[1]=="Mes_inicio":
                        if datonuevo != datetime.datetime.strptime(datonuevo, "%Y-%m-%d").strftime('%Y-%m-%d'):
                            error=True
                        else:
                             #Hay que poner el día 1 del mes
                            datonuevo=pd.to_datetime(datonuevo).date().replace(day=1).strftime('%Y-%m-%d')
                            newDF.loc[Posicion[0],Posicion[1]]=datonuevo
                            if datonuevo>newDF.loc[Posicion[0],"Mes_fin"]:
                                error=True
                    elif Posicion[1]=="Mes_fin":
                        if datonuevo != datetime.datetime.strptime(datonuevo, "%Y-%m-%d").strftime('%Y-%m-%d'):
                            error=True
                        else:
                            #Hay que poner el día 1 del mes
                            datonuevo=pd.to_datetime(datonuevo).date().replace(day=1).strftime('%Y-%m-%d')
                            newDF.loc[Posicion[0],Posicion[1]]=datonuevo
                            if datonuevo<newDF.loc[Posicion[0],"Mes_inicio"]:
                                error=True
                    elif Posicion[1]=="Talla_Gen_Edad":
                        if p.get_attr('especie')=="TURBOT":
                            if len(re.findall(r"^[2][0-9]\s[1-4]$",datonuevo))==0 or len(datonuevo)!=4:
                                error=True
                        elif p.get_attr('especie')=="SOLE":
                            if len(re.findall(r"^[2][0-9]\s[1-6]$",datonuevo))==0 or len(datonuevo)!=4:
                                error=True

            if not error:
                newDF=newDF.loc[newDF['Activar']=='True']  
                df2=pd.DataFrame({'Activar':['False'], 'Granja':[granjas[0]], 'Ajuste_por':["Gen"],'Talla_Gen_Edad':["24 1"],
                                'Mes_inicio':[pd.to_datetime(fecha).date().replace(day=1)],'Mes_fin':[pd.to_datetime(fecha).date().replace(day=1)],'Ajuste':[0], 'Por_Cull':['False'],})
                newDF=pd.concat([newDF if not newDF.empty else None, df2 if not df2.empty else None], ignore_index=True)
                newDF.to_csv( p.get_attr('path_df_ajustes_mortalidad'), index = False)
                df_ajustes_mortalidad=newDF.copy()    

            df_ajustes_mortalidad["Activar"] = df_ajustes_mortalidad["Activar"].map(str)
            df_ajustes_mortalidad["Por_Cull"] = df_ajustes_mortalidad["Por_Cull"].map(str)
            return df_ajustes_mortalidad.to_dict('records')
        else:
            return no_update
    except Exception as e:
        escribir_log('critical',dame_sesion()+": update_ajustes_mortalidad "+"Error {0}".format(str(e)))
        df_ajustes_mortalidad["Activar"] = df_ajustes_mortalidad["Activar"].map(str)
        df_ajustes_mortalidad["Por_Cull"] = df_ajustes_mortalidad["Por_Cull"].map(str)
        return df_ajustes_mortalidad.to_dict('records')



@callback(
    Output('df_reparto_mort','data'),
    Output('plot_dist_mort','figure'), 
    Input('select_gr_dist_mort','value'),
    Input('df_reparto_mort','data'),
    prevent_initial_call=True
)
def actualizar_reparto_mort(granja,datos):
    escribir_log('info', dame_sesion()+": callback: actualizar_reparto_mort")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        entrada=callback_context.triggered_id
        if entrada=='df_reparto_mort':
            data=pd.DataFrame(datos,columns=datos[0].keys())
            
            #Para evitar introducir vacíos
            for i in range(1, data.shape[1]):
                data[data.columns[i]]=pd.to_numeric(data[data.columns[i]], errors='coerce')
            data= data.fillna(0)
            data_rest =pd.read_csv(p.get_attr('path_df_reparto_mort')) 
            data_rest=data_rest.loc[data_rest['Granja']!=granja]
            newDF=pd.concat([data if not data.empty else None, data_rest if not data_rest.empty else None], ignore_index=True)
            newDF.to_csv( p.get_attr('path_df_reparto_mort'), index = False)
            
            df_reparto_mort=newDF.loc[newDF['Granja']==granja].reset_index().drop(columns=['index'], axis=1).copy()
    
            #No hay totales
            
        if entrada=='select_gr_dist_mort':
            #Cambio en la granja
            newDF =pd.read_csv(p.get_attr('path_df_reparto_mort')) 
            df_reparto_mort=newDF.loc[newDF['Granja']==granja].reset_index().drop(columns=['index'], axis=1).copy()

        #df_reparto_mort Este valor no se puede copiar en el fichero porque está filtrado por Granja
        if df_reparto_mort.empty:
            df_reparto_mort=p.creador_generico_handson_6([granja])
        pesos=rnorm3(n=1000, mean_1=df_reparto_mort.loc[0,'PesoMedio_1'], cv_1=df_reparto_mort.loc[0,'CV_1']/100, mean_2=df_reparto_mort.loc[0,'PesoMedio_2'], cv_2=df_reparto_mort.loc[0,'CV_2']/100)
        #pesos=pd.DataFrame(Pesos=pesos)
        mean_pesos = int(round(np.mean(pesos),0))
        hist_data = [pesos]
        group_labels = ['']
        colors = ['#333F44']
        if (p.get_attr('especie'))=='TURBOT':
            rango=[0,4000]
        if (p.get_attr('especie'))=='SOLE':
            rango=[0,1500]
    # Create distplot with curve_type set to 'normal'
        figura = ff.create_distplot(hist_data, group_labels, colors=colors, show_hist=False, show_rug=False ).add_vline(x=mean_pesos,
                    line=dict(dash='dash')).update_layout(showlegend=False,title_text=f'Peso medio total: {mean_pesos}').update_xaxes(range = rango)

        return df_reparto_mort.to_dict('records'), figura
    except Exception as e:
        escribir_log('critical', dame_sesion()+': actualizar_reparto_mort ' +"Error {0}".format(str(e)))
        return no_update, no_update
    
    

################################################GROWTH################################################
def layout_growth():
    try:
        return [
            dbc.Card(html.H4("Growth", className='text-center'), color="info", inverse=True, style={"height": "6vh"}),
            html.Div([ 
                dcc.Tabs(id='growth_tab', children=[ 
                    dcc.Tab(label='Growth estimado', id='growth_estimado', value='growth_estimado'),
                    dcc.Tab(label='Ajustes', id='ajustes_growth', value='ajustes_growth'),
                ], value='growth_estimado'),
                html.Div(id="tab-content-growth")
                ],style={"padding": "20px 20px 20px 20px"}),
        ]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': layout_growth ' +"Error {0}".format(str(e)))

# Callback para actualizar el tab de
#perdidas. Esta puesto así apara que tarde menos en 
#cargar la página de inicio
@callback(
    Output("contenedor_growth", "children"),
    Input("tab-content-growth", "children"),
    Input('mem_fecha','data'),
    Input('d_growth_type','on'),
    State("growth_tab", "value")
    #prevent_initial_call=True
)
def layout_historico(niño,dato_fecha,tipo_dato,active_tab):

    try:
        if not niño is None and active_tab=='growth_estimado':
            df_mean_historic_growth=inicializar_actualizar_growth('growth_estimado','historico')[0]
            return [
                dash_table.DataTable(id="df_mean_historic_growth",
                    data=df_mean_historic_growth.to_dict('records'),
                    columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja'] else 'text')} for i in df_mean_historic_growth.columns],
                    style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                    style_cell_conditional=[{'if': {'column_id': 'Granja'},'textAlign': 'center'}],
                    fixed_columns={'headers':True, 'data':1}, style_table={'overflowX': 'auto','minWidth': '100%'})
                ]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': layout_historico ' +"Error {0}".format(str(e)))





# Callback para actualizar el tab de
#perdidas. Esta puesto así apara que tarde menos en 
#cargar la página de inicio
@callback(
    Output("tab-content-growth", "children"),
    Input("growth_tab", "value"),
    #prevent_initial_call=True
)
def render_tab_content_growth(active_tab):
    escribir_log('info', dame_sesion()+": callback: render_tab_content_growth")
    try:
        if active_tab == 'growth_estimado':
            resultado=inicializar_actualizar_growth(active_tab,'estimado')
            df_growth_type=resultado[0]
            df_desired_growth=resultado[1]  
            return[                 
                dbc.Row([ 
                    dbc.Col([html.Br(),
                    html.Br(),
                    dbc.Col([
                        daq.BooleanSwitch(
                            label={'label':'Crecimiento en %','style':{'font-family': 'Arial',
                                    'font-size':15}},
                            labelPosition='right',id='d_growth_type',
                            on=df_growth_type, color="#FF0000"
                    )], width=5),
                    html.Br()
                    ], width=6),
                    html.Br(),
                        html.Div([
                            dash_table.DataTable(id="df_desired_growth",
                                data=df_desired_growth.to_dict('records'),
                                columns=[{'name': i, 'id': i, 'type':('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja','Total'])} for i in df_desired_growth.columns],
                                style_cell={'textAlign': 'right'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                                style_cell_conditional=[{'if': {'column_id': 'Granja'},'textAlign': 'center'}],
                                fixed_columns={'headers':True, 'data':1}, style_table={'overflowX': 'auto','minWidth': '100%'}),
                            html.Br(),html.Br(),html.Hr(),
                            html.B("Growth Historico"),
                            dcc.Loading(html.Div(id="contenedor_growth"),
                    target_components={'contenedor_growth':'children'},delay_show=10),#,delay_hide=1),
                    ])
                ])
            ]
        
        if active_tab == 'ajustes_growth':
            resultado=inicializar_actualizar_growth(active_tab)
            df_ajustes_crecimiento=resultado[0]
            default_campos_granjas=resultado[1].sort_values()
            default_fecha=resultado[2]
            return [ 
                html.Br(), 
                dbc.Row([ 
                        dash_table.DataTable(id="df_ajustes_crecimiento",
                        data=df_ajustes_crecimiento.to_dict('records'),
                        columns=[{
                            'id': 'Activar','name': 'Activar','type': 'text','presentation':'dropdown','on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': "False"}},
                            {'id': 'Granja','name': 'Granja','type': 'text','presentation': 'dropdown','on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': default_campos_granjas.tolist()[0]}},
                            {'id': 'Ajuste_por','name': 'Ajuste_por','type': 'text','presentation': 'dropdown','on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': "Gen"}},
                            {'id': 'Talla_Gen_Edad','name': 'Talla_Gen_Edad', 'type': 'text', 'on_change': {'action': 'coerce','failure': 'default'}},
                            {'id': 'Mes_inicio','name': 'Mes_inicio','type': 'datetime','on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': default_fecha}},
                            {'id': 'Mes_fin','name': 'Mes_fin','type': 'datetime','on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': default_fecha}},
                            {'id': 'Ajuste','name': 'Ajuste','type': 'numeric','format': Format(precision=2, scheme=Scheme.decimal_integer),'on_change': {'action': 'coerce','failure': 'default'},'validation': {'default': "0"}} ],
                        dropdown={
                            'Activar': {'options': [{'label': i, 'value': i}for i in ['True','False']]},
                            'Granja': {'options': [{'label': i, 'value': i} for i in default_campos_granjas.tolist()]},
                            'Ajuste_por': {'options': [{'label': i, 'value': i} for i in ['Gen', 'Talla', 'Edad']]}
                        },
                        editable=True,style_cell={'textAlign': 'center'},style_header={'textAlign': 'center','fontWeight': 'bold'},
                        style_table={'overflowX': 'auto','minWidth': '100%'},
                        tooltip ={i: {'value': "Ej talla: 1000 - 1500/ Ej Gen: 21 3/ Ej Edad: 150 - 325. Dejar siempre espacios entre '-'",
                            'use_with': 'both' } for i in ["Talla_Gen_Edad"]},tooltip_delay=0, tooltip_duration=None, css=[{"selector": ".Select-menu-outer","rule": 'display : block !important'}]),
                ]),
            ]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': render_tab_content_growth ' +"Error {0}".format(str(e)))
        return no_update
            
def inicializar_actualizar_growth(tipo, tipo2='estimado'):
    escribir_log('info', dame_sesion()+": callback: inicializar_actualizar_growth")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        default_campos_granjas=pd.read_csv(p.get_attr('path_default_campos_granjas'))['Granja'].sort_values()
        meses_max_sim=18
        default_fecha=pd.read_csv(p.get_attr('path_default_fecha'))['date'].to_list()[0]
        #Growth estimado
        if tipo=='growth_estimado':
            df_growth_type=pd.read_csv(p.get_attr('path_d_growth_type'))
            df_growth_type=df_growth_type.loc[df_growth_type['Button'] == "d_growth_type",  "State"].to_list()[0]
            if tipo2=='estimado':
                #Actualizo las columnas de fecha
                if os.path.exists(p.get_attr("path_df_desired_growth")):
                    df_desired_growth=pd.read_csv(p.get_attr('path_df_desired_growth'))
                    month_names= date_col_names(pd.to_datetime(default_fecha).date(), df_desired_growth.shape[1] -2)
                    new_names=[df_desired_growth.columns[0]]+month_names+[df_desired_growth.columns[df_desired_growth.shape[1]-1]]
                    df_desired_growth.columns= new_names
                    df_desired_growth.to_csv(p.get_attr("path_df_desired_growth"),index=False)
            
                else:
                    lista_granjas=default_campos_granjas.to_list()
                    lista_granjas.sort()
                    df_desired_growth=p.creador_generico_handson_1(lista_granjas, meses_max_sim, default_fecha)
                    df_desired_growth.to_csv(p.get_attr("path_df_desired_growth"),index=False)
                columnas_meses=df_desired_growth.columns[1:]
                

                #if df_growth_type:  #Es True
                #    for i, j in zip(reversed(columnas_meses[1:]), reversed(columnas_meses[:len(columnas_meses)-1])):
                #        df_desired_growth[i]=round(df_desired_growth[i]/df_desired_growth[j]*100,1)

                #    #Esta línea no la puedo poner en común con el else pq sino me afecta a la división anterior
                #    df_desired_growth.loc[df_desired_growth['Granja'] == "Total", columnas_meses]=[0]*len(columnas_meses)
                #    #Pongo a 0 el primer mes
                #    df_desired_growth[columnas_meses[0]]= [0]*df_desired_growth.shape[0]

                #    df_desired_growth.loc[df_desired_growth['Granja'] == "Total", columnas_meses] = round(df_desired_growth.loc[0:df_desired_growth.shape[0]-1,columnas_meses].mean(axis=0)*df_desired_growth.shape[0]/(df_desired_growth.shape[0]-1),1).to_list()
                #    df_desired_growth['Total'] = round(df_desired_growth[columnas_meses[0:len(columnas_meses)-1]].mean(axis=1),1)
            
                #else:
                df_desired_growth.loc[df_desired_growth['Granja'] == "Total", columnas_meses]=[0]*len(columnas_meses)
                df_desired_growth.loc[df_desired_growth['Granja']  == "Total",columnas_meses]= df_desired_growth[columnas_meses].sum(axis=0).to_list()
                df_desired_growth['Total'] =0
                df_desired_growth['Total'] = df_desired_growth[columnas_meses].sum(axis=1) #no se puede sumar la primera columna que es granja
                df_desired_growth= df_desired_growth.fillna(0)
                return [df_growth_type, df_desired_growth]
            if tipo2=='historico':
                df_mean_historic_growth=p.mean_historic_growth_func(granjas =default_campos_granjas.to_list(), 
                    en_por = df_growth_type,
                    fecha_desde = "2017-12-01") #Esta fecha va a cañón

                if df_mean_historic_growth is None:
                    df_mean_historic_growth=p.creador_generico_handson_1(default_campos_granjas.to_list(), meses_max_sim, default_fecha)
                return [df_mean_historic_growth]
        
        #Ajustes growth
        if tipo=='ajustes_growth':
            if os.path.exists(p.get_attr("path_df_ajustes_crecimiento")):
                df_ajustes_crecimiento=pd.read_csv(p.get_attr("path_df_ajustes_crecimiento"))
            else:
                df_ajustes_crecimiento=p.creador_generico_handson_3(default_campos_granjas.to_list(), col_por_cul=False)
                df_ajustes_crecimiento.to_csv(p.get_attr("path_df_ajustes_crecimiento"),index=False)
            df_ajustes_crecimiento['Mes_inicio']=df_ajustes_crecimiento['Mes_inicio'].apply(lambda x: pd.to_datetime(x).date())
            df_ajustes_crecimiento['Mes_fin']=df_ajustes_crecimiento['Mes_fin'].apply(lambda x: pd.to_datetime(x).date())
            df_ajustes_crecimiento["Talla_Gen_Edad"]= df_ajustes_crecimiento["Talla_Gen_Edad"].map(str).replace(to_replace="nan", value="")
            df_ajustes_crecimiento["Activar"] = df_ajustes_crecimiento["Activar"].map(str)
            return [df_ajustes_crecimiento, default_campos_granjas, default_fecha]
    except Exception as e:
        escribir_log('critical', dame_sesion()+': inicializar_actualizar_growth ' +"Error {0}".format(str(e)))

    
     
#desired_growth se puede editar y va por fecha y por el botónc checkbox
# tiene totales en columna y fila que habrá que recalcular cuando se edite
#Esta callback puede dar problemas si se actualiza la fecha y el tab no está 
#seleccionada pq en ese caso el sistema dirá que no existe. ¡¡¡¡OJO!!!

@callback(
    Output('df_desired_growth','data'),
    Output('df_desired_growth','columns'),
    Output('df_mean_historic_growth','data'),
    Output('df_mean_historic_growth','columns'),
    Input('df_desired_growth','data'),
    Input('mem_fecha','data'),
    Input('d_growth_type','on'),
    prevent_initial_call=True,
    running=[
        (Output("d_growth_type", "disabled"), True, False)
    ]
)
def update_desired_growth_data(datos,dato_fecha,df_growth_type):
    escribir_log('info', dame_sesion()+": callback: update_desired_growth_data")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
        
        entrada=callback_context.triggered_id

        #Obtengo el growth_type
        df=pd.read_csv(p.get_attr('path_d_growth_type'))
        df.loc[df['Button'] == "d_growth_type",  "State"]=df_growth_type
        df.to_csv(p.get_attr('path_d_growth_type'), index=False)
        newDF =pd.DataFrame(datos,columns=datos[0].keys())
        #Tengo que comprobar que el fichero esté actualizado con el número de granjas

        df_desired_growth=pd.read_csv(p.get_attr('path_df_desired_growth'))
        #comparo newDF con df_desired_growth
        if len(newDF['Granja'])!=len(df_desired_growth['Granja']):
            for i in df_desired_growth['Granja'].to_list():
                if newDF.loc[newDF['Granja']==i].empty:
                    ceros=[0]*(len(newDF.columns)-1)
                    newDF.loc[len(newDF)]=[i]+ceros
        if len(newDF['Granja'])>len(df_desired_growth['Granja']):
            newDF=newDF.loc[newDF['Granja'].isin(df_desired_growth['Granja'].to_list())]


        #if entrada=='date':
        if entrada=='mem_fecha':
            fecha=pd.read_json(StringIO(dato_fecha), orient='split').loc[0,'date']
            month_names= date_col_names(pd.to_datetime(fecha).date(), newDF.shape[1] -2)
            new_names=[newDF.columns[0]]+month_names+[newDF.columns[newDF.shape[1]-1]]
            newDF.columns= new_names
            if df_growth_type:
                #Tengo que leer del fichero y guardar los nombres de las nuevas columnas
                df_desired_growth=pd.read_csv(p.get_attr('path_df_desired_growth'))
                df_desired_growth.columns= new_names
                df_desired_growth.to_csv(p.get_attr('path_df_desired_growth'), index = False)
            else:
                newDF.to_csv(p.get_attr('path_df_desired_growth'), index = False)
            columnas=[{'name': i, 'id': i, 'type':('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja','Total'])} for i in newDF.columns]
            return newDF.to_dict('records'),columnas, no_update, columnas
        
        if entrada=='d_growth_type':
            pass
            #No hago nada pq no tengo los datos de biomasa

            ##Guardo el estado de d-growth_type y leo el fichero
            #df.to_csv(p.get_attr('path_d_growth_type'), index = False)
            #Lo tengo que leer del fichero: si pasa de false a true hay que hacer los cálculos y si paso de true a false no me valen los valores
            #newDF =pd.read_csv(p.get_attr('path_df_desired_growth'))

        if entrada=='df_desired_growth': 
            #Para evitar introducir vacíos
            for i in range(1, newDF.shape[1]):
                newDF[newDF.columns[i]]=pd.to_numeric(newDF[newDF.columns[i]], errors='coerce')
            newDF= newDF.fillna(0)
        
        ##Tengo que volver a calcular los totales si pasa de false a true y si entrada es df_desired_growth. Lo hago para todos y no me complico
        columnas_meses=newDF.columns[1:] #Incluyo la columna Total

        ##Si es True, no puedo guardarlo 
        #if df_growth_type:
        #    for i, j in zip(reversed(columnas_meses[1:]), reversed(columnas_meses[:len(columnas_meses)-1])):
        #        newDF[i]=round(newDF[i]/newDF[j]*100,1)

        #    newDF.loc[newDF['Granja'] == "Total",columnas_meses]= [0]*len(columnas_meses)
        #    #Pongo a 0 el primer mes
        #    newDF[columnas_meses[0]]= [0]*newDF.shape[0]
        #    #Calculo los totales
        #    newDF.loc[newDF['Granja'] == "Total", columnas_meses] = round(newDF.loc[0:newDF.shape[0]-1,columnas_meses].mean(axis=0)*newDF.shape[0]/(newDF.shape[0]-1),1).to_list()
        #    newDF['Total'] = round(newDF[columnas_meses[0:len(columnas_meses)-1]].mean(axis=1),1)
        #    newDF=newDF.fillna(0)
        #else:
        #    #Si es false sí puedo guardarlo
        #    #Calculo los totales
        newDF.loc[newDF['Granja'] == "Total",columnas_meses]= [0]*len(columnas_meses)
        newDF.loc[newDF['Granja']  == "Total",columnas_meses]= newDF[columnas_meses].sum(axis=0).to_list()
        newDF['Total']= 0
        newDF['Total'] = newDF[columnas_meses].sum(axis=1) #no se puede sumar la primera columna que es granja
        newDF= newDF.fillna(0) 
        newDF.to_csv(p.get_attr('path_df_desired_growth'), index = False)
        
        historico=inicializar_actualizar_growth('growth_estimado','historico')[0]
        columnas=[{'name': i, 'id': i, 'type':('numeric' if i not in ['Granja'] else 'text'), 'editable': (i not in  ['Granja','Total'])} for i in newDF.columns]
        return newDF.to_dict('records'), columnas, historico.to_dict('records'), columnas
    except Exception as e:
        escribir_log('critical', dame_sesion()+': update_desired_growth_data ' +"Error {0}".format(str(e)))
        return no_update, no_update, no_update, no_update




#Callback para actualizar la tabla de ajustes crecimiento   

@callback(
    Output('df_ajustes_crecimiento','data'),
    Input('df_ajustes_crecimiento','data'),
    State('df_ajustes_crecimiento', 'data_previous'),
    State('date','date'),
    State('granjas_sim','value'),
    prevent_initial_call=True
)
def df_update_ajustes_crecimiento(datos,datos_previos,fecha,granjas):
    
    escribir_log('info', dame_sesion()+": callback: df_update_ajustes_crecimiento")
    try:
        user=current_user.name
        p=funcsif()
        p.inicializar(user)
    
        newDF = pd.DataFrame(datos,columns=datos[0].keys())
    
        antiguoDF = pd.DataFrame(datos_previos,columns=datos_previos[0].keys())
        antiguoDF["Activar"] = antiguoDF["Activar"].map(str)
        newDF["Activar"] = newDF["Activar"].map(str)
        
        df_ajustes_crecimiento=pd.read_csv(p.get_attr('path_df_ajustes_crecimiento'))
        ###Validacion
        error=False
        if antiguoDF.shape==newDF.shape:
            Posicion=obtener_celda_distinta(newDF,antiguoDF)
            if not Posicion is None:
                datonuevo=newDF.loc[Posicion[0],Posicion[1]] 
                if Posicion[1]=="Mes_inicio":
                    if datonuevo != datetime.datetime.strptime(datonuevo, "%Y-%m-%d").strftime('%Y-%m-%d'):
                        error=True
                    else:
                        #Hay que poner el día 1 del mes
                        datonuevo=pd.to_datetime(datonuevo).date().replace(day=1).strftime('%Y-%m-%d')
                        newDF.loc[Posicion[0],Posicion[1]]=datonuevo
                        if datonuevo>newDF.loc[Posicion[0],"Mes_fin"]:
                            error=True
                elif Posicion[1]=="Mes_fin":
                    if len(datonuevo)!=10:
                        error=True
                    if datonuevo != datetime.datetime.strptime(datonuevo, "%Y-%m-%d").strftime('%Y-%m-%d'):
                        error=True
                    else:
                        #Hay que poner el día 1 del mes
                        datonuevo=pd.to_datetime(datonuevo).date().replace(day=1).strftime('%Y-%m-%d')
                        newDF.loc[Posicion[0],Posicion[1]]=datonuevo
                        if datonuevo<newDF.loc[Posicion[0],"Mes_inicio"]:
                            error=True
                elif (Posicion[1]=="Talla_Gen_Edad" or Posicion[1]=="Ajuste_por"  or Posicion[1]=='Activar') and newDF.loc[Posicion[0],"Activar"]=="True":
                    if Posicion[1]=="Activar":
                        datonuevo=newDF.loc[Posicion[0],"Talla_Gen_Edad"] 
                    if newDF.loc[Posicion[0],"Ajuste_por"]=="Gen":
                        if p.get_attr('especie')=="TURBOT":
                            if len(re.findall(r"^[2][0-9]\s[1-4]$",datonuevo))==0 or len(datonuevo)!=4:
                                error=True
                        elif p.get_attr('especie')=="SOLE":
                            if len(re.findall(r"^[2][0-9]\s[1-6]$",datonuevo))==0 or len(datonuevo)!=4:
                                error=True
                    elif newDF.loc[Posicion[0],"Ajuste_por"]=="Edad":
                        if len(datonuevo.split("-"))!=2:
                            error=True
                        else:
                            start, end = datonuevo.replace(" ","").split("-")
                            if (start.isdigit() and end.isdigit()):
                                start=int(start)
                                end=int(end)
                                if (start>end or start<0 or end<0):
                                    error=True
                            else:
                                error=True
                    elif newDF.loc[Posicion[0],"Ajuste_por"]=="Talla":
                        if not datonuevo in dame_tallas(p.get_attr('especie')):
                            error=True
                if not error:
                    df_ajustes_crecimiento=newDF.copy()
        df_ajustes_crecimiento["Activar"] = df_ajustes_crecimiento["Activar"].map(str)
        if len(df_ajustes_crecimiento.loc[df_ajustes_crecimiento["Activar"]=='False'])==0:
            #Si un false se cambia a true => hay que añadir una linea de false
            df2=pd.DataFrame({'Activar':['False'], 'Granja':[granjas[0]], 'Ajuste_por':["Gen"],'Talla_Gen_Edad':["24 1"],
                            'Mes_inicio':[pd.to_datetime(fecha).date().replace(day=1)],'Mes_fin':[pd.to_datetime(fecha).date().replace(day=1)],'Ajuste':[0],})
            df_ajustes_crecimiento=pd.concat([df_ajustes_crecimiento if not df_ajustes_crecimiento.empty else None, df2 if not df2.empty else None], ignore_index=True)
            df_ajustes_crecimiento=df_ajustes_crecimiento.fillna(0)
        if len(df_ajustes_crecimiento.loc[df_ajustes_crecimiento["Activar"]=='False'])>1:
            indice=df_ajustes_crecimiento.loc[df_ajustes_crecimiento["Activar"]=='False'].index.min()
            df_ajustes_crecimiento=df_ajustes_crecimiento.drop(indice)
        df_ajustes_crecimiento["Activar"] = df_ajustes_crecimiento["Activar"].map(str)
        df_ajustes_crecimiento.to_csv(p.get_attr('path_df_ajustes_crecimiento'),index=False)
        return df_ajustes_crecimiento.to_dict('records')
    except Exception as e:
        escribir_log('critical',dame_sesion()+": df_update_ajustes_crecimiento Error {0}".format(str(e)))
        df_ajustes_crecimiento["Activar"] = df_ajustes_crecimiento["Activar"].map(str)
        return df_ajustes_crecimiento.to_dict('records')
   