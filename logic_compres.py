import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import os
import logic_comu

# ==============================================================================
# 1. CARREGA ARXIUS
# ==============================================================================

#   0_DATOS_COMPRAS_REALES.csv
#   1_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv
#   2_DATOS_ALBARANES_COMPRA_ALUMNOS.csv
#   3_DATOS_FACTURAS_COMPRA_ALUMNOS.csv
#   4_FECHA_ENTREGA_TRABAJOS.csv


def carregaArxius(
    file_compres_real,
    file_dades_compra_comandes_alumne,
    file_dades_compra_albarans_alumne,
    file_dades_compra_factures_alumne,
):

    # Intentam llegirs el contingut dels fitxers
    try:
        # Feim servir engine='python' y sep=None
        # per autodetectar separador (, o ;)

        df_real = pd.read_csv(file_compres_real, sep=None, engine="python", dtype=str)
        df_ped = pd.read_csv(
            file_dades_compra_comandes_alumne, sep=None, engine="python", dtype=str
        )
        df_alb = pd.read_csv(
            file_dades_compra_albarans_alumne, sep=None, engine="python", dtype=str
        )
        df_fac = pd.read_csv(
            file_dades_compra_factures_alumne, sep=None, engine="python", dtype=str
        )

    except Exception as e:
        print(f"Error carregant els arxius: {e}")
        return None, None, None, None

    # Imprimim els df per verificar que s'han carregat correctament
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

    return df_real, df_ped, df_alb, df_fac


# ==============================================================================
# 1. FINAL CÀRREGA ARXIUS
# ==============================================================================

# ==============================================================================
# 3.1.3 DATA ENTREGA TREBALL
# ==============================================================================


def insertaDataEntregaTreball(df_real, grup, dataVto):
    # CARREGAM EN DATAFRAME LA PLANTILLA QUE JA TENIM DISSENYADA

    if grup == "ADG21O":
        df_dataEntrega = logic_comu.carregaCSV("ADG21O_DATA_LLIURAMENT_TASCA.csv")
    elif grup == "ADG32O":
        df_dataEntrega = logic_comu.carregaCSV("ADG32O_DATA_LLIURAMENT_TASCA.csv")

    # INSERIM COM A DATA DE ENTREGA DE LA TASA
    # LA DATA DE VENCIMENT DE LA TASCA
    df_dataEntrega["FECHA_ENTREGA"] = dataVto

    df_dataEntrega["FECHA_ENTREGA"] = pd.to_datetime(
        df_dataEntrega["FECHA_ENTREGA"], format="%Y-%m-%d"
    ).dt.date

    # INSERIM en df_real la nova columna ['R_FECHA_ENTREGA'] amb la data de
    # vencimient de la tasca
    df_real["R_FECHA_ENTREGA"] = dataVto
    df_real["R_FECHA_ENTREGA"] = pd.to_datetime(
        df_real["R_FECHA_ENTREGA"], format="%Y-%m-%d"
    ).dt.date
    # print("ABANS DE MODIFICAR DATA ENTREGA AMB st.data_editor")
    # print(df_real)

    # CREAM EDITOR DE DADES
    # Amb aquest editor podem modificar les
    # dates de lliurament de cada alumne
    # 'column_config' permet que la columna de data
    # faci servir un widget de calendari

    # Inicializar los datos en el estado de la sesión
    if "df_dataEntrega" not in st.session_state:
        st.session_state.df_dataEntrega = df_dataEntrega

    df_editat = st.data_editor(
        st.session_state.df_dataEntrega,
        column_config={
            "FECHA_ENTREGA": st.column_config.DateColumn(
                "Fecha de Entrega (AAAA-MM-DD)",
                format="YYYY-MM-DD",
            ),
            "EXPEDIENT": st.column_config.NumberColumn(
                "Expedient", disabled=True
            ),  # Bloqueamos edición de ID
            "EMPRESA_ALUMNO": st.column_config.TextColumn(
                "Empresa alumne", disabled=True
            ),  # Bloqueamos edición de Nombre
        },
        hide_index=True,
        width="stretch",
    )

    # Botó per desar els canvis
    if st.button("Desar canvis"):

        # Un cop modificades les dates en edited_df,
        # hem d'inserir aquesta data en df_real per poder comparar-la
        # amb la data en que la factures de compra estan disponibles
        # i determinar si l'alumnat ha d'haver registrat o no les
        # factures de compra

        # Canviam l'estat de la session de df_dataEntrega a df_editat,
        st.session_state.df_dataEntrega = df_editat
        st.success(
            "Les dates d'entrega s'han desat correctament en el dataframe (df_dataEntrega)"
        )
        # Inserim la data de entrega en df_real
        df_real = logic_comu.insereixDataEntregaEnDFDesti(
            df_real, "R_FECHA_ENTREGA", "R_EMPRESA_C", df_editat
        )

        # Comprovem si la funcio ha retornat None
        if df_real is None:
            return None

        # df_real no es NONE, podem continuar
        # Desam df_editat com a fitxer CSV per si l'hem de tornar
        # a utilitzar
        if grup == "ADG21O":
            nombre_archivo = "ADG21O_DATA_LLIURAMENT_TASCA.csv"
        elif grup == "ADG32O":
            nombre_archivo = "ADG32O_DATA_LLIURAMENT_TASCA.csv"

        logic_comu.desaCSV(df_editat, nombre_archivo, "LLISTATS_CSV")

        st.session_state.compres_insercio_data_entrega = True

        return df_real


# ==========================================================
# 3.1.4 NETEJA VARIABLES
# ==========================================================

# ==========================================================
# 3.1.5 COMANDES DUPLICADES
# ==========================================================


# ==========================================================
# 3.1.6 UNIO DE DATAFRAMES (merge)
# ==========================================================


def uneixDataFrames(df_real, df_ped, df_alb, df_fac):

    df_real_ped = logic_comu.unionDataFrames(
        df_real,
        df_ped,
        "R_NUMERO_CP",
        "A_NUMERO_CP",
        "left",
        "_real",
        "_ped",
        True,
    )

    # SI ALUMNE INTRODUEIX DUES COMANDES DIFERENTS, PERÒ EN LA 2A
    # INDICA EL MATEIX NUM DE COMANDA QUE L'ANTERIOR, PER TANT TENIM
    # DUES COMANDES DIFERENTS AMB NUM DE COMANDA IGUAL
    # QUAN FEM LA UNIÓ df_real i df_ped, TENIM:
    # R_NUMERO_CP <-> A_NUMERO_CP
    #    53749           53749
    #    -----           53749
    # EN df_real NOMÉS TENIM UNA COMANDA 53749
    # EN df_ped TENIM DUES FILES AMB EL MATEIX NUM DE COMANDA 53749
    # QUAN ES FA EL MERGE, EN EL DF_RESULTANT (df_real_ped),
    # ES CREA UNA FILA MÉS PER INTEGRAR LA COMANDA REPETIDA:
    # R_NUMERO_CP <-> A_NUMERO_CP
    #    53749           53749
    #    53749           53749
    # DE TAL FORMA QUE EN df_real_ped, ES DUPLICA LA COMANDA REAL,
    # DUPLICANT TOTS ELS ELEMENTS (CLIENT, IMPORT, DATA, etc.)
    # PER TANT ES FA NECESSARI NETEJAR AQUESTS VALORS DUPLICATS I
    # DEIXAR NOMES UN REGISTRE EN L'APARTAT DE DADES REALS.

    # VEURE IMATGE EXPLICATIVA EN IMATGES/MERGE_DUPLICAT.png

    # PER ELIMINAR ELS VALORS REALS EN LA COMANDA DUPLICADA, APLICAM
    # LES INSTRUCCIONS SEGÜENTS:

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

    # DESAM CSV
    carpetaDesti = "HISTORIC_CORRECCIONS"
    filename_df_real_ped = prefNomFitxerCorreccio + "df_real_ped.csv"
    logic_comu.desaCSV(df_real_ped, filename_df_real_ped, carpetaDesti)

    # UNIO ENTRE df_real i df_alb

    # No tenim cap relació directa entre df_real i df_alb
    # però amb l'ajuda de df_ped podem establir una relació indirecta
    # df_real <-> df_ped <-> NUM. COMANDA
    # df_ped <-> df_alb <-> EXPEDIENTE + REF. ODOO COMANDA COMPRA
    # A cada num. de comanda li correspon un (EXP. + REF. ODOO C-COMPRA)
    # D'aquesta manera assignam aquesta clau única a cada comanda real

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

    # DESAM CSV
    carpetaDesti = "HISTORIC_CORRECCIONS"
    filename_df_real = prefNomFitxerCorreccio + "df_real.csv"
    logic_comu.desaCSV(df_real, filename_df_real, carpetaDesti)

    # Ja podem fer merge entre df_real i df_alb, aplicant clau única,
    # però abans cal reanomenar la columna _merge (creada en el merge
    # anterior) per evitar problemes:

    df_real.rename(columns={"_merge": "_merge_01"}, inplace=True)

    df_real_alb = logic_comu.unionDataFrames(
        df_real,
        df_alb,
        "A_CLAU_UNICA_CP",
        "A_CLAU_UNICA_CA",
        "left",
        "_real",
        "_alb",
        True,
    )

    # DESAM CSV
    filename_df_real_alb = prefNomFitxerCorreccio + "df_real_alb.csv"
    logic_comu.desaCSV(df_real_alb, filename_df_real_alb, carpetaDesti)

    # UNIO ENTRE df_real i df_fac
    df_real_fac = logic_comu.unionDataFrames(
        df_real,
        df_fac,
        "A_CLAU_UNICA_CP",
        "A_CLAU_UNICA_CF",
        "left",
        "_real",
        "_fac",
        True,
    )

    # DESAM CSV
    filename_df_real_fac = prefNomFitxerCorreccio + "df_real_fac.csv"
    logic_comu.desaCSV(df_real_fac, filename_df_real_fac, carpetaDesti)

    return df_real_ped, df_real, df_real_alb, df_real_fac


# ==============================================================================
# 3.1.7 RESEARCH OF ORPHAN OPERATIONS
# ==============================================================================


def researchOrphanOperations(df_real, df_ped, df_alb, df_fac):

    # OBTENIM COMANDES ALUMNES ORFES.
    # Es a dir, un alumne ha introduit una comanda, la qual no
    # apareix en les dades reals df_real

    df_comandesOrfes = logic_comu.unionDataFrames(
        df_ped, df_real, "A_NUMERO_CP", "R_NUMERO_CP", "left", "_ped", "_real", True
    )

    df_nomesComandesOrfes = df_comandesOrfes[df_comandesOrfes["_merge"] == "left_only"]

    # DESAM CSV
    carpetaDesti = "HISTORIC_CORRECCIONS"
    filename_df_nomesComandesOrfes = (
        prefNomFitxerCorreccio + "df_nomesComandesOrfes.csv"
    )
    logic_comu.desaCSV(
        df_nomesComandesOrfes, filename_df_nomesComandesOrfes, carpetaDesti
    )

    # OBTENIM ALBARANS ALUMNES ORFES.
    # Es a dir, un alumne ha introduit un albarà, el qual no
    # apareix en les dades reals df_real

    df_alb_orfes = logic_comu.unionDataFrames(
        df_alb,
        df_real,
        "A_CLAU_UNICA_CA",
        "A_CLAU_UNICA_CP",
        "left",
        "_alb",
        "_real",
        True,
    )

    df_nomesAlbaransOrfes = df_alb_orfes[df_alb_orfes["_merge"] == "left_only"]

    # DESAM CSV
    filename_df_nomesAlbaransOrfes = (
        prefNomFitxerCorreccio + "df_nomesAlbaransOrfes.csv"
    )
    logic_comu.desaCSV(
        df_nomesAlbaransOrfes, filename_df_nomesAlbaransOrfes, carpetaDesti
    )

    # OBTENIM FACTURES ALUMNES ORFES.
    # Es a dir, un alumne ha introduit una factura, el qual no
    # apareix en les dades reals df_real

    df_fac_orfes = logic_comu.unionDataFrames(
        df_fac,
        df_real,
        "A_CLAU_UNICA_CF",
        "A_CLAU_UNICA_CP",
        "left",
        "_fac",
        "_real",
        True,
    )

    df_nomesFacturesOrfes = df_fac_orfes[df_fac_orfes["_merge"] == "left_only"]

    # DESAM CSV
    filename_df_nomesFacturesOrfes = (
        prefNomFitxerCorreccio + "df_nomesFacturesOrfes.csv"
    )
    logic_comu.desaCSV(
        df_nomesFacturesOrfes, filename_df_nomesFacturesOrfes, carpetaDesti
    )

    return df_nomesComandesOrfes, df_nomesAlbaransOrfes, df_nomesFacturesOrfes


# ==============================================================================
# 3.1.8 CORRECCIO D'OPERACIONS - COMANDES
# ==============================================================================


def correccioComandes(df_real_ped, prefNomFitxerCorreccio):

    informe_pedidos = []

    for index, row in df_real_ped.iterrows():
        info_pedidos = {
            "NUM. COMANDA COMPRA INICIAL": row["R_NUMERO_CP"],
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
            "DATA ENTREGA TASCA": row["R_FECHA_ENTREGA"],
            "DATA FACTURA COMPRA DISPONIBLE": pd.to_datetime(row["R_FECHA_EMISION_C"])
            + timedelta(days=1),
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

        # DETERMINAM SI FACTURA DE COMPRA ESTÀ DISPONIBLE
        dataEntregaTasca = pd.to_datetime(row["R_FECHA_ENTREGA"])
        dataDisponibleFactura = pd.to_datetime(row["R_FECHA_EMISION_C"]) + timedelta(
            days=1
        )
        if dataEntregaTasca >= dataDisponibleFactura:
            estatFactEsperat = "TOTALMENTE FACTURADO"
            if str(row["A_ESTADO_FACTURACION_CP"]).strip().upper() == estatFactEsperat:
                info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "✅"
            else:
                info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "❌"
        else:
            estatFactEsperat = "FACTURAS EN ESPERA"
            if str(row["A_ESTADO_FACTURACION_CP"]).strip().upper() == estatFactEsperat:
                info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "✅"
            else:
                info_pedidos["COMPROVACIO ESTAT FACTURACIO COMANDA"] = "❌"

        informe_pedidos.append(info_pedidos)

    # CREAM DF CORRECCIO COMANDES COMPRA
    dfCorrecioComandesCompra = pd.DataFrame(informe_pedidos)

    fileName = prefNomFitxerCorreccio + "InformeCorreccióComandesCompra.csv"

    logic_comu.desaCSV(dfCorrecioComandesCompra, fileName, "HISTORIC_CORRECCIONS")

    return dfCorrecioComandesCompra


"""

# ==============================================================================
# 5.2. LÒGICA DE CORRECCIO ALBARANS
# ==============================================================================


informe_albarans = []

for index, row in df_real_alb.iterrows():
    info_albarans = {
        "NUM. COMANDA COMPRA INICIAL": row["R_NUMERO_CP"],
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

    if row["R_IMPORTE_C"] != row["A_IMPORTE_CA"]:
        info_albarans["COINCIDEIXEN IMPORTS"] = "❌"

    if str(row["A_ESTADO_CA"]).strip().upper() == "HECHO":
        info_albarans["COMPROVACIO ESTAT ALBARÀ"] = "✅"

    informe_albarans.append(info_albarans)


# CREAM DF CORRECCIO ALBARANS COMPRA
dfCorrecioAlbaransCompra = pd.DataFrame(informe_albarans)

fileName = "22_InformeCorreccioAlbaransCompra.xlsx"
logic_comu.exportToExcel(dfCorrecioAlbaransCompra, fileName)


# ==============================================================================
# 5.3. LÒGICA DE CORRECCIO FACTURES
# ==============================================================================


informe_factures = []

for index, row in df_real_fac.iterrows():
    info_factures = {
        "NUM. COMANDA COMPRA INICIAL": row["R_NUMERO_CP"],
        "DATA ENTREGA TASCA": row["R_FECHA_ENTREGA"],
        "FACTURA COMPRA DISPONIBLE EN DATA ENTREGA": "",
        "FACTURA COMPRA REGISTRADA EN ODOO": "",
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
        "ALUMNE - IMPORT": row["A_IMPORTE_CF"],
        "COINCIDEIXEN IMPORTS": "✅",
    }

    # FACTURA DE COMPRA REGISTRADA EN ODOO
    if (
        str(row["A_EMPRESA_CF"]).strip().upper() == "NAN"
        and str(row["A_PROVEEDOR_CF"]).strip().upper() == "NAN"
        and str(row["A_FECHA_EMISION_CF"]).strip().upper() == "NAT"
        and str(row["A_NUMERO_CF"]).strip().upper() == "NAN"
        and str(row["A_IMPORTE_CF"]).strip().upper() == "NAN"
    ):
        info_factures["FACTURA COMPRA REGISTRADA EN ODOO"] = "NO - ❌"
        info_factures["ALUMNE - EMPRESA ALUMNE"] = "❌ - SENSE DADES"
        info_factures["ALUMNE - PROVEÏDOR"] = "❌ - SENSE DADES"
        info_factures["ALUMNE - DATA EMISIÓ"] = "❌ - SENSE DADES"
        info_factures["ALUMNE - NUM FACTURA"] = "❌ - SENSE DADES"
        info_factures["ALUMNE - IMPORT"] = "❌ - SENSE DADES"

    else:
        info_factures["FACTURA COMPRA REGISTRADA EN ODOO"] = "SI - ✅"

    dataEntregaTasca = row["R_FECHA_ENTREGA"]
    dataDisponibleFactura = row["R_FECHA_EMISION_C"] + timedelta(days=1)
    if dataEntregaTasca >= dataDisponibleFactura:
        info_factures["FACTURA COMPRA DISPONIBLE EN DATA ENTREGA"] = "SI - ✅"
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

        if row["R_FECHA_EMISION_C"] != row["A_FECHA_EMISION_CF"]:
            info_factures["COINCIDEIXEN DATES EMISIÓ"] = "❌"

        if row["R_NUMERO_CF"] != row["A_NUMERO_CF"]:
            info_factures["COINCIDEIXEN NUM FACTURA"] = "❌"

        if row["R_IMPORTE_C"] != row["A_IMPORTE_CF"]:
            info_factures["COINCIDEIXEN IMPORTS"] = "❌"

    else:
        info_factures["FACTURA COMPRA DISPONIBLE EN DATA ENTREGA"] = "NO - ❌"
        print(str(row["A_EMPRESA_CF"]).strip().upper())
        print(str(row["A_PROVEEDOR_CF"]).strip().upper())
        print(str(row["A_FECHA_EMISION_CF"]).strip().upper())
        print(str(row["A_NUMERO_CF"]).strip().upper())
        print(str(row["A_IMPORTE_CF"]).strip().upper())
        print("--------------------------------")
        if str(row["A_EMPRESA_CF"]).strip().upper() != "NAN":
            info_factures["COINCIDEIXEN EMPRESES"] = "❌"

        if str(row["A_PROVEEDOR_CF"]).strip().upper() != "NAN":
            info_factures["COINCIDEIXEN PROVEÏDORS"] = "❌"

        if str(row["A_FECHA_EMISION_CF"]).strip().upper() != "NAT":
            info_factures["COINCIDEIXEN DATES EMISIÓ"] = "❌"

        if str(row["A_NUMERO_CF"]).strip().upper() != "NAN":
            info_factures["COINCIDEIXEN NUM FACTURA"] = "❌"

        if str(row["A_IMPORTE_CF"]).strip().upper() != "NAN":
            info_factures["COINCIDEIXEN IMPORTS"] = "❌"

    informe_factures.append(info_factures)

# CREAM DF CORRECCIO FACTURES COMPRA
dfCorrecioFacturesCompra = pd.DataFrame(informe_factures)
fileName = "23_InformeCorreccioFacturesCompra.xlsx"
logic_comu.exportToExcel(dfCorrecioFacturesCompra, fileName)
"""
