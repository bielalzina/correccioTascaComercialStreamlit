import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logic_comu

# ==============================================================================
# LÓGICA DE NEGOCIO: COMPRAS
# ==============================================================================


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
R_NUMERO_CF	                    A_IMPORTE_CP	                    A_ORIGEN_CA	                           A_IMPORTE_CF
R_IMPORTE_C	                    A_ACUMULADO_CP	                    A_IMPORTE_CA	                        A_ACUMULADO_CF
R_ACUMULADO_C	                A_ESTADO_CP	                        A_ACUMULADO_CA	                        A_ESTADO_PAGO_CF
                                A_ESTADO_FACTURACION_CP	            A_ESTADO_CA	

"""

# ==============================================================================
# INSERIM DATA ENTREGA TREBALL EN df_fac
# ==============================================================================

df_fac = logic_comu.insereixDataEntregaEnDFDesti(
    df_fac, "A_FECHA_ENTREGA_CF", "A_EMPRESA_CF", df_fechas
)

# ==============================================================================
# INSERIM DATA ENTREGA TREBALL EN df_ped
# ==============================================================================

df_ped = logic_comu.insereixDataEntregaEnDFDesti(
    df_ped, "A_FECHA_ENTREGA_CP", "A_EMPRESA_CP", df_fechas
)

# ==============================================================================
# 2. NETEJA TIPUS DE DADES
# ==============================================================================

# df_real
df_real = logic_comu.netejaTipusDadesDFReal(df_real)

# df_ped
df_ped = logic_comu.netejaTipusDadesDFPed(df_ped)

# df_alb
df_alb = logic_comu.netejaTipusDadesDFAlb(df_alb)

# df_fac
df_fac = logic_comu.netejaTipusDadesDFFac(df_fac)

# ==============================================================================
# 3. DUPLICATS
# ==============================================================================


# A NIVELL DE COMPRES, LES UNIQUES OPERACIONS QUE PODEN SER DUPLICADES
# SON QUAN UN ALUMNE INTRODUEIX DOS COPS LA MATEIXA COMANDA, O BE
# INTRODUEIX DUES COMANDES DIFERENTS, PERÒ AMB EL MATEIX NUMEERO AMBDUES
# PER TOT AIXÒ, NOMES TINDREM EN COMPTE POSSIBLES DUPLICATS EN df_ped

# OBTENIM DF ANB COMANDES QUE TENEN ASSIGNAT EL MATEIX NUMERO
df_duplicats_df_ped_a_numero_cp = logic_comu.obtenirDuplicats(df_ped, "A_NUMERO_CP")

print(df_duplicats_df_ped_a_numero_cp)


# ==============================================================================
# 4. UNIO DE TOTS ELS DATAFRAMES
# ==============================================================================

# =========================================
# 4.1. df_real + df_ped + = df_real_ped
# =========================================

df_real_ped = logic_comu.unionDataFrames(
    df_real, df_ped, "R_NUMERO_CP", "A_NUMERO_CP", "left", "_real", "_ped", True
)


# logic_comu.exportToExcel(df_real_ped, "DF_REAL_PED_abans.xlsx")

# SI ALUMNE INTRODUEIX DUES COMANDES DIFERENTS, PERÒ EN LA 2A
# INDICA EL MATEIX NUM DE COMANDA QUE L'ANTERIOR, PER TANT TENIM
# DUES COMANDES DIFERENTS AMB NUM DE COMANDA IGUAL
# QUAN FEM LA UNIÓ df_real i df_ped, el df_resultant
# R_NUMERO_CP <-> A_NUMERO_CP
#    53749
# FILES AMB EL MATEIX NUM DE COMANDA (PERO DIFERENT DETALL)
# EN DF_FINAL DUPLICA LA COMANDA REAL, DUPLICANT EL CLIENT REAL,
# IMPORT REAL, DATA REAL.
# PER TANT ES FA NECESSARI NETEJAR AQUESTS VALORS DUPLICATS I
# DEIXAR NOMES UN REGISTRE EN L'APARTAT DE DADES REALS.

# VEURE IMATGE EXPLICATIVA EN IMATGES/MERGE_DUPLICAT.png

mask = df_real_ped.duplicated(subset=["R_NUMERO_CP"], keep="first")
columnes_a_netejar = [
    "R_IDTOTS_C",
    "R_ID_C",
    "R_EXPEDIENT_C",
    "R_EMPRESA_C",
    "R_ESTADO_FC",
    "R_PROVEEDOR_C",
    "R_FECHA_EMISION_C",
    "R_NUMERO_CP",
    "R_NUMERO_CA",
    "R_NUMERO_CF",
    "R_IMPORTE_C",
    "R_ACUMULADO_C",
]

df_real_ped.loc[mask, columnes_a_netejar] = np.nan

logic_comu.exportToExcel(df_real_ped, "DF_REAL_PED.xlsx")

# OBTENIM COMANDES ALUMNES ORFES.
# Es a dir, un alumne ha introduit una comanda, la qual no
# apareix en les dades reals df_real

df_comandesOrfes = logic_comu.unionDataFrames(
    df_ped, df_real, "A_NUMERO_CP", "R_NUMERO_CP", "left", "_ped", "_real", True
)


df_nomesComandesOrfes = df_comandesOrfes[df_comandesOrfes["_merge"] == "left_only"]

# logic_comu.exportToExcel(nomesComandesOrfes, "NOMES_COMANDES_ORFES.xlsx")

# print(df_nomesComandesOrfes)

# =========================================
# 4.2. df_real + df_alb = df_real_alb
# =========================================

# No tenim cap relació directa entre df_real i df_alb
# però amb l'ajuda de df_ped podem establir una relació indirecta
# df_real <-> df_ped <-> NUM. COMANDA
# df_ped <-> df_alb <-> EXPEDIENTE + REF. INTERNA ODOO COMANDA COMPRA
# A CADA NUM DE COMANDA LI CORRESPON UN (EXP. + REF. INTERNA ODOO COMANDA COMPRA)
# D'AQUESTA FORMA PODEM ASSIGNAR (EXP + REF. ODOO) A CADA NUM. COMANDA EN DF_REAL

df_real = logic_comu.unionDataFrames(
    df_real,
    df_ped[["A_NUMERO_CP", "A_CLAU_UNICA_CP"]],
    "R_NUMERO_CP",
    "A_NUMERO_CP",
    "left",
    "_real",
    "_ped",
    True,
)

# logic_comu.exportToExcel(df_real, "DF_REAL_AMB_CLAU_UNICA_CP.xlsx")

# ARA JA PODEM UNIR DF_REAL + DF_ALB

# ABANS CAL REANOMBRAR LA COLUMNA _MERGE PER EVITAR CONFLICTE
df_real.rename(columns={"_merge": "_merge_01"}, inplace=True)


df_real_alb = logic_comu.unionDataFrames(
    df_real, df_alb, "A_CLAU_UNICA_CP", "A_CLAU_UNICA_CA", "left", "_real", "_alb", True
)

# logic_comu.exportToExcel(df_real_alb, "DF_REAL_ALB.xlsx")

# OBTENIM ALBARANS ALUMNES ORFES.
# Es a dir, un alumne ha introduit un albarà, el qual no
# apareix en les dades reals df_real

df_alb_orfes = logic_comu.unionDataFrames(
    df_alb, df_real, "A_CLAU_UNICA_CA", "A_CLAU_UNICA_CP", "left", "_alb", "_real", True
)


df_nomesAlbaransOrfes = df_alb_orfes[df_alb_orfes["_merge"] == "left_only"]

# logic_comu.exportToExcel(df_nomesAlbaransOrfes, "NOMES_ALBARANS_ORFES.xlsx")


# =========================================
# 4.3. df_real + df_fac = df_real_fac
# =========================================

df_real_fac = logic_comu.unionDataFrames(
    df_real, df_fac, "A_CLAU_UNICA_CP", "A_CLAU_UNICA_CF", "left", "_real", "_fac", True
)

# logic_comu.exportToExcel(df_real_fac, "DF_REAL_FAC.xlsx")

# OBTENIM FACTURES ALUMNES ORFES.
# Es a dir, un alumne ha introduit una factura, el qual no
# apareix en les dades reals df_real

df_fac_orfes = logic_comu.unionDataFrames(
    df_fac, df_real, "A_CLAU_UNICA_CF", "A_CLAU_UNICA_CP", "left", "_fac", "_real", True
)


df_nomesFacturesOrfes = df_fac_orfes[df_fac_orfes["_merge"] == "left_only"]

# logic_comu.exportToExcel(df_nomesFacturesOrfes, "NOMES_FACTURES_ORFES.xlsx")


# ==============================================================================
# 5. LÒGICA DE CORRECCIO
# ==============================================================================

informe_pedidos = []
informe_albarans = []
informe_factures = []

# nomsColumnes = df_final.columns.tolist()
# print(nomsColumnes)


# ==============================================================================
# 5.1. LÒGICA DE CORRECCIO COMANDES
# ==============================================================================

for index, row in df_real_ped.iterrows():
    info_pedidos = {
        "EMPRESAULA - EMPRESA ALUMNE": row["R_EMPRESA_C"],
        "ALUMNE - EMPRESA ALUMNE": row["A_EMPRESA_CP"],
        "COINCIDEIXEN EMPRESES": "✅",
        "EMPRESAULA - PROVEÏDOR": row["R_PROVEEDOR_C"],
        "ALUMNE - PROVEÏDOR": row["A_PROVEEDOR_CP"],
        "COINCIDEIXEN PROVEÏDORS": "✅",
        "EMPRESAULA - DATA EMISIÓ": row["R_FECHA_EMISION_C"],
        "ALUMNE - DATA EMISIÓ": row["A_FECHA_EMISION_CP"],
        "COINCIDEIXEN DATES EMISIÓ": "✅",
        "EMPRESAULA - NUM COMANDA": row["R_NUMERO_CP"],
        "ALUMNE - NUM COMANDA": row["A_NUMERO_CP"],
        "COINCIDEIXEN NUM COMANDA": "✅",
        "EMPRESAULA - IMPORT": row["R_IMPORTE_C"],
        "ALUMNE - IMPORT": row["A_IMPORTE_CP"],
        "COINCIDEIXEN IMPORTS": "✅",
        "ESTAT COMANDA": row["A_ESTADO_CP"],
        "COMPROVACIO ESTAT COMANDA": "❌",
        "ESTAT FACTURACIO COMANDA": row["A_ESTADO_FACTURACION_CP"],
        "COMPROVACIO ESTAT FACTURACIO COMANDA": "❌",
    }

    if (
        str(row["R_EMPRESA_C"]).strip().upper()
        != str(row["A_EMPRESA_CP"]).strip().upper()
    ):
        info_pedidos["COINCIDEIXEN EMPRESES"] = "❌"

    if (
        str(row["R_PROVEEDOR_C"]).strip().upper()
        != str(row["A_PROVEEDOR_CP"]).strip().upper()
    ):
        info_pedidos["COINCIDEIXEN PROVEÏDORS"] = "❌"

    if row["R_FECHA_EMISION_C"] != row["A_FECHA_EMISION_CP"]:
        info_pedidos["COINCIDEIXEN DATES EMISIÓ"] = "❌"

    if row["R_NUMERO_CP"] != row["A_NUMERO_CP"]:
        info_pedidos["COINCIDEIXEN NUM COMANDA"] = "❌"

    if row["R_IMPORTE_C"] != row["A_IMPORTE_CP"]:
        info_pedidos["COINCIDEIXEN IMPORTS"] = "❌"

    if row["A_ESTADO_CP"] == "Pedido de compra":
        info_pedidos["COMPROVACIO ESTAT COMANDA"] = "✅"

    if row["A_FECHA_ENTREGA_CP"] >= row["A_FECHA_EMISION_CP"] + pd.Timedelta(days=1):
        if str(row["A_ESTADO_FACTURACION_CP"]).upper() == "TOTALMENTE FACTURADO":
            info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "✅"
        else:
            info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "❌"
    else:
        if str(row["A_ESTADO_FACTURACION_CP"]).upper() == "FACTURAS EN ESPERA":
            info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "✅"
        else:
            info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "❌"

    informe_pedidos.append(info_pedidos)


# CREAM DF CORRECCIO COMANDES COMPRA
dfCorrecioComandesCompra = pd.DataFrame(informe_pedidos)

fileName = "InformeCorreccióComandesCompra.xlsx"

logic_comu.exportToExcel(dfCorrecioComandesCompra, fileName)


"""
# ==============================================================================
# 5.2. LÒGICA DE CORRECCIO ALBARANS
# ==============================================================================

for index, row in df_final.iterrows():
    info_albarans = {
        "EMPRESAULA - EMPRESA ALUMNE": row["R_EMPRESA_C"],
        "ALUMNE - EMPRESA ALUMNE": row["A_EMPRESA_CA"],
        "COINCIDEIXEN EMPRESES": "✅",
        "EMPRESAULA - PROVEÏDOR": row["R_PROVEEDOR_C"],
        "ALUMNE - PROVEÏDOR": row["A_PROVEEDOR_CA"],
        "COINCIDEIXEN PROVEÏDORS": "✅",
        "EMPRESAULA - DATA EMISIÓ": row["R_FECHA_EMISION_C"],
        "ALUMNE - DATA EMISIÓ": row["A_FECHA_EMISION_CA"],
        "COINCIDEIXEN DATES EMISIÓ": "✅",
        "EMPRESAULA - NUM ALBARÀ": row["R_NUMERO_CA"],
        "ALUMNE - NUM ALBARÀ": row["A_NUMERO_CA"],
        "COINCIDEIXEN NUM ALBARÀ": "✅",
        "EMPRESAULA - IMPORT": row["R_IMPORTE_C"],
        "ALUMNE - IMPORT": row["A_IMPORTE_CA"],
        "COINCIDEIXEN IMPORTS": "✅",
        "ESTAT ALBARÀ": row["A_ESTADO_CA"],
        "COMPROVACIO ESTAT ALBARÀ": "❌",
    }

    if (
        str(row["R_EMPRESA_C"]).strip().upper()
        != str(row["A_EMPRESA_CA"]).strip().upper()
    ):
        info_albarans["COINCIDEIXEN EMPRESES"] = "❌"

    if (
        str(row["R_PROVEEDOR_C"]).strip().upper()
        != str(row["A_PROVEEDOR_CA"]).strip().upper()
    ):
        info_albarans["COINCIDEIXEN PROVEÏDORS"] = "❌"

    if row["R_FECHA_EMISION_C"] != row["A_FECHA_EMISION_CA"]:
        info_albarans["COINCIDEIXEN DATES EMISIÓ"] = "❌"

    if row["R_NUMERO_CA"] != row["A_NUMERO_CA"]:
        info_albarans["COINCIDEIXEN NUM ALBARÀ"] = "❌"

    if row["R_IMPORTE_C"] != row["A_IMPORTE_CP"]:
        info_pedidos["COINCIDEIXEN IMPORTS"] = "❌"

    if row["A_ESTADO_CP"] == "Pedido de compra":
        info_pedidos["COMPROVACIO ESTAT COMANDA"] = "✅"

    # COMPROVAM SI FACTURA ESTÀ DISPONIBLE
    dataEntregaTasca = row["A_FECHA_ENTREGA_FV"]
    dataDisponibleFactura = row["R_FECHA_EMISION_C"] + timedelta(days=1)

    if dataEntregaTasca < dataDisponibleFactura:
        estatFactEsperat = "FACTURAS EN ESPERA"
        if row["A_ESTADO_FACTURACION_CP"] == estatFactEsperat:
            info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "✅"
        else:
            info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "❌"

    else:
        estatFactEsperat = "TOTALMENTE FACTURADO"
        if row["A_ESTADO_FACTURACION_CP"] == estatFactEsperat:
            info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "✅"
        else:
            info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "❌"

    informe_pedidos.append(info_pedidos)


# CREAM DF CORRECCIO ALBARANS COMPRA
dfCorrecioAlbaransCompra = pd.DataFrame(informe_albarans)

# ==============================================================================
# 5.3. LÒGICA DE CORRECCIO FACTURES
# ==============================================================================


for index, row in df_final.iterrows():
    info_factures = {
        "EMPRESAULA - EMPRESA ALUMNE": row["R_EMPRESA_C"],
        "ALUMNE - EMPRESA ALUMNE": row["A_EMPRESA_CF"],
        "COINCIDEIXEN EMPRESES": "✅",
        "EMPRESAULA - PROVEÏDOR": row["R_PROVEEDOR_C"],
        "ALUMNE - PROVEÏDOR": row["A_PROVEEDOR_CF"],
        "COINCIDEIXEN PROVEÏDORS": "✅",
        "EMPRESAULA - DATA EMISIÓ": row["R_FECHA_EMISION_C"],
        "ALUMNE - DATA EMISIÓ": row["A_FECHA_EMISION_CF"],
        "COINCIDEIXEN DATES EMISIÓ": "✅",
        "EMPRESAULA - NUM FACTURA": row["R_NUMERO_CF"],
        "ALUMNE - NUM FACTURA": row["A_NUMERO_CF"],
        "COINCIDEIXEN NUM FACTURA": "✅",
        "EMPRESAULA - IMPORT": row["R_IMPORTE_C"],
        "ALUMNE - IMPORT": row["A_IMPORTE_CA"],
        "COINCIDEIXEN IMPORTS": "✅",
    }

    if (
        str(row["R_EMPRESA_C"]).strip().upper()
        != str(row["A_EMPRESA_CF"]).strip().upper()
    ):
        info_factures["COINCIDEIXEN EMPRESES"] = "❌"

    if (
        str(row["R_PROVEEDOR_C"]).strip().upper()
        != str(row["A_PROVEEDOR_CF"]).strip().upper()
    ):
        info_factures["COINCIDEIXEN PROVEÏDORS"] = "❌"

    if row["R_FECHA_EMISION_C"] != row["A_FECHA_EMISION_CP"]:
        info_factures["COINCIDEIXEN DATES EMISIÓ"] = "❌"

    if row["R_NUMERO_CF"] != row["A_NUMERO_CF"]:
        info_factures["COINCIDEIXEN NUM FACTURA"] = "❌"

    if row["R_IMPORTE_C"] != row["A_IMPORTE_CF"]:
        info_factures["COINCIDEIXEN IMPORTS"] = "❌"

    informe_factures.append(info_factures)

# CREAM DF CORRECCIO FACTURES COMPRA
dfCorrecioFacturesCompra = pd.DataFrame(informe_factures)
"""
