import os
import pandas as pd
from funcionalidades.funcsifv2 import funcsif
from funcionalidades.myfunc import mesChar_toNum
import numpy as np

p=funcsif()
user="MEM"
p.inicializar(user)


flag=False #Si masterDF se borra hay que ponerlo a False
##### SETTINGS #####
meses_max_sim =18  

#if config_especie == "TURBOT":
#campos_granjas = ['Cervo_P', 'Lira_P', 'Merexo_P', 'Couso_P', 'Oye_P', 'Palmeira_P', 'Quilmas_P', 'Vilan_P', 'Tocha_P', 'SSF', 'SSF_Iberia']
campos_granjas=['SSF_Iberia']
#elif config_especie == "SOLE":
#    campos_granjas = ['Cervo Sole', 'Tocha Sole', 'Hafnir_P', 'Couso i+d', 'Anglet_P']
campos_granjas.sort()
p.crear_estructura_if(campos_granjas, meses_max_sim)
if os.path.exists(p.get_attr("path_default_campos_granjas")):
    default_campos_granjas = pd.read_csv(p.get_attr("path_default_campos_granjas"))['Granja'].tolist()
else:
    default_campos_granjas = campos_granjas
    df = pd.DataFrame({'Granja': default_campos_granjas})
    df.to_csv(p.get_attr("path_default_campos_granjas"), index=False)


if os.path.exists(p.get_attr("path_default_fecha")):
    default_fecha = pd.to_datetime(pd.read_csv(p.get_attr("path_default_fecha"))['date'].iloc[0]).date()
else:
    default_fecha = pd.to_datetime("2024-05-31").date()



resultado=p.import_initial_data(continue_flag = flag,fecha = default_fecha)

#Granjas
#granjas=['Cervo_P', 'Lira_P', 'Merexo_P', 'Couso_P', 'Oye_P',  'Palmeira_P', 'Quilmas_P', 'Vilán_P', 'Tocha_P', 'SSF_Iberia'] #################Para mis pruebas
granjas=['SSF_Iberia']

all_alevines= p.import_format_func(path =p.get_attr("path_df_alevines"), val_name = "Num")


#print(all_alevines.shape)
pesos_medios_entrada_alev=pd.read_csv(p.get_attr("path_df_alevines_pm_cv"))
pesos_medios_entrada_alev['CV']=pesos_medios_entrada_alev['CV']/100


#print(pesos_medios_entrada_alev.shape)
all_ventas= p.import_format_func(p.get_attr("path_df_despesques"), val_name='BiomasaVentas')

#print(all_ventas.shape)
all_dispersion_df =p.import_format_func(path = p.get_attr("path_df_dispersion"), val_name = "cv", from_por = True)


#print(all_dispersion_df.shape)
all_edad_venta_df =p.import_format_func(path = p.get_attr("path_df_edad_pescas"), val_name = "Edad")

#all_edad_venta_df.to_csv(r"C:\Users\MEM\Documents\IFv2\TURBOT\MEM\resultado.csv", index=False)

#print(all_edad_venta_df.shape)
all_acabar_gen =p.import_format_acabar_gen() #Es None en Python, en R es vacío pero no escribe nada si lo pasas a fichero


##print(all_acabar_gen.shape)
#print("NULL")
all_mortalidad = p.import_format_func(path =p.get_attr("path_df_losses"), val_name = "Num")



#print(all_mortalidad.shape)
all_reparto_mort = p.import_format_mort_dist()   #Son distintos en R y en python



#print(all_reparto_mort.shape)
all_ajustes_mort_gen = p.import_format_mort_aj_gen_func()


##print(all_ajustes_mort_gen.shape)
#print("NULL")
culling_edad = pd.read_csv(p.get_attr("path_default_culling_por"))["Edad"].values.item(0)
#print(culling_edad.shape)
culling_por = pd.read_csv(p.get_attr("path_default_culling_por"))["Por"].values.item(0)
#print(culling_por.shape)
curvas= pd.read_csv(p.get_attr("path_curvas"))


#print(curvas.shape)
all_crecimientoD= p.import_format_func(path =p.get_attr("path_df_desired_growth"), val_name = "Tones")


#print(all_crecimientoD.shape)
all_ajustes_edad= p.import_format_growth_aj_edad_func()



#if hasattr(all_ajustes_edad, '__len__'):
#    print(all_ajustes_edad.shape)
#else:
#    print(all_ajustes_edad) 
all_ajustes_talla = p.import_format_growth_aj_talla_o_gen_func(type = "Talla")


#if hasattr(all_ajustes_talla, '__len__'):
#    print(all_ajustes_talla.shape)
#else:
#    print(all_ajustes_talla) 
all_ajustes_gen = p.import_format_growth_aj_talla_o_gen_func(type = "Gen")


#if hasattr(all_ajustes_gen, '__len__'):
#    print(len(all_ajustes_gen))
#else:
#    print(all_ajustes_gen) 

d_growth_type = pd.read_csv(p.get_attr("path_d_growth_type"))
d_growth_type= d_growth_type.loc[d_growth_type['Button'] == "d_growth_type", "State"].values.item(0)
meses_sim=12

for loop in range(1,(meses_sim+1)) :
    
    mes_loop = pd.to_datetime(resultado['FechaFin'].unique()[0]).month
    ano_loop = pd.to_datetime(resultado['FechaFin'].unique()[0]).year
    print(mes_loop, ano_loop)

    resultado=p.set_alevines(resultado_df = resultado, all_alevines_df =all_alevines,\
        peces_x_tanque = 2500, pm_y_cv_df = pesos_medios_entrada_alev)          #son distintos los valores de PEsomedio y Biomasa de los tanques inventados. Las diferencias
                                                                                #son mínimas
    
    
    
    resultado=p.set_ventas(resultado_df = resultado, all_ventas_df = all_ventas, all_dispersion_df = all_dispersion_df,
        all_edad_venta_df = all_edad_venta_df, all_acabar_gen = all_acabar_gen, continue_flag= flag, loop = loop)     #Si se intercambian los df de resultado_df de R y Python, sale
                                                                                                                      #el mismo resultado
    
    
  
    resultado=p.set_bajas(resultado_df = resultado, all_reparto_mort_df = all_reparto_mort, all_ajustes_mort_gen_df = all_ajustes_mort_gen, 
                                culling_edad = culling_edad, culling_por = culling_por, all_mortalidad_df = all_mortalidad)
    
    
    #resultado_df.to_csv(r"C:\Users\MEM\Documents\IFv2\TURBOT\MEM\desordenado_py.csv", index=False)
    ##resultado=resultado.sort_values(["PesoMedio","Tanque","Fecha"], ascending=[False, False,False]).copy()

    
    resultado=p.set_crecimiento(resultado_df = resultado, curvas_df = curvas,  all_crecimientoD_df = all_crecimientoD,  
                                            all_ajustes_edad_df = all_ajustes_edad,  all_ajustes_talla_df = all_ajustes_talla, 
                                            all_ajustes_gen_df = all_ajustes_gen, d_growth_type = d_growth_type)

    
    #escribir=resultado.sort_values(['NumFinal'],ascending=[False]).copy()
    #escribir=escribir.loc[escribir['NumFinal']>0,'NumFinal']
    #print(escribir)
    
    resultado = p.set_next_and_write(resultado_df = resultado, continue_flag = flag, loop = loop)
    
    
#resultado=pd.read_csv(r"C:\Users\MEM\Documents\IFv2\TURBOT\MEM\resultado_antes.csv")
p.set_resultado()

