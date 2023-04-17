from fastapi import FastAPI
import pandas as pd
from ruteo.clusterizacion import clusterizacion
from ruteo.get_routing import routing
from typing import Union

app = FastAPI()

@app.get("/")
def home():
    return{"Home":"Please check the docs in /docs"}


@app.get("/{datos_in}")
async def read_item(datos_in:str, n_clusters:int=1,seed:int=None,dist_type:str='Haversine',algorithm:str='Genetico',ident:str='prueba',key_googlemaps: Union[str, None] = None):
    datos_in = (datos_in.split(";"))
    data_base = {"coordenadas": datos_in, "parametros" : {"n_clusters":n_clusters,"seed":seed}}
    df = pd.DataFrame(data=data_base["coordenadas"],columns=["coordenadas"])
    df = pd.DataFrame(df.coordenadas.str.split(',').tolist(),columns = ['codigo','longitud','latitud'])
    df.longitud =  df.longitud.astype(float)
    df.latitud =  df.latitud.astype(float)
    #Clusterization
    grupos,sede_grupos,df_sedes = clusterizacion(df,n_clusters,seed)
    coor_sedes = df_sedes.to_numpy()
    coor_sedes = coor_sedes[:,1:3]
    #Creation routes
    Resumen_df,df_plot,df_rutas = routing(grupos,n_clusters,sede_grupos,coor_sedes,seed,dist_type,algorithm,ident,key_googlemaps)

    Resumen_df_json = Resumen_df.to_dict(orient='dict')
    df_plot_json =  df_plot.to_dict(orient='dict')
    df_rutas_json = df_rutas.to_dict(orient='dict')

    out = {"resumen" : Resumen_df_json,
           "df_plot" : df_plot_json,
           "df_rutas" : df_rutas_json
           }

    return out