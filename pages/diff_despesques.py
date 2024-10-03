
import dash_bootstrap_components as dbc
from dash import html, Input, Output, callback, dash_table, no_update, dcc
import pandas as pd
import numpy as np
import os
from datetime import datetime
from .funcionalidades.funcsifv2 import funcsif
from .funcionalidades.myfunc import mesChar_toNum, escribir_log
from .funcionalidades.User import dame_sesion
from flask_login import current_user
from .home import get_sidebar, banner

def layout():
    if current_user.is_authenticated:
        user=current_user.name
    else:
        return html.Div(["Haga ", dcc.Link("login", href="/"), " para operar"], className='text-center')
    p=funcsif()
    p.inicializar(user)
    default_campos_granjas = pd.read_csv(p.get_attr("path_default_campos_granjas"))['Granja'].to_list()+['All']
    Render_diff_despesques=calcular_diff_despesques(default_campos_granjas, user)
    if Render_diff_despesques is None:
        col_names=["Granja","Talla"]
        Render_diff_despesques = pd.DataFrame(columns=col_names)
        Render_diff_despesques[col_names]=Render_diff_despesques[col_names].to_string()
    layout= [
        get_sidebar(__name__),
        dbc.Container([banner()], fluid=True),
        html.Br(),
        html.Br(),
        dbc.Container([
            html.Div([
                dbc.Card([
                    dbc.Card(html.H4("Diferencial Despesques", className='text-center'), color="info", inverse=True, style={"height": "6vh"},),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.B("Seleccione las granjas para visualizar los datos", style={"margin-bottom":"2w"}), 
                                dbc.Checklist(
                                    id='granjas_despesques',
                                    options=[{'label': gr, 'value': gr} for gr in default_campos_granjas],
                                    value=['All'],
                                    inline=False,
                                    style={"column-count":"2","borderColor": "#808080"},
                                    input_checked_style={
                                                            "backgroundColor": "#808080",
                                                            "borderColor": "#808080",
                                                        },
                                )],width=6,),
                        ],),
                    ], style={"padding": "20px 20px 20px 20px","height": "100%"})
                ]),
                dash_table.DataTable(id='Render_diff_despesques',
                        data=Render_diff_despesques.to_dict('records'),
                        columns=[{'name': i, 'id': i, 'type':('numeric' if i not in ['Granja','Talla'] else 'text')} for i in Render_diff_despesques.columns],
                        filter_action='native',
                        style_cell={'textAlign': 'right'},fixed_columns={'headers':True, 'data':2},
                        style_header={'textAlign': 'center','fontWeight': 'bold'},
                        style_cell_conditional=[
                            {
                                'if': {'column_id': ('Granja', 'Talla')},
                                'textAlign': 'center'
                            }],
                        style_table={'overflowX': 'auto','minWidth': '100%'}),
            ])
        ], fluid='md')
    ]
    
    return layout


def calcular_diff_despesques(granjas, user):
    escribir_log('info', dame_sesion()+': funcion calcular_diff_despesques: diff_despesques')
    p=funcsif()
    p.inicializar(user)
    if os.path.exists(p.get_attr("path_pescas_tallas_detail")):
        despesques = pd.read_csv(p.get_attr("path_pescas_tallas_detail"))
    else:
        despesques = None
    if os.path.exists(p.get_attr("path_df_despesques")):
        despesques_inten = pd.read_csv(p.get_attr("path_df_despesques"))
        despesques_inten=pd.melt(despesques_inten, id_vars = ["Granja", "Talla"], var_name="MesAno", value_name="Biomasa_inten")
        despesques_inten["Mes"] = despesques_inten["MesAno"].str.split("-").str[0].apply(mesChar_toNum)
        despesques_inten["Ano"] = despesques_inten["MesAno"].str.split("-").str[1].astype(int)
        despesques_inten = despesques_inten.drop(columns="MesAno", axis=1)
    else:
        despesques_inten = None
    if not (despesques is None or despesques_inten is None):
        if "All" in granjas:
            #La primera se hace con All
            #Estas dos líneas siguientes están copiadas del Quillo
            #pero no son correctas porque al estar los despesques de 
            #SSF, SSF_iberia y las granjas, se resumarán los despesques
            despesques["Granja"] = "All"
            despesques_inten["Granja"] = "All"

        else:
            despesques=despesques.loc[despesques["Granja"].isin(granjas)].reset_index(drop=True).copy()
            despesques_inten=despesques_inten.loc[despesques_inten["Granja"].isin(granjas)].reset_index(drop=True).copy()
    

        if not (despesques.empty or despesques_inten.empty):
            despesques["Mes"] = despesques["FechaFin"].apply(lambda x: pd.to_datetime(x).date().month)
            despesques["Ano"] = despesques["FechaFin"].apply(lambda x: pd.to_datetime(x).date().year)
            despesques = despesques[["Granja", "Talla", "Biomasa", "Mes", "Ano"]]

            fechas_simuladas=despesques[["Ano", "Mes"]].copy()
            fechas_simuladas=fechas_simuladas.groupby(["Ano","Mes"]).size().reset_index()[["Ano","Mes"]]

            despesques_inten=pd.merge(despesques_inten, fechas_simuladas, on=["Ano","Mes"], how='inner')

            despesques = despesques.groupby(["Granja", "Talla", "Ano", "Mes"]).agg({'Biomasa': 'sum'}).reset_index()
            despesques_inten = despesques_inten.groupby(["Granja", "Talla", "Ano", "Mes"]).agg({'Biomasa_inten':'sum'}).reset_index()
            data = pd.merge(despesques_inten, despesques, on=['Granja', 'Talla', 'Mes', 'Ano'], how='left')

            data['Biomasa'] = data['Biomasa'].fillna(0)

            orden_df=data.groupby(["Ano","Mes"]).size().reset_index().copy()[["Ano","Mes"]]

            orden_df['Fecha'] = orden_df.apply(lambda fila: pd.to_datetime(datetime.strptime(str(fila.Ano)+"-"+str(fila.Mes)+"-01", "%Y-%m-%d")).date(), axis=1)
            
            orden_df = orden_df.sort_values(by='Fecha')
            
            orden_df['Mes_char'] = orden_df['Fecha'].apply(lambda x: pd.to_datetime(x).strftime('%b'))
            
            orden_df['letter'] = [chr(i+97) for i in range(len(orden_df))]
            orden_df['MesChar'] = orden_df['letter'] + "." + orden_df['Mes_char'] + "-" + orden_df['Ano'].astype(str)
            orden_df = orden_df[['Mes', 'Ano', 'MesChar']]

            data = pd.merge(data, orden_df, on=['Mes', 'Ano'])
            data['Diff'] = round(data['Biomasa_inten'] - data['Biomasa'],0)
            data = data.pivot_table(index=['Granja', 'Talla'], columns='MesChar', values='Diff', fill_value=0).reset_index()
            # Agregar totales (el equivalente al adorn_totals)
            lista_total=["Total","Total"]
            lista_total=lista_total+data.sum(numeric_only=True,axis=0).to_list()

           
            data.loc[len(data)]=lista_total
            data.index.name = None
            data.columns.name=None
            data = data.map(lambda x: f"{x:,}" if isinstance(x, (np.int32, np.int64, np.float64)) else x)
            return data
        else:
            return None
    else:
        return None


@callback(
    Output('Render_diff_despesques', 'data'),
    Output('Render_diff_despesques', 'columns'),
    Input('granjas_despesques', 'value'),
    prevent_initial_call=True
)
def update_diff_despesques(granjas):
    escribir_log('info', dame_sesion()+': callback update_diff_despesques: diff_despesques')
    user=current_user.name
    Render_diff_despesques=calcular_diff_despesques(granjas, user)
    if Render_diff_despesques is None:
        return [],no_update
    columnas=[{'name': i, 'id': i, 'type': ('numeric' if i not in ['Granja','Talla'] else 'text')} for i in Render_diff_despesques.columns]
    
    return Render_diff_despesques.to_dict('records'), columnas



