import pandas as pd
from datetime import datetime, timedelta
import os

# ==============================================================================
# LÓGICA DE NEGOCIO: COMPRAS
# ==============================================================================

def obtenir_expedient (nom_empresa):
    try:
        if pd.isna(nom_empresa):
            return "UNKNOWN"
        parts = str(nom_empresa).split(" ")
        if len(parts) >= 2:
            return parts[1]
        else:
            return "UNKNOWN"
    except: 
        return "ERROR"


def procesar_correccion_compras(file_real, 
                               file_ped, 
                               file_alb, 
                               file_fac, 
                               file_fec):

    """
    Función principal que recibe los 5 archivos subidos a la web
    y devuelve 4 DataFrames: (Informe, 
                              Huerfanos_Alb, 
                              Huerfanos_Fac, 
                              Pedidos_Inventados)
    """                           

    # 1. CARREGA ARXIUS PUJATS PER STRAMLIT

    try:
        # Feim servir engine = 'python' i sep = None per autodetectar el separador (, o ;)
        df_real = pd.read_csv(file_real, engine='python', sep=None)
        df_ped = pd.read_csv(file_ped, engine='python', sep=None)
        df_alb = pd.read_csv(file_alb, engine='python', sep=None)
        df_fac = pd.read_csv(file_fac, engine='python', sep=None)
        df_fec = pd.read_csv(file_fec, engine='python', sep=None)

    except Exception as e:
        return None, None, None, None, f"Error al carregar arxius: {str(e)}"

     # 2. LIMPIEZA DE TIPOS
    # Real
    df_real['R_FECHA_EMISION_C'] = pd.to_datetime(df_real['R_FECHA_EMISION_C'], dayfirst=True)
    df_real['R_IMPORTE_C'] = pd.to_numeric(df_real['R_IMPORTE_C'], errors='coerce').fillna(0.00)
    
    
    print(df_real)
