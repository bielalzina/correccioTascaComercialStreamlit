import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logic_comu

# ==============================================================================
# LÓGICA DE NEGOCIO: COMPRAS
# ==============================================================================


def obtenir_expedient(nom_empresa):
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

if any(
    dadesCarregades is None
    for dadesCarregades in [df_real, df_ped, df_alb, df_fac, df_fechas]
):
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

# ==============================================================================
# INSERIM DATA ENTREGA TREBALL EN df_fac
# ==============================================================================

# CONVERTIM df_fechas['EMPRESA_ALUMNO'] i df_fechas['FECHA_ENTREGA'] en un diccionari
mapaDatesEntrega = dict(zip(df_fechas["EMPRESA_ALUMNO"], df_fechas["FECHA_ENTREGA"]))

# print(mapaDatesEntrega)

# INSERIM LA DATA EN df_fac
df_fac["A_FECHA_ENTREGA_FV"] = df_fac["A_EMPRESA_CF"].map(mapaDatesEntrega)


# for fila in df_fac.itertuples():
#     print(f"EMPRESA: {fila.A_EMPRESA_CF} - DATA: {fila.A_FECHA_ENTREGA_FV}")


# ==============================================================================
# 2. NETEJA TIPUS DE DADES
# ==============================================================================

# DATES

df_real["R_FECHA_EMISION_C"] = pd.to_datetime(df_real["R_FECHA_EMISION_C"])
df_ped["A_FECHA_ALTA_ODOO_CP"] = pd.to_datetime(df_ped["A_FECHA_ALTA_ODOO_CP"])
df_ped["A_FECHA_EMISION_CP"] = pd.to_datetime(df_ped["A_FECHA_EMISION_CP"])
df_alb["A_FECHA_ALTA_ODOO_CA"] = pd.to_datetime(df_alb["A_FECHA_ALTA_ODOO_CA"])
df_alb["A_FECHA_EMISION_CA"] = pd.to_datetime(df_alb["A_FECHA_EMISION_CA"])
df_fac["A_FECHA_EMISION_CF"] = pd.to_datetime(df_fac["A_FECHA_EMISION_CF"])
df_fac["A_FECHA_ENTREGA_FV"] = pd.to_datetime(df_fac["A_FECHA_ENTREGA_FV"])

# NUMERICS
df_real["R_IMPORTE_C"] = pd.to_numeric(df_real["R_IMPORTE_C"], errors="coerce").fillna(
    0.00
)
df_ped["A_IMPORTE_CP"] = pd.to_numeric(df_ped["A_IMPORTE_CP"], errors="coerce").fillna(
    0.00
)
df_alb["A_IMPORTE_CA"] = pd.to_numeric(df_alb["A_IMPORTE_CA"], errors="coerce").fillna(
    0.00
)
df_fac["A_IMPORTE_CF"] = pd.to_numeric(df_fac["A_IMPORTE_CF"], errors="coerce").fillna(
    0.00
)


# ==============================================================================
# 3. DUPLICATS
# ==============================================================================

# Real
DUPLICATS_DF_REAL_R_NUMERO_CP = df_real[df_real.duplicated("R_NUMERO_CP", keep=False)]
# DUPLICATS_DF_REAL_R_CLAU_UNICA = df_real[df_real.duplicated("CLAU_UNICA", keep=False)]

# Pedidos
DUPLICATS_DF_PED_A_NUMERO_CP = df_ped[df_ped.duplicated("A_NUMERO_CP", keep=False)]
DUPLICATS_DF_PED_A_CLAU_UNICA_CP = df_ped[
    df_ped.duplicated("A_CLAU_UNICA_CP", keep=False)
]

# Albaranes
DUPLICATS_DF_ALB_A_CLAU_UNICA_CA = df_alb[
    df_alb.duplicated("A_CLAU_UNICA_CA", keep=False)
]

# Facturas
DUPLICATS_DF_FAC_A_CLAU_UNICA_CF = df_fac[
    df_fac.duplicated("A_CLAU_UNICA_CF", keep=False)
]

# RESUM DUPLICATS

duplicats = {
    "DUPLICATS DF_REAL R_NUMERO_CP": len(DUPLICATS_DF_REAL_R_NUMERO_CP),
    # "DUPLICATS DF_REAL R_CLAU_UNICA": len(DUPLICATS_DF_REAL_R_CLAU_UNICA),
    "DUPLICATS DF_PED A_NUMERO_CP": len(DUPLICATS_DF_PED_A_NUMERO_CP),
    "DUPLICATS DF_PED A_CLAU_UNICA_CP": len(DUPLICATS_DF_PED_A_CLAU_UNICA_CP),
    "DUPLICATS DF_ALB A_CLAU_UNICA_CA": len(DUPLICATS_DF_ALB_A_CLAU_UNICA_CA),
    "DUPLICATS DF_FAC A_CLAU_UNICA_CF": len(DUPLICATS_DF_FAC_A_CLAU_UNICA_CF),
}

print("======================================================================")
print("RESUM DUPLICATS")
print("======================================================================")

for key, value in duplicats.items():
    if value > 0:
        parts = str(key).split(" ")
        if parts[1] == "DF_REAL":
            if parts[2] == "R_NUMERO_CP":
                print("NUM. PEDIDOS COMPRA DUPLICATS EN DF_REAL: " + str(value))
                print(DUPLICATS_DF_REAL_R_NUMERO_CP[["R_EMPRESA_C", "R_NUMERO_CP"]])
                print("---------------------------------------------------------------")
            # if parts[2] == "R_CLAU_UNICA":
            #    print("NUM. CLAUS UNIQUES DUPLICADES EN DF_REAL: " + str(value))
            #    print(DUPLICATS_DF_REAL_R_CLAU_UNICA[["R_EMPRESA_C", "CLAU_UNICA"]])
            #    print("---------------------------------------------------------------")
        if parts[1] == "DF_PED":
            if parts[2] == "A_NUMERO_CP":
                print("NUM. PEDIDOS COMPRA DUPLICATS EN DF_PED: " + str(value))
                print(DUPLICATS_DF_PED_A_NUMERO_CP[["A_EMPRESA_CP", "A_NUMERO_CP"]])
                print("---------------------------------------------------------------")
            if parts[2] == "A_CLAU_UNICA_CP":
                print("NUM. CLAUS UNIQUES DUPLICADES EN DF_PED: " + str(value))
                print(DUPLICATS_DF_PED_A_CLAU_UNICA_CP[["A_EMPRESA_CP", "CLAU_UNICA"]])
                print("---------------------------------------------------------------")
        if parts[1] == "DF_ALB":
            if parts[2] == "A_CLAU_UNICA_CA":
                print("NUM. CLAUS UNIQUES DUPLICADES EN DF_ALB: " + str(value))
                print(DUPLICATS_DF_ALB_A_CLAU_UNICA_CA[["A_EMPRESA_CA", "CLAU_UNICA"]])
                print("---------------------------------------------------------------")
        if parts[1] == "DF_FAC":
            if parts[2] == "A_CLAU_UNICA_CF":
                print("NUM. CLAUS UNIQUES DUPLICADES EN DF_FAC: " + str(value))
                print(DUPLICATS_DF_FAC_A_CLAU_UNICA_CF[["A_EMPRESA_CF", "CLAU_UNICA"]])
                print("---------------------------------------------------------------")
    if value == 0:
        print(key + " = " + str(value))
        print("---------------------------------------------------------------")

# ==============================================================================
# 4. UNIO DE TOTS ELS DATAFRAMES
# ==============================================================================

# df_ped + df_alb = DF_CPA

df_cpa = pd.merge(
    df_ped,
    df_alb,
    left_on="A_CLAU_UNICA_CP",
    right_on="A_CLAU_UNICA_CA",
    how="outer",
    suffixes=("_cp", "_ca"),
    indicator=True,
    # validate="one_to_one",
)

print("LEN DF_REAL: " + str(len(df_real)))
print("LEN DF_PED: " + str(len(df_ped)))
print("LEN DF_ALB: " + str(len(df_alb)))
print("LEN DF_FAC: " + str(len(df_fac)))
print("LEN DF_CPA: " + str(len(df_cpa)))

logic_comu.exportToExcel(df_cpa, "DF_CPA.xlsx")

df_cpa.rename(columns={"_merge": "_merge_df_cpa"}, inplace=True)

# df_cpa + df_fac = DF_CPAF

df_cpaf = pd.merge(
    df_cpa,
    df_fac,
    left_on="A_CLAU_UNICA_CP",
    right_on="A_CLAU_UNICA_CF",
    how="outer",
    suffixes=("_cp", "_cf"),
    indicator=True,
    # validate="one_to_one",
)

print("LEN DF_CPAF: " + str(len(df_cpaf)))

logic_comu.exportToExcel(df_cpaf, "DF_CPAF.xlsx")

df_cpaf.rename(columns={"_merge": "_merge_df_cpaf"}, inplace=True)

# df_cpaf + df_real = DF_FINAL

df_final = pd.merge(
    df_real,
    df_cpaf,
    left_on="R_NUMERO_CP",
    right_on="A_NUMERO_CP",
    how="outer",
    suffixes=("_real", "_cpaf"),
    indicator=True,
    # validate="one_to_one",
)

df_final = df_final.sort_values(by=["R_EMPRESA_C", "R_NUMERO_CP"])

# SI ALUMNE REPETEIX UN NUM DE COMANDA, PER EXEMPLE TE DUES
# FILES AMB EL MATEIX NUM DE COMANDA (PERO DIFERENT DETALL)
# EN DF_FINAL DUPLICA LA COMANDA REAL, DUPLICANT EL CLIENT REAL,
# IMPORT REAL, DATA REAL.
# PER TANT ES FA NECESSARI NETEJAR AQUESTS VALORS DUPLICATS I
# DEIXAR NOMES UN REGISTRE EN L'APARTAT DE DADES REALS.

mask = df_final.duplicated(subset=["R_NUMERO_CP"], keep="first")
columnes_a_netejar = [
    "R_IDTOTS_C",
    "R_ID_C",
    "R_EXPEDIENT_C",
    "R_EMPRESA_C",
    "R_ESTADO_FC",
    "R_PROVEEDOR_C",
    "R_FECHA_EMISION_C",
    "R_NUMERO_CA",
    "R_NUMERO_CF",
    "R_IMPORTE_C",
    "R_ACUMULADO_C",
]

df_final.loc[mask, columnes_a_netejar] = np.nan

print("LEN DF_FINAL: " + str(len(df_final)))

logic_comu.exportToExcel(df_final, "DF_FINAL.xlsx")


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
