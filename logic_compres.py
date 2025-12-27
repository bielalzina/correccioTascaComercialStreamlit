import pandas as pd
from datetime import datetime, timedelta
import os
import logic_comu

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

# 1. CARREGA ARXIUS 
#   0_DATOS_COMPRAS_REALES.csv
#   1_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv
#   2_DATOS_ALBARANES_COMPRA_ALUMNOS.csv
#   3_DATOS_FACTURAS_COMPRA_ALUMNOS.csv
#   4_FECHA_ENTREGA_TRABAJOS.csv

df_real = logic_comu.carregaCSV("0_DATOS_COMPRAS_REALES.csv")
df_ped = logic_comu.carregaCSV("1_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv")
df_alb = logic_comu.carregaCSV("2_DATOS_ALBARANES_COMPRA_ALUMNOS.csv")
df_fac = logic_comu.carregaCSV("3_DATOS_FACTURAS_COMPRA_ALUMNOS.csv")
df_fechas = logic_comu.carregaCSV("4_FECHA_ENTREGA_TRABAJOS.csv")

if any(dadesCarregades is None for dadesCarregades in [df_real, df_ped, df_alb, df_fac, df_fechas]):
  print("NO ES POT SEGUIR EXECUTANT EL PROGRAMA PER FALTA DE DADES")
  exit()

# print(df_real)
# print("====================================")
# print(df_ped)
# print("====================================")
# print(df_alb)
# print("====================================")
# print(df_fac)
# print("====================================")
# print(df_fechas)
# print("====================================")

"""
0_DATOS_COMPRAS_REALES.csv	    1_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv  2_DATOS_ALBARANES_COMPRA_ALUMNOS.csv  3_DATOS_FACTURAS_COMPRA_ALUMNOS.csv
ID-TOTS	                        ID-TOTS	                            ID-TOTS	                                ID-TOTS
CLAU_UNICA	                    CLAU_UNICA	                        CLAU_UNICA	                            CLAU_UNICA
ID	                            A_CON_CP	                        A_CON_CA	                            A_CON_CF
R_EXPEDIENT_C	                A_EXPEDIENT_CP	                    A_EXPEDIENT_CA	                        A_EXPEDIENT_CF
R_EMPRESA_C	                    A_EMPRESA_CP	                    A_EMPRESA_CA	                        A_EMPRESA_CF
R_ESTADO_FC	                    A_REF_ODOO_CP	                    A_REF_ODOO_CA	                        A_REF_ODOO_CF
R_PROVEEDOR_C	                A_FECHA_ALTA_ODOO_CP	            A_FECHA_ALTA_ODOO_CA	                A_PROVEEDOR_CF
R_FECHA_EMISION_C	            A_NUMERO_CP	                        A_NUMERO_CA	                            A_NUMERO_CF
R_NUMERO_CP	                    A_FECHA_EMISION_CP	                A_FECHA_EMISION_CA	                    A_FECHA_EMISION_CF
R_NUMERO_CA	                    A_PROVEEDOR_CP	                    A_PROVEEDOR_CA	                        A_ORIGEN_CF
R_NUMERO_CF	                    A_IMPORTE_CP	                    A_ORIGEN_CA	                            A_IMPORTE_CF
R_IMPORTE_C	                    A_ACUMULADO_CP	                    A_IMPORTE_CA	                        A_ACUMULADO_CF
R_ACUMULADO_C	                A_ESTADO_CP	                        A_ACUMULADO_CA	                        A_ESTADO_PAGO_CF
                                A_ESTADO_FACTURACION_CP	            A_ESTADO_CA	

"""

# 2. NETEJA TIPUS DE DADES

# DATES

df_real['R_FECHA_EMISION_C'] = pd.to_datetime(df_real['R_FECHA_EMISION_C'], dayfirst=True)
df_ped['A_FECHA_ALTA_ODOO_CP'] = pd.to_datetime(df_ped['A_FECHA_ALTA_ODOO_CP'], dayfirst=True)
df_ped['A_FECHA_EMISION_CP'] = pd.to_datetime(df_ped['A_FECHA_EMISION_CP'], dayfirst=True)
df_alb['A_FECHA_ALTA_ODOO_CA'] = pd.to_datetime(df_alb['A_FECHA_ALTA_ODOO_CA'], dayfirst=True)
df_alb['A_FECHA_EMISION_CA'] = pd.to_datetime(df_alb['A_FECHA_EMISION_CA'], dayfirst=True)
df_fac['A_FECHA_EMISION_CF'] = pd.to_datetime(df_fac['A_FECHA_EMISION_CF'], dayfirst=True)
df_fechas['FECHA_ENTREGA'] = pd.to_datetime(df_fechas['FECHA_ENTREGA'], dayfirst=True)

# NUMERICS
df_real['R_IMPORTE_C'] = pd.to_numeric(df_real['R_IMPORTE_C'], errors='coerce').fillna(0.00)
df_ped['A_IMPORTE_CP'] = pd.to_numeric(df_ped['A_IMPORTE_CP'], errors='coerce').fillna(0.00)
df_alb['A_IMPORTE_CA'] = pd.to_numeric(df_alb['A_IMPORTE_CA'], errors='coerce').fillna(0.00)
df_fac['A_IMPORTE_CF'] = pd.to_numeric(df_fac['A_IMPORTE_CF'], errors='coerce').fillna(0.00)

# 3. DUPLICATS NUMERO COMANDA

"""
def procesar_correccion_compras(file_real, 
                               file_ped, 
                               file_alb, 
                               file_fac, 
                               file_fec):

    
    # Función principal que recibe los 5 archivos subidos a la web
    # y devuelve 4 DataFrames: 
    # (Informe, Huerfanos_Alb, Huerfanos_Fac, Pedidos_Inventados)
                       

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
"""