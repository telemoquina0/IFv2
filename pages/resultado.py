import dash_bootstrap_components as dbc
from dash import html, dash_table,dcc
import pandas as pd
import os
from .funcionalidades.funcsifv2 import funcsif
from .funcionalidades.myfunc import budget_dcast, escribir_log
from .funcionalidades.User import dame_sesion
from flask_login import current_user
from .home import get_sidebar,banner

    
def layout():
    
    if current_user.is_authenticated:
        user=current_user.name
    else:
        return html.Div(["Haga ", dcc.Link("login", href="/"), " para operar"], className='text-center')
    
    df_resultado=presentar_resultado(user)

    #columnas resultado "FARM","DATA","TYPE","YearClass","Gen","a_jun-2024","b_jul-2024","c_ago-2024","d_sep-2024","e_oct-2024","f_nov-2024","g_dic-2024","h_ene-2025","i_feb-2025","j_mar-2025","k_abr-2025"
    layout= [
        get_sidebar(__name__),
        dbc.Container([banner()], fluid=True),
        dbc.Container([
            html.Div([
                dbc.Card(html.H4("Resultado", className='text-center'), color="info", inverse=True, style={"height": "6vh"},),
                dash_table.DataTable(id='df_resultado',
                            data=df_resultado.to_dict('records'),
                            columns=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['FARM','DATA','TYPE','YearClass','Gen'] else 'text'),
                                      'format': {'specifier': '.2f'}} for i in df_resultado.columns],
                            filter_action='native', page_size=dame_longitud(df_resultado), 
                            style_header={'textAlign': 'center','fontWeight': 'bold'},style_cell_conditional=[
                                {'if': {'column_id': ('FARM','DATA','TYPE','YearClass','Gen')},'textAlign': 'center'}
                            ],
                            style_cell={'textAlign': 'right'},style_table={'overflowX': 'auto','minWidth': '100%'}),
                
            ]),
        ], fluid='md')
    ]
    
    return layout


def presentar_resultado(user):
    escribir_log('info', dame_sesion()+': función presentar_resultado: resultado')
    p=funcsif()
    p.inicializar(user)
    df_resultado=None
    if os.path.exists(p.get_attr('path_resultado_dcasted')):
        df_resultado=pd.read_csv(p.get_attr("path_resultado_dcasted"))
        #df_resultado['value']= round(df_resultado['value'],2)
        #df_resultado=budget_dcast(df_resultado)
        df_resultado.loc[:, df_resultado.columns.str.contains('_')]=round(df_resultado.loc[:, df_resultado.columns.str.contains('_')],2)
        columnas_a_sumar=df_resultado.columns[5:]
        df_resultado['Totals']=0
        df_resultado['Totals']= df_resultado[columnas_a_sumar].sum(axis=1) #Suma de filas
    else:
        default_fecha=pd.read_csv(p.get_attr('path_default_fecha')).loc[0,'date']
        df_resultado=p.creador_generico_handson_resultado(meses_max_sim=18, default_fecha=default_fecha)
    return df_resultado

#Miro la longitud para que si se filtra aparezca en una sola página
def dame_longitud(df):
    escribir_log('info', dame_sesion()+': función dame_longitud: resultado')
    if df.empty:
        return 0
    len_1=len(df.loc[(df['DATA']== "growth") & (df['TYPE']== "biomass"),'Gen'].unique())
    len_2=len(df.loc[(df['DATA']== "sales") & (df['TYPE']== "biomass"),'Gen'].unique())
    return len_1+len_2

      