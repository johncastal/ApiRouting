from fastapi import FastAPI,APIRouter
import pandas as pd
from ruteo.clusterizacion import clusterizacion
from ruteo.get_routing import routing
from typing import Union

app = FastAPI()

router = APIRouter()

@router.get("/")
async def home():
    return {"Home":"Please check the docs in /docs"}


@router.get("/{datos_in}")
async def read_item(datos_in:str, n_clusters:int=1,seed:int=None,dist_type:str='Haversine',algorithm:str='Genetic',objective:str="Distance",ident:str='0',key_googlemaps: Union[str, None] = None):
    datos_in = (datos_in.split(";"))
    data_base = {"coord": datos_in, "parametros" : {"n_clusters":n_clusters,"seed":seed}}
    df1 = pd.DataFrame(data=data_base["coord"],columns=["coord"])
    df = df1.coord.str.split(',', expand=True)
    df.columns = ['label', 'longitud', 'latitud']
    df.longitud =  df.longitud.astype(float)
    df.latitud =  df.latitud.astype(float)
    #Clusterization
    grupos,sede_grupos,df_sedes = clusterizacion(df,n_clusters,seed)
    coor_sedes = df_sedes.to_numpy()
    coor_sedes = coor_sedes[:,1:3]
    #Routes building
    Resumen_df,df_plot,df_rutas = routing(grupos,n_clusters,sede_grupos,coor_sedes,seed,dist_type,algorithm,objective,ident,key_googlemaps)

    Resumen_df_json = Resumen_df.to_dict(orient='dict')
    df_plot_json =  df_plot.to_dict(orient='dict')
    df_rutas_json = df_rutas.to_dict(orient='dict')

    out = {"summary" : Resumen_df_json,
           "df_plot" : df_plot_json,
           "df_routes" : df_rutas_json
           }

    return out


# Register the router with the FastAPI instance
app.include_router(router, prefix="/api")