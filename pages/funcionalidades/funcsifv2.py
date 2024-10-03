import os
import pandas as pd
import numpy as np
import datetime
from datetime import date
import calendar
import itertools
import numbers
import string
import math
from .myfunc import date_col_names, RangoPeso_directo_letra, rnorm2, GeneracionFunc, imatia_query, fechas_stolt_func_new, mesChar_toNum, seq_dates, seq_edades, rnorm3, \
    RangoPeso_directo_letra_para_df, add_months, dispersion_pesos_func, RangoPesoFunc_custom, RangoPesoFunc_plus_letter,budget_dcast, escribir_log
import plotly.express as px
from plotly.io import to_image, write_image
import plotly.graph_objects as go
from werkzeug.security import generate_password_hash

# Define las funciones adicionales que podrían estar en 'myFunc.R' y 'app_config.R'

class funcsif:
    
    def __init__(self):
        
        self.especie="TURBOT"
        self.user="Default"
        self.parent_dir=os.path.join(os.path.dirname( __file__ ), '..', '..')
        self.path_d_growth_type=os.path.join(self.parent_dir,self.especie, self.user,"Temp","inputs", "mod", "last_df_materialSwitch.csv")
        self.path_df_alevines=os.path.join(self.parent_dir,self.especie, self.user, "Temp","inputs","mod", "last_df_alevines.csv") 
        self.path_df_alevines_pm_cv=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "inputs", "mod", "last_df_alevines_pm_y_cv.csv") 
        self.path_df_despesques=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "inputs", "mod", "last_df_despesques.csv") 
        self.path_df_acabar_gen=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "inputs", "mod", "last_df_acabar_gen.csv") 
        self.path_df_dispersion=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "inputs", "mod", "last_df_dispersion.csv") 
        self.path_df_edad_pescas=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "inputs", "mod", "last_df_edad_pescas.csv") 
        self.path_df_losses =os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "last_df_losses.csv") 
        self.path_df_ajustes_mortalidad =os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "last_df_ajustes_mortalidad.csv") 
        self.path_default_culling_por =os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "last_culling_por.csv") 
        self.path_df_reparto_mort =os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "last_df_reparto_mort.csv") 
        self.path_df_desired_growth =os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "last_df_desired_growth.csv")
        self.path_df_ajustes_crecimiento =os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "last_df_ajustes_crecimiento.csv") 
        self.path_df_stock_opt =os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "last_df_stock_optimo.csv") 
        self.path_default_campos_granjas = os.path.join(self.parent_dir,self.especie, self.user,"Temp", "inputs", "mod", "default_campos_granjas_sim.csv") 
        self.path_default_fecha =os.path.join(self.parent_dir, self.especie, self.user,"Temp", "inputs", "mod","default_fecha.csv") 
        self.path_masterDF=os.path.join(self.parent_dir, self.especie, self.user,"Temp", "outputs", "csv", "masterDF.csv") 
        self.path_pescas_tallas_detail=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "outputs", "csv", "pescas_tallas_detail.csv") 
        #################################################################
        self.path_programa_python= os.path.join(os.path.dirname( __file__ ), '..', '..')  
        ######################################################################
        self.path_resultado=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "outputs", "csv", "resultado.csv")
        self.path_resultado_dcasted=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "outputs", "csv", "resultado_dcasted.csv")
        self.path_resultado_dcasted_xls=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "outputs", "csv", "resultado_dcasted.xlsx")
        self.solo_path_plots= os.path.join (self.parent_dir,self.especie, self.user, "Temp", "outpus", "plots" )
        self.solo_path_csv=os.path.join(self.parent_dir,self.especie, self.user,"Temp", "outputs", "csv")
        
        self.path_curvas=os.path.join(self.path_programa_python, self.especie,r"curvas.csv")
        self.path_historical_data= os.path.join(self.path_programa_python,self.especie, r"historical_data_2017_2019.csv")
        self.path_distribucion_optima= os.path.join(self.path_programa_python,self.especie,r"distribucion_optima.csv")
        self.path_fixed_temp_data=os.path.join(self.path_programa_python,self.especie)
        self.port=8050

    
    def __reassign__(self):
        self.path_d_growth_type=os.path.join(self.parent_dir,self.especie, self.user, "Temp","inputs", "mod", "last_df_materialSwitch.csv") 
        self.path_df_alevines=os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "last_df_alevines.csv") 
        self.path_df_alevines_pm_cv=os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "last_df_alevines_pm_y_cv.csv") 
        self.path_df_despesques=os.path.join(self.parent_dir,self.especie, self.user,  "Temp", "inputs", "mod", "last_df_despesques.csv") 
        self.path_df_acabar_gen=os.path.join(self.parent_dir,self.especie, self.user,  "Temp", "inputs", "mod", "last_df_acabar_gen.csv") 
        self.path_df_dispersion=os.path.join(self.parent_dir,self.especie, self.user,  "Temp", "inputs", "mod", "last_df_dispersion.csv") 
        self.path_df_edad_pescas=os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "last_df_edad_pescas.csv") 
        self.path_df_losses =os.path.join(self.parent_dir,self.especie, self.user,   "Temp", "inputs", "mod", "last_df_losses.csv") 
        self.path_df_ajustes_mortalidad =os.path.join(self.parent_dir, self.especie, self.user,  "Temp", "inputs", "mod", "last_df_ajustes_mortalidad.csv") 
        self.path_default_culling_por =os.path.join(self.parent_dir, self.especie, self.user,  "Temp", "inputs", "mod", "last_culling_por.csv") 
        self.path_df_reparto_mort =os.path.join(self.parent_dir, self.especie, self.user,  "Temp", "inputs", "mod", "last_df_reparto_mort.csv") 
        self.path_df_desired_growth =os.path.join(self.parent_dir,self.especie, self.user,   "Temp", "inputs", "mod", "last_df_desired_growth.csv")
        self.path_df_ajustes_crecimiento =os.path.join(self.parent_dir, self.especie, self.user,  "Temp", "inputs", "mod", "last_df_ajustes_crecimiento.csv") 
        self.path_df_stock_opt =os.path.join(self.parent_dir, self.especie, self.user,  "Temp", "inputs", "mod", "last_df_stock_optimo.csv") 
        self.path_default_campos_granjas = os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "default_campos_granjas_sim.csv") 
        self.path_default_fecha =os.path.join(self.parent_dir, self.especie, self.user, "Temp", "inputs", "mod", "default_fecha.csv") 
        self.path_masterDF=os.path.join(self.parent_dir,self.especie, self.user,  "Temp", "outputs", "csv", "masterDF.csv") 
        self.path_pescas_tallas_detail=os.path.join(self.parent_dir, self.especie, self.user,  "Temp", "outputs", "csv", "pescas_tallas_detail.csv") 
        self.path_resultado=os.path.join(self.parent_dir,self.especie, self.user,  "Temp", "outputs", "csv", "resultado.csv")
        self.path_resultado_dcasted=os.path.join(self.parent_dir, self.especie, self.user, "Temp", "outputs", "csv", "resultado_dcasted.csv")
        self.path_resultado_dcasted_xls=os.path.join(self.parent_dir,self.especie, self.user,  "Temp", "outputs", "csv", "resultado_dcasted.xlsx")
        self.solo_path_plots=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "outputs", "plots")
        self.solo_path_csv=os.path.join(self.parent_dir,self.especie, self.user, "Temp", "outputs", "csv")
        self.path_curvas=os.path.join(self.path_programa_python, self.especie,r"curvas.csv")
        self.path_historical_data= os.path.join(self.path_programa_python,self.especie, r"historical_data_2017_2019.csv")
        self.path_distribucion_optima= os.path.join(self.path_programa_python,self.especie,r"distribucion_optima.csv")
    
    def get_attr(self,variable):
        nueva_variable="self."+variable
        valor_interno=eval(nueva_variable)
        return valor_interno
    
    def dame_usuarios(self,bool_especie=False):
        configuracion=pd.read_csv(os.path.join(self.parent_dir, 'static','config.csv'))
        if bool_especie:
            return configuracion[['User','Especie']]
        else:
            return configuracion['User']

    
    def crear_carpetas(self):
        lista_usuarios=self.dame_usuarios(True)
        #recorro el arbol de directorios
        #Tengo que agrupar los usuarios por especie
        Especies=lista_usuarios['Especie'].unique()
        for especie in Especies:
            lista_usuarios_especie=lista_usuarios.loc[lista_usuarios['Especie']==especie,'User'].to_list()
            for usuario in lista_usuarios_especie:
                if not os.path.isdir(os.path.join(self.parent_dir, especie, usuario)):
                    os.mkdir(os.path.join(self.parent_dir, especie, usuario))
        self.generacion()

    def generacion(self):
        configuracion=pd.read_csv(os.path.join(self.parent_dir, 'static','config.csv'))
        for usuario in configuracion['User']:
            configuracion.loc[configuracion['User']==usuario,'Pw']=generate_password_hash("P"+usuario)
        configuracion.to_csv(os.path.join(self.parent_dir, 'static','config.csv'),index=False)
        
    
    def get_pw(self,usuario):
        fichero=os.path.join(self.parent_dir, 'static', 'config.csv' )
        if os.path.exists(fichero):
            configuracion=pd.read_csv(fichero)
        if configuracion['User'].isin([usuario]).sum()==0:
            return None
        else:
            return configuracion.loc[configuracion['User']==usuario]['Pw'].values.item(0)

        
    
    def inicializar(self,usuario):
        fichero=os.path.join(self.parent_dir, 'static', 'config.csv' )
        if os.path.exists(fichero):
            configuracion=pd.read_csv(fichero)
            if configuracion['User'].isin([usuario]).sum()!=0:
                self.especie=configuracion.loc[configuracion['User']==usuario,'Especie'].values.item(0)
                self.user=usuario
                self.__reassign__()
        



    # Creador de tablas estilo para la tabla resultados
    #Devuelve el dataframe creado pero vacío
    
    def creador_generico_handson_resultado(self, meses_max_sim, default_fecha):
        col_meses= date_col_names(fecha_start=default_fecha, numero_meses=meses_max_sim)
        col_meses=[f"{a}_{b}" for b, a in zip (col_meses, string.ascii_lowercase)]
        col_strings=["FARM","DATA","TYPE","YearClass","Gen"]
        col_names= col_strings + col_meses
        df = pd.DataFrame(columns=col_names)
        df[col_meses] = df[col_meses].apply(pd.to_numeric)
        df[col_strings]=df[col_strings].to_string()
        return df

    #Crea una tabla con las filas los nombres de las granjas presentes en campos granjas
    #y como nombre de columnas las fechas de los meses posteriores a default_fecha
    #con tantos meses-año columnas como meses maximo de simulación.
    # Los valores de la tabla están rellenados a cero
    
    def creador_generico_handson_1(self,campos_granjas, meses_max_sim, default_fecha):
        df = pd.DataFrame({'Granja': campos_granjas})
        meses_df = pd.DataFrame(np.zeros((len(df), meses_max_sim)), columns=date_col_names(fecha_start=default_fecha, numero_meses=meses_max_sim))

        df = pd.concat([df if not df.empty else None, meses_df if not meses_df.empty else None], axis=1)
        columnas_meses=df.columns[1:]
        df['Total'] = df[columnas_meses].sum(axis=1)
        total_row = pd.DataFrame(df.sum(axis=0)).transpose()
        total_row['Granja'] = 'Total'
        total_row = total_row[df.columns]
        df = pd.concat([df if not df.empty else None, total_row if not total_row.empty else None], ignore_index=True)
        df[columnas_meses] = df[columnas_meses].apply(pd.to_numeric)
        return df

    # Creador de tabla estilo ventas
    #Crea una tabla con las filas los nombres de las granjas presentes en campos granjas
    #además de las tallas según la especia y como nombre de columnas las fechas de los meses posteriores a default_fecha
    #con tantos meses-año columnas como meses maximo de simulación.
    # Los valores de la tabla están rellenados a cero
    # ¡¡¡OJO!!! especie puede tomar los valores TURBOT o SOLE .Si tiene valor SOLE la talla comienza en b.100 - 200
    # pero en el rodaballo (TURBOT) comienza en a.0 - 300. Este es el mismo comportamiento que la función en R 
    
    def creador_generico_handson_2(self,campos_granjas, meses_max_sim, default_fecha):
        Talla = sorted(set([RangoPeso_directo_letra(x, self.especie) for x in range(101, 20001, 100)]))
        Granja = campos_granjas
        df = pd.DataFrame([(g, t) for g in Granja for t in Talla], columns=['Granja', 'Talla'])
        meses_df = pd.DataFrame(np.zeros((len(df), meses_max_sim)), columns=date_col_names(default_fecha, meses_max_sim))
        df = pd.concat([df if not df.empty else None, meses_df if not meses_df.empty else None], axis=1)
        df = df.sort_values(by=['Granja', 'Talla']).reset_index(drop=True) 
        return df

    # Creador de tabla estilo ajustes
    #Crea una tabla con solo una fila (la primera granja de campos_granjas) y
    # con las columnas:
    # Activar (que se pone a False)
    # Ajuste_por que se pone a Gen
    # Talla_Gen_Edad que se deja vacío
    # Mes_inicio que coje el día actual
    # Mes_fin que coje el día actual
    # Ajuste lo pone a entero
    # Por_Cull solo aparece si col_por_cul es True y su valor es False 
    
    def creador_generico_handson_3(self,campos_granjas, col_por_cul=False):
        dd=date.today().strftime("%y")
        df = pd.DataFrame({
            'Activar': [False],
            'Granja': [campos_granjas[0]],
            'Ajuste_por': ['Gen'],
            'Talla_Gen_Edad': [f'{dd} 1'],
            'Mes_inicio': [datetime.datetime.now().date().replace(day=1)],
            'Mes_fin': [datetime.datetime.now().date().replace(day=1)],
            'Ajuste': [0]
        })
        if col_por_cul:
            df['Por_Cull'] = [False]
        return df

    # Creador de tabla con peso medio
    #Crea un data frame con una fila por granja en campos_granjas
    #y con las columnas PesoMedio, CV y Edad con valores fijados
    #y los mismos para todas
    
    def creador_generico_handson_4(self,campos_granjas):
        if self.especie=="TURBOT":
            edad=100
        elif self.especie=="SOLE":
            edad=133
        df = pd.DataFrame({
            'Granja': campos_granjas,
            'PesoMedio': [14]*len(campos_granjas),
            'CV': [15]*len(campos_granjas),
            'Edad': [edad]*len(campos_granjas)
        })
        return df

    # Creador de tabla de gen y mes
    #Genera un dataframe de solo una fila con los campos
    # Activar puesto a False
    # Granja con el primer valor del array campos_granjas
    # Gen puesto a vacío
    # Mes puesto a la fecha del día que se ejecuta el programa
    
    def creador_generico_handson_5(self, campos_granjas):
        dd=date.today().strftime("%y")
        df = pd.DataFrame({
            'Activar': [False],
            'Granja': [campos_granjas[0]],
            'Gen': [f'{dd} 1'],
            'Mes': [datetime.datetime.now().date().replace(day=1)]
        })
        return df

    # Creador de tabla con peso medio y CV
    #Devuelve un data frame con tantas filas como granjas hay en campos_granjas
    # Cada fila consta de las siguientes columnas:
    # Granja es el nombre de la granja
    # PesoMedio_1 inicializado a 1000
    # CV_1 inicializado a 12
    # PesoMedio_2 inicializado a 1000
    # CV_2 inicializado a 12
    
    def creador_generico_handson_6(self, campos_granjas):
        if self.especie=="TURBOT":
            pesomedio_1=1000
            pesomedio_2=1000
            cv_1=12
            cv_2=12
        elif self.especie=="SOLE":
            pesomedio_1=1000
            pesomedio_2=1000
            cv_1=12
            cv_2=12
        df = pd.DataFrame({
            'Granja': campos_granjas,
            'PesoMedio_1': [pesomedio_1]*len(campos_granjas),
            'CV_1': [cv_1]*len(campos_granjas),
            'PesoMedio_2': [pesomedio_2]*len(campos_granjas),
            'CV_2': [cv_2]*len(campos_granjas)
        })
        return df

    # Creador de tabla con peso medio y CV
    def creador_generico_handson_7(self, campos_granjas):
        df = pd.DataFrame({
            'Granja': campos_granjas,
            'Tones': [100]*len(campos_granjas)
        })
        return df

    #Función que crea la estructura de directorios para el programa
    #En el mismo directorio desde donde se ejecuta crea dos carpetas
    #La carpeta Temp tiene la siguiente estructura
    # Temp
    # -inputs 
    #       .fixed donde copia 3 ficheros ubicados en un directorio fijo (¡¡¡ojo!!! con esto) que está puesto a machete en el programa. ESTO YA NO ES ASI
    #       .mod donde estan distintos csv que genera esta función y después el programa con las simulaciones
    #-outputs
    #       .csv donde el programa escribirá los resultados de las simulaciones en formato csv
    #       .plots donde el programa guardará las gráficas de los resultados de las simulaciones
    #Si la estructura de directorios está creada no hace nada
    #Los parámetros que se le pasan son el array con las granjas, el número de meses que se quiere hacer la simulación
    # y la especie ("TURBOT" para rodaballo y "SOLE" para lenguado)
    
    def crear_estructura_if(self,campos_granjas, meses_max_sim):
        try:
            # Parent Directories
            if os.path.exists(os.path.join(self.parent_dir,self.especie, self.user,"Temp", "inputs")):
                escribir_log('info',"El directorio Temp ya existe, no se creará de nuevo.")
            else:
                # Primero creo las carpetas
                # Parent Directories
                os.makedirs(os.path.join(self.parent_dir,self.especie, self.user,'Temp', 'inputs', 'mod'), exist_ok=True)
                os.makedirs(os.path.join(self.parent_dir,self.especie, self.user, 'Temp', 'outputs', 'csv'), exist_ok=True)
                os.makedirs(os.path.join(self.parent_dir,self.especie, self.user, 'Temp','outputs', 'plots'), exist_ok=True)

                # Creación de archivos temporales en el directorio 'mod'
                default_campos_granjas= pd.DataFrame({"Granja": campos_granjas})
                default_campos_granjas.to_csv(self.path_default_campos_granjas, index=False)
                # default_fecha.csv
                default_fecha = pd.DataFrame({"date": [datetime.datetime.today().replace(day=1).date()]})
                default_fecha.to_csv(self.path_default_fecha, index=False)
                
                # last_df_alevines.csv
                last_df_alevines = self.creador_generico_handson_1(campos_granjas, meses_max_sim, default_fecha.loc[0,"date"])
                last_df_alevines.to_csv(self.path_df_alevines, index=False)
                
                # last_df_losses.csv
                last_df_losses  = self.creador_generico_handson_1(campos_granjas, meses_max_sim, default_fecha.loc[0,"date"])
                last_df_losses.to_csv(self.path_df_losses, index=False)

                # last_df_desired_growth.csv
                last_df_desired_growth = self.creador_generico_handson_1(campos_granjas, meses_max_sim, default_fecha.loc[0,"date"])
                last_df_desired_growth.to_csv(self.path_df_desired_growth, index=False)
            
                # last_df_despesques.csv
                last_df_ventas = self.creador_generico_handson_2(campos_granjas, meses_max_sim, default_fecha.loc[0,"date"])
                last_df_ventas.to_csv(self.path_df_despesques, index=False)
            
                # last_df_ajustes_crecimiento.csv
                last_df_ajustes_crecimiento = self.creador_generico_handson_3(campos_granjas, col_por_cul = False)
                last_df_ajustes_crecimiento.to_csv(self.path_df_ajustes_crecimiento, index=False)
            
                # last_df_ajustes_mortalidad.csv
                last_df_ajustes_mortalidad = self.creador_generico_handson_3(campos_granjas, col_por_cul = True)
                last_df_ajustes_mortalidad.to_csv( self.path_df_ajustes_mortalidad, index=False)
            
                # last_df_inputs_pm_y_cv.csv
                last_df_alevines_pm_y_cv = self.creador_generico_handson_4(campos_granjas)
                last_df_alevines_pm_y_cv.to_csv( self.path_df_alevines_pm_cv, index=False)
            
                # last_df_acabar_gen.csv
                last_df_acabar_gen = self.creador_generico_handson_5(campos_granjas)
                last_df_acabar_gen.to_csv( self.path_df_acabar_gen, index=False)
            
                # last_culling_por.csv
                last_culling_por = pd.DataFrame({'Por': [1],'Edad': [166]}) 
                last_culling_por.to_csv( self.path_default_culling_por, index=False)
            
                # last_df_reparto_mort.csv
                last_df_reparto_mort =self.creador_generico_handson_6(campos_granjas)
                last_df_reparto_mort.to_csv( self.path_df_reparto_mort, index=False)
            
                # last_df_dispersion.csv. Se le quitan los totales
                last_df_dispersion = self.creador_generico_handson_1(campos_granjas, meses_max_sim, default_fecha.loc[0,"date"])
                last_df_dispersion=last_df_dispersion.drop(columns=['Total'], axis=1)
                last_df_dispersion= last_df_dispersion.loc [last_df_dispersion.Granja != "Total"].copy()
                last_df_dispersion.to_csv(self.path_df_dispersion, index=False)
            
                # last_df_edad_pescas.csv. Se le quitan los totales
                last_df_edad_pescas = self.creador_generico_handson_1(campos_granjas, meses_max_sim, default_fecha.loc[0,"date"])
                last_df_edad_pescas=last_df_edad_pescas.drop(columns=['Total'], axis=1)
                last_df_edad_pescas = last_df_edad_pescas.loc [last_df_edad_pescas.Granja != "Total"] 
                last_df_edad_pescas.to_csv(self.path_df_edad_pescas, index=False)
            
                # last_df_materialSwitch.csv
                last_df_materialSwitch=pd.DataFrame({
                    'Button': ["continue", "d_growth_type"],
                    'State': [False, False]
                    }) 
                last_df_materialSwitch.to_csv( self.path_d_growth_type, index=False)
            
                # last_df_stock_optimo.csv
                last_df_stock_optimo =self.creador_generico_handson_7(campos_granjas)
                last_df_stock_optimo.to_csv( self.path_df_stock_opt, index=False)

                escribir_log('info',"Directorio Temp creado y archivos temporales inicializados. Éxito.")

            if os.path.exists(os.path.join(self.parent_dir,self.especie, self.user,"settings_history")):
                escribir_log('info', "El directorio settings_history ya existe, no se creará de nuevo.")
            else:
                os.makedirs(os.path.join(self.parent_dir,self.especie, self.user,"settings_history"), exist_ok=True)
                escribir_log('info', "Directorio settings_history creado. Éxito.")
        except Exception as e:
             escribir_log('critical', 'crear_estructura_if ' +"Error {0}".format(str(e)))



    #Función que devuelve un dataframe de los alevines con las siguientes columnas
    # Granja, Edad, PesoMedio, Num, Tanque, Gen
    #Num es el número de peces
    
    def Budg_Expand_alevines_all(self,data, peces_x_tanque=2500, inputs_sett=None):
        try:
            result = pd.DataFrame(columns=['Granja', 'Edad', 'PesoMedio', 'Num', 'Tanque', 'Gen'])
            result['Granja'] = result['Granja'].astype(str)
            result['Edad'] = result['Edad'].astype(int)
            result['Num'] = result['Num'].astype(int)
            result['Tanque'] = result['Tanque'].astype(str)
            result['Gen'] = result['Gen'].astype(str)


            data['Num']=data['Num'].astype(np.int64)
            data=data.assign(NumTanquesIniciales=round(data['Num'] / peces_x_tanque, 0))
            data['NumTanquesIniciales'] =data['NumTanquesIniciales'].astype(np.int32)
            data['pecesPorTanque'] = np.where(data['NumTanquesIniciales']==0, 0, round(data['Num']/data['NumTanquesIniciales'], 0))
            data['pecesPorTanque'] = data['pecesPorTanque'].astype(np.int32)
            data.loc[data['Num']<=peces_x_tanque,'NumTanquesIniciales']=1
            
            if not data.loc[data['Num']<=peces_x_tanque].empty:
                data.loc[data['Num']<=peces_x_tanque,'pecesPorTanque']=data.loc[data.loc[data['Num']<=peces_x_tanque,'pecesPorTanque'].index,'Num'].to_list()
            data['numrecalc'] = (data['NumTanquesIniciales'] * data['pecesPorTanque']).astype(np.int64)
            for i, row in data.iterrows():
                iter_pecesPorTanque = row['pecesPorTanque']
                iter_num = row['numrecalc'] #Tiene que ser entero
                iter_granja = row['Granja']
                iter_NumTanquesIniciales = row['NumTanquesIniciales']  #Tiene que ser int
                iter_Mes = int(row['Mes'])
                iter_Ano = int(row['Ano'])
                ## Aqui se pone el peso medio y CV adecuado para cada granja
                pesomedio = inputs_sett.loc[inputs_sett['Granja'] == iter_granja, 'PesoMedio'].values.item(0)
                CV = inputs_sett.loc[inputs_sett['Granja'] == iter_granja, 'CV'].values.item(0)
                edad_entrada = inputs_sett.loc[inputs_sett['Granja'] == iter_granja, 'Edad'].values.item(0)
                desvest = pesomedio * CV
                pesos = np.sort(rnorm2( pesomedio, desvest, iter_num))
                #pesos_split=np.array_split(pesos,iter_NumTanquesIniciales)
                #tanques= list(map(lambda x: np.mean(x), pesos_split))
                #pesos = np.random.normal(pesomedio, desvest, iter_num)
                #pesos.sort()
                # Dividir los pesos en tanques y calcular la media de cada tanque
                tanques = [np.mean(tanque) for tanque in np.array_split(pesos, np.ceil(len(pesos) / iter_pecesPorTanque).astype(int))]
                id_tanque = [f"{j}_Indef_{iter_granja}_{iter_Mes}_{iter_Ano}" for j in range(1, iter_NumTanquesIniciales + 1)]
                
                fecha = datetime.datetime(iter_Ano, iter_Mes, 1)
                gen = GeneracionFunc(fecha, self.especie)
                iter_df = pd.DataFrame({
                    'Granja': np.repeat(iter_granja, iter_NumTanquesIniciales),
                    'Edad': np.repeat(edad_entrada, iter_NumTanquesIniciales),
                    'PesoMedio': tanques,
                    'Num': np.repeat(iter_pecesPorTanque, iter_NumTanquesIniciales),
                    'Tanque': id_tanque,
                    'Gen': np.repeat(gen, iter_NumTanquesIniciales)
                })
                result = pd.concat([result if not result.empty else None, iter_df if not iter_df.empty else None], ignore_index=True)
                #result=result.drop_duplicates(ignore_index=True)

            

            return result
        except Exception as e:
             escribir_log('critical', 'Budg_Expand_alevines_all ' +"Error {0}".format(str(e)))

    #Función que devuelve una serie con las etiquetas correspondientes a las
    # fechas en el formato letra_abreviaturames_año
    #la letra corresponde al orden (de menor a mayor) de la fecha en ese conjunto
    #Las etiquetas salen en el mismo orden en el que entraron las fechas.
    
    def fecha_table_format_func(self, fechas):
        fechas = pd.to_datetime(fechas)
        fechas_unicas_df = pd.DataFrame({'Fecha': fechas.unique()}).sort_values(by='Fecha').reset_index(drop=True)
        fechas_unicas_df['letter'] = [chr(i+97) for i in range(len(fechas_unicas_df))]

        df = pd.DataFrame({'Fecha': fechas, 'Order': range(1, len(fechas)+1)})
        df['Mes_char'] = df['Fecha'].dt.month.map(lambda x: calendar.month_abbr[x])
        df['Ano'] = df['Fecha'].dt.year
        df = df.merge(fechas_unicas_df, on='Fecha', how='left')
        df['MesChar'] = df['letter'] + '_' + df['Mes_char'] + '_' + df['Ano'].astype(str)
        df = df.sort_values(by='Order').reset_index(drop=True)

        return df['MesChar']

    #Función que calcula la media de crecimiento histórico según la especie. En funcion de los datos de entrada saca una tabla con los crecimientos medios por Granja y por Mes-Año 
    #incluyendo los totales. Lanza las consultas a la base de datos
    #especie puede ser "TURBOT" o "SOLE"
    #granjas son las granjas de interés
    #path_df_desired_growth el archivo con la ruta completa donde se encuentra el fichero last_df_desired_growth.csv
    #en_por si es True los totales son valores medios
    #Fecha_desde la fecha desde que se lanzan las consultas a la base de datos
    
    def mean_historic_growth_func(self, granjas, en_por=False, fecha_desde="2017-12-01"):
        try:
            granjas = [granja.replace("Vilan_P", "Vilán_P") for granja in granjas] #Creo que es porque en Elastic Aqua está guardado con acento
            granjas_solas = [granja for granja in granjas if granja not in ["SSF", "SSF_Iberia"]]
            ssf = [granja for granja in granjas if granja == "SSF"]
            ssf_iberia = [granja for granja in granjas if granja == "SSF_Iberia"]

            data_frames = pd.DataFrame()
            
            # Se define la consulta SQL
            sql = f"""
                SELECT codigoplanta as Granja,
                        fechafin as FechaFin,
                        yield_kgm, 
                        interfarm_bin,
                        mes_pasadoB
                FROM VistaPSConsolidadoDatos
                WHERE fechafin > '{fecha_desde}'
                AND codigoplanta IN yyyyy
                AND (mes_actualB + mes_pasadoB)  > 0
            """
            
            if self.especie == "TURBOT":
                
                # Ejecutar la consulta SQL y almacenar los resultados en granjas_data
                
                if len(granjas_solas)>0 :
                    sql_granjas=sql
                    sql_granjas=sql_granjas.replace("yyyyy", "(\'"+"\', \'".join([str(elem) for elem in granjas_solas])+"\')")
                    granjas_data=imatia_query(sql_granjas)
                    granjas_data["Granja"].replace("Vilán_P", "Vilan_P")
                    data_frames=pd.concat([data_frames if not data_frames.empty else None, granjas_data], ignore_index=True)
                    data_frames=data_frames.drop_duplicates(ignore_index=True)

                if len(ssf) == 1:
                    # Hacer lo mismo para SSF
                    sql_ssf=sql
                    granjas_ssf=['Cervo_P', 'Lira_P', 'Merexo_P', 'Couso_P', 'Oye_P',  'Palmeira_P', 'Quilmas_P', 'Vilán_P', 'Tocha_P']
                    sql_ssf=sql_ssf.replace("yyyyy", "( \'"+"\', \'".join([str(elem) for elem in granjas_ssf])+"\')")
                    ssf_data=imatia_query(sql_ssf)
                    ssf_data['Granja']='SSF'
                    data_frames=pd.concat([data_frames if not data_frames.empty else None, ssf_data], ignore_index=True)
                    data_frames=data_frames.drop_duplicates(ignore_index=True)

                if len(ssf_iberia) == 1:
                    # Hacer lo mismo para SSF Iberia
                    sql_ssf_ib=sql
                    granjas_ssf_ib=['Cervo_P', 'Lira_P', 'Merexo_P', 'Couso_P',  'Palmeira_P', 'Quilmas_P', 'Vilán_P', 'Tocha_P']
                    sql_ssf_ib=sql_ssf_ib.replace("yyyyy", "( \'"+"\', \'".join([str(elem) for elem in granjas_ssf_ib])+"\')")
                    ssf_iberia_data=imatia_query(sql_ssf_ib)
                    ssf_iberia_data['Granja']='SSF_Iberia'
                    data_frames=pd.concat([data_frames if not data_frames.empty else None, ssf_iberia_data], ignore_index=True)
                    data_frames=data_frames.drop_duplicates(ignore_index=True)
                    

            elif self.especie == "SOLE":
            
                # Ejecutar la consulta SQL y almacenar los resultados en granjas_data
                
                if len(granjas_solas)>0 :
                    sql_granjas=sql
                    sql_granjas=sql_granjas.replace("yyyyy", "( \'"+"\', \'".join([str(elem) for elem in granjas_solas])+"\')")
                    granjas_data=imatia_query(sql_granjas)
                    data_frames=pd.concat([data_frames if not data_frames.empty else None, granjas_data], ignore_index=True)
                    data_frames=data_frames.drop_duplicates(ignore_index=True)
                
                #if len(ssf) == 1:
                #    # Hacer lo mismo para SSF
                #    sql_ssf=sql
                #    granjas_ssf=['Cervo Sole', 'Tocha Sole', 'Hafnir_P', 'Couso i+d', 'Anglet_P']
                #    granjas_ssf=sql_ssf.replace("yyyyy", "( \'"+"\', \'".join([str(elem) for elem in granjas_ssf])+"\')")
                #    ssf_data=imatia_query(sql_ssf)
                #    ssf_data['Granja']='SSF'
                #    data_frames=pd.concat([data_frames if not data_frames.empty else None, ssf_data], ignore_index=True)
                #    data_frames=data_frames.drop_duplicates(ignore_index=True)
                
                #if len(ssf_iberia) == 1:
                #    # Hacer lo mismo para SSF Iberia
                #    sql_ssf_ib=sql
                #    granjas_ssf_ib=['Cervo Sole', 'Tocha Sole', 'Couso i+d', 'Anglet_P']
                #    sql_ssf_ib=sql_ssf_ib.replace("yyyyy", "( \'"+"\', \'".join([str(elem) for elem in granjas_ssf_ib])+"\')")
                #    ssf_iberia_data=imatia_query(sql_ssf_ib)
                #    ssf_iberia_data['Granja']='SSF_Iberia'
                #    data_frames=pd.concat([data_frames if not data_frames.empty else None, ssf_iberia_data], ignore_index=True)
                #    data_frames=data_frames.drop_duplicates(ignore_index=True)

         
            else:
                escribir_log('error',"Historic growth error")
                return None

            PSheet=data_frames.copy()
            # Realizar cálculos en las columnnas meditante agrupaciones
            PSheet = PSheet.groupby(['Granja', 'FechaFin']).agg({
                'interfarm_bin': 'sum',
                'yield_kgm': 'sum',
                'mes_pasadoB': 'sum'
            }).reset_index()  #no poner drop=True
            
            PSheet['Mes'] = PSheet['FechaFin'].apply(lambda x: pd.to_datetime(x).date().month)
            PSheet['Ano'] =PSheet['FechaFin'].apply(lambda x: pd.to_datetime(x).date().year)

            #Añadido para evitar que salga infinito
            if not PSheet.loc[PSheet['mes_pasadoB']==0.0].empty:
            #if hasattr(PSheet.loc[PSheet['mes_pasadoB']==0.0], '__len__'):
                longitud=len(PSheet.loc[PSheet['mes_pasadoB']==0.0])
                PSheet.loc[PSheet['mes_pasadoB']==0.0, 'mes_pasadoB']=[1.0]*longitud 
           

            PSheet['Yield_kgm'] = PSheet['yield_kgm'] + PSheet['interfarm_bin']
            PSheet['Yield_por'] = PSheet['Yield_kgm'] / PSheet['mes_pasadoB'] * 100
            PSheet['FechaFin']=PSheet['FechaFin'].apply(lambda x: pd.to_datetime(x).date())
            PSheet['Dias_mes'] = PSheet.apply(lambda row: fechas_stolt_func_new(row.FechaFin, "dias_mes"), axis=1)
            PSheet['Dias_mes']=pd.to_numeric(PSheet['Dias_mes'])
            PSheet = PSheet[['Granja', 'Ano', 'Mes', 'Yield_kgm', 'Yield_por', 'Dias_mes']]
            
            
            PSheet = PSheet.groupby(['Granja', 'Mes']).agg({
                'Yield_kgm': 'sum',
                'Yield_por': 'sum',
                'Dias_mes': 'sum'
            }).reset_index() #no poner drop=True
            
            

            # Calcular el crecimiento medio
            PSheet['Mean_daily_growth'] = PSheet['Yield_kgm'] / PSheet['Dias_mes']
            PSheet['Mean_daily_growth_por'] = PSheet['Yield_por'] / PSheet['Dias_mes']
            PSheet = PSheet.drop(columns=['Yield_kgm', 'Yield_por','Dias_mes'], axis=1)

            # Leer meses desde un archivo CSV
            months_to_show = pd.read_csv(self.path_df_desired_growth).drop(columns=['Granja', 'Total'], axis=1).columns
            months_to_show_df=pd.DataFrame()
            months_to_show_df['Month_year']=months_to_show
            months_to_show_df['Mes_char']=months_to_show_df.apply(lambda row : str(row.Month_year).split('-')[0], axis=1)
            
            months_to_show_df['Ano']=months_to_show_df.apply(lambda row: str(row.Month_year).split('-')[1], axis=1)
            months_to_show_df['Ano']=months_to_show_df['Ano'].apply(lambda x: pd.to_numeric(x))
            months_to_show_df['Mes'] = months_to_show_df.apply(lambda row: mesChar_toNum(row.Mes_char), axis=1)
            months_to_show_df['Mes']=pd.to_numeric(months_to_show_df['Mes'])
            months_to_show_df['Fecha'] =months_to_show_df.apply(lambda row:datetime.datetime(row.Ano, row.Mes, 1), axis=1).apply(lambda x: pd.to_datetime(x).date()) ##pd.to_datetime(months_to_show_df.apply(lambda row:datetime.datetime(row.Ano, row.Mes, 1), axis=1)).dt.date
            months_to_show_df['Dias_mes'] =months_to_show_df.apply(lambda row:fechas_stolt_func_new(row.Fecha, "dias_mes"), axis=1)
            months_to_show_df['Dias_mes']=months_to_show_df['Dias_mes'].apply(lambda x: pd.to_numeric(x))
            result_type = ['Mean_growth_por' if en_por else 'Mean_growth'][0]
            
            # Combinar y dar formato al resultado final
            res = list(itertools.product(months_to_show_df['Month_year'],granjas))
            result = pd.DataFrame(res,columns=("Month_year","Granja"))
            result=result.merge(months_to_show_df[["Month_year", "Dias_mes", "Mes"]], how='right',on='Month_year').copy()
            
            result=result.merge(PSheet, on=['Granja', 'Mes']).copy()
            
            #result['Mean_growth'] = round(result['Dias_mes'] * result['Mean_daily_growth']/1000, 0)
            result['Mean_growth'] = result.apply(lambda row: round(row.Dias_mes*row.Mean_daily_growth/1000, 0),axis=1)
            #result['Mean_growth_por'] = round(result['Dias_mes'] * result['Mean_daily_growth_por'], 2)
            result['Mean_growth_por'] = result.apply(lambda row: round(row.Dias_mes * row.Mean_daily_growth_por, 2), axis=1)

            result = result.pivot_table(index='Granja', columns='Month_year', values=result_type).reset_index()  #no poner drop=True
        
            # Ordenar el resultado
            name_order=["Granja"]+months_to_show.tolist()
            result = result[name_order].copy()
            # Agregar totales y calcular promedios si es necesario
            lista_total=[["Total"]]
            lista_total.append(result.sum(numeric_only=True,axis=0).values.tolist())
            lista_total=list(np.concatenate(lista_total))
            result.loc[len(result)]=lista_total
            result.index.name = None
            result.columns.name=None
            if en_por:
                result.iloc[-1, 1:] = round(result.iloc[-1, 1:].astype(float) / (len(result) - 1), 2)
            
            return result
        except Exception as e:
             escribir_log('critical', 'mean_historic_growth_func ' +"Error {0}".format(str(e)))

    #Función que borra los resultados del último mes que se han simulado.
    #Los resultados los borra de los archivos masterDF.csv, resultado_dcasted.csv. En caso 
    #de que estos ficheros solo tengan resultados de un mes entonces borra esos ficheros y también
    # resultado.csv y resultado_dcasted.xlsx
    #Si existen los dos archivos masterDF.csv y resultado_dcasted.csv, genera un nuevo resultado
    
    def borrar_ultimo_mes_func(self):
        # Si el archivo existe y hay al menos dos meses simulados, se procede a borrar el último mes.
        if os.path.exists(self.path_masterDF):
            masterDF = pd.read_csv(self.path_masterDF)
            if len(masterDF['FechaFin'].unique()) > 1:
                masterDF = masterDF.loc[masterDF['FechaFin'] != masterDF['FechaFin'].max()]
                masterDF.to_csv(self.path_masterDF, index=False)
            else: #en caso de que solo tenga un mes, se elimina el fichero
                os.remove(self.path_masterDF)

        if os.path.exists(self.path_pescas_tallas_detail):
            pescas_tallas_detail = pd.read_csv(self.path_pescas_tallas_detail)
            if len(pescas_tallas_detail['FechaFin'].unique()) > 1:
                pescas_tallas_detail = pescas_tallas_detail.loc[pescas_tallas_detail['FechaFin'] != pescas_tallas_detail['FechaFin'].max()]
                pescas_tallas_detail.to_csv(self.path_pescas_tallas_detail, index=False)
            else: #en caso de que solo tenga 1 mes, se elimina el fichero
                os.remove(self.path_pescas_tallas_detail)

        # Se genera el nuevo resultado si ambos archivos existen.
        if os.path.exists(self.path_masterDF) and os.path.exists(self.path_pescas_tallas_detail):
            self.set_resultado()
        else:
            # Si uno o ambos archivos no existen, se eliminan los resultados generados anteriormente.
            if os.path.exists(self.path_resultado):
                os.remove(self.path_resultado)
            if os.path.exists(self.path_resultado_dcasted):
                os.remove(self.path_resultado_dcasted)
            if os.path.exists(self.path_resultado_dcasted_xls):
                os.remove(self.path_resultado_dcasted_xls)
        escribir_log('info',"Último mes borrado")

    #Función que lee el fichero de path
    #Si Talla está entre los nombres de las columnas se mantiene para la clasificación
    
    def import_format_func(self, path, val_name, from_por=False):
        try:
            data = pd.read_csv(path)
            id_vars = ["Granja", "Talla"] if "Talla" in data.columns else ["Granja"]

            #Pasamos de formato ancho a largo:
            # -de Granja [otros] y otras columnas con los mes-año 
            # -a Granja [otros], columna de valor (Num), columna de Mes y columna de Año
            data = pd.melt(data, id_vars=id_vars, var_name="MesAno", value_name=val_name).copy()
            #Nos quedamos solo con las granjas y con los MesAno quitándonos los totales
            data = data.loc[(data["Granja"] != "Total") & (data["MesAno"] != "Total")].copy()
            #Transformamos las columnas Mes y Ano para quedarnos con el número del mes y el del año
            data["MesAno"]=data["MesAno"].astype(str)
            data["Mes"] = data["MesAno"].str.split("-").str[0].apply(mesChar_toNum)
            data["Ano"] = data["MesAno"].str.split("-").str[1].astype(int)
            data = data.drop(columns="MesAno", axis=1)
            #Eliminamos los valores negativos si los hubiera
            data = data.loc[data[val_name] > 0]
            #Transformación para los valores numéricos (dividirlo por 100)
            if from_por and len(data) > 0:
                data[val_name] = data[val_name].apply(lambda x: x/100 )
            return data
        except Exception as e:
             escribir_log('critical', 'import_format_func ' +"Error {0}".format(str(e)))


    #Devuelve un dataframe con "Granja", "Edad", "Mes", "Ano", "Ajuste" a partir del fichero
    #r"Temp/inputs/mod/last_df_ajustes_crecimiento.csv" si Ajuste_por es Edad 
    #La edad es la de los peces
    #Para devolver el dataframe tiene que haber líneas en el fichero donde "Ajuste_por" ha de ser igual
    #a "Edad" y Ajuste en el fichero ha de ser distinto de 0
    
    def import_format_growth_aj_edad_func(self):
        try:
            data = pd.read_csv(self.path_df_ajustes_crecimiento,header=0)
            data = data.loc[(data["Ajuste_por"] == "Edad") & (data["Ajuste"] != 0)]
            data=data.drop(columns="Activar", axis=1)
            if len(data) < 1:
                return None
            #Asignar a Mes_inicio y Mes_fin el día 1 del mes
            data["Mes_inicio"] = data["Mes_inicio"].apply( lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date().replace(day=1))
            data["Mes_fin"] = data["Mes_fin"].apply( lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date().replace(day=1))
            
            #Si alguna fecha de fin es menor o igual que la de inicio se 
            #devuelve un error y se sale de la función
            if sum(data["Mes_inicio"] > data["Mes_fin"]) > 0:
                return "Error Fechas"
            
            data["Fecha"] = data.apply(lambda row: seq_dates(row["Mes_inicio"], row["Mes_fin"]), axis=1)
            data["Edad"] = data["Talla_Gen_Edad"].apply(lambda x: seq_edades(x))
            #Separa en distintas filas los resultados de seq_edades y seq_dates 
            data = data.explode("Fecha").explode("Edad")
            data[["Mes", "Ano"]] = data["Fecha"].str.split("-", expand=True)[[1, 0]].astype(int)
            return data[["Granja", "Edad", "Mes", "Ano", "Ajuste"]]
        except Exception as e:
             escribir_log('critical', 'import_format_growth_aj_edad_func ' +"Error {0}".format(str(e)))

    #Devuelve un dataframe con "Granja", "Talla_Gen_Edad", "Mes", "Ano", "Ajuste" a partir del fichero
    #r"Temp/inputs/mod/last_df_ajustes_crecimiento.csv" si Ajuste_por es "Talla" o es "Gen", en 
    # cuyo caso la columna "Talla_Gen_Edad" toma el nombre "Talla" o "Gen"
    #Para devolver el dataframe tiene que haber líneas en el fichero donde "Ajuste_por" ha de ser igual
    #al type que se ha pasdo por parámetro y Ajuste en el fichero ha de ser distinto de 0
    
    def import_format_growth_aj_talla_o_gen_func(self, type):
        try:
            data = pd.read_csv(self.path_df_ajustes_crecimiento,header=0)
            data = data.loc[(data["Ajuste_por"] == type) & (data["Ajuste"] != 0)]
            data=data.drop(columns="Activar", axis=1)
            if len(data) < 1:
                return None
            #Asignar a Mes_inicio y Mes_fin el día 1 del mes
            data["Mes_inicio"] = data["Mes_inicio"].apply( lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date().replace(day=1))
            data["Mes_fin"] = data["Mes_fin"].apply( lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date().replace(day=1))
            
            #Si alguna fecha de fin es menor o igual que la de inicio se 
            #devuelve un error y se sale de la función
            if sum(data["Mes_inicio"] > data["Mes_fin"]) > 0:
                return "Error Fechas"
            
            data["Fecha"] = data.apply(lambda row: seq_dates(row["Mes_inicio"], row["Mes_fin"]), axis=1)
            
            #Separa en distintas filas los resultados de seq_edades y seq_dates 
            data = data.explode("Fecha")
            data[["Mes", "Ano"]] = data["Fecha"].str.split("-", expand=True)[[1, 0]].astype(int)
            data=data[["Granja", "Talla_Gen_Edad", "Mes", "Ano", "Ajuste"]].copy()
            data=data.rename(columns={'Talla_Gen_Edad': type})
            if "Talla" in data.columns:
                data["Talla"]=data["Talla"].apply(lambda x: RangoPesoFunc_plus_letter(x, self.especie))
            return(data)
        except Exception as e:
             escribir_log('critical', 'import_format_growth_aj_talla_o_gen_func ' +"Error {0}".format(str(e)))

    #Devuelve un dataframe con "Granja", "Talla_Gen_Edad", "Mes", "Ano", "Ajuste", "Por_Cull" a partir del fichero
    #r"Temp/inputs/mod/last_df_ajustes_mortalidad.csv" si activar es True y Ajuste distinto de 0
    #
    
    def import_format_mort_aj_gen_func(self):
        try:
            data = pd.read_csv(self.path_df_ajustes_mortalidad,header=0)
            data = data.loc[(data["Activar"] == True) & (data["Ajuste"] != 0)]
            data=data.drop(columns="Activar", axis=1)
            if len(data) < 1:
                #data=pd.DataFrame(columns=["Granja", "Gen", "Mes", "Ano", "Ajuste", "Por_Cull"])
                return None
            #Asignar a Mes_inicio y Mes_fin el día 1 del mes
            data["Mes_inicio"] = data["Mes_inicio"].apply( lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date().replace(day=1))
            data["Mes_fin"] = data["Mes_fin"].apply( lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date().replace(day=1))
            
            #Si alguna fecha de fin es menor o igual que la de inicio se 
            #devuelve un error y se sale de la función
            if  data.apply(lambda row: np.where(row.Mes_inicio>row.Mes_fin,1,0),axis=1).sum()>0:
                return "Error Fechas"
            
            data["Fecha"] = data.apply(lambda row: seq_dates(row["Mes_inicio"], row["Mes_fin"]), axis=1)
            
            #Separa en distintas filas los resultados de seq_edades y seq_dates 
            data = data.explode("Fecha")
            data[["Mes", "Ano"]] = data["Fecha"].str.split("-", expand=True)[[1, 0]].astype(int)
            data=data[["Granja", "Talla_Gen_Edad", "Mes", "Ano", "Ajuste", "Por_Cull"]].copy()
            data=data.rename(columns={'Talla_Gen_Edad': "Gen"})
            
            return(data)
        except Exception as e:
             escribir_log('critical', 'import_format_mort_aj_gen_func ' +"Error {0}".format(str(e)))

    #Devuelve un dataframe con "Granja", "Gen", "Mes", "Ano" a partir del fichero
    #r"Temp/inputs/mod/last_df_acabar_gen.csv" si activar es True
    #
    
    def import_format_acabar_gen(self):
        try:
            data = pd.read_csv(self.path_df_acabar_gen)
            data = data.loc[data['Activar'] == True]
            data=data.drop(columns="Activar", axis=1)
            if len(data) < 1:
                return None
            data['Ano'] = data['Mes'].apply(lambda x: pd.to_datetime(x).date().year)
            data['Mes'] = data['Mes'].apply(lambda x: pd.to_datetime(x).date().month)
            return data
        except Exception as e:
             escribir_log('critical', 'import_format_acabar_gen ' +"Error {0}".format(str(e)))

    #Función que devuelve un data frame con todos los datos lanzando consultas a la Elastic (BD) si continue_flag es false
    #o los toma de la última simulación
    #Necesita como parámetros continue_flag(datos nuevo o de la última simulación), path_granjas_sim (fichero que guarda las granjas sobre
    #las que se obtienen los datos), fecha (¡ojo! en formato date; es la fecha hasta la que se lanza la consulta en la BD) y
    #especie ("TURBOT" rodaballo y "SOLE" lenguado)
    
    def import_initial_data(self, continue_flag, fecha):
        try:
            if not continue_flag:
                granjas = pd.read_csv(self.path_default_campos_granjas, sep=",")
                if self.especie=="TURBOT":
                    granjas = granjas.replace("Vilan_P", "Vilán_P") #Para lanzar la consulta a Elastic
                granjas_solas = [granja for granja in granjas.Granja if granja not in ["SSF", "SSF_Iberia"]]
                ssf = [granja for granja in granjas.Granja if granja == "SSF"]
                ssf_iberia = [granja for granja in granjas.Granja if granja == "SSF_Iberia"]
                
                data_frames = pd.DataFrame()
                sql = f"SELECT codigoplanta as Granja, dias as Edad, peso as PesoMedio, numeroindividuos as Num, descgeneracion as Gen, descestanque as Tanque, codigoespecie as especie FROM VistaHistoricoEstanquesUltimoCicloDia WHERE codigoplanta IN ( yyyyy ) AND numeroindividuos > 0 AND fecha = '{fecha}'"
                
                if self.especie == "TURBOT":
                
                    # Ejecutar la consulta SQL y almacenar los resultados en data_frames
                    
                    if len(granjas)>0 :
                        sql_granjas=sql
                        sql_granjas=sql_granjas.replace("yyyyy", "\'"+"\', \'".join([str(elem) for elem in granjas_solas])+"\'")
                        granjas_data=imatia_query(sql_granjas)
                        granjas_data["Granja"]=granjas_data["Granja"].replace("Vilán_P", "Vilan_P")
                        data_frames=pd.concat([data_frames if not data_frames.empty else None, granjas_data], ignore_index=True)
                        #data_frames=data_frames.drop_duplicates(ignore_index=True)
                        
                    
                    if len(ssf) == 1:
                        # Hacer lo mismo para SSF
                        sql_ssf=sql
                        granjas_ssf=['Cervo_P', 'Lira_P', 'Merexo_P', 'Couso_P', 'Oye_P',  'Palmeira_P', 'Quilmas_P', 'Vilán_P', 'Tocha_P']
                        sql_ssf=sql_ssf.replace("yyyyy", " \'"+"\', \'".join([str(elem) for elem in granjas_ssf])+"\'")
                        ssf_data=imatia_query(sql_ssf)
                        ssf_data['Granja']='SSF'
                        data_frames=pd.concat([data_frames if not data_frames.empty else None, ssf_data], ignore_index=True)
                        #data_frames=data_frames.drop_duplicates(ignore_index=True)
                        
                    
                    if len(ssf_iberia) == 1:
                        # Hacer lo mismo para SSF Iberia
                        sql_ssf_ib=sql
                        granjas_ssf_ib=['Cervo_P', 'Lira_P', 'Merexo_P', 'Couso_P',  'Palmeira_P', 'Quilmas_P', 'Vilán_P', 'Tocha_P']
                        sql_ssf_ib=sql_ssf_ib.replace("yyyyy", " \'"+"\', \'".join([str(elem) for elem in granjas_ssf_ib])+"\'")
                        ssf_iberia_data=imatia_query(sql_ssf_ib)
                        ssf_iberia_data['Granja']='SSF_Iberia'
                        data_frames=pd.concat([data_frames if not data_frames.empty else None, ssf_iberia_data], ignore_index=True)
                        #data_frames=data_frames.drop_duplicates(ignore_index=True)
            
                elif self.especie == "SOLE":
            
                    # Ejecutar la consulta SQL y almacenar los resultados en data_frames
                    
                    if len(granjas)>0 :
                        sql_granjas=sql
                        sql_granjas=sql_granjas.replace("yyyyy", " \'"+"\', \'".join([str(elem) for elem in granjas_solas])+"\'")
                        granjas_data=imatia_query(sql_granjas)
                        data_frames=pd.concat([data_frames if not data_frames.empty else None, granjas_data], ignore_index=True)
                        data_frames=data_frames.drop_duplicates(ignore_index=True)
                        
                    
                    #if len(ssf) == 1:
                    #    # Hacer lo mismo para SSF
                    #    sql_ssf=sql
                    #    granjas_ssf=['Cervo Sole', 'Tocha Sole', 'Hafnir_P', 'Couso i+d', 'Anglet_P']
                    #    granjas_ssf=sql_ssf.replace("yyyyy", " \'"+"\', \'".join([str(elem) for elem in granjas_ssf])+"\'")
                    #    ssf_data=imatia_query(sql_ssf)
                    #    ssf_data['Granja']='SSF'
                    #    data_frames=pd.concat([data_frames if not data_frames.empty else None, ssf_data], ignore_index=True)
                    #    #data_frames=data_frames.drop_duplicates(ignore_index=True)
                        
                    
                    #if len(ssf_iberia) == 1:
                    #    # Hacer lo mismo para SSF Iberia
                    #    sql_ssf_ib=sql
                    #    granjas_ssf_ib=['Cervo Sole', 'Tocha Sole', 'Couso i+d', 'Anglet_P']
                    #    sql_ssf_ib=sql_ssf_ib.replace("yyyyy", " \'"+"\', \'".join([str(elem) for elem in granjas_ssf_ib])+"\'")
                    #    ssf_iberia_data=imatia_query(sql_ssf_ib)
                    #    ssf_iberia_data['Granja']='SSF_Iberia'
                    #    data_frames=pd.concat([data_frames if not data_frames.empty else None, ssf_iberia_data], ignore_index=True)
                    #    #data_frames=data_frames.drop_duplicates(ignore_index=True)
                        

                else:
                    escribir_log('error',"import_initial_data error: especie desconocida")

                #hay que lanzar una excepcion si no hay datos
                if data_frames is None:
                    raise ValueError('La consulta SQL no devuelve datos. Considere cambiar la fecha y/o granjas')
                if data_frames.empty:
                    raise ValueError('La consulta SQL no devuelve datos. Considere cambiar la fecha y/o granjas')
                all_data=data_frames.copy()
                all_data['especie'] = all_data['especie'].replace("LE", "SOLE")
                all_data['especie'] = all_data['especie'].replace("R", "TURBOT")
                all_data = all_data.loc[all_data['especie'] == self.especie].drop(columns=['especie'])
                fecha_fin = fecha
                all_data['Virtual'] = False
                all_data['Fecha'] = pd.to_datetime(fecha).date()
            else:
                # codigo para coger los datos de la ultima simulacion
                if os.path.exists(self.path_masterDF):
                    all_data = pd.read_csv(self.path_masterDF)
                    all_data= all_data[["Granja", "EdadFinal", "PesoMedioFinal", "NumFinal", "Gen", "Tanque", "Virtual", "FechaFin"]]
                    all_data = all_data.loc[all_data['FechaFin'] == all_data['FechaFin'].max()]
                    all_data=all_data.loc[all_data['NumFinal'] > 0].rename(columns={'EdadFinal': 'Edad', 'PesoMedioFinal': 'PesoMedio', 'NumFinal': 'Num', 'FechaFin': 'Fecha'}).copy()
                    all_data['Fecha'] = all_data['Fecha'].apply(lambda x: pd.to_datetime(x).date())
                    fecha_fin = pd.to_datetime(all_data['Fecha'].unique()[0]).date()
                    
                else:
                    # No deberia dejar llegar a esta opcion ya que input continue no puede ser TRUE si no hay masterDF
                    escribir_log('info',"No hay master df guardado para initial data")
                    return None
            
            #Columnnas adicionales
            
            fecha_fin = datetime.datetime.strptime(str(fecha_fin), "%Y-%m-%d").date().replace(day=1)  #se pone a día 1 todas las fechas_fin
            fecha_fin = pd.to_datetime(datetime.datetime.strptime(fechas_stolt_func_new(fecha=add_months(fecha_fin, 1)), "%Y-%m-%d").date()).date()

            all_data['Biomasa'] = all_data['Num'] * all_data['PesoMedio'] / 1000
            all_data['YearClass'] = "20" + all_data['Gen'].str[0:2]  #Comprobar que toma bien el año
            all_data['BiomasaBajas'] = 0.0
            all_data['NumBajas'] = 0
            all_data['Cull'] = False
            all_data['NumBajas_cull'] = 0
            all_data['BiomasaBajas_cull'] = 0.0
            all_data['NumSinBajas'] = 0
            all_data['BiomasaSinBajas'] = 0.0
            all_data['FechaFin'] = fecha_fin
            all_data['DiasMes'] = (all_data['FechaFin'] - all_data['Fecha']).apply (lambda x: x.days)
            all_data['PesoMedioSinBajas'] = 0.0
            all_data['Talla'] = all_data['PesoMedio'].apply(lambda x: RangoPeso_directo_letra(x, self.especie))
            all_data['BiomasaPescas'] = 0.0
            all_data['BiomasaSinPescas'] = 0.0
            all_data['NumPescas'] = 0
            all_data['NumSinPescas'] = 0
            all_data['PesoMedioSinPescas'] = 0.0
            all_data['Tasa'] = 0.0
            all_data['PesoMedioFinal'] = 0.0
            all_data['BiomasaFinal'] = 0.0
            all_data['NumFinal'] = 0
            all_data['EdadFinal'] = all_data['Edad'] + all_data['DiasMes']
            all_data['TallaFinal'] = " "
            all_data['Input'] = False
            
            return all_data
        
        except Exception as e:
             escribir_log('critical', 'import_initial_data ' +"Error {0}".format(str(e)))

        
    #Función que genera x miles de muestras de pesos de peces de forma aleatoria
    #según media y CV como si siguieran una distribución normal
    #Devuelve un dataframe con la granja, los grupos de pesos y el número relativo
    #de ejemplares en es grupo para esa granja.
    
    def import_format_mort_dist(self):
        try:
            all_reparto_mort = pd.read_csv(self.path_df_reparto_mort)
            all_reparto_mort['CV_1'] = all_reparto_mort['CV_1'].apply(lambda x: x/100)
            all_reparto_mort['CV_2'] = all_reparto_mort['CV_2'].apply(lambda x: x/100)
            all_pesos_df = pd.DataFrame(columns=['Granja', 'Peso', 'Num'])
            for i in range(len(all_reparto_mort)):
                i_granja = all_reparto_mort.loc[i, 'Granja']
                i_mean_1 = all_reparto_mort.loc[i, 'PesoMedio_1']
                i_mean_2 = all_reparto_mort.loc[i, 'PesoMedio_2']
                i_cv_1 = all_reparto_mort.loc[i, 'CV_1']
                i_cv_2 = all_reparto_mort.loc[i, 'CV_2']
                
                
                pesos = rnorm3(n=2300, mean_1 = i_mean_1, mean_2 = i_mean_2, cv_1 = i_cv_1, cv_2 = i_cv_2)
                #flat_pesos=[x for xs in pesos for x in xs]
                pesos_df = pd.DataFrame({'Peso': pesos.flatten()})
                pesos_df['Granja'] = i_granja
                pesos_df['Num'] = 1
                all_pesos_df = pd.concat([all_pesos_df if not all_pesos_df.empty else None, pesos_df], ignore_index=True)
                #all_pesos_df=all_pesos_df.drop_duplicates(ignore_index=True)
            
            
            all_pesos_df['Rango'] = RangoPesoFunc_custom(all_pesos_df['Peso'])

            #Borramos los outlier (pesos negativos, outliers)
            all_pesos_df = all_pesos_df.dropna(subset=['Rango'])
            #Agrupa por Granja y Rango y cuenta el número de peces en cada uno
            all_pesos_df = all_pesos_df.groupby(['Granja', 'Rango']).agg({'Num': 'sum'}).reset_index()
            #Obtenemos el total de peso por granja
            tot = all_pesos_df.groupby('Granja')['Num'].sum()
            #Uno All_pesos_df y tot por granja. El resultado es un dataframe
            #con las columnas de all_pesos_df y la de tot. Las columnas que se llamen igual
            #en tot aparecen en el resultado con el sufijo _total
            all_pesos_df = all_pesos_df.merge(tot, on='Granja', suffixes=('', '_total'))
            #La columna Por es el número relativo de cada grupo en cada granja
            all_pesos_df['Por'] = all_pesos_df['Num'] / all_pesos_df['Num_total']
            #Me quedo con la granja, el rango de pesos y el número relativo de cada grupo en cada granja
            all_pesos_df = all_pesos_df[['Granja', 'Rango', 'Por']]
            return all_pesos_df
        except Exception as e:
             escribir_log('critical', 'import_format_mort_dist ' +"Error {0}".format(str(e)))

    #Función que devuelve un dataframe con los alevines por granja, Edad, Peso medio, tanque, etc
    
    def set_alevines(self,resultado_df, all_alevines_df, pm_y_cv_df, peces_x_tanque=2500):
        try:
            mes_loop = pd.to_datetime(resultado_df['FechaFin'].unique()[0]).month
            ano_loop = pd.to_datetime(resultado_df['FechaFin'].unique()[0]).year
            if all_alevines_df is None:
                escribir_log('info', "No hay datos en tabla inputs alevines")
                return resultado_df
                
            alevines_mes = all_alevines_df.loc[(all_alevines_df['Ano'] == ano_loop) & (all_alevines_df['Mes'] == mes_loop) & (all_alevines_df['Num'] > 0)].copy()
            if alevines_mes.shape[0] == 0:
                escribir_log('info', f"No hay alevines el mes: {mes_loop} del ano: {ano_loop}")
                return resultado_df
            
            alevines_del_mes = self.Budg_Expand_alevines_all(data=alevines_mes, peces_x_tanque=peces_x_tanque, inputs_sett=pm_y_cv_df)
            
            #Añadido el date al final
            alevines_del_mes['Fecha'] = pd.to_datetime(resultado_df['Fecha'].unique()[0]).date()
            alevines_del_mes['Biomasa'] = alevines_del_mes['PesoMedio'] * alevines_del_mes['Num'].apply(lambda x: x/1000)
            alevines_del_mes['YearClass'] = "20" + alevines_del_mes['Gen'].str[:2]
            alevines_del_mes['BiomasaBajas'] = 0.0
            alevines_del_mes['NumBajas'] = 0
            alevines_del_mes['Cull'] = False
            alevines_del_mes['NumBajas_cull'] = 0
            alevines_del_mes['BiomasaBajas_cull'] = 0.0
            alevines_del_mes['NumSinBajas'] = 0
            alevines_del_mes['BiomasaSinBajas'] = 0.0
            alevines_del_mes['FechaFin'] = resultado_df['FechaFin'].unique()[0]
            alevines_del_mes['DiasMes'] =  (alevines_del_mes['FechaFin'] - alevines_del_mes['Fecha']).apply (lambda x: x.days)
            alevines_del_mes['PesoMedioSinBajas'] = 0.0
            alevines_del_mes['Talla'] = alevines_del_mes['PesoMedio'].apply(lambda x: RangoPeso_directo_letra(x, self.especie))
            alevines_del_mes['BiomasaPescas'] = 0.0
            alevines_del_mes['BiomasaSinPescas'] = 0.0
            alevines_del_mes['NumPescas'] = 0
            alevines_del_mes['NumSinPescas'] = 0
            alevines_del_mes['PesoMedioSinPescas'] = 0.0
            alevines_del_mes['Tasa'] = 0
            alevines_del_mes['PesoMedioFinal'] = 0.0
            alevines_del_mes['BiomasaFinal'] = 0.0
            alevines_del_mes['NumFinal'] = 0
            alevines_del_mes['EdadFinal'] = alevines_del_mes['Edad'] + alevines_del_mes['DiasMes']
            alevines_del_mes['TallaFinal'] = ""
            alevines_del_mes['Virtual'] = True
            alevines_del_mes['Input'] = True

            resultado_df = pd.concat([resultado_df if not resultado_df.empty else None, alevines_del_mes if not alevines_del_mes.empty else None], ignore_index=True)
            return resultado_df
        except Exception as e:
             escribir_log('critical', 'set_alevines ' +"Error {0}".format(str(e)))

    
    def set_ventas(self,resultado_df, all_ventas_df, all_dispersion_df, all_edad_venta_df, all_acabar_gen, continue_flag, loop):
        try:
            #np.random.seed(7777)
            por_desorden = 15
            initial_names = resultado_df.columns
            #Se altera el orden de resultado_df
            resultado_df = resultado_df.sample(n=resultado_df.shape[0],random_state=777).reset_index(drop=True) 
            #resultado_df = resultado_df.sample(frac=1).reset_index(drop=True)
            
            
            seccion = round(resultado_df.shape[0] * (por_desorden / 100))
            desordenado = resultado_df.iloc[:seccion, :].copy()
            ordenado = resultado_df.iloc[seccion:, :].sort_values(by='Edad', ascending=False).copy()

            ordenado['i'] = range(ordenado.shape[0])
            desordenado['i']=ordenado.sample(desordenado.shape[0],random_state=777)['i'].reset_index(drop=True)

            #desordenado['i'].values=ordenado.loc['i'].sample(desordenado.shape[0],random_state=777).to_list()
            #desordenado['i']=np.random.choice(ordenado['i'], size=len(desordenado), replace=False).values
            resultado_df = pd.concat([ordenado if not ordenado.empty else None, desordenado if not desordenado.empty else None], ignore_index=True)
            resultado_df=resultado_df.sort_values(by='i').copy()
            #resultado_df = resultado_df.sort_values(by='i').reset_index(drop=True)
            #resultado_df.drop('i', axis=1, inplace=True)
            resultado_df.drop(columns=['i'], inplace=True)
           
            
            resultado_df['id_pescas'] = range(resultado_df.shape[0])
            #resultado_df['id_pescas'] = range(1, len(resultado_df) + 1)
            resultado_df['Biomasa']=resultado_df['Biomasa'].astype(float)
            resultado_df['BiomasaPescas']=resultado_df['BiomasaPescas'].astype(float)
            resultado_df['BiomasaSinPescas'] = resultado_df['Biomasa']
            resultado_df['NumSinPescas']=resultado_df['Num']
            

            fecha_fin = pd.to_datetime(resultado_df['FechaFin'].unique()[0]).date()
            mes_loop = fecha_fin.month
            ano_loop = fecha_fin.year

            if all_ventas_df is None: 
                return resultado_df[initial_names]
            if all_ventas_df.empty:
                return resultado_df[initial_names]
            
            ventas_mes = all_ventas_df.loc[(all_ventas_df['Ano'] == ano_loop)&(all_ventas_df['Mes'] == mes_loop) & (all_ventas_df['BiomasaVentas'] > 0)].copy()
            ventas_mes['BiomasaVentas']=ventas_mes['BiomasaVentas'].astype(float)
            disp_mes = all_dispersion_df.loc[(all_dispersion_df['Ano'] == ano_loop)& (all_dispersion_df['Mes'] == mes_loop) & (all_dispersion_df['cv'] > 0)].copy()
            edad_ventas_mes = all_edad_venta_df.loc[(all_edad_venta_df['Ano'] == ano_loop) & (all_edad_venta_df['Mes'] == mes_loop)].copy()
            if all_acabar_gen is not None and not all_acabar_gen.empty:
                acabar_gen_mes = all_acabar_gen.loc[(all_acabar_gen['Ano'] == ano_loop)&(all_acabar_gen['Mes'] == mes_loop)]
            

            #Si no hay ventas se devuelve la entrada tal cual
            if ventas_mes.empty:
                return resultado_df[initial_names]
            # Para saber que tallas saco de cada tanque hay que recoger los datos en otra df 
            
            pescas_tallas_detail = pd.DataFrame(columns=['Granja', 'FechaFin', 'Gen', 'Talla', 'Biomasa', 'Num'])

            resultado_df=resultado_df.reset_index(drop=True) #Tengo que hacerlo así para que el índice coincida con el número de línea

            for i in range(resultado_df.shape[0]):
                
                i_granja = resultado_df.loc[i,'Granja']
                
                i_gen = resultado_df.loc[i, 'Gen']
                i_id_pescas = resultado_df.loc[i,'id_pescas']
                i_cv = disp_mes.loc[disp_mes['Granja'] == i_granja,'cv'].to_list()
                

                i_edad = resultado_df.loc[i,'Edad']
                i_edad_lim = edad_ventas_mes.loc[edad_ventas_mes['Granja'] == i_granja,'Edad'].to_list()
                
                if len(i_edad_lim)==0:
                    i_edad_lim = 0
                else:
                    i_edad_lim=i_edad_lim.item(0)
            
                
                if i_edad_lim > i_edad:  #Salta a la siguiente iteración en el for
                    continue

                if len(i_cv)!=0:
                    #i_cv=i_cv.item(0) Vamos a probar sin hacer esto
                    i_tanque_disper = resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, ['id_pescas', 'Num', 'PesoMedio']]
                    #i_tanque_disper['Pesos_peces'] = i_tanque_disper.map(lambda x: dispersion_pesos_func(n=x['Num'], mean=x['PesoMedio'], cv=i_cv), axis=1) ####Cambié apply por map (de mapply) para adaptarlo mejor a python
                    i_tanque_disper['Pesos_peces'] = i_tanque_disper.apply(lambda x: dispersion_pesos_func(n=int(x['Num']), mean=x['PesoMedio'], cv=i_cv), axis=1)
                    i_tanque_disper = i_tanque_disper.drop('PesoMedio', axis=1)
                    i_tanque_disper["Pesos_peces"]=i_tanque_disper['Pesos_peces'].str.split(',')
                    #i_tanque_disper = i_tanque_disper.set_index(['id_pescas', 'Num']).apply(lambda x: x.str.split(',').explode()).reset_index()
                    i_tanque_disper=i_tanque_disper.explode('Pesos_peces')
                    i_tanque_disper['Pesos_peces'] = pd.to_numeric(i_tanque_disper['Pesos_peces'])
                    i_tanque_disper['Talla'] = RangoPeso_directo_letra_para_df(i_tanque_disper, "Pesos_peces", especie=self.especie)
                    i_tanque_disper['Num']=1
                    #i_tanque_disper = i_tanque_disper.groupby(['id_pescas', 'Talla']).agg({'Num': 'sum', 'Biomasa': ('Pesos_peces','sum')/1000, 'PesoMedio': ('Pesos_peces','sum')/('Num', 'sum')}).reset_index()
                    i_tanque_disper = i_tanque_disper.groupby(['id_pescas', 'Talla']).agg({'Num': 'sum', 'Pesos_peces': 'sum'}).reset_index() #No poner el drop true
                    i_tanque_disper['Biomasa']=i_tanque_disper['Pesos_peces']/1000.0
                    i_tanque_disper['PesoMedio']=i_tanque_disper['Pesos_peces']/i_tanque_disper['Num']
                    i_tanque = i_tanque_disper.copy().reset_index(drop=True)

                
                else:
                    i_tanque = resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas,['id_pescas', 'Talla', 'Num', 'Biomasa', 'PesoMedio']].copy().reset_index(drop=True)  #Dejar sin drop=true
                
                #Puedo hacerlo así pq vengo de un reset_index de i_tanque
                for j in range(i_tanque.shape[0]):
                    j_talla = i_tanque.loc[j,'Talla']
                    j_biomasa_tanque = i_tanque.loc[j,'Biomasa']
                    j_num_tanque = i_tanque.loc[j,'Num']
                    j_pesomedio_tanque = i_tanque.loc[j, 'PesoMedio']
                    j_biomasa_vender = ventas_mes.loc[(ventas_mes['Talla'] == j_talla) & (ventas_mes['Granja'] == i_granja),'BiomasaVentas'].to_list()

                    if all_acabar_gen is not None:
                        acabar_check = acabar_gen_mes.loc[(acabar_gen_mes['Granja'] == i_granja) & (acabar_gen_mes['Gen'] == i_gen)]
                        if not acabar_check.empty:
                            j_biomasa_vender = j_biomasa_tanque
                    
                    if len(j_biomasa_vender)==0:
                        continue
                    
                    #j_biomasa_vender=j_biomasa_vender[0] #Esto lo pongo yo
                    #if not isinstance(j_biomasa_vender, numbers.Number):
                    #    continue
                    if j_biomasa_vender >= j_biomasa_tanque:
                        ventas_mes.loc[(ventas_mes['Talla'] == j_talla) & (ventas_mes['Granja'] == i_granja),'BiomasaVentas'] = ventas_mes.loc[(ventas_mes['Talla'] == j_talla) & (ventas_mes['Granja'] == i_granja),'BiomasaVentas'] -j_biomasa_tanque
                        resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaPescas'] =resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaPescas'] +j_biomasa_tanque
                        resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaSinPescas'] = resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaSinPescas']-j_biomasa_tanque
                        resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumPescas'] =resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumPescas'] + j_num_tanque
                        resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumSinPescas'] = resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumSinPescas']-j_num_tanque
                        
                        ####Tengo que hacerlo así pq me han aparecido listas en el fichero
                        if hasattr(j_biomasa_tanque, '__len__'):
                            j_biomasa_tanque=j_biomasa_tanque[0]
                        if hasattr(j_num_tanque, '__len__'):
                            j_num_tanque=j_num_tanque[0]
                        pescas_row = pd.DataFrame({'Granja': [i_granja], 'FechaFin':[str(fecha_fin)], 'Gen':[i_gen], 'Talla':[j_talla], 'Biomasa':[j_biomasa_tanque], 'Num':[j_num_tanque]})
                        pescas_tallas_detail=pd.concat([pescas_tallas_detail if not pescas_tallas_detail.empty else None, pescas_row if not pescas_row.empty else None], ignore_index=True)

                    else:
                        # Checkeo que el Num despues de pescas sea entero
                        supuesto_NumPescas = j_biomasa_vender / (j_pesomedio_tanque / 1000)
                        if supuesto_NumPescas % 1 == 0:
                            #Si es entero
                            ventas_mes.loc[(ventas_mes['Talla'] == j_talla) & (ventas_mes['Granja'] == i_granja), 'BiomasaVentas'] = 0
                            resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaPescas'] =resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaPescas']+ j_biomasa_vender
                            resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaSinPescas'] =resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaSinPescas']- j_biomasa_vender
                            resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumPescas'] =resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumPescas'] + supuesto_NumPescas
                            resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumSinPescas'] =resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumSinPescas'] - supuesto_NumPescas
                            
                            ####Tengo que hacerlo así pq me han aparecido listas en el fichero
                            if hasattr(j_biomasa_vender, '__len__'):
                                j_biomasa_vender=j_biomasa_vender[0]
                            if hasattr(supuesto_NumPescas, '__len__'):
                                supuesto_NumPescas=supuesto_NumPescas[0]

                            pescas_row = pd.DataFrame({'Granja': [i_granja], 'FechaFin':[str(fecha_fin)], 'Gen':[i_gen], 'Talla':[j_talla], 'Biomasa':[j_biomasa_vender], 'Num':[supuesto_NumPescas]})
                            pescas_tallas_detail=pd.concat([pescas_tallas_detail if not pescas_tallas_detail.empty else None, pescas_row if not pescas_row.empty else None], ignore_index=True)

                        else:
                            #Si no
                            NumPescas_redondeado = np.floor(supuesto_NumPescas)
                            if NumPescas_redondeado > 0:
                                BiomasaPescas_redondeada = NumPescas_redondeado * (j_pesomedio_tanque / 1000)
                                ventas_mes.loc[(ventas_mes['Talla'] == j_talla) & (ventas_mes['Granja'] == i_granja), 'BiomasaVentas'] =j_biomasa_vender - BiomasaPescas_redondeada
                                resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaPescas'] =resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaPescas']+ BiomasaPescas_redondeada
                                resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaSinPescas'] =resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'BiomasaSinPescas']- BiomasaPescas_redondeada
                                resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumPescas'] =resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumPescas']+ NumPescas_redondeado
                                resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumSinPescas'] =resultado_df.loc[resultado_df['id_pescas'] == i_id_pescas, 'NumSinPescas']- NumPescas_redondeado
                                
                                ####Tengo que hacerlo así pq me han aparecido listas en el fichero
                                if hasattr(BiomasaPescas_redondeada, '__len__'):
                                    BiomasaPescas_redondeada=BiomasaPescas_redondeada[0]
                                if hasattr(NumPescas_redondeado, '__len__'):
                                    NumPescas_redondeado=NumPescas_redondeado[0]
                                pescas_row = pd.DataFrame({'Granja': [i_granja], 'FechaFin':[str(fecha_fin)], 'Gen':[i_gen], 'Talla':[j_talla], 'Biomasa':[BiomasaPescas_redondeada], 'Num':[NumPescas_redondeado]})
                                pescas_tallas_detail=pd.concat([pescas_tallas_detail if not pescas_tallas_detail.empty else None, pescas_row if not pescas_row.empty else None], ignore_index=True)
            if continue_flag:
                
                if os.path.exists(self.path_pescas_tallas_detail):
                    old_pescas_tallas_detail = pd.read_csv(self.path_pescas_tallas_detail)
                    pescas_tallas_detail = pd.concat([old_pescas_tallas_detail if not old_pescas_tallas_detail.empty else None,pescas_tallas_detail if not pescas_tallas_detail.empty else None], ignore_index=True)
                    #pescas_tallas_detail=pescas_tallas_detail.drop_duplicates(ignore_index=True)
                    #pescas_tallas_detail['FechaFin']=pescas_tallas_detail['FechaFin'].apply(lambda x: pd.to_datetime(datetime.datetime.strptime(str(x), "%Y-%m-%d")).date())
                    pescas_tallas_detail.to_csv(self.path_pescas_tallas_detail, index=False)
                else:
                    escribir_log('info',"No hay datos previos de simulacion")
                    #pescas_tallas_detail['FechaFin']=pescas_tallas_detail['FechaFin'].apply(lambda x: pd.to_datetime(datetime.datetime.strptime(str(x), "%Y-%m-%d")).date())
                    pescas_tallas_detail.to_csv(self.path_pescas_tallas_detail, index=False)

            else:
                if loop == 1:
                    #pescas_tallas_detail['FechaFin']=pescas_tallas_detail['FechaFin'].apply(lambda x: pd.to_datetime(datetime.datetime.strptime(str(x), "%Y-%m-%d")).date())
                    #pescas_tallas_detail['FechaFin']=pd.to_datetime(datetime.datetime.strptime(str(pescas_tallas_detail['FechaFin']), "%Y-%m-%d")).date()
                    pescas_tallas_detail.to_csv(self.path_pescas_tallas_detail, index=False)
                else:
                    #Tengo que incluir estas dos líneas porque si no han puesto ventas nunca se crea el fichero de pescas detail
                    if not os.path.exists(self.path_pescas_tallas_detail):
                        pescas_tallas_detail.to_csv(self.path_pescas_tallas_detail, index=False)
                    old_pescas_tallas_detail = pd.read_csv(self.path_pescas_tallas_detail)

                    pescas_tallas_detail = pd.concat([old_pescas_tallas_detail if not old_pescas_tallas_detail.empty else None,pescas_tallas_detail if not pescas_tallas_detail.empty else None], ignore_index=True)
                    #pescas_tallas_detail=pescas_tallas_detail.drop_duplicates(ignore_index=True)
                    #pescas_tallas_detail['FechaFin']=pescas_tallas_detail['FechaFin'].apply(lambda x: pd.to_datetime(datetime.datetime.strptime(str(x), "%Y-%m-%d")).date())
                    pescas_tallas_detail.to_csv(self.path_pescas_tallas_detail, index=False)

            resultado_df['BiomasaSinPescas'] = np.where(resultado_df['NumSinPescas'] == 0, 0, resultado_df['BiomasaSinPescas'])
            resultado_df['PesoMedioSinPescas'] = np.where(resultado_df['NumSinPescas'] == 0, 0, resultado_df['BiomasaSinPescas'] / resultado_df['NumSinPescas'] * 1000)

            resultado_df = resultado_df[initial_names]
            return resultado_df
        except Exception as e:
             escribir_log('critical', 'set_ventas ' +"Error {0}".format(str(e)))

    
    def set_bajas(self,resultado_df, all_ajustes_mort_gen_df, all_reparto_mort_df, culling_edad, culling_por, all_mortalidad_df):
        try:
            np.random.seed(7777)
            disp_coef = 0.11 # Para el culling solo
            initial_names = resultado_df.columns.tolist()
            fecha_fin = pd.to_datetime(resultado_df['FechaFin'].unique())[0].date()
            mes_loop = fecha_fin.month
            ano_loop = fecha_fin.year
            resultado_df['Index'] = range(resultado_df.shape[0])
            

            # M+S
            if all_mortalidad_df is not None:
                mort_mes = all_mortalidad_df.loc[(all_mortalidad_df['Ano'] == ano_loop) & (all_mortalidad_df['Mes'] == mes_loop) & (all_mortalidad_df['Num'] > 0)].copy()
                if not mort_mes.empty:
                    resultado_df['Rango'] = RangoPesoFunc_custom(pesos=resultado_df['PesoMedioSinPescas'])
                    num_por_rango = resultado_df.groupby(['Granja', 'Rango']).agg(Num_granja= ('NumSinPescas','sum')).reset_index() #quitado drop true

                    donde_y_cuanto = num_por_rango.merge(all_reparto_mort_df, on=['Granja', 'Rango'], how='left')
                    donde_y_cuanto = donde_y_cuanto.merge(mort_mes[['Granja', 'Num']], on='Granja', how='left')
                    donde_y_cuanto['Num_a_restar'] = round(donde_y_cuanto['Por'] * donde_y_cuanto['Num'])
                    donde_y_cuanto['Num_a_restar'] = np.where(donde_y_cuanto['Num_a_restar'].gt(donde_y_cuanto['Num_granja']), 
                                                            donde_y_cuanto['Num_granja'], donde_y_cuanto['Num_a_restar'])
                    donde_y_cuanto['Por_new'] = donde_y_cuanto['Num_a_restar'] / donde_y_cuanto['Num']
                    
                    donde_y_cuanto = donde_y_cuanto.dropna(subset=['Por_new'])


                    
                    # Desvio el porcentaje de los rangos que no existen a las otros rangos
                    total_por_recalc = donde_y_cuanto.groupby('Granja').agg(total_por_recalc=('Por_new','sum')).reset_index() #quitado drop true
                    donde_y_cuanto = donde_y_cuanto.merge(total_por_recalc, on='Granja')
                    donde_y_cuanto['Por_recalc'] = donde_y_cuanto['Por_new'] / donde_y_cuanto['total_por_recalc']
                    #Incluyo esta parte porque en lenguado se ha dado el caso de que Num_a_restar, Por_new y total_por_recalc son 0 => Por_recalc es NaN
                    donde_y_cuanto['Por_recalc']=donde_y_cuanto['Por_recalc'].fillna(0)
                    donde_y_cuanto['Num_a_restar_final'] = round(donde_y_cuanto['Por_recalc'] * donde_y_cuanto['Num']).astype(np.int32)
                    
                    donde_y_cuanto = donde_y_cuanto[['Granja', 'Rango', 'Num_a_restar_final']].copy()
                    donde_y_cuanto=donde_y_cuanto.loc[donde_y_cuanto['Num_a_restar_final']>0].copy()
                    donde_y_cuanto=donde_y_cuanto.reset_index(drop=True) #Hay que hacerlo para recorrer el indice, quite drop true
                    # Resto M+S
                    for i in range(donde_y_cuanto.shape[0]):
                        i_granja = donde_y_cuanto.loc[i,'Granja']
                        i_arestar = donde_y_cuanto.loc[i,'Num_a_restar_final']
                        i_rango = donde_y_cuanto.loc[i,'Rango']
                        
                        if i_arestar > 0:
                            i_data = resultado_df.loc[(resultado_df['Granja'] == i_granja) & (resultado_df['Rango'] == i_rango)]
                            while i_arestar >0: 
                                if i_data.shape[0] == 1:
                                    indexEsp = i_data['Index'].values.item(0)
                                else:
                                    indexEsp = np.random.choice(i_data['Index'].values,size=1).item(0)
                                iter_num_bajas_random = 1
                                
                                if iter_num_bajas_random <= resultado_df.loc[indexEsp,'NumSinPescas']:
                                    resultado_df.loc[indexEsp, 'NumBajas'] =resultado_df.loc[indexEsp, 'NumBajas'] +iter_num_bajas_random
                                    #Compruebo si indexExp tiene longitud 
                                    
                                    if hasattr(indexEsp, '__len__'):
                                        i_arestar =i_arestar- (iter_num_bajas_random * len(indexEsp))
                                    else:
                                        i_arestar =i_arestar- iter_num_bajas_random 
                            
            resultado_df['BiomasaBajas'] = resultado_df['NumBajas'] * resultado_df['PesoMedioSinPescas'] / 1000
            resultado_df['NumSinBajas'] = resultado_df['NumSinPescas'] - resultado_df['NumBajas']
            resultado_df['BiomasaSinBajas'] = resultado_df['BiomasaSinPescas'] - resultado_df['BiomasaBajas']
            resultado_df['PesoMedioSinBajas'] = resultado_df['PesoMedioSinPescas']
            resultado_df['BiomasaBajas_cull']=resultado_df['BiomasaBajas_cull'].astype(float)
            
            resultado_df['NumBajas_cull']=resultado_df['NumBajas_cull'].astype(np.int32)
            # Resto el culling
            for iter_granja in resultado_df['Granja'].unique():
                iter_arestar_culling = resultado_df.loc[(resultado_df['Edad'].between(culling_edad, culling_edad + 31)) & 
                                                        (resultado_df['Granja'] == iter_granja) & 
                                                        (resultado_df['Cull'] == False), 'NumSinBajas'].sum() * (culling_por/100)
                iter_arestar_culling = round(iter_arestar_culling)
                iter_data = resultado_df.loc[(resultado_df['Granja'] == iter_granja) & 
                                            (resultado_df['Edad'].between(culling_edad, culling_edad + 31)) & 
                                            (resultado_df['Cull'] == False)].sort_values('PesoMedio')
                
                if iter_arestar_culling > 0:
                    # Genero una df con todos los tanques dispersos de ese lote
                    iter_data=iter_data.reset_index(drop=True) #Hay que hacerlo así para acceder a las filas como si fuese el índice. Quitado drop true
                    for i in iter_data.index:
                        iter_num = iter_data.loc[i,'NumSinBajas']
                        iter_pesoMedio = iter_data.loc[i,'PesoMedioSinBajas']
                        iter_index = iter_data.loc[i,'Index']
                        pesos = rnorm2(mean=iter_pesoMedio, sd=(iter_pesoMedio * disp_coef), n=iter_num)
                        
                        if hasattr(pesos, '__len__'):
                            Index = np.repeat(iter_index, len(pesos))
                        else:
                            Index= np.repeat(iter_index, 1)
                        iter_df = pd.DataFrame({'pesos': pesos, 'Index': Index})
                        if i == 0:
                            cull_df = iter_df
                        else:
                            cull_df = pd.concat([cull_df if not cull_df.empty else None,iter_df if not iter_df.empty else None], ignore_index=True)
                            cull_df=cull_df.drop_duplicates(ignore_index=True)
                    
                    cull_df = cull_df.sort_values('pesos')
                    cull_df = cull_df.head(iter_arestar_culling)
                    cull_df['Num'] = 1
                    cull_df = cull_df.groupby('Index').agg(Num_cull=('Num', 'sum'), Bio_cull= ('pesos', 'sum')).reset_index()
            
                    cull_df['Bio_cull']=cull_df['Bio_cull']/1000
                    cull_df=cull_df.reset_index(drop=True) #Hay que hacerlo así para recorrer el DF por el número de fila
                    for i in range(cull_df.shape[0]):
                        iter_index_index = cull_df.loc[i,'Index']
                        iter_Bio_cull = cull_df.loc[i,'Bio_cull']
                        if hasattr(iter_Bio_cull, '__len__'):
                            iter_Bio_cull = float(iter_Bio_cull[0])
                                    
                        iter_Num_cull = cull_df.loc[i,'Num_cull']
                        resultado_df.loc[resultado_df['Index'] == iter_index_index, 'BiomasaBajas_cull'] = iter_Bio_cull
                        resultado_df.loc[resultado_df['Index'] == iter_index_index, 'NumBajas_cull'] = iter_Num_cull
                    
                    resultado_df.loc[resultado_df['Index'].isin(iter_data['Index']), 'Cull'] = True
            
            resultado_df['BiomasaBajas'] =resultado_df['BiomasaBajas']+ resultado_df['BiomasaBajas_cull']
            resultado_df['NumBajas'] =resultado_df['NumBajas']+ resultado_df['NumBajas_cull']
            resultado_df['NumSinBajas'] = resultado_df['NumSinPescas'] - resultado_df['NumBajas']
            resultado_df['BiomasaSinBajas'] = resultado_df['BiomasaSinPescas'] - resultado_df['BiomasaBajas']
            resultado_df['PesoMedioSinBajas'] = np.where(resultado_df['NumSinBajas'] == 0, 0, resultado_df['BiomasaSinBajas'] / resultado_df['NumSinBajas'] * 1000)
            # Ajuste por generacion
            if all_ajustes_mort_gen_df is not None:
                if not all_ajustes_mort_gen_df.empty:
                    ajuste_mort_gen_del_mes = all_ajustes_mort_gen_df.loc[(all_ajustes_mort_gen_df['Ano'] == ano_loop) & 
                                                                        (all_ajustes_mort_gen_df['Mes'] == mes_loop)]
                    ajuste_mort_gen_del_mes.columns = ajuste_mort_gen_del_mes.columns.str.replace('Ajuste', 'Ajuste_bajas')
                    
                    if ajuste_mort_gen_del_mes.shape[0] > 0:
                        # Este ajuste que no es por culling se suma a lo que ya hay en M+S
                        ajuste_mort_gen_del_mes_no_cull = ajuste_mort_gen_del_mes.loc[ajuste_mort_gen_del_mes['Por_Cull'] == False].groupby(['Granja', 'Gen']).agg({'Ajuste_bajas': 'sum'}).reset_index()
                        if ajuste_mort_gen_del_mes_no_cull.shape[0] > 0:
                            for i in range(ajuste_mort_gen_del_mes_no_cull.shape[0]):
                                i_granja = ajuste_mort_gen_del_mes_no_cull.loc[i,'Granja']
                                i_gen = ajuste_mort_gen_del_mes_no_cull.loc[i,'Gen']
                                i_ajuste_bajas = ajuste_mort_gen_del_mes_no_cull.loc[i,'Ajuste_bajas']
                                np.random.seed(7777)
                                to_sample = resultado_df.loc[(resultado_df['Granja'] == i_granja) & (resultado_df['Gen'] == i_gen), 'Index'].values
                                
                                if len(to_sample) > 0:
                                    if len(to_sample) == 1:
                                        indexEsp = np.repeat(to_sample, i_ajuste_bajas)
                                    else:
                                        #Como a  veces es negativo lo pongo como valor absoluto
                                        indexEsp = np.random.choice(to_sample, size=abs(i_ajuste_bajas), replace=True).item(0)
                                        
                                    indexEsp_df = pd.DataFrame({'Index': [indexEsp], 'Ajuste_bajas': [1]}).groupby('Index').agg({'Ajuste_bajas': 'sum'}).reset_index()
                                    resultado_df = resultado_df.merge(indexEsp_df, on='Index', how='left')
                                    resultado_df['Ajuste_bajas'] = resultado_df['Ajuste_bajas'].fillna(0)
                                    resultado_df['NumBajas'] = resultado_df['NumBajas']+resultado_df['Ajuste_bajas']
                                    resultado_df['BiomasaBajas'] = resultado_df['BiomasaBajas'] +(resultado_df['Ajuste_bajas'] * resultado_df['PesoMedioSinBajas'] / 1000)
                                    resultado_df = resultado_df.drop(columns=['Ajuste_bajas'])
                        
                        # Este ajuste solo se aplica si es un culling mayor al estandar
                        ajuste_mort_gen_del_mes_cull = ajuste_mort_gen_del_mes.loc[ajuste_mort_gen_del_mes['Por_Cull'] == True].groupby(['Granja', 'Gen']).agg(num_cul=('Ajuste_bajas', 'mean')).reset_index()
                        if len(ajuste_mort_gen_del_mes_cull) > 0:
                            ajuste_mort_gen_del_mes_cull=ajuste_mort_gen_del_mes_cull.reset_index() #Hay que hacerlo así para recorrer el df por número de fila. Quitado drop true
                            for i in range(ajuste_mort_gen_del_mes_cull.shape[0]):
                                iter_granja = ajuste_mort_gen_del_mes_cull.loc[i,'Granja']
                                iter_gen = ajuste_mort_gen_del_mes_cull.loc[i,'Gen']
                                iter_arestar_culling = ajuste_mort_gen_del_mes_cull.loc[i,'num_cul']
                                iter_data = resultado_df.loc[(resultado_df['Granja'] == iter_granja) & (resultado_df['Gen'] == iter_gen)]
                                por_matar = iter_arestar_culling - iter_data['NumBajas_cull'].sum()
                                if por_matar > 0:
                                    iter_data=iter_data.reset_index(drop=True) #Hay que hacerlo así para recorrer el df por número de fila Quitado drop true
                                    for i in range(iter_data.shape[0]):
                                        iter_num = iter_data.loc[i,'Num']
                                        iter_pesoMedio = iter_data.loc[i,'PesoMedio']
                                        iter_index = iter_data.loc[i,'Index']
                                        pesos = rnorm2(mean=iter_pesoMedio, sd=(iter_pesoMedio * disp_coef), n=iter_num)
                                        Index = np.repeat(iter_index, len(pesos))
                                        iter_df = pd.DataFrame({'pesos': pesos, 'Index': Index})
                                        
                                        if i == 0:
                                            cull_df = iter_df
                                        else:
                                            cull_df = pd.concat([cull_df if not cull_df.empty else None,iter_df if not iter_df.empty else None], ignore_index=True)
                                            cull_df=cull_df.drop_duplicates(ignore_index=True)
                                    cull_df = cull_df.sort_values('pesos')
                                    cull_df = cull_df.head(int(por_matar))
                                    cull_df['Num'] = 1
                                    cull_df = cull_df.groupby('Index').agg(Num_cull=('Num', 'sum'), Bio_cull=('pesos', 'sum')).reset_index() #quitado drop true
                                    cull_df['Bio_cull']=cull_df['Bio_cull']/1000
                                    cull_df=cull_df.reset_index(drop=True)  #Hay que hacerlo así para recorrer el df por número de fila
                                    for i in range(cull_df.shape[0]):
                                        iter_index_index = cull_df.loc[i,'Index']
                                        iter_Bio_cull = cull_df.loc[i,'Bio_cull']
                                        iter_Num_cull = cull_df.loc[i,'Num_cull']
                                        resultado_df.loc[resultado_df['Index'] == iter_index_index, 'BiomasaBajas_cull'] = resultado_df.loc[resultado_df['Index'] == iter_index_index, 'BiomasaBajas_cull']+iter_Bio_cull
                                        resultado_df.loc[resultado_df['Index'] == iter_index_index, 'NumBajas_cull'] = resultado_df.loc[resultado_df['Index'] == iter_index_index, 'NumBajas_cull']+iter_Num_cull
                                        resultado_df.loc[resultado_df['Index'] == iter_index_index, 'BiomasaBajas'] = resultado_df.loc[resultado_df['Index'] == iter_index_index, 'BiomasaBajas']+iter_Bio_cull
                                        resultado_df.loc[resultado_df['Index'] == iter_index_index, 'NumBajas'] =resultado_df.loc[resultado_df['Index'] == iter_index_index, 'NumBajas']  +iter_Num_cull
            
            # Para que no haya mas muertos que peces
            resultado_df['BiomasaBajas'] = np.where(resultado_df['BiomasaBajas'].gt(resultado_df['BiomasaSinPescas']), 
                                                    resultado_df['BiomasaSinPescas'], resultado_df['BiomasaBajas'])
            resultado_df['NumBajas'] = np.where(resultado_df['NumBajas'].gt(resultado_df['NumSinPescas']), 
                                                resultado_df['NumSinPescas'], resultado_df['NumBajas'])
            
            resultado_df['NumSinBajas'] = resultado_df['NumSinPescas'] - resultado_df['NumBajas']
            resultado_df['BiomasaSinBajas'] = resultado_df['BiomasaSinPescas'] - resultado_df['BiomasaBajas']
            resultado_df['PesoMedioSinBajas'] = np.where(resultado_df['NumSinBajas'] == 0, 0, 
                                                        resultado_df['BiomasaSinBajas'] / resultado_df['NumSinBajas'] * 1000)
            
            resultado_df = resultado_df[initial_names].copy()
            
            return resultado_df
        except Exception as e:
             escribir_log('critical', 'set_bajas ' +"Error {0}".format(str(e)))

    
    def set_crecimiento(self,resultado_df, curvas_df, all_crecimientoD_df, all_ajustes_edad_df,
                        all_ajustes_talla_df, all_ajustes_gen_df, d_growth_type):
        try:
            initial_names = resultado_df.columns.tolist()
            fecha_fin = pd.to_datetime(resultado_df['FechaFin'].unique())[0].date()
            mes_loop = fecha_fin.month
            ano_loop = fecha_fin.year
            resultado_df=resultado_df.drop(columns=['Tasa']).copy()
            resultado_df = resultado_df.merge(curvas_df.loc[curvas_df['Mes'] == mes_loop].drop(columns='Mes'), 
                                    on=['Granja', 'Edad'], how='left')
            
            resultado_df['Tasa'] = resultado_df['Tasa'] * (resultado_df['DiasMes'] - 2)
            
            if resultado_df['Tasa'].isna().count() > 0:
                escribir_log('info', "Hay edades muy altas sin tasa, aplico una tasa de 0.001")
                resultado_df.loc[resultado_df['Tasa'].isna(), 'Tasa'] = 0.001
            
            
            #### Austes varios por edad, talla y gen ####
            # Edad
            if all_ajustes_edad_df is not None:
                ajuste_edad_del_mes = all_ajustes_edad_df.loc[(all_ajustes_edad_df['Ano'] == ano_loop) & 
                                                            (all_ajustes_edad_df['Mes'] == mes_loop)]
                # Puede haber ajustes que coincidan en edad, talla o gen para el mismo mes asi que hago ddply y calculo el ajuste medio
                if ajuste_edad_del_mes.shape[0] > 0:
                    #ajuste_edad_del_mes = ajuste_edad_del_mes.groupby(['Granja', 'Edad']).agg({'Ajuste': 'mean'}).reset_index()
                    ajuste_edad_del_mes = ajuste_edad_del_mes.groupby(['Granja', 'Edad'], as_index=False)['Ajuste'].mean()
                    resultado_df = resultado_df.merge( ajuste_edad_del_mes, on=['Granja', 'Edad'], how='left')
                    resultado_df['Ajuste'] = resultado_df['Ajuste'].fillna(0)
                    resultado_df['Tasa'] = resultado_df['Tasa'] + ((resultado_df['Ajuste'] / 100) * resultado_df['Tasa'])
                    resultado_df = resultado_df.drop(columns=['Ajuste'])
            
            # Talla
            if all_ajustes_talla_df is not None:
                if not all_ajustes_talla_df.empty:
                    ajuste_talla_del_mes = all_ajustes_talla_df.loc[(all_ajustes_talla_df['Ano'] == ano_loop) & 
                                                                    (all_ajustes_talla_df['Mes'] == mes_loop)]
                    # Puede haber ajustes que coincidan en edad, talla o gen para el mismo mes asi que hago ddply y calculo el ajuste medio
                    if ajuste_talla_del_mes.shape[0] > 0:
                        #ajuste_talla_del_mes = ajuste_talla_del_mes.groupby(['Granja', 'Talla']).agg({'Ajuste': 'mean'}).reset_index()
                        ajuste_talla_del_mes = ajuste_talla_del_mes.groupby(['Granja', 'Talla'], as_index=False)['Ajuste'].mean()
                        resultado_df = resultado_df.merge( ajuste_talla_del_mes, on=['Granja', 'Talla'], how='left')
                        resultado_df['Ajuste'] = resultado_df['Ajuste'].fillna(0)
                        resultado_df['Tasa'] = resultado_df['Tasa'] + ((resultado_df['Ajuste'] / 100) * resultado_df['Tasa'])
                        resultado_df = resultado_df.drop(columns=['Ajuste'])
            
            
            # Gen
            if all_ajustes_gen_df is not None:
                
                if not all_ajustes_gen_df.empty:
                    ajuste_gen_del_mes = all_ajustes_gen_df.loc[(all_ajustes_gen_df['Ano'] == ano_loop) & 
                                                                (all_ajustes_gen_df['Mes'] == mes_loop)]
                    # Puede haber ajustes que coincidan en edad, talla o gen para el mismo mes asi que hago ddply y calculo el ajuste medio
                    if ajuste_gen_del_mes.shape[0] > 0:
                        
                        #ajuste_gen_del_mes = ajuste_gen_del_mes.groupby(['Granja', 'Gen']).agg({'Ajuste': 'mean'}).reset_index()
                        ajuste_gen_del_mes = ajuste_gen_del_mes.groupby(['Granja', 'Gen'], as_index=False)['Ajuste'].mean()
                        resultado_df = resultado_df.merge(ajuste_gen_del_mes, on=['Granja', 'Gen'], how='left')
                        resultado_df['Ajuste'] = resultado_df['Ajuste'].fillna(0)
                        resultado_df['Tasa'] = resultado_df['Tasa'] + ((resultado_df['Ajuste'] / 100) * resultado_df['Tasa'])
                        resultado_df = resultado_df.drop(columns=['Ajuste'])
            
            #######  Ajuste de curva para crecimiento deseado ######
            
            crecimientoDes_del_mes = all_crecimientoD_df.loc[(all_crecimientoD_df['Mes'] == mes_loop) & 
                                                            (all_crecimientoD_df['Ano'] == ano_loop) & 
                                                            (all_crecimientoD_df['Tones'] > 0)]
            if crecimientoDes_del_mes.shape[0] > 0:
                #Esto HAY QUE REVISARLO
                if d_growth_type:
                    tot_bio = resultado_df.loc[resultado_df['Input'] == False].groupby(['Granja'],as_index=False).agg(init_tones=('Biomasa', 'sum')) 
                    tot_bio['init_tones']=tot_bio['init_tones']/1000
                    crecimientoDes_del_mes = crecimientoDes_del_mes.merge(tot_bio, on='Granja', how='left')
                    
                    crecimientoDes_del_mes['Tones'] = crecimientoDes_del_mes['Tones'] / 100 * crecimientoDes_del_mes['init_tones']
                    crecimientoDes_del_mes = crecimientoDes_del_mes.drop(columns=['init_tones'])
                #else:
                biomasa_alevines = resultado_df.loc[resultado_df['Input'] == True].groupby(['Granja'], as_index=False).agg(Biomasa_alev=('Biomasa', 'sum'))
                biomasa_alevines['Biomasa_alev']=biomasa_alevines['Biomasa_alev']/1000
                
                crecimientoDes_del_mes = crecimientoDes_del_mes.merge(biomasa_alevines, on='Granja', how='left')
                crecimientoDes_del_mes['Biomasa_alev'] = crecimientoDes_del_mes['Biomasa_alev'].fillna(0)
                crecimientoDes_del_mes['Tones'] = crecimientoDes_del_mes['Tones'] - crecimientoDes_del_mes['Biomasa_alev']
                crecimientoDes_del_mes = crecimientoDes_del_mes.drop(columns=['Biomasa_alev'])
        
                ajuste_DF = pd.DataFrame({'Granja': crecimientoDes_del_mes['Granja'].unique(), 'Ajuste': np.repeat(1.0, crecimientoDes_del_mes['Granja'].unique().shape[0])})
            
                #posibles_ajustes = np.arange(0.65, 1.20, 0.000005) #Esta variable no se utiliza
                if crecimientoDes_del_mes.shape[0] > 0:
                    for granja in crecimientoDes_del_mes['Granja'].unique():
                        yield_quiero = crecimientoDes_del_mes.loc[crecimientoDes_del_mes['Granja'] == granja, 'Tones'] * 1000
                        diff_prev = 10000
                        posible_ajuste = 1#diff_prev/10
                        ronda = 1
                        cambio_de_ronda = np.arange(50, 1000000, 100)
                        increm_decrem = 0.1 #posible_ajuste/5
                        maxima_diff_permitida = 100
                        while abs(diff_prev) > maxima_diff_permitida and ronda< 2000:  #Añadido lo de ronda<2000 para evitar que se quede en bucle infinito
                            iter_data = resultado_df.loc[resultado_df['Granja'] == granja, ['Tasa', 'PesoMedioSinBajas', 'NumSinBajas', 'BiomasaPescas', 'Biomasa']]
                            
                            iter_data['Tasa'] = iter_data['Tasa'] * posible_ajuste
                            iter_data['PesoMedioFinal'] = np.where(iter_data['PesoMedioSinBajas'] == 0, 0, 
                                                                (iter_data['PesoMedioSinBajas'] * iter_data['Tasa']) + iter_data['PesoMedioSinBajas'])
                            iter_data['BiomasaFinal'] = (iter_data['PesoMedioFinal'] * iter_data['NumSinBajas']) / 1000
                        
                            iter_yield = (iter_data['BiomasaFinal'].sum() - iter_data['Biomasa'].sum() + iter_data['BiomasaPescas'].sum())

                            diff_prev = yield_quiero.iloc[0] - iter_yield
                            if abs(diff_prev) > maxima_diff_permitida:
                                if diff_prev > 0:
                                    posible_ajuste = posible_ajuste+ increm_decrem
                                else:
                                    posible_ajuste = posible_ajuste-increm_decrem
                            else:
                                #En esta línea en R esta ajuste_DF[ajuste_DF$Granja == granja, "Ajuste"] <- i <- posible_ajuste¿¿¿¿????
                                ajuste_DF.loc[ajuste_DF['Granja'] == granja, 'Ajuste'] = posible_ajuste
                            if ronda in cambio_de_ronda:
                                increm_decrem = increm_decrem/10
                            ronda =ronda+ 1
                
                # Multiplico la tasa por el mejor ajuste
                for granja in ajuste_DF['Granja'].unique():
                    resultado_df.loc[resultado_df['Granja'] == granja, 'Tasa'] *= ajuste_DF.loc[ajuste_DF['Granja'] == granja, 'Ajuste'].values
                
            resultado_df['PesoMedioFinal'] = np.where(resultado_df['PesoMedioSinBajas'] == 0, 0, 
                                                    (resultado_df['PesoMedioSinBajas'] * resultado_df['Tasa']) + resultado_df['PesoMedioSinBajas'])
            resultado_df['BiomasaFinal'] = (resultado_df['PesoMedioFinal'] * resultado_df['NumSinBajas']) / 1000
            resultado_df['NumFinal'] = resultado_df['NumSinBajas']
            resultado_df['TallaFinal'] = resultado_df['PesoMedioFinal'].apply(lambda x: RangoPeso_directo_letra(x, self.especie))
            resultado_df['TallaFinal'] = np.where(resultado_df['NumFinal'] == 0, resultado_df['Talla'], resultado_df['TallaFinal'])
            
            resultado_df = resultado_df[initial_names]
            
            return resultado_df
        except Exception as e:
             escribir_log('critical', 'set_crecimiento ' +"Error {0}".format(str(e)))

    
    def set_next_and_write(self,continue_flag, loop, resultado_df):
        try:
        
            # Falta masterDF_stock_disperso. Necesitara la tabla de dispersion para calcularse.
            # masterDF
            if continue_flag:
                if os.path.exists(self.path_masterDF):
                    old_masterDF = pd.read_csv(self.path_masterDF)
                    masterDF = pd.concat([old_masterDF if not old_masterDF.empty else None,resultado_df if not resultado_df.empty else None], ignore_index=True)
                    #masterDF=masterDF.drop_duplicates(ignore_index=True)
                    masterDF.to_csv(self.path_masterDF, index=False)
                else:
                    escribir_log('info',"No hay datos previos de simulacion")
                    resultado_df.to_csv(self.path_masterDF, index=False)
            else:
                if loop == 1:
                    resultado_df.to_csv(self.path_masterDF, index=False)
                else:
                    old_masterDF = pd.read_csv(self.path_masterDF)
                    masterDF = pd.concat([old_masterDF if not old_masterDF.empty else None,resultado_df if not resultado_df.empty else None], ignore_index=True)
                    #masterDF=masterDF.drop_duplicates(ignore_index=True)
                    masterDF.to_csv(self.path_masterDF, index=False)
            
            
            fecha_fin = pd.to_datetime(resultado_df['FechaFin'].unique())[0].date()
            fecha_fin = datetime.datetime.strptime(str(fecha_fin), "%Y-%m-%d").date().replace(day=1)  #se pone a día 1 todas las fechas_fin
            fecha_fin = pd.to_datetime(datetime.datetime.strptime(fechas_stolt_func_new(add_months(fecha_fin, 1)), "%Y-%m-%d").date()).date()

            next_resultado_df = resultado_df.loc[resultado_df['NumFinal'] > 0].copy()
            next_resultado_df=next_resultado_df.assign(Edad=next_resultado_df['EdadFinal'])
            next_resultado_df=next_resultado_df.assign(PesoMedio=next_resultado_df['PesoMedioFinal'])
            next_resultado_df=next_resultado_df.assign(Num=next_resultado_df['NumFinal'])
            next_resultado_df=next_resultado_df.assign(Fecha=next_resultado_df['FechaFin'])
            next_resultado_df=next_resultado_df.assign(Biomasa=next_resultado_df['BiomasaFinal'])
            next_resultado_df['BiomasaBajas'] = 0.0
            next_resultado_df['NumBajas'] = 0
            next_resultado_df['NumBajas_cull'] = 0
            next_resultado_df['BiomasaBajas_cull'] = 0.0
            next_resultado_df['NumSinBajas'] = 0
            next_resultado_df['BiomasaSinBajas'] = 0.0
            next_resultado_df['FechaFin'] = fecha_fin


            #########Solo para pruebas
            #next_resultado_df['Fecha']=next_resultado_df['Fecha'].apply(lambda x: pd.to_datetime(x).date())
            ############################

            next_resultado_df['DiasMes'] = (next_resultado_df['FechaFin'] - next_resultado_df['Fecha']).apply (lambda x: x.days)
            next_resultado_df['PesoMedioSinBajas'] = 0.0
            next_resultado_df=next_resultado_df.assign(Talla=next_resultado_df['TallaFinal'])
            next_resultado_df['BiomasaPescas'] = 0.0
            next_resultado_df['BiomasaSinPescas'] = 0.0
            next_resultado_df['NumPescas'] = 0
            next_resultado_df['NumSinPescas'] = 0
            next_resultado_df['PesoMedioFinal'] = 0
            next_resultado_df['PesoMedioSinPescas'] = 0.0
            next_resultado_df['Tasa'] = 0.0
            next_resultado_df['BiomasaFinal'] = 0.0
            next_resultado_df['NumFinal'] = 0
            next_resultado_df['EdadFinal'] = next_resultado_df['Edad'] + next_resultado_df['DiasMes']
            next_resultado_df['TallaFinal'] = " "
            next_resultado_df['Input'] = False

            return next_resultado_df
        except Exception as e:
             escribir_log('critical', 'set_next_and_write ' +"Error {0}".format(str(e)))


    
    def set_resultado(self):
        try:
            if not os.path.exists(self.path_masterDF):
                return None
            
            data = pd.read_csv(self.path_masterDF)
            data['Year'] = data['FechaFin'].apply(lambda x: pd.to_datetime(x).date().year)
            data['Mes'] = data['FechaFin'].apply(lambda x: pd.to_datetime(x).date().month)
            data['YearClass'] = data['YearClass'].astype(str) #Hay que convertir el tipo para poder hacer los merge
            data['Gen'] = data['Gen'].astype(str)

            if os.path.exists(self.path_pescas_tallas_detail):
                data_sales = pd.read_csv(self.path_pescas_tallas_detail)

                data_sales['Year'] =data_sales['FechaFin'].apply(lambda x: pd.to_datetime(x).date().year)
                data_sales['Mes'] = data_sales['FechaFin'].apply(lambda x: pd.to_datetime(x).date().month)
        
            ##################Plantilla####################
            plantilla = pd.DataFrame(columns=['DATA', 'TYPE'])
            plantilla.loc[len(plantilla),:] = ['final', 'number,avweight,biomass']
            plantilla.loc[len(plantilla),:] = ['growth', 'biomass,%']
            plantilla.loc[len(plantilla),:] = ['inputs', 'number,avweight,biomass']
            plantilla.loc[len(plantilla),:] = ['harvests', 'number,avweight,biomass']
            plantilla.loc[len(plantilla),:] = ['losses', 'number,avweight,biomass']
            plantilla.loc[len(plantilla),:] = ['sales', 'biomass']
            plantilla.loc[len(plantilla),:] = ['biomass end of month', 'biomass']
            plantilla.loc[len(plantilla),:] = ['initial', 'number,avweight,biomass']
            plantilla.loc[len(plantilla),:] = ['culling', 'number,avweight,biomass']
            
            plantilla['TYPE'] = plantilla['TYPE'].apply(lambda x: x.split(','))  
            plantilla=plantilla.explode('TYPE').reset_index(drop=True)  #A lo mejor hay que quitar el drop true:MIRAR

            

            #### Importar y crear plantilla de resultados ####
            campos_plantilla = plantilla.loc[~plantilla['DATA'].isin(['biomass end of month', 'sales'])]
            campos_plantilla_rangos = plantilla.loc[plantilla['DATA'].isin(['biomass end of month', 'sales'])]
            
            tallas = [RangoPeso_directo_letra(x, self.especie) for x in range(1, 10001, 50)]
            tallas = np.unique(tallas)

            generaciones = np.unique(data['Gen'])
            farms = data['Granja'].unique()
            dates = data['FechaFin'].unique()

            resultado = campos_plantilla.copy()
            resultado['FARM'] = ','.join(farms)
            resultado['Gen'] = ','.join(generaciones)
            resultado['Date'] = ','.join(dates)
            resultado = resultado.assign(FARM=resultado['FARM'].str.split(',')).explode('FARM')
            resultado = resultado.assign(Gen=resultado['Gen'].str.split(',')).explode('Gen')
            resultado = resultado.assign(Date=resultado['Date'].str.split(',')).explode('Date')
            resultado['YearClass'] = '20' + resultado['Gen'].str[:2]
            resultado['YearClass'] =resultado['YearClass'].astype('str')
            resultado=resultado.reset_index(drop=True)
            
            resultado_tallas = campos_plantilla_rangos.copy()
            resultado_tallas['FARM'] = ','.join(farms)
            resultado_tallas['Gen'] = ','.join(tallas)
            resultado_tallas['Date'] = ','.join(dates)
            resultado_tallas = resultado_tallas.assign(FARM=resultado_tallas['FARM'].str.split(',')).explode('FARM')
            resultado_tallas = resultado_tallas.assign(Gen=resultado_tallas['Gen'].str.split(',')).explode('Gen')
            resultado_tallas = resultado_tallas.assign(Date=resultado_tallas['Date'].str.split(',')).explode('Date')
            resultado_tallas['YearClass'] = resultado_tallas['Gen']
            resultado_tallas=resultado_tallas.reset_index(drop=True)
            

            resultado = pd.concat([resultado if not resultado.empty else None,resultado_tallas if not resultado_tallas.empty else None], ignore_index=True)
            resultado=resultado.drop_duplicates(ignore_index=True)
            resultado['Mes'] = resultado['Date'].apply(lambda x: pd.to_datetime(x).date().month)
            resultado['Year'] = resultado['Date'].apply(lambda x: pd.to_datetime(x).date().year)
            resultado['Month'] = resultado['Date'].apply(lambda x: pd.to_datetime(x).date().strftime('%b-%Y'))

            resultado['valor'] = 0
            
            ###########Inputs#############
            inputs=data.copy()
            inputs = inputs.loc[inputs["Input"]==True]
            
            id_vars=["FARM","Year","Mes","YearClass","Gen"]
            if not inputs.empty:
                inputs = inputs.groupby(['Granja', 'Year', 'Mes', 'YearClass', 'Gen']).agg(number=('Num', 'sum'), biomass=('Biomasa', 'sum')).reset_index()
                
                inputs['avweight'] = (inputs['biomass'] / inputs['number']) * 1000
                inputs_restar_initial=inputs.copy()
                inputs=inputs.rename(columns={'Granja': 'FARM'})
                inputs = pd.melt(inputs, id_vars=id_vars, var_name='TYPE')#
                inputs['DATA'] = 'inputs'
                
            else:
                inputs = pd.DataFrame(columns=['FARM', 'Year', 'Mes', 'YearClass', 'Gen', 'TYPE', 'value', 'DATA'])
                inputs = inputs.astype({'FARM': str, 'Year': int,'Mes': int, 'YearClass': int, 'Gen':str, 'TYPE':str, 'value':float, 'DATA':str})
                inputs_restar_initial = pd.DataFrame(columns=['Granja', 'Year', 'Mes', 'YearClass', 'Gen', 'number', 'biomass', 'avweight'])
                inputs_restar_initial = inputs_restar_initial.astype({'Granja': str, 'Year': int,'Mes': int, 'YearClass': int, 'Gen':str, 'number':float, 'biomass':float, 'avweight':float})
            
            #inputs['YearClass'] = inputs['YearClass'].astype(str) #Hay que convertir el tipo para poder hacer el merge
            

            resultado = resultado.merge(inputs, on=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'DATA','Gen'], how='left')
            resultado['valor'] = np.where(resultado['value'].isna(), resultado['valor'], resultado['value'])
            resultado=resultado.drop(columns=['value'])
            

            ###########initial##########
            initial=data.copy()
            initial = initial.groupby(['Granja', 'Year', 'Mes', 'YearClass', 'Gen']).agg({'Num': 'sum', 'Biomasa': 'sum'}).reset_index()
            # Para quitar los alevines de los datos iniciales
            initial= initial.merge(inputs_restar_initial, on = ["Granja", "Year", "Mes", "YearClass", "Gen"], how='left')
            #Columnas en R
            #Granja Year Mes    YearClass  Gen     number.x     biomass.x   number.y   biomass.y  av.weight
            #Columnas en python
            # Granja  Year  Mes  YearClass   Gen      Num        Biomasa    number      biomass   avweight
            initial['number'] = np.where(initial['number'].isna(), initial['Num'], initial['Num'] - initial['number'])
            initial['number'] = initial['number'].astype(int)
            initial['biomass'] = np.where(initial['biomass'].isna(), initial['Biomasa'], initial['Biomasa'] - initial['biomass'])
            initial['avweight'] = np.where(initial['biomass'] == 0, 0, initial['biomass'] / initial['number'] * 1000)
            initial=initial.drop(columns=['Num','Biomasa'])
            
            #Columnas finales
            #FARM Year Mes    YearClass  Gen   avweight
            initial=initial.rename(columns={'Granja': 'FARM'})
            initial = pd.melt(initial, id_vars=id_vars)
            initial['DATA'] = 'initial'
            initial=initial.rename(columns={'variable': 'TYPE'})
            initial['YearClass'] = initial['YearClass'].astype(str) #Hay que convertir el tipo para poder hacer el merge

            resultado = resultado.merge(initial, on=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'DATA','Gen'], how='left')
            resultado['valor'] = np.where(resultado['value'].isna(), resultado['valor'], resultado['value'])
            resultado=resultado.drop(columns=['value'])
            resultado=resultado.reset_index(drop=True)
            resultado=resultado.drop_duplicates(ignore_index=True)


            ##########finals###########
            finals=data.copy()
            finals = finals.groupby(['Granja', 'Year', 'Mes', 'YearClass', 'Gen']).agg(number=('NumFinal', 'sum'), biomass= ('BiomasaFinal', 'sum'), avweight = ('BiomasaFinal', 'sum') ).reset_index()
            finals['avweight'] = finals['avweight']  / finals['number'] * 1000

            finals=finals.rename(columns={'Granja':'FARM'})
            finals = pd.melt(finals, id_vars=id_vars)
            finals=finals.rename(columns={'variable':'TYPE'})
            finals['DATA'] = 'final'
            finals['YearClass'] = finals['YearClass'].astype(str) #Hay que convertir el tipo para poder hacer el merge
            

            resultado = resultado.merge( finals, on=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'DATA','Gen'], how='left')
            resultado['valor'] = np.where(resultado['value'].isna(), resultado['valor'], resultado['value'])
            resultado=resultado.drop(columns=['value'])
            resultado=resultado.reset_index(drop=True)
            resultado=resultado.drop_duplicates(ignore_index=True)

            
            ##########harvest#################
            harvests=data.copy()
            harvests = harvests.groupby(['Granja', 'Year', 'Mes', 'YearClass', 'Gen']).agg(number=('NumPescas', 'sum'), biomass=('BiomasaPescas', 'sum'), avweight=('BiomasaPescas', 'sum')).reset_index()
            harvests['avweight'] = harvests['avweight'] / harvests['number'] * 1000
            harvests=harvests.rename(columns={'Granja':'FARM'})
            harvests = pd.melt(harvests, id_vars=id_vars)
            harvests['DATA'] = 'harvests'
            harvests=harvests.rename(columns={'variable':'TYPE'})
            harvests['YearClass']=harvests['YearClass'].astype(str) #Hay que convertir el tipo para poder hacer el merge
            
            resultado = resultado.merge( harvests, on=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'DATA','Gen'], how='left')
            resultado['valor'] = np.where(resultado['value'].isna(), resultado['valor'], resultado['value'])
            resultado=resultado.drop(columns=['value'])
            resultado=resultado.drop_duplicates(ignore_index=True)
            
            ################growth###############
            # Para que sumen los alevines al yield tiene que ser asi.
            initial_para_G = initial.loc[initial['TYPE'] == 'biomass'][['FARM', 'Year', 'Mes', 'YearClass', 'Gen', 'value']].copy()
            initial_para_G=initial_para_G.rename(columns={'value': 'initial_biomass'})
            
            final_para_G = finals.loc[finals['TYPE'] == 'biomass'][['FARM', 'Year', 'Mes', 'YearClass', 'Gen', 'value']].copy()
            final_para_G=final_para_G.rename(columns={'value': 'final_biomass'})
            
            harvests_para_G = harvests.loc[harvests['TYPE'] == 'biomass'][['FARM', 'Year', 'Mes', 'YearClass', 'Gen', 'value']].copy()
            harvests_para_G=harvests_para_G.rename(columns={'value': 'harvest_biomass'})
            
            growth = initial_para_G.merge( final_para_G, on=['FARM', 'Year', 'Mes', 'YearClass', 'Gen'], how='left')
            
            growth = growth.merge(harvests_para_G, on=['FARM', 'Year', 'Mes', 'YearClass', 'Gen'], how='left')
            
            growth['value'] = growth['final_biomass'] - growth['initial_biomass'] + growth['harvest_biomass']
            growth_por = growth.copy()
            growth_por['value'] = np.where(growth_por['initial_biomass'] == 0, 0, growth_por['value'] / growth_por['initial_biomass'] * 100)
            
            growth=growth.drop(columns=['initial_biomass', 'final_biomass', 'harvest_biomass'])
            growth['TYPE'] = 'biomass'
            growth['DATA'] = 'growth'
            
            growth_por=growth_por.drop(columns=['initial_biomass', 'final_biomass', 'harvest_biomass'])
            growth_por['TYPE'] = '%'
            growth_por['DATA'] = 'growth'

            growth_all = pd.concat([growth if not growth.empty else None,growth_por if not growth_por.empty else None], ignore_index=True)
            growth_all=growth_all.drop_duplicates(ignore_index=True)
            
            resultado = resultado.merge(growth_all, on=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'DATA','Gen'], how='left')
            resultado['valor'] = np.where(resultado['value'].isna(), resultado['valor'], resultado['value'])
            resultado=resultado.drop(columns=['value'])
            resultado=resultado.drop_duplicates(ignore_index=True)


            #######losses############
            losses=data.copy()
            losses = data.groupby(['Granja', 'Year', 'Mes', 'YearClass', 'Gen']).agg(number=('NumBajas', 'sum'), biomass=('BiomasaBajas', 'sum'), avweight=('BiomasaBajas', 'sum')).reset_index()
            losses['avweight'] = losses['avweight'] / losses['number'] * 1000
            losses=losses.rename(columns={'Granja':'FARM'})
            
            losses = pd.melt(losses, id_vars=id_vars)
            losses['DATA'] = 'losses'
            losses=losses.rename(columns={'variable':'TYPE'})
            losses['YearClass']=losses['YearClass'].astype(str) #Hay que convertir el tipo para poder hacer el merge
            
            resultado = resultado.merge(losses, on=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'DATA','Gen'], how='left')
            resultado['valor'] = np.where(resultado['value'].isna(), resultado['valor'], resultado['value'])
            resultado=resultado.drop(columns=['value'])
            resultado=resultado.drop_duplicates(ignore_index=True)

            ###########culling##########
            culling=data.copy()
            culling = data.groupby(['Granja', 'Year', 'Mes', 'YearClass', 'Gen']).agg(number=('NumBajas_cull', 'sum'), biomass=('BiomasaBajas_cull', 'sum'), avweight=('BiomasaBajas_cull', 'sum')).reset_index()
            culling['avweight'] = culling['avweight'] / culling['number'] * 1000
            culling=culling.rename(columns={'Granja':'FARM'})
            culling = pd.melt(culling, id_vars=id_vars)
            culling['DATA'] = 'culling'
            culling=culling.rename(columns={'variable':'TYPE'})
            culling['YearClass']=culling['YearClass'].astype(str) #Hay que convertir el tipo para poder hacer el merge
            
            resultado = resultado.merge(culling, on=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'DATA','Gen'], how='left')
            resultado['valor'] = np.where(resultado['value'].isna(), resultado['valor'], resultado['value'])
            resultado=resultado.drop(columns=['value'])
            resultado=resultado.drop_duplicates(ignore_index=True)

            
            
            ##########MS############ESTO NO VALE PARA NADA PORQUE NO HAY MS como DATA en resultado
            ms=data.copy()
            ms['DifNumbajas']=ms['NumBajas']-ms['NumBajas_cull']
            ms['DifBiomas']=ms['BiomasaBajas']-ms['BiomasaBajas_cull']
            ms = ms.groupby(['Granja', 'Year', 'Mes', 'YearClass', 'Gen']).agg(number=('DifNumbajas', 'sum'), biomass=('DifBiomas', 'sum'), avweight=('DifBiomas', 'sum')).reset_index()
            ms['avweight'] = ms['avweight'] / ms['number'] * 1000
            ms=ms.rename(columns={'Granja':'FARM'})
            ms = pd.melt(ms, id_vars=id_vars)
            ms['DATA'] = 'M+S'
            ms=ms.rename(columns={'variable':'TYPE'})
            ms['YearClass']=ms['YearClass'].astype(str) #Hay que convertir el tipo para poder hacer el merge
        
            resultado = resultado.merge(ms, on=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'DATA','Gen'], how='left')
            resultado['valor'] = np.where(resultado['value'].isna(), resultado['valor'], resultado['value'])
            resultado=resultado.drop(columns=['value'])
            resultado=resultado.drop_duplicates(ignore_index=True)

            

            ###########sales(Tallas)#################
            if os.path.exists(self.path_pescas_tallas_detail):
                sales=data_sales.copy()
                sales = sales.groupby(['Granja', 'Year', 'Mes', 'Talla']).agg(biomass=('Biomasa', 'sum')).reset_index()
                sales=sales.rename(columns={'Talla': 'YearClass','Granja':'FARM'})
                sales['Year']=sales['Year'].astype('int64')
                sales['Mes']=sales['Mes'].astype('int64')
                sales['YearClass']=sales['YearClass'].astype('str')
                id_vars=["FARM", "Year", "Mes", "YearClass"]
                sales = pd.melt(sales, id_vars=id_vars)
                sales['DATA'] = 'sales'
                sales=sales.rename(columns={'variable':'TYPE'})

            else:
                sales = pd.DataFrame(columns=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'value', 'DATA'])
                sales = sales.astype({'FARM': str, 'Year': int,'Mes': int, 'YearClass': str, 'TYPE':str, 'value':float, 'DATA':str})
            
            resultado = resultado.merge(sales, on=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'DATA'], how='left')
            resultado['valor'] = np.where(resultado['value'].isna(), resultado['valor'], resultado['value'])
            resultado=resultado.drop(columns=['value'])
            resultado=resultado.drop_duplicates(ignore_index=True)


            ###### biomass end of the month (Tallas) ######
            endStock=data.copy()
            endStock = data.groupby(['Granja', 'Year', 'Mes', 'TallaFinal']).agg(biomass=('BiomasaFinal', 'sum')).reset_index()
            endStock=endStock.rename(columns={'Granja':'FARM','TallaFinal': 'YearClass'})
            id_vars =["FARM", "Year", "Mes", "YearClass"]
            endStock = pd.melt(endStock, id_vars=id_vars)
            endStock['DATA'] = 'biomass end of month'
            endStock=endStock.rename(columns={'variable':'TYPE'})
            endStock['YearClass']=endStock['YearClass'].astype(str) #Hay que convertir el tipo para poder hacer el merge
            
            resultado = resultado.merge(endStock, on=['FARM', 'Year', 'Mes', 'YearClass', 'TYPE', 'DATA'], how='left')
            resultado['valor'] = np.where(resultado['value'].isna(), resultado['valor'], resultado['value'])
            resultado=resultado.drop(columns=['value'])
            resultado=resultado.drop_duplicates(ignore_index=True)

            
            ###### Consolidado ######
            consolidado=resultado.copy()
            consolidado = consolidado.loc[resultado['TYPE'].isin(['biomass', 'number'])].groupby(['YearClass', 'Gen', 'Year', 'Mes', 'TYPE', 'DATA', 'Date', 'Month']).agg({'valor': 'sum'}).reset_index()
            consolidado['FARM'] = 'Consolidado'

            consolidado_growth = consolidado.loc[(consolidado['DATA'].isin(['growth', 'initial'])) & (consolidado['TYPE'] == 'biomass')].copy()
            consolidado_growth = consolidado_growth.pivot_table(index=['FARM', 'Year', 'Mes', 'TYPE', 'Date', 'Month', 'YearClass', 'Gen'], columns='DATA', values='valor').reset_index().dropna()
            
            consolidado_growth['valor'] =np.where(consolidado_growth['initial']==0,0, consolidado_growth['growth'] / consolidado_growth['initial'] * 100)
            consolidado_growth=consolidado_growth.drop(columns=['growth', 'initial'])
            consolidado_growth['TYPE'] = '%'
            consolidado_growth['DATA'] = 'growth'
            consolidado_av = consolidado.pivot_table(index=['FARM', 'Year', 'Mes', 'DATA', 'Date', 'Month', 'YearClass', 'Gen'], columns='TYPE', values='valor').reset_index().dropna()
            consolidado_av['number']=consolidado_av['number'].astype(int)
            consolidado_av['valor'] = np.where(consolidado_av['number']==0, 0, consolidado_av['biomass'] / consolidado_av['number'] * 1000)
            consolidado_av=consolidado_av.drop(columns=['biomass','number'])
            consolidado_av['TYPE'] = 'avweight'
            consolidado = pd.concat([consolidado if not consolidado.empty else None,consolidado_av if not consolidado_av.empty else None,consolidado_growth if not consolidado_growth.empty else None], ignore_index=True)
            consolidado=consolidado.drop_duplicates(ignore_index=True)
            resultado = pd.concat([resultado if not resultado.empty else None,consolidado if not consolidado.empty else None], ignore_index=True)
            resultado=resultado.drop_duplicates(ignore_index=True)
            resultado=resultado.fillna(0)
            resultado=resultado.drop_duplicates(ignore_index=True)
            #with pd.option_context("future.no_silent_downcasting", True):
            #    resultado = resultado.fillna(False).infer_objects(copy=False)

            ###### Totales ######
            totales = resultado.loc[resultado['TYPE'].isin(['biomass', 'number'])].groupby(['FARM', 'Year', 'Mes', 'TYPE', 'DATA', 'Date', 'Month']).agg({'valor': 'sum'}).reset_index()
            totales['YearClass'] = 'TOTAL'
            totales['Gen'] = 'TOTAL'

            totales_growth = totales.loc[(totales['DATA'].isin(['growth', 'initial'])) & (totales['TYPE'] == 'biomass')].copy()
            totales_growth = totales_growth.pivot_table(index=['FARM', 'Year', 'Mes', 'TYPE', 'Date', 'Month', 'YearClass', 'Gen'], columns='DATA', values='valor').reset_index().dropna()
            
            totales_growth['valor'] = totales_growth['growth'] / totales_growth['initial'] * 100
            totales_growth=totales_growth.drop(columns=['growth', 'initial'])
            totales_growth['TYPE'] = '%'
            totales_growth['DATA'] = 'growth'
            totales_av = totales.pivot_table(index=['FARM', 'Year', 'Mes', 'DATA', 'Date', 'Month', 'YearClass', 'Gen'], columns='TYPE', values='valor').reset_index().dropna()
            
            totales_av['number']=totales_av['number'].astype(int)
            totales_av['valor'] = np.where(totales_av['number']==0, 0,totales_av['biomass'] / totales_av['number'] * 1000)
            totales_av=totales_av.drop(columns=['biomass', 'number']).copy()
            totales_av['TYPE'] = 'avweight'
            totales = pd.concat([totales if not totales.empty else None,totales_av if not totales_av.empty else None,totales_growth if not totales_growth.empty else None], ignore_index=True)
            totales=totales.drop_duplicates(ignore_index=True)
            resultado = pd.concat([resultado if not resultado.empty else None, totales if not totales.empty else None], ignore_index=True).copy()
            resultado=resultado.drop_duplicates(ignore_index=True)
            resultado=resultado.fillna(0)
            resultado=resultado.drop_duplicates(ignore_index=True)

            ###### ultimo retoque ######
            resultado=resultado.drop(columns=['Year', 'Mes', 'Date'])
            resultado = resultado.pivot_table(index=['FARM', 'DATA', 'TYPE', 'YearClass', 'Gen'], columns='Month', values='valor').reset_index()

            #Para que en las biomass de sales y biomass end of month me ponga TOTAL al final tengo que hacer el siguiente cambio
            resultado.loc[(resultado['Gen']=="TOTAL") & (resultado['DATA'].isin(["biomass end of month", "sales"])) & (resultado['TYPE']=="biomass"), "YearClass"]="t.TOTAL"
            resultado.loc[(resultado['Gen']=="TOTAL") & (resultado['DATA'].isin(["biomass end of month", "sales"])) & (resultado['TYPE']=="biomass"), "Gen"]="t.TOTAL"
            resultado = resultado.sort_values(['FARM', 'DATA', 'TYPE', 'Gen'], ignore_index=True)
            
            ######  ordeno columnas ######
            #Encontrar las columnas de resultado que son fechas (aquellas que tienen '-')
            columnas_fecha = [col for col in resultado.columns if '-' in col]
            anos=[x[4:len(x)+1] for x in columnas_fecha]
            meses=[x[:3] for x in columnas_fecha]
            orden_df = pd.DataFrame({'columnas_fecha' : columnas_fecha, 'anos' : anos, 'meses' : meses})
            orden_df['mesnum']=orden_df['meses'].apply(lambda x: mesChar_toNum(x))
            orden_df=orden_df.sort_values(['anos','mesnum'])
            columnas_fecha_ordenadas = orden_df['columnas_fecha']
            columnas_no_fecha = [col for col in resultado.columns if '-' not in col]
            columnas_no_fecha.extend(columnas_fecha_ordenadas) 
            resultado=resultado[columnas_no_fecha].copy()
            
            ###### Para powerBI ######
            # Tabla resumen
            resultado.columns=[col for col in resultado.columns if '-' not in col] +[f"{a}_{b}" for b, a in zip (columnas_fecha_ordenadas, string.ascii_lowercase)]
            id_vars=["FARM", "DATA", "TYPE", "YearClass", "Gen"]
            resultado=pd.melt(resultado, id_vars = id_vars)
            resultado=resultado.rename(columns={'variable':'Mes'})
            resultado['Year']=resultado['Mes'].str[6:].astype(int)
            resultado['Month']=resultado['Mes'].str[2:5].apply(lambda x: mesChar_toNum(x))
            max_year = int(resultado['Year'].max())
            max_month = str(resultado.loc[(resultado['Year'] == max_year) & (resultado['Month'] ==resultado.loc[resultado['Year'] == max_year, 'Month'].max()),'Mes'].unique()[0])
            resultado['last'] = np.where((resultado['Year'] == max_year) & (resultado['Mes'] == max_month), True, False)
            resultado['id'] = resultado['FARM'] + resultado['Gen'] + resultado['Year'].astype(str) + resultado['Mes'].astype(str)

            #Para que en las biomass de sales y biomass end of month me ponga TOTAL al final tengo que hacer el siguiente cambio
            resultado_dcasted = budget_dcast(resultado)
            resultado.loc[resultado['Gen']=="t.TOTAL", "YearClass"]="TOTAL"
            resultado.loc[resultado['Gen']=="t.TOTAL", "Gen"]="TOTAL"
            resultado_dcasted.loc[(resultado['YearClass']=="TOTAL") & ((resultado['DATA']=='biomass end of month') | (resultado['DATA']=='sales')) & (resultado['TYPE']=='biomass'), "YearClass"]="TOTAL"
            resultado_dcasted.loc[(resultado['YearClass']=="TOTAL") & ((resultado['DATA']=='biomass end of month') | (resultado['DATA']=='sales')) & (resultado['TYPE']=='biomass'), "Gen"]="TOTAL"


            resultado.to_csv(self.path_resultado, index=False)
            resultado_dcasted.to_csv(self.path_resultado_dcasted, index=False)
            resultado_dcasted.to_excel(self.path_resultado_dcasted_xls, index=False)
        except Exception as e:
             escribir_log('critical', 'set_resultado ' +"Error {0}".format(str(e)))



    
    def my_plots_all_opt(self,data_to_plot, granjas, opt,n_plots, save=False,legend=False): 
        
        data = data_to_plot.loc[data_to_plot['Granja'].isin(granjas)].groupby(['FechaFin', 'TallaFinal', 'Granja']).agg(BiomasaFinal_tn=('BiomasaFinal','sum')).reset_index()
        data['BiomasaFinal_tn']=data['BiomasaFinal_tn'].apply(lambda x: x/1000)
        initial_data = data_to_plot.loc[data_to_plot['Granja'].isin(granjas) & (data_to_plot['Fecha'] == min(data_to_plot['Fecha']))].groupby(['Fecha', 'Talla', 'Granja']).agg(BiomasaFinal_tn=('Biomasa','sum')).reset_index().rename(columns={'Fecha': 'FechaFin', 'Talla': 'TallaFinal'})
        initial_data['BiomasaFinal_tn']=initial_data['BiomasaFinal_tn'].apply(lambda x: x/1000)
        data = pd.concat([data if not data.empty else None,initial_data if not initial_data.empty else None], ignore_index=True)
        data=data.drop_duplicates(ignore_index=True)
        fechas = list(np.sort(data['FechaFin'].unique()))
        TallaFinal=list(set([RangoPeso_directo_letra(x,self.especie) for x in np.arange(1, 10000, 50)]))
        diccionario={'TallaFinal': TallaFinal, 'Granja': granjas, 'FechaFin': fechas}
        tallas_todas = pd.DataFrame(itertools.product(*diccionario.values()),columns=diccionario.keys())
        plots = []
        if self.especie == "TURBOT":
            opt = opt.loc[opt['Granja'].isin(granjas)].pivot_table(index=['Granja', 'Talla_500'], columns='Fecha', values='BiomasaFinal_tn').reset_index().rename(columns={'05 - optima': 'Optima_mayo', '11 - optima': 'Optima_nov', 'Talla_500': 'TallaFinal'})
            opt = tallas_todas.merge(opt, on=['Granja', 'TallaFinal'], how='left').fillna(0)
            #opt['Optima_mayo'] = opt['Optima_mayo'].replace(np.nan, 0)
            #opt['Optima_nov'] = opt['Optima_nov'].replace(np.nan, 0)

            data = data.merge(opt, on=['Granja', 'TallaFinal', 'FechaFin'], how='left')
            data['BiomasaFinal_tn'] = data['BiomasaFinal_tn'].fillna(0)
            data_consolidada = data.groupby(['FechaFin', 'TallaFinal']).agg({'BiomasaFinal_tn': 'sum', 'Optima_mayo': 'sum', 'Optima_nov': 'sum'}).reset_index()
            
            y_top_lim = data_consolidada[['BiomasaFinal_tn', 'Optima_mayo', 'Optima_nov']].max().max()
            y_top_lim = y_top_lim * 1.5
            y_lims = [0, y_top_lim]
            
            data_consolidada['Diff_may'] = data_consolidada['BiomasaFinal_tn'] - data_consolidada['Optima_mayo']
            data_consolidada['Diff_nov'] = data_consolidada['BiomasaFinal_tn'] - data_consolidada['Optima_nov']
            
            #data_consolidada['ColorRed_may'] = np.where(data_consolidada['Diff_may'] > 0, True, False)
            #data_consolidada['ColorRed_nov'] = np.where(data_consolidada['Diff_nov'] > 0, True, False)
            
            Lista_granjas=["SSF_Iberia", "Cervo_P","Couso_P" ,"Lira_P" ,"Merexo_P", "Oye_P" ,"Palmeira_P" ,"Quilmas_P","SSF","Tocha_P" ,"Vilan_P"]
            fechas = data['FechaFin'].sort_values().unique()
            for i in range(n_plots):
                if i >= len(fechas):
                    continue
                
                fecha = fechas[i]
                plt_data = data.loc[data['FechaFin'] == fecha].copy().reset_index()
                plt_data_consolidada = data_consolidada.loc[data_consolidada['FechaFin'] == fecha].copy().reset_index()
                title = f"Biomasa final: {plt_data['BiomasaFinal_tn'].sum().round():,} Tn - Optima: {plt_data['Optima_mayo'].sum().round():,} Tn".replace(".",";").replace(",",".").replace(";",",")
                title = f"Fecha de cierre: {fecha} / {title}"

                fig=px.bar(plt_data, x='TallaFinal', y='BiomasaFinal_tn', color='Granja',
                    color_discrete_map={"SSF_Iberia": "#E04050", 
                                        "Cervo_P": "#b54747",
                                        "Couso_P": "#3d99f5",
                                        "Lira_P": "#edf035",
                                        "Merexo_P": "#ed74e9",
                                        "Oye_P": "#b58e02",
                                        "Palmeira_P": "#57f26c",
                                        "Quilmas_P": "#1132ed",
                                        "SSF": "#56B4E9",
                                        "Tocha_P": "#d97236",
                                        "Vilan_P": "#7d1cba"},
                    labels={"TallaFinal": "", "BiomasaFinal_tn": "Biomasa Final (tn)"})
                
                # Añadir anotaciones y líneas adicionales
                fig.add_trace(go.Scatter(x=plt_data_consolidada['TallaFinal'], 
                                        y=[0]*len(plt_data_consolidada), 
                                        text=plt_data_consolidada['BiomasaFinal_tn'].round().apply(lambda x: f'{x:g}'),
                                        mode='text', textposition='top center',
                                        textfont=dict(weight='bold',size=15), opacity=0.8,
                                        showlegend=False))
                fig.add_trace(go.Scatter(x=[plt_data_consolidada['TallaFinal'][0]], y=[y_lims[1]*0.9] ,mode="text",text=["May         "],textposition="middle left",textfont=dict(weight='bold',size=12),showlegend=False))
                fig.add_trace(go.Scatter(x=[plt_data_consolidada['TallaFinal'][0]], y=[y_lims[1]*0.8] ,mode="text",text=["Nov         "],textposition="middle left",textfont=dict(weight='bold',size=12),showlegend=False))
                fig.add_hline(y=y_lims[1]*0.9, line_color="purple", line_width=15, opacity=0.2)
                fig.add_hline(y=y_lims[1]*0.8, line_color="turquoise", line_width=15, opacity=0.2)
                fig.add_trace(go.Scatter(x=plt_data_consolidada['TallaFinal'], 
                                        y=[y_lims[1]*0.9]*len(plt_data_consolidada), 
                                        text=plt_data_consolidada['Diff_may'].round().apply(lambda x: f'{x:g}'),
                                        mode='text', textposition='middle center',
                                        textfont=dict(color='black',size=12),
                                        showlegend=False))

                fig.add_trace(go.Scatter(x=plt_data_consolidada['TallaFinal'], 
                                        y=[y_lims[1]*0.8]*len(plt_data_consolidada), 
                                        text=plt_data_consolidada['Diff_nov'].round().apply(lambda x: f'{x:g}'),
                                        mode='text', textposition='middle center',
                                        textfont=dict(color='black',size=12),
                                        showlegend=False))

                fig.add_trace(go.Scatter(x=plt_data_consolidada['TallaFinal'], 
                                        y=plt_data_consolidada['Optima_mayo'], 
                                        mode='markers', marker=dict(symbol='line-ew', color='purple', size=30, line=dict(color='purple',width=5)),
                                        opacity=0.4,showlegend=False))

                fig.add_trace(go.Scatter(x=plt_data_consolidada['TallaFinal'], 
                                        y=plt_data_consolidada['Optima_nov'], 
                                        mode='markers', marker=dict(symbol='line-ew', size=30, color='turquoise',line=dict(color='turquoise',width=5)),
                                        opacity=0.4,showlegend=False))

                            
                # Configuración de la estética del gráfico
                fig.update_layout(
                    xaxis_title="",
                    yaxis=dict(showticklabels=False),
                    yaxis_title="",
                    title=title,
                    title_font=dict(size=25),
                    xaxis=dict(tickangle=25, tickfont=dict(size=15,weight='bold')),
                    showlegend=False,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(size=10)
                )
                if legend:
                    fig.update_layout(
                        legend=dict(title_text='Granja', traceorder='normal'),
                        showlegend=True
                    )
                plots.append(fig)
                # Guardar el gráfico si es necesario
                if save:
                    #El write_image de plotly no funciona en windows. Hay que instalar orca
                    #https://github.com/plotly/orca/blob/master/README.md

                    file_name=os.path.join(self.solo_path_plots, f"Plot_{i}_rodaballo.jpg")
                    #fig.write_image(file_name,format='jpg', height=900,width=1100,
                    #            engine='orca')#engine='kaleido')
                    
                
        elif self.especie == "SOLE":
            ##############################
            #Nuevo para hacerlo igual que rodaballo pero hay que asegurar porque no tienen ciertas tablas
            hay_optima=False
            if opt is not None:
                if not opt.loc[opt['Granja'].isin(granjas)].empty:
                    opt = opt.loc[opt['Granja'].isin(granjas)].pivot_table(index=['Granja', 'Talla_500'], columns='Fecha', values='BiomasaFinal_tn').reset_index().rename(columns={'05 - optima': 'Optima_mayo', '11 - optima': 'Optima_nov', 'Talla_500': 'TallaFinal'})
                    opt = tallas_todas.merge(opt, on=['Granja', 'TallaFinal'], how='left').fillna(0)
                    data = data.merge(opt, on=['Granja', 'TallaFinal', 'FechaFin'], how='left')
                    data['BiomasaFinal_tn'] = data['BiomasaFinal_tn'].fillna(0)
                    data_consolidada = data.groupby(['FechaFin', 'TallaFinal']).agg({'BiomasaFinal_tn': 'sum', 'Optima_mayo': 'sum', 'Optima_nov': 'sum'}).reset_index()
                    data_consolidada['Diff_may'] = data_consolidada['BiomasaFinal_tn'] - data_consolidada['Optima_mayo']
                    data_consolidada['Diff_nov'] = data_consolidada['BiomasaFinal_tn'] - data_consolidada['Optima_nov']
                    y_top_lim = data_consolidada[['BiomasaFinal_tn', 'Optima_mayo', 'Optima_nov']].max().max()
                    hay_optima=True
                ##############################################
                else:
                    #Los antiguos
                    data_consolidada = data.groupby(['FechaFin', 'TallaFinal']).agg({'BiomasaFinal_tn': 'sum'}).reset_index()
                    y_top_lim = data_consolidada['BiomasaFinal_tn'].max()
            else:
                data_consolidada = data.groupby(['FechaFin', 'TallaFinal']).agg({'BiomasaFinal_tn': 'sum'}).reset_index()
                y_top_lim = data_consolidada['BiomasaFinal_tn'].max()



            y_top_lim = y_top_lim * 1.5
            y_lims = [0, y_top_lim]
            
            Lista_granjas= ["Cervo Sole", "Tocha Sole","Hafnir_P" ,"Anglet_P" ,"Couso i+d"]#,"SSF_Iberia","SSF"]
            fechas = data['FechaFin'].sort_values().unique()
            for i in range(n_plots):
                if i >= len(fechas):
                    continue
                
                fecha = fechas[i]
                plt_data = data.loc[data['FechaFin'] == fecha].copy().reset_index()
                plt_data_consolidada = data_consolidada.loc[data_consolidada['FechaFin'] == fecha].copy().reset_index()
                
                if hay_optima:
                    #Nuevo
                    title = f"Biomasa final: {plt_data['BiomasaFinal_tn'].sum().round():,} Tn".replace(".",";").replace(",",".").replace(";",",")
                    ###########################
                else:
                    #Antiguo
                    title = f"Biomasa final: {plt_data['BiomasaFinal_tn'].sum().round():,} Tn".replace(".",";").replace(",",".").replace(";",",")
                title = f"Fecha de cierre: {fecha} / {title}"

                # Crear la figura básica con plotly.express
                fig = px.bar(plt_data, x='TallaFinal', y='BiomasaFinal_tn', color='Granja',
                        labels={"TallaFinal": "", "BiomasaFinal_tn": "Biomasa Final (tn)"},
                        color_discrete_map={
                            'Cervo Sole': '#49d6c3',
                            'Tocha Sole': '#b54747',
                            'Hafnir_P': '#3d99f5',
                            'Anglet_P': '#edf035',
                            'Couso i+d': '#ed74e9'#,
                            #"SSF_Iberia": "#E04050",
                            #"SSF": "#56B4E9"
                        })
                fig.add_trace(go.Scatter(x=plt_data_consolidada['TallaFinal'], 
                                        y=[0]*len(plt_data_consolidada), 
                                        text=plt_data_consolidada['BiomasaFinal_tn'].round().apply(lambda x: f'{x:g}'),
                                        mode='text', textposition='top center',
                                        textfont=dict(weight='bold',size=15), opacity=0.8,
                                        showlegend=False))
                
                if hay_optima:
                    pass
                    #Nuevo
                    #fig.add_trace(go.Scatter(x=[plt_data_consolidada['TallaFinal'][0]], y=[y_lims[1]*0.9] ,mode="text",text=["May         "],textposition="middle left",textfont=dict(weight='bold',size=12),showlegend=False))
                    #fig.add_trace(go.Scatter(x=[plt_data_consolidada['TallaFinal'][0]], y=[y_lims[1]*0.8] ,mode="text",text=["Nov         "],textposition="middle left",textfont=dict(weight='bold',size=12),showlegend=False))
                    #fig.add_hline(y=y_lims[1]*0.9, line_color="purple", line_width=15, opacity=0.2)
                    #fig.add_hline(y=y_lims[1]*0.8, line_color="turquoise", line_width=15, opacity=0.2)
                    #fig.add_trace(go.Scatter(x=plt_data_consolidada['TallaFinal'], 
                    #                        y=[y_lims[1]*0.9]*len(plt_data_consolidada), 
                    #                        text=plt_data_consolidada['Diff_may'].round().apply(lambda x: f'{x:g}'),
                    #                        mode='text', textposition='middle center',
                    #                        textfont=dict(color='black',size=12),
                    #                        showlegend=False))

                    #fig.add_trace(go.Scatter(x=plt_data_consolidada['TallaFinal'], 
                    #                        y=[y_lims[1]*0.8]*len(plt_data_consolidada), 
                    #                        text=plt_data_consolidada['Diff_nov'].round().apply(lambda x: f'{x:g}'),
                    #                        mode='text', textposition='middle center',
                    #                        textfont=dict(color='black',size=12),
                    #                        showlegend=False))

                    #fig.add_trace(go.Scatter(x=plt_data_consolidada['TallaFinal'], 
                    #                        y=plt_data_consolidada['Optima_mayo'], 
                    #                        mode='markers', marker=dict(symbol='line-ew', color='purple', size=30, line=dict(color='purple',width=5)),
                    #                        opacity=0.4,showlegend=False))

                    #fig.add_trace(go.Scatter(x=plt_data_consolidada['TallaFinal'], 
                    #                        y=plt_data_consolidada['Optima_nov'], 
                    #                        mode='markers', marker=dict(symbol='line-ew', size=30, color='turquoise',line=dict(color='turquoise',width=5)),
                    #                        opacity=0.4,showlegend=False))

                #############################
                # Personalizar el tema y estilo
                fig.update_layout(
                    xaxis_title="",
                    yaxis_title="",
                    title=title,
                    title_font=dict(size=20),
                    xaxis=dict(tickangle=25, tickfont=dict(size=12,weight='bold'), title_standoff=15),
                    yaxis=dict(visible=False),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    showlegend=False,
                    font=dict(size=10),
                )

                if legend:
                    fig.update_layout(
                        legend=dict(title_text='Granja', traceorder='normal'),
                        showlegend=True
                    )
                # Guardar el gráfico si es necesario
                plots.append(fig)
                if save:
                    #El write_image de plotly no funciona en windows. Hay que instalar orca
                    #https://github.com/plotly/orca/blob/master/README.md
                    file_name=os.path.join(self.solo_path_plots, "Plot_{i}lenguado.png")
                    #write_image(fig, file_name,format='jpg', height=900,width=1100,
                    #            engine='orca')#engine='kaleido')
        return plots

                
    
    def gen_evol_plot(self, master_DF, granja, historical_data, n_plots=10, max_historic_rows=30000):
        master_DF = master_DF.loc[master_DF['Granja'] == granja].copy()
        
        data = master_DF.loc[master_DF['PesoMedioFinal'] > 0][['Granja', 'EdadFinal', 'PesoMedioFinal', 'Gen', 'FechaFin']]
        data['FechaFin']=str(data['FechaFin'])
        
        data_initial = master_DF.loc[master_DF['Fecha']==master_DF['Fecha'].min()][['Granja', 'Edad', 'PesoMedio', 'Gen', 'Fecha']].rename(columns={'Fecha': 'FechaFin', 'PesoMedio': 'PesoMedioFinal', 'Edad': 'EdadFinal'})
        data_initial['FechaFin']=str(data_initial['FechaFin'])
        if granja not in historical_data['Granja'].unique():
            if self.especie=="SOLE":
                if granja == "Cervo Sole" or granja == "Tocha Sole":
                    historical_data = historical_data.loc[historical_data['Granja'].isin(["Hafnir_P", "Couso i+d", "Anglet_P"])].copy()
                    historical_data['Granja'] = granja
        if granja == "SSF":
            if self.especie=="TURBOT":
                historical_data = historical_data.loc[historical_data['Granja'] != "Mira_P"].copy()
            historical_data['Granja'] = "SSF"
        if granja == "SSF_Iberia":
            if self.especie=="TURBOT":
                historical_data = historical_data.loc[(historical_data['Granja'] !="Mira_P") &  (historical_data['Granja'] !="Oye_P")].copy()
            historical_data['Granja'] = "SSF_Iberia"
        
            #La comento hasta que se implemente shiny
            #shinyalert(title="No hay historico para esta granja, se usara el resto de granjas como referencia.", type="warning")

        historical_data=historical_data.loc[historical_data['Granja']==granja].rename(columns={'PesoMedio': 'PesoMedioFinal', 'Edad': 'EdadFinal'})
        if historical_data.shape[0] > max_historic_rows:
            historical_data = historical_data.sample(n=max_historic_rows, random_state=777)
        
        plots = []

        gens = pd.concat([data['Gen'], data_initial['Gen']], ignore_index=True).unique().tolist()
        gens.sort() 
        base_size=12
    
        for i in range(n_plots):
            if i >= len(gens):
                continue
            
            i_gen = gens[i]
           
            # Definimos la figura principal
            fig = go.Figure()

            # Añadimos los puntos históricos
            fig.add_trace(go.Scatter(
                x=historical_data['EdadFinal'],
                y=historical_data['PesoMedioFinal'],
                mode='markers',
                marker=dict(color='white', opacity=0.2),
                name='Histórico'
            ))

            # Añadimos los puntos de la generación actual
            fig.add_trace(go.Scatter(
                x=data.loc[data['Gen'] == i_gen, 'EdadFinal'],
                y=data.loc[data['Gen'] == i_gen, 'PesoMedioFinal'],
                mode='markers',
                marker=dict(color='green'),
                name='Fin'
            ))

            # Añadimos los puntos iniciales
            fig.add_trace(go.Scatter(
                x=data_initial.loc[data_initial['Gen'] == i_gen, 'EdadFinal'],
                y=data_initial.loc[data_initial['Gen'] == i_gen, 'PesoMedioFinal'],
                mode='markers',
                marker=dict(color='red'),
                name='Inicio'
            ))

            # Configuramos el diseño de la gráfica
            fig.update_layout(
                title=f"{granja} / Generacion: {i_gen}",
                xaxis_title="Edad Final",
                yaxis_title="Peso Medio Final",
                paper_bgcolor='black',
                plot_bgcolor='black',
                font=dict(color='white', size=base_size),
                legend=dict(
                    bgcolor='black',
                    bordercolor='white',
                    borderwidth=1
                ),
                xaxis=dict(
                    tickfont=dict(size=base_size*0.8, color='white'),
                    titlefont=dict(size=base_size, color='white'),
                    showgrid=True,
                    gridcolor='#595959',
                    zerolinecolor='white',
                ),
                yaxis=dict(
                    tickfont=dict(size=base_size*0.8, color='white'),
                    titlefont=dict(size=base_size, color='white'),
                    showgrid=True,
                    gridcolor='#595959',
                    zerolinecolor='white',
                )
            )

            # Guardamos la figura en un archivo
            #https://github.com/plotly/orca/blob/master/README.md
            file_name = os.path.join(self.solo_path_plots, f"Plot_{granja}_Generacion_{i_gen}.png")
            #with open(file_name, 'wb') as w:
            #    w.write(to_image(fig,format="png", engine='orca'))
            plots.append(fig)
        return plots
    
        
        


    
    def obtener_tabla_disponibilidad(self,granja):
        if not os.path.exists(self.path_masterDF):
            return None
        master_df_no_ini =pd.read_csv(self.path_masterDF)[["Granja","PesoMedioFinal","BiomasaFinal","NumFinal","FechaFin","TallaFinal","EdadFinal"]]
        master_df_no_ini=master_df_no_ini.rename(columns={'PesoMedioFinal':'PesoMedio' , 'BiomasaFinal':'Biomasa', 'NumFinal':'Num', 'FechaFin':'Fecha', 'TallaFinal':'Talla', 'EdadFinal':'Edad'})
        master_df_no_ini=master_df_no_ini.loc[master_df_no_ini['Biomasa']>0]
        all_dispersion_df = self.import_format_func(path = self.path_df_dispersion, val_name = "cv", from_por = True)
        all_edad_venta_df = self.import_format_func(path = self.path_df_edad_pescas, val_name = "Edad_lim")
        fecha=pd.read_csv(self.path_default_fecha)['date'].to_list()[0]
        initial_data = self.import_initial_data(continue_flag = False, fecha = fecha)[["Granja","PesoMedio","Biomasa","Num","Fecha","Talla","Edad"]]
        if initial_data is None or master_df_no_ini is None:
            return None
        
        data = pd.concat([initial_data if not initial_data.empty else None, master_df_no_ini if not master_df_no_ini.empty else None], ignore_index=True)
        data=data.drop_duplicates(ignore_index=True)
        data["Fecha"]=data["Fecha"].apply(lambda x: pd.to_datetime(x).date().replace(day=1))
        data["Fecha"] = data["Fecha"].apply(lambda x: add_months(x, 1))
        data["MesChar"] = self.fecha_table_format_func(data["Fecha"])
        data['Ano'] = data['Fecha'].apply(lambda x: pd.to_datetime(x).date().year)
        data['Mes'] = data['Fecha'].apply(lambda x: pd.to_datetime(x).date().month)
        data=data.merge(all_dispersion_df, on=["Granja","Ano","Mes"], how='left')
        data['cv']=data['cv'].fillna(0)
        data=data.merge(all_edad_venta_df, on=["Granja","Ano","Mes"], how='left')
        data['Edad_lim']=data['Edad_lim'].fillna(0)
        data['Edad_lim']=data['Edad']-data['Edad_lim']
        data=data.loc[data['Edad_lim']>=0].copy()
        data=data.drop(columns=["Edad", "Edad_lim"], axis=1)
        data_no_disp = data.loc[data['cv']==0].drop(columns=['cv'], axis=1).copy()
        data_disp = data.loc[data['cv']!=0].copy()
        if data_disp.shape[0]>0:
            nuevo_df=data_disp[['Num','PesoMedio','cv']].copy()
            data_disp['Pesos_peces']=nuevo_df.apply(func=lambda x: dispersion_pesos_func(int(x.Num), x.PesoMedio, x.cv), axis=1)
            data_disp= data_disp.drop(columns=["PesoMedio"], axis=1).copy()
            data_disp["Pesos_peces"]=data_disp['Pesos_peces'].str.split(',')
            data_disp=data_disp.explode("Pesos_peces")
            data_disp["Pesos_peces"] =pd.to_numeric(data_disp["Pesos_peces"])
            data_disp["Talla"] = RangoPeso_directo_letra_para_df(data_disp, "Pesos_peces", especie=self.especie)
            data_disp["Num"] = 1
            data_disp=data_disp.drop(columns=["cv"], axis=1).copy()
            data_disp = data_disp.rename(columns={'Pesos_peces': 'PesoMedio'})
            data_disp["Biomasa"] = data_disp["PesoMedio"] * data_disp["Num"] / 1000
            data = pd.concat([data_no_disp if not data_no_disp.empty else None, data_disp if not data_disp.empty else None], ignore_index=True)
            data=data.drop_duplicates(ignore_index=True)
        else:
            data = data_no_disp
                        
        data = data.groupby(['Granja', 'MesChar','Talla', 'Fecha']).agg({'Num': 'sum','Biomasa': 'sum'}).reset_index()
        data['PesoMedio']=data['Biomasa']/data['Num']*1000
        data['Biomasa']=data['Biomasa'].apply(lambda x: round(math.ceil(x)))
        data=pd.pivot_table(data, index=['Granja', 'Talla'], columns='MesChar', values='Biomasa').reset_index().copy()
        data=data.fillna(0)
        data=data.loc[data['Granja']==granja].copy()
        data.loc[len(data)]=data.iloc[0]
        data.loc[len(data)-1, 'Granja']='Total'
        data.loc[len(data)-1, 'Talla']='-'
        columnas_meses=data.columns[2:]
        data.loc[data['Granja'] == "Total",columnas_meses]= [0]*len(columnas_meses)
        data.loc[data['Granja']  == "Total",columnas_meses]= data[columnas_meses].sum(axis=0).to_list()
        return data
           

