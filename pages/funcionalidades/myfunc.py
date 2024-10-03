import datetime
import pandas as pd
from sqlalchemy import URL, create_engine,text
import pymssql
import urllib
import numpy as np
import string
import calendar
import math
from dateutil.relativedelta import relativedelta
import logging
from logging.handlers import RotatingFileHandler
import os


## Funciones propias 


def fechas_stolt_func_new(fecha, type="cierre"):
# La fecha tiene que entrar en este formato: "2021-01-28"
# Devuelve:
#     - Fin de mes SSF (type = "cierre")
#     - Inicio de mes SSF (type = "inicio")
#     - Month_ssf (type = "month")
#     - Year_ssf (type = "year")
# Como se pretende usar en funciones 'sapply', el resultado se devuelve en modo char si es cierre o inicio. 
# La funcion sapply no permite devolver la fecha ne formato fecha
##########¡¡¡OJO!!!####################
#Hasta junio de 2021 Stolt contaba los meses por semanas completas
#el programa tiene eso en cuenta y por eso aparecen dias de mes de 35 y 28 días
#para las fechas anteriores a junio de 2021.

    # Convierto en Char
    fecha = str(fecha)

    # Si no hay "-" o los primeros numeros antes del "-" no son 4 digitos devuelve error
    nohay_ = "-" not in fecha
    year_no_first = len(fecha.split("-")[0]) != 4
    if nohay_ or year_no_first:
        return "Format ERror"

    fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
    # Si la fecha es entre el 2021-05-31 al 2021-06-30 (incluidas) se devuelve el resultado a pelo
    if fecha >= datetime.date(2021, 5, 31) and fecha <= datetime.date(2021, 6, 30):
        cierre = datetime.datetime.strptime("2021-06-30", "%Y-%m-%d").date()
        inicio = datetime.datetime.strptime("2021-05-31", "%Y-%m-%d").date()
        Month_ssf = 6
        Year_ssf = 2021
    # Si la fecha es  > 2021-06-30 el inicio y cierre es el del mes natural
    elif fecha > datetime.date(2021, 6, 30):
        cierre=fecha.replace(day=calendar.monthrange(fecha.year, fecha.month)[-1])
        inicio = fecha.replace(day=1)
        Month_ssf = fecha.month
        Year_ssf = fecha.year if fecha.month != 12 else fecha.year + 1
    # Si la fecha es  < 2021-05-31 el inicio y cierre es el del mes stolt antiguo
    else:
        # Check if the date is less than the last Sunday of the month
        cierre_mes_natural=fecha.replace(day=calendar.monthrange(fecha.year, fecha.month)[-1])
        #Me quedo con el último domingo
        ultimo_domingo_mes_fecha= cierre_mes_natural - datetime.timedelta(days=(cierre_mes_natural.weekday()+1) % 7)

        if fecha <= ultimo_domingo_mes_fecha:
            # Si la fecha es menor que el último domingo de mes
            cierre_mes_natural_anterior = (fecha.replace(day=1) - datetime.timedelta(days=1))
            ultimo_domingo_mes_anterior=cierre_mes_natural_anterior-datetime.timedelta(days=(cierre_mes_natural_anterior.weekday() + 1) % 7)

            cierre = ultimo_domingo_mes_fecha
            inicio = (ultimo_domingo_mes_anterior + datetime.timedelta(days=1))
        else:
            # Si la fecha es mayor que el último domingo de mes
            cierre_mes_natural_mes_siguiente = (fecha.replace(day=1) + relativedelta(months=2) - datetime.timedelta(days=1))
            ultimo_domingo_mes_siguiente=cierre_mes_natural_mes_siguiente-datetime.timedelta(days=(cierre_mes_natural_mes_siguiente.weekday() + 1) % 7)
            cierre = ultimo_domingo_mes_siguiente
            inicio = (ultimo_domingo_mes_fecha + datetime.timedelta(days=1))

        # Particularity of November months
        if cierre.month == 11:
            cierre_mes_natural_noviembre = (cierre.replace(day=1) + relativedelta(months=1) - datetime.timedelta(days=1))
            # If the close falls on Friday, Saturday or Sunday, that date will be used if not the normal ssf close

            if (cierre_mes_natural_noviembre.weekday()==4 | cierre_mes_natural_noviembre.weekday()==5 | cierre_mes_natural_noviembre.weekday()==6): 
                cierre = cierre_mes_natural_noviembre

        Month_ssf = cierre.month
        Year_ssf = cierre.year if cierre.month != 12 else cierre.year + 1
    # Resultado
    if type == "cierre":
        resultado = cierre
    elif type == "inicio":
        resultado = inicio
    elif type == "month":
        resultado = Month_ssf
    elif type == "year":
        resultado = Year_ssf
    elif type == "dias_mes":
        resultado = (cierre - inicio).days + 1
    else:
        return "ErRor_fechas_stolt_new"

    return str(resultado)

#Genera las fechas de cierre de los meses entre las dos fechas de entrada de parámetros para la consulta de IMATIA
def date_query_generator_new( from_date='2016-01-01', to_date='2050-12-01'):
    """
    This function creates a string with the dates in the format for SQL. It returns the dates between ().
    """
    from_date = datetime.datetime.strptime(from_date, '%Y-%M-%d')
    to_date = datetime.datetime.strptime(to_date, '%Y-%M-%d')
    #Cambié la siguiente (funciona la comentada)
    dates_raw = [fechas_stolt_func_new(i) for i in pd.date_range(from_date,to_date, freq='MS').strptime("%Y-%M-%d")]
    #dates_raw = [fechas_stolt_func_new(i) for i in pd.date_range(from_date,to_date, freq='MS').strftime("%Y-%M-%d")]
    ## dates_raw = [str(date) for date in [from_date + datetime.timedelta(days=i) for i in range((to_date - from_date).days + 1)]]
    
    # Manual adjustments
    dates_raw = [date.replace('2019-11-30', '2019-11-24') for date in dates_raw]
    
    dates = ", ".join(["'" + date + "'" for date in dates_raw])
    dates = f"({dates})"
    
    return dates

#Transforma el nombre del mes en número
#Se han cambiado los nombres de los meses
    #con la primera en mayúsculas
def mesChar_toNum(month_char):
    month_dict = {
        'Jan': 1, 'Ene': 1, 'jan':1, 'ene':1,
        'Feb': 2, 'feb':2,
        'Mar': 3, 'mar':3,
        'Apr': 4, 'Abr': 4, 'abr':4, 'apr':4,
        'May': 5, 'may':5,
        'Jun': 6, 'jun': 6,
        'Jul': 7, 'jul':7,
        'Aug': 8, 'Ago': 8, 'ago':8, 'aug':8,
        'Sep': 9, 'sep':9,
        'Oct': 10, 'oct':10,
        'Nov': 11, 'nov':11,
        'Dec': 12, 'Dic': 12, 'dec':12, 'dic':12
    }
    
    month_char = month_char.lower()
    if month_char in month_dict:
        return month_dict[month_char]
    else:
        return "ErRor_meschar_to_Num"

#Función que devuelve una cadena en funcion de la fecha y la especie
def GeneracionFunc( fecha, especie):
    """
    Esta función calcula la generación de peces a partir de una fecha en formato cadena: 2018-01-28
    """
    if especie == "TURBOT":
        dividendo = 3
    elif especie == "SOLE":
        dividendo = 2
    else:
        return "GEN_ErRor"
    
    mes = math.ceil(fecha.month/dividendo)
    ano=str(fecha.year)[2:]
    generacion = f"{ano} {mes}"

    #En la funcion del Quillo de R le pone SG sin espacios
    if especie == "SOLE":
        generacion += "SG"
    return generacion


#Función que devuelve un dataframe con los peces clasificados por su talla dentro de bins
def RangoPeso_directo_letra_para_df( df, colname, especie):
    if especie == "TURBOT":
        cortes_vec = [0, 300, 400, 600, 800, 1000, 1500, 2000, 2500, 3000, 4000, 10**100]
        tallas = ["0 - 300", "300 - 400", "400 - 600", "600 - 800", "800 - 1000", "1000 - 1500", "1500 - 2000", "2000 - 2500", "2500 - 3000", "3000 - 4000", "4000"]
    elif especie == "SOLE":
        cortes_vec = [0, 100, 200, 300, 400, 500, 600, 800, 10**100]
        tallas = ["0 - 100", "100 - 200", "200 - 300", "300 - 400", "400 - 500", "500 - 600", "600 - 800", "800 - 10000"]
    else:
        escribir_log('error',"Error RangoPeso_directo_letra_para_df")
        return None
    
    letras_df = pd.DataFrame({"Talla_let": [f"{chr(i+97)}.{talla}" for i, talla in enumerate(tallas)], "Talla": tallas})
    
    df["orden"] = range(len(df))
    df["Talla"] = pd.cut(df[colname], bins=cortes_vec, labels=tallas, include_lowest=True) #si hace falta a la hora de presentar resultados a lo mejor hace falta el  campo precision=50 dentro de cut
    df["Talla"] = df["Talla"].astype(str)
    df["Talla"] = df["Talla"].str.replace("(", "")
    df["Talla"] = df["Talla"].str.replace("]", "")
    df["Talla"] = df["Talla"].str.replace("[", "")
    df["Talla"] = df["Talla"].str.replace(",", " - ")
    #Esta parte habrá que comprobarla porque es para que aparezca con un determinado formato. Seguramente
    #jugando con precision de cut (un poco más arriba en esta funcion).
    df["Talla"] = df["Talla"].str.replace("4000 - Inf", "4000")

    #Esta parte habrá que comprobarla porque es para que aparezca con un determinado formato. Seguramente
    #jugando con precision de cut (un poco más arriba en esta funcion).
    if especie == "TURBOT":
        df["Talla"] = df["Talla"].str.replace(" - 100000000000000000000", "")
    elif especie == "SOLE":
        df["Talla"] = df["Talla"].str.replace(" - 100000000000000000000", " - 10000")
    
    df = pd.merge(df, letras_df, on="Talla", how="left")
    df = df.sort_values("orden")
    return df["Talla_let"]

#Función que en función de la etiqueta de peso y la especie 
#devuelve la etiqueta de peso con una letra
def RangoPesoFunc_plus_letter( x, especie):
    x = str(x)
    if especie == "TURBOT":
        if x == "4000":
            y = "k.4000"
        elif x == "3000 - 4000":
            y = "j.3000 - 4000"
        elif x == "2500 - 3000":
            y = "i.2500 - 3000"
        elif x == "2000 - 2500":
            y = "h.2000 - 2500"
        elif x == "1500 - 2000":
            y = "g.1500 - 2000"
        elif x == "1000 - 1500":
            y = "f.1000 - 1500"
        elif x == "800 - 1000":
            y = "e.800 - 1000"
        elif x == "600 - 800":
            y = "d.600 - 800"
        elif x == "400 - 600":
            y = "c.400 - 600"
        elif x == "300 - 400":
            y = "b.300 - 400"
        elif x == "300":
            y = "a.300"
        else:
            y = x
        return y
    elif especie == "SOLE":
        if x == "800 - 10000":
            y = "h.800 - 10000"
        elif x == "600 - 800":
            y = "g.600 - 800"
        elif x == "500 - 600":
            y = "f.500 - 600"
        elif x == "400 - 500":
            y = "e.400 - 500"
        elif x == "300 - 400":
            y = "d.300 - 400"
        elif x == "200 - 300":
            y = "c.200 - 300"
        elif x == "100 - 200":
            y = "b.100 - 200"
        elif x == "0 - 100":
            y = "a.0 - 100"
        else:
            y = x
        return y
    else:
        return "TallasErRor"

#Función que convierte a formato long
def budget_dcast( data):
    #HACER EL RESET INDEX
    nuevo_dato = pd.pivot_table(data, index=['FARM', 'DATA', 'TYPE', 'YearClass', 'Gen'], columns='Mes', values='value').reset_index().copy()
    return nuevo_dato

#Función que dado un valor n devuelve valores normales aleatorios
def rnorm2( mean, sd, n=1000):
    if n == 1:
        return mean
    else:
        np.random.seed(7777)
        vector=np.random.normal(mean, sd, size=n)
        media=np.mean(vector)
        std=np.std(vector)
        if std==0:
            return vector
        else:
            return mean+sd*((vector-media)/std)
        #return mean+sd*np.random.normal(0, 1, size=n)

#Función que devuelve una serie con las letras y los márgenes entre los que se encuentran
#los pesos de los peces 
def RangoPesoFunc_custom(pesos, corte=100):
    
    my_letters = [f"{a}{b}" for a in string.ascii_lowercase  if a<"g" for b in string.ascii_lowercase]
    
    rango_superior=round(151*corte)
    tallas_cut=pd.cut(pd.Series(range(0,rango_superior,corte)),bins=range(0,rango_superior,corte),include_lowest=True, right=False,precision=0).unique()
    
    tallas=[str(i).replace(","," -").replace("[","").replace(")","") for i in tallas_cut.categories]
    tallas=pd.Series([f"{a}.{b}" for a,b in zip(my_letters[:len(tallas)], tallas)])
    tallas_df = pd.DataFrame({'Talla_cut': tallas_cut[:-1], 'Talla': tallas})

    
    Pesos = pd.DataFrame({'Pesos': pesos})
    Pesos['id'] = pd.Series(np.arange(0, len(pesos)))
    Pesos['Talla_cut'] =pd.cut(Pesos['Pesos'], bins = range(0, rango_superior, corte), include_lowest=True, right=False)
    Pesos = Pesos.merge(tallas_df, on = "Talla_cut", how='left')
    Pesos =Pesos.sort_values('id')
    return Pesos['Talla']
    

#Función que devuelve la etiqueta del rango en el que 
#se engloba el peso de un pez. Los intervalos son
#abiertos en el inicio y cerrados en el final ej: (0,300] 
def RangoPeso_directo_letra( x, especie):
    if x == 0:
        return "Error talla peso 0"
    
    #En Python cortes_vec tienen que ser todos del mismo tamaño
    if especie == "TURBOT":
        cortes_vec = [0, 300, 400, 600, 800, 1000, 1500, 2000, 2500, 3000, 4000, 5000]
    elif especie == "SOLE":
        cortes_vec = [0, 100, 200, 300, 400, 500, 600, 800, 1000]
    else:
        escribir_log('error',"Error RangoPeso_directo_letra")
        return None
    
    
    #talla devuelve los índices de cortes_vec. Si está fuera de índice significa que el peso
    #es mayor de 5000 en el caso de Rodaballo y de 1000 en el caso del Lenguado
    talla= np.digitize(x, bins=cortes_vec, right=True)
    
    #Para controlar los outliers (valores fuera de índice)
    if talla>=len(cortes_vec): 
        talla=len(cortes_vec)-1
    
    talla_sig=cortes_vec[talla]
    talla=cortes_vec[talla-1]
    
    letra_index = np.min(np.where(talla <= np.array(cortes_vec)))
    letra = string.ascii_lowercase[letra_index]
    talla = f"{letra}.{talla} - {talla_sig}"

    if especie == "TURBOT":
        talla = talla.replace(" - 5000", "")
    if especie == "SOLE":
        talla = talla.replace(" - 1000", " - 10000")
    
    return talla

#Función que devuelve una lista con las etiquetas de las tallas
#según la especie
def dame_tallas(especie):

    if especie == "TURBOT":
        cortes_vec = [0, 300, 400, 600, 800, 1000, 1500, 2000, 2500, 3000, 4000, 5000]
    elif especie == "SOLE":
        cortes_vec = [0, 100, 200, 300, 400, 500, 600, 800, 1000]
    else:
        return []
    long=len(cortes_vec)
    talla = [f"{i} - {j}" for i,j in zip(cortes_vec[0:long-1], cortes_vec[1:])]

    if especie == "TURBOT":
        talla[long-2]= talla[long-2].replace(" - 5000", "")
    if especie == "SOLE":
        talla[long-2]= talla[long-2].replace(" - 1000", " - 10000")
    return talla

    
#Lanza la consulta contra Elastic Aqua con odbc
def imatia_query_antigua(sql):
    if sql=="":
        return "sqlErRor"
    driver_name = "SQL Server"
    db_name = "ELASTIC_AQUA_STOLT"
    server_address = "EMEA-ELASTIC1.stolt.stoltroot.local"
    user_name = "odbc"
    pwd = "ODBC"
    params = urllib.parse.quote_plus("DRIVER={SQL Server};"
                                    "SERVER="+server_address+";"
                                    "DATABASE="+db_name+";"
                                    "UID="+user_name+";"
                                    "PWD="+pwd+";")
    
    engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params), pool_pre_ping=True)
    conn=engine.connect()
    data = pd.read_sql_query(text(sql), conn)
    conn.close()
    engine.dispose()
    return data

#Lanza la consulta contra Elastic Aqua sin odbc
def imatia_query(sql):
    if sql=="":
        return "sqlErRor"
    
    url_object = URL.create(
        "mssql+pymssql",
        username="Elastic1",
        password="El@sti@12#%!@",  # plain (unescaped) text
        host="EMEA-ELASTIC1.stolt.stoltroot.local",
        database="ELASTIC_AQUA_STOLT_BI",
        #"ELASTIC_AQUA_STOLT_BI"
    )
    engine = create_engine(url_object, pool_pre_ping=True)
    conn=engine.connect()
    
    data = pd.read_sql_query(sql, conn)
    conn.close()
    engine.dispose()
    return data

#Añade meses a una fecha
def add_months( start_date, months):
    return start_date + relativedelta(months=months)

#Funcion que devuelve los valores concatenados 
#de dos distribuciones normales de longitud n
#(el resultado tiene longitud 2*n), media mean
#y desviacion estandard mean*cv cada una.
def rnorm3(n, mean_1, cv_1, mean_2, cv_2):
    np.random.seed(7777)
    
    sd_1 =np.where(mean_1==0,1, mean_1 * cv_1)
    pesos_1 = np.random.normal(0, 1, n)
    media_1=np.mean(pesos_1)
    std_1=np.std(pesos_1)
    pesos_1=mean_1+sd_1*((pesos_1-media_1)/std_1)


    sd_2 = np.where(mean_2==0,1, mean_2 * cv_2)
    pesos_2 = np.random.normal(0, 1, n)
    media_2=np.mean(pesos_2)
    std_2=np.std(pesos_2)
    pesos_2= mean_2+sd_2*((pesos_2-media_2)/std_2)
    pesos = np.concatenate([pesos_1, pesos_2])

    return pesos

#Función que devuelve en formato array de cadenas
#los valores de una distribución normal de n muestras
#mean como media y desviación=mean*cv
def dispersion_pesos_func( n, mean, cv):
    if n <= 1:
        return mean
    else:
        np.random.seed(7777)
        sd = mean * cv
        pesos = np.random.normal(mean, sd,size=n)
        media=np.mean(pesos)
        std=np.mean(pesos)
        pesos=mean+sd*((pesos-media)/std)
    
        pesos_str = ','.join(map(str, pesos))
        return pesos_str
    
# Funcion para generar nombres de columnas de fecha
#con 3 letras del nombre del mes en inglés (la primera en mayúscula)
#la salida es una lista con este formato de elementos Mmm-yyyy de tipo
#string. El primer elemento corresponde a fecha_start+1 mes y los siguientes
#elementos son los siguientes meses. La lista tiene tantos elementos como
#el indicado en numero_meses.
#fecha_start ha de estar en el formato yyyy-mm-dd
def date_col_names( fecha_start, numero_meses):
    fecha_start=pd.to_datetime(fecha_start).date()
    year = fecha_start.year
    month = f"{fecha_start.month:02d}"
    fecha_start = datetime.datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
    fecha_start = add_months(start_date=fecha_start, months=1)
    nombre_DF = [fecha_start + relativedelta(months=i) for i in range(numero_meses)]
    nombre_DF = [f"{calendar.month_abbr[date.month]}-{date.year}" for date in nombre_DF]
    return nombre_DF


#Dada una cadena que contine los límites de edad
#genera la secuencia del rango de edades entre esos dos límites
#y lo devuelve en formato cadena separados por comas 
def seq_edades(rango_edades):
    try:
        if (len(rango_edades.split("-"))>1) :
            start, end = map(int, rango_edades.split("-"))
        else:
            raise ValueError()
        edades = [i for i in range(start, end + 1)]
        return edades
    except Exception as e:
        escribir_log('critical', "seq_edades Error {0}".format(str(e)))

#Dada una fecha de inicio y otra de fin genera una secuencia con distintos meses
#y la devuelve en formato string con los elementos separados por comas
def seq_dates(fecha_inicio, fecha_fin):
    dates = pd.date_range(start=fecha_inicio, end=fecha_fin, freq="MS").strftime("%Y-%m-%d")
    return dates
#Compara dos dataframes con el mismo número de filas y columnas.
#Hay que asegurarse que las columnas son las mismas y van en el mismo orden
#Devuelve la posición del primer elemento diferente.
#Si no hay difencia devuelve none
#Si no se cumple que tengan la misma forma los dos df devuelve un
#texto con el error
def obtener_celda_distinta( df1,df2):
    if df1.shape[1]==df2.shape[1]:
        if df1.shape[0]==df2.shape[0]:
            for i in df1.columns:
                Igual=np.where(df1[i]==df2[i], 0,1)
                if Igual.sum()!=0:
                    return [Igual.tolist().index(1), i]
            return None        
        else:
            escribir_log('error', "Error: los df tienen distintas filas")
            return None
    else:
        escribir_log('error', "Error: los df tienen distintas columnas")
        return None
    
#Crea el objeto de log y lo configura la primera vez que lo llama
#Escribe el mensaje con el tipo que se le pasa. Si el tipo de mensaje
#no es de los establecidos, no lo escribe.
def escribir_log(tipo_mensaje, mensaje):
    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        file_name=os.path.join(os.path.dirname( __file__ ), '..', '..','LOG', 'logs.log')
        file_handler = RotatingFileHandler(file_name, maxBytes=1000000, backupCount=10)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    match tipo_mensaje:
        case 'error':
            logger.error(mensaje)
        case 'info':
            logger.info(mensaje)
        case 'warning':
            logger.warning(mensaje)
        case 'critical':
            logger.critical(mensaje)
        
