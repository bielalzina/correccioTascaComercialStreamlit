import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import os
import logic_comu
import glob


def correccioCompres(grup, tasca):

    # ==============================================================================
    # 1. CARREGA ARXIUS
    # ==============================================================================

    #   ADG32O_02.12_00_DATOS_COMPRAS_REALES.csv
    #   ADG32O_02.12_01_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv
    #   ADG32O_02.12_02_DATOS_ALBARANES_COMPRA_ALUMNOS.csv
    #   ADG32O_02.12_03_DATOS_FACTURAS_COMPRA_ALUMNOS.csv
    #   ADG32O_02.12_04_FECHA_ENTREGA_TRABAJOS.csv

    # El grup i la tasca vendran informats com a parametres de la funció, d'aquesta
    # manera definirem dos prefixos pels arxius:

    prefNomFitxerSOURCES = grup + "_" + tasca + "_"
    # prefNomFitxerSOURCES = "ADG32O_02.12_"

    prefNomFitxerCORRECCIO = grup + "_" + tasca + "_" + "COMPRES_"
    # prefNomFitxerCORRECCIO = "ADG32O_02.12_COMPRES_"

    # Carpeta LLISTATS_CSV
    carpetaCSV = "LLISTATS_CSV"

    # Carpeta HISTORIC_CORRECCIONS
    carpetaHC = "HISTORIC_CORRECCIONS"

    # Abans de recuperar les fonts de dades, per fer les correccions, eliminarem tots els arxius existents relacionats amb les COMPRES:

    # Definim ruta y patró
    # El asterisco (*) actúa como comodín para cualquier carácter posterior

    rutaHistoricsCorreccions = os.getcwd() + "/" + carpetaHC + "/"
    patro = rutaHistoricsCorreccions + prefNomFitxerCORRECCIO + "*"

    # patro = C:\Users\GABRIEL\Documents\GitHub\correccioTascaComercialStreamlit\HISTORIC_CORRECCIONS\ADG32O_02.12_COMPRES_*

    # Obté la lista de fitxers i elimina els existents
    archivos_a_eliminar = glob.glob(patro)

    for ruta_archivo in archivos_a_eliminar:
        try:
            os.remove(ruta_archivo)
            # print(f"Eliminado: {os.path.basename(ruta_archivo)}")
        except OSError as e:
            print(f"Error: {e.strerror}")

    # Intentam llegirs el contingut dels fitxers mitjançant la funcio carregaCSV
    # que esta en el fitxer logic_comu.py
    # carregaCSV(fileName, carpeta):

    fileNameReal = prefNomFitxerSOURCES + "00_DATOS_COMPRAS_REALES.csv"
    fileNamePed = prefNomFitxerSOURCES + "01_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv"
    fileNameAlb = prefNomFitxerSOURCES + "02_DATOS_ALBARANES_COMPRA_ALUMNOS.csv"
    fileNameFac = prefNomFitxerSOURCES + "03_DATOS_FACTURAS_COMPRA_ALUMNOS.csv"
    fileNameFechaEntrega = prefNomFitxerSOURCES + "04_FECHA_ENTREGA_TRABAJOS.csv"

    try:
        df_real = logic_comu.carregaCSV(fileNameReal, carpetaCSV)
        df_ped = logic_comu.carregaCSV(fileNamePed, carpetaCSV)
        df_alb = logic_comu.carregaCSV(fileNameAlb, carpetaCSV)
        df_fac = logic_comu.carregaCSV(fileNameFac, carpetaCSV)
        df_fechaEntrega = logic_comu.carregaCSV(fileNameFechaEntrega, carpetaCSV)

    except Exception as e:
        print(f"Error carregant els arxius: {e}")

    # Inserim la data de entrega en df_real
    # Si volem corregir les compres, cal disposar d'aquesta data en el
    # dataframe de dades reals, per podetr determinar si s'han
    # registrat les factures de compra a data de entrega
    # Pero, abans, netejem els tipus de dades del dataframe de data de entrega

    df_fechaEntrega = logic_comu.netejaTipusDadesDFFechaEntrega(df_fechaEntrega)

    df_real = logic_comu.insereixDataEntregaEnDFDesti(
        df_real, "R_FECHA_ENTREGA", "R_EMPRESA_C", df_fechaEntrega
    )

    # També obtindrem un llistat dels alumnes que no han lliurat la tasca
    # No corregirem una tasca que no dsiposam
    df_alumnes_morosos = df_fechaEntrega[
        df_fechaEntrega["Estat entrega"] == "NO ENTREGADA"
    ]

    # DESAM CSV MOROSOS

    filename = prefNomFitxerCORRECCIO + "01_ALUMNES_MOROSOS.csv"
    logic_comu.desaCSV(df_alumnes_morosos, filename, carpetaHC)

    # NETEJA DE TIPOS DE DADES
    df_real = logic_comu.netejaTipusDadesDFReal(df_real)
    df_ped = logic_comu.netejaTipusDadesDFPed(df_ped)
    df_alb = logic_comu.netejaTipusDadesDFAlb(df_alb)
    df_fac = logic_comu.netejaTipusDadesDFFac(df_fac)

    # COMANDES DUPLICADES
    # A nivell de compres, les operacions que normalment es dupliquen son les
    # comandes: l'alumne introdueix 2 cops la mateixa comanda o bé introdueix dues
    # comandes diferents, introduint el mateix número de comanda. Per tot això,
    # nomes tindrem en compte possibles duplicats en df_ped.

    df_ped_duplicats = logic_comu.obtenirDuplicats(df_ped, "A_NUMERO_CP")

    # DESAM CSV COMANDES DUPLICADES
    filename = prefNomFitxerCORRECCIO + "02_COMANDES_DUPLICADES.csv"
    logic_comu.desaCSV(df_ped_duplicats, filename, carpetaHC)

    # Filtram df_real amb els alumnes que han lliurat la tasca. No cap corregir una
    # tasca que no dsiposam

    df_real_alumnes_tasca_entregada = df_real.merge(
        df_fechaEntrega[df_fechaEntrega["Estat entrega"] == "ENTREGADA"],
        left_on="R_EXPEDIENT_C",
        right_on="Expediente",
        how="inner",
    )

    # DESAM CSV DF REAL FILTRAT
    filename = prefNomFitxerCORRECCIO + "03_DF_REAL_ALUMNES_TASCA_ENTREGADA.csv"
    logic_comu.desaCSV(df_real_alumnes_tasca_entregada, filename, carpetaHC)

    # UNIO DATAFRAMES
    # df_real_ped = df_real_filtrada + df_ped

    df_real_ped = logic_comu.unionDataFrames(
        df_real_alumnes_tasca_entregada,
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

    # APLICAM el FILTRE

    df_real_ped.loc[mask, columnes_a_netejar] = np.nan

    # DESAM CSV "UNIO_DF_REAL_PED.csv"
    filename = prefNomFitxerCORRECCIO + "04_UNIO_DF_REAL_PED.csv"
    logic_comu.desaCSV(df_real_ped, filename, carpetaHC)

    # UNIO DATAFRAMES
    # df_real_alb = df_real_filtrada + df_alb

    # No tenim cap relació directa entre df_real i df_alb
    # però amb l'ajuda de df_ped podem establir una relació indirecta
    # df_real <-> df_ped <-> NUM. COMANDA
    # df_ped <-> df_alb <-> EXPEDIENTE + REF. ODOO COMANDA COMPRA
    # A cada num. de comanda li correspon un (EXP. + REF. ODOO C-COMPRA)
    # D'aquesta manera assignam aquesta clau única a cada comanda real

    df_real_alumnes_tasca_entregada_clauUnica = logic_comu.unionDataFrames(
        df_real_alumnes_tasca_entregada,
        df_ped[["A_NUMERO_CP", "A_CLAU_UNICA_CP"]],
        "R_NUMERO_CP",
        "A_NUMERO_CP",
        "left",
        "_real",
        "_ped",
        True,
    )

    # DESAM CSV
    filename = (
        prefNomFitxerCORRECCIO + "05_DF_REAL_ALUMNES_TASCA_ENTREGADA_CLAU_UNICA.csv"
    )
    logic_comu.desaCSV(
        df_real_alumnes_tasca_entregada_clauUnica,
        filename,
        carpetaHC,
    )

    # Ja podem fer merge entre df_real i df_alb, aplicant clau única,
    # però abans cal reanomenar la columna _merge (creada en el merge
    # anterior) per evitar problemes:

    df_real_alumnes_tasca_entregada_clauUnica.rename(
        columns={"_merge": "_merge_01"}, inplace=True
    )

    df_real_alb = logic_comu.unionDataFrames(
        df_real_alumnes_tasca_entregada_clauUnica,
        df_alb,
        "A_CLAU_UNICA_CP",
        "A_CLAU_UNICA_CA",
        "left",
        "_real",
        "_alb",
        True,
    )

    # DESAM CSV
    filename = prefNomFitxerCORRECCIO + "06_UNIO_DF_REAL_ALB.csv"
    logic_comu.desaCSV(df_real_alb, filename, carpetaHC)

    # UNIO ENTRE df_real i df_fac
    df_real_fac = logic_comu.unionDataFrames(
        df_real_alumnes_tasca_entregada_clauUnica,
        df_fac,
        "A_CLAU_UNICA_CP",
        "A_CLAU_UNICA_CF",
        "left",
        "_real",
        "_fac",
        True,
    )

    # DESAM CSV
    filename = prefNomFitxerCORRECCIO + "07_UNIO_DF_REAL_FAC.csv"
    logic_comu.desaCSV(df_real_fac, filename, carpetaHC)

    # Recerca d'operacions ORFES

    # Es pot donar el cas que els alumnes hagin creat operacions, les quals
    # no tenen una comanda real de referencia (quasevol operació de compra
    # sempre està associada a una comanda real). Per exemple, pot haver registrat
    # una comanda de compra indicant un numero de comanda equivocat,
    # la qual cosa fa que no es pugui associar aquesta operació a cap comanda real,
    # o per exemple, por haver introduit la factura de compra sense establir
    # una relació a la comanda real que s'esta facturant.
    # Els registres resultants son considerats ORFES, perque no tenen cap comanda
    # real associada.

    # OBTENIM COMANDES ALUMNES ORFES.
    # Es a dir, un alumne ha introduit una comanda, la qual no
    # apareix en les dades reals df_real.
    # Primer feim una unio entre df_ped i df_real, obtenint un df on tenim totes
    # les comandes registrades pels alumnes (esquerra) i la seva comanda real (dreta)
    # associada (existeixi o no)

    df_ped_real = logic_comu.unionDataFrames(
        df_ped,
        df_real_alumnes_tasca_entregada_clauUnica,
        "A_NUMERO_CP",
        "R_NUMERO_CP",
        "left",
        "_ped",
        "_real",
        True,
    )

    # Del df obtnigut només ens interessa les comandes regsitrades pels alumnes (esquerra)
    # que no tenen cap comanda real associada (dreta)

    df_comandes_orfes = df_ped_real[df_ped_real["_merge"] == "left_only"]

    # DESAM CSV
    filename = prefNomFitxerCORRECCIO + "08_COMANDES_ALUMNES_ORFES.csv"
    logic_comu.desaCSV(df_comandes_orfes, filename, carpetaHC)

    # OBTENIM ALBARANS ALUMNES ORFES.
    # Es a dir, un alumne ha introduit un albarà, el qual no
    # apareix en les dades reals df_real

    df_alb_real = logic_comu.unionDataFrames(
        df_alb,
        df_real_alumnes_tasca_entregada_clauUnica,
        "A_CLAU_UNICA_CA",
        "A_CLAU_UNICA_CP",
        "left",
        "_alb",
        "_real",
        True,
    )

    df_albarans_orfes = df_alb_real[df_alb_real["_merge"] == "left_only"]

    # DESAM CSV
    filename = prefNomFitxerCORRECCIO + "09_ALBARANS_ALUMNES_ORFES.csv"
    logic_comu.desaCSV(df_albarans_orfes, filename, carpetaHC)

    # OBTENIM FACTURES ALUMNES ORFES.
    # Es a dir, un alumne ha introduit una factura, el qual no
    # apareix en les dades reals df_real

    df_fac_real = logic_comu.unionDataFrames(
        df_fac,
        df_real_alumnes_tasca_entregada_clauUnica,
        "A_CLAU_UNICA_CF",
        "A_CLAU_UNICA_CP",
        "left",
        "_fac",
        "_real",
        True,
    )

    df_factures_orfes = df_fac_real[df_fac_real["_merge"] == "left_only"]

    # DESAM CSV
    filename = prefNomFitxerCORRECCIO + "10_FACTURES_ALUMNES_ORFES.csv"
    logic_comu.desaCSV(df_factures_orfes, filename, carpetaHC)

    # CORRECCIO D'OPERACIONS - COMANDES

    informe_pedidos = []

    for index, row in df_real_ped.iterrows():
        info_pedidos = {
            "Num. Comanda compra": row["R_NUMERO_CP"],
            "Real Empresa": row["R_EMPRESA_C"],
            "Alumn@ Empresa": row["A_EMPRESA_CP"],
            "Empreses ==": "✅",
            "Real Proveïdor": row["R_PROVEEDOR_C"],
            "Alumn@ Proveïdor": row["A_PROVEEDOR_CP"],
            "Proveïdors ==": "✅",
            "Real Data emisió": row["R_FECHA_EMISION_C"],
            "Alumn@ Data emisió": row["A_FECHA_EMISION_CP"],
            "Dates emisió ==": "✅",
            "Real Num. Comanda": row["R_NUMERO_CP"],
            "Alumn@ Num. Comanda": row["A_NUMERO_CP"],
            "Num. Comanda ==": "✅",
            "Real Import": row["R_IMPORTE_C"],
            "Alumn@ Import": row["A_IMPORTE_CP"],
            "Import ==": "✅",
            "Estat Comanda": row["A_ESTADO_CP"],
            "Estat Comanda OK": "❌",
            "Data Entrega Tasca": row["R_FECHA_ENTREGA"],
            "Data Factura Compra Disponible": pd.to_datetime(row["R_FECHA_EMISION_C"])
            + timedelta(days=1),
            "Estat Fact. Comanda": row["A_ESTADO_FACTURACION_CP"],
            "Estat Fact. Comanda OK": "❌",
        }

        if (
            str(row["R_EMPRESA_C"]).strip().upper()
            != str(row["A_EMPRESA_CP"]).strip().upper()
        ):
            info_pedidos["Empreses =="] = "❌"

        if (
            str(row["R_PROVEEDOR_C"]).strip().upper()
            != str(row["A_PROVEEDOR_CP"]).strip().upper()
        ):
            info_pedidos["Proveïdors =="] = "❌"

        if row["R_FECHA_EMISION_C"] != row["A_FECHA_EMISION_CP"]:
            info_pedidos["Dates emisió =="] = "❌"

        if row["R_NUMERO_CP"] != row["A_NUMERO_CP"]:
            info_pedidos["Num. Comanda =="] = "❌"

        if row["R_IMPORTE_C"] != row["A_IMPORTE_CP"]:
            info_pedidos["Import =="] = "❌"

        if row["A_ESTADO_CP"] == "Pedido de compra":
            info_pedidos["Estat Comanda OK"] = "✅"

        # DETERMINAM SI FACTURA DE COMPRA ESTÀ DISPONIBLE
        dataEntregaTasca = pd.to_datetime(row["R_FECHA_ENTREGA"])
        dataDisponibleFactura = pd.to_datetime(row["R_FECHA_EMISION_C"]) + timedelta(
            days=1
        )
        if dataEntregaTasca >= dataDisponibleFactura:
            estatFactEsperat = "TOTALMENTE FACTURADO"
            if str(row["A_ESTADO_FACTURACION_CP"]).strip().upper() == estatFactEsperat:
                info_pedidos["Estat Fact. Comanda OK"] = "✅"
            else:
                info_pedidos["Estat Fact. Comanda OK"] = "❌"
        else:
            estatFactEsperat = "FACTURAS EN ESPERA"
            if str(row["A_ESTADO_FACTURACION_CP"]).strip().upper() == estatFactEsperat:
                info_pedidos["Estat Fact. Comanda OK"] = "✅"
            else:
                info_pedidos["Estat Fact. Comanda OK"] = "❌"

        informe_pedidos.append(info_pedidos)

        # CREAM DF CORRECCIO COMANDES COMPRA
        dfCorreccioComandesCompra = pd.DataFrame(informe_pedidos)

        # DESAM CSV
        fileName = prefNomFitxerCORRECCIO + "11_DF_CORRECCIO_COMANDES_COMPRA.csv"
        logic_comu.desaCSV(dfCorreccioComandesCompra, fileName, carpetaHC)

    # CORRECCIO D'OPERACIONS - ALBARANS

    informe_albarans = []

    for index, row in df_real_alb.iterrows():
        info_albarans = {
            "Num. Comanda compra": row["R_NUMERO_CP"],
            "Real Empresa": row["R_EMPRESA_C"],
            "Alumn@ Empresa": row["A_EMPRESA_CA"],
            "Empreses ==": "✅",
            "Real Proveïdor": row["R_PROVEEDOR_C"],
            "Alumn@ Proveïdor": row["A_PROVEEDOR_CA"],
            "Proveïdors ==": "✅",
            "Real Data emisió": row["R_FECHA_EMISION_C"],
            "Alumn@ Data emisió": row["A_FECHA_EMISION_CA"],
            "Dates emisió ==": "✅",
            "Real Num. Comanda": row["R_NUMERO_CA"],
            "Alumn@ Num. Comanda": row["A_NUMERO_CA"],
            "Num. Albarà ==": "✅",
            "Real Import": row["R_IMPORTE_C"],
            "Alumn@ Import": row["A_IMPORTE_CA"],
            "Import ==": "✅",
            "Estat Albarà": row["A_ESTADO_CA"],
            "Estat Albarà OK": "❌",
        }

        if (
            str(row["R_EMPRESA_C"]).strip().upper()
            != str(row["A_EMPRESA_CA"]).strip().upper()
        ):
            info_albarans["Empreses =="] = "❌"

        if (
            str(row["R_PROVEEDOR_C"]).strip().upper()
            != str(row["A_PROVEEDOR_CA"]).strip().upper()
        ):
            info_albarans["Proveïdors =="] = "❌"

        if row["R_FECHA_EMISION_C"] != row["A_FECHA_EMISION_CA"]:
            info_albarans["Dates emisió =="] = "❌"

        if row["R_NUMERO_CA"] != row["A_NUMERO_CA"]:
            info_albarans["Num. Albarà =="] = "❌"

        if row["R_IMPORTE_C"] != row["A_IMPORTE_CA"]:
            info_albarans["Import =="] = "❌"

        if str(row["A_ESTADO_CA"]).strip().upper() == "HECHO":
            info_albarans["Estat Albarà OK"] = "✅"

        informe_albarans.append(info_albarans)

        # CREAM DF CORRECCIO ALBARANS COMPRA
        dfCorrecioAlbaransCompra = pd.DataFrame(informe_albarans)

        fileName = prefNomFitxerCORRECCIO + "12_DF_CORRECCIO_ALBARANS_COMPRA.csv"

        logic_comu.desaCSV(dfCorrecioAlbaransCompra, fileName, carpetaHC)

    # CORRECCIO D'OPERACIONS - FACTURES

    informe_factures = []

    for index, row in df_real_fac.iterrows():
        info_factures = {
            "Num. Comanda compra": row["R_NUMERO_CP"],
            "Data entrega tasca": row["R_FECHA_ENTREGA"],
            "Fra. compra disponible en data entrega": "",
            "Fra. compra registrada en ODOO": "",
            "Real Empresa": row["R_EMPRESA_C"],
            "Alumn@ Empresa": row["A_EMPRESA_CF"],
            "Empreses ==": "✅",
            "Real Proveïdor": row["R_PROVEEDOR_C"],
            "Alumn@ Proveïdor": row["A_PROVEEDOR_CF"],
            "Proveïdors ==": "✅",
            "Real Data emisió": row["R_FECHA_EMISION_C"],
            "Alumn@ Data emisió": row["A_FECHA_EMISION_CF"],
            "Dates emisió ==": "✅",
            "Real Num. Factura": row["R_NUMERO_CF"],
            "Alumn@ Num. Factura": row["A_NUMERO_CF"],
            "Num. Factura ==": "✅",
            "Real Import": row["R_IMPORTE_C"],
            "Alumn@ Import": row["A_IMPORTE_CF"],
            "Import ==": "✅",
        }

        # FACTURA DE COMPRA REGISTRADA EN ODOO
        if (
            str(row["A_EMPRESA_CF"]).strip().upper() == "NAN"
            and str(row["A_PROVEEDOR_CF"]).strip().upper() == "NAN"
            and str(row["A_FECHA_EMISION_CF"]).strip().upper() == "NAT"
            and str(row["A_NUMERO_CF"]).strip().upper() == "NAN"
            and str(row["A_IMPORTE_CF"]).strip().upper() == "NAN"
        ):
            info_factures["Fra. compra registrada en ODOO"] = "NO - ❌"
            info_factures["Alumn@ Empresa"] = "❌ - SENSE DADES"
            info_factures["Alumn@ Proveïdor"] = "❌ - SENSE DADES"
            info_factures["Alumn@ Data emisió"] = "❌ - SENSE DADES"
            info_factures["Alumn@ Num. Factura"] = "❌ - SENSE DADES"
            info_factures["Alumn@ Import"] = "❌ - SENSE DADES"

        else:
            info_factures["Fra. compra registrada en ODOO"] = "SI - ✅"

        dataEntregaTasca = row["R_FECHA_ENTREGA"]
        dataDisponibleFactura = row["R_FECHA_EMISION_C"] + timedelta(days=1)
        if dataEntregaTasca >= dataDisponibleFactura:
            info_factures["Fra. compra disponible en data entrega"] = "SI - ✅"
            if (
                str(row["R_EMPRESA_C"]).strip().upper()
                != str(row["A_EMPRESA_CF"]).strip().upper()
            ):
                info_factures["Empreses =="] = "❌"

            if (
                str(row["R_PROVEEDOR_C"]).strip().upper()
                != str(row["A_PROVEEDOR_CF"]).strip().upper()
            ):
                info_factures["Proveïdors =="] = "❌"

            if row["R_FECHA_EMISION_C"] != row["A_FECHA_EMISION_CF"]:
                info_factures["Dates emisió =="] = "❌"

            if row["R_NUMERO_CF"] != row["A_NUMERO_CF"]:
                info_factures["Num. Factura =="] = "❌"

            if row["R_IMPORTE_C"] != row["A_IMPORTE_CF"]:
                info_factures["Import =="] = "❌"

        else:
            info_factures["Fra. compra disponible en data entrega"] = "NO - ❌"
            if str(row["A_EMPRESA_CF"]).strip().upper() != "NAN":
                info_factures["Empreses =="] = "❌"

            if str(row["A_PROVEEDOR_CF"]).strip().upper() != "NAN":
                info_factures["Proveïdors =="] = "❌"

            if str(row["A_FECHA_EMISION_CF"]).strip().upper() != "NAT":
                info_factures["Dates emisió =="] = "❌"

            if str(row["A_NUMERO_CF"]).strip().upper() != "NAN":
                info_factures["Num. Factura =="] = "❌"

            if str(row["A_IMPORTE_CF"]).strip().upper() != "NAN":
                info_factures["Import =="] = "❌"

        informe_factures.append(info_factures)

        # CREAM DF CORRECCIO FACTURES COMPRA
        dfCorrecioFacturesCompra = pd.DataFrame(informe_factures)

        fileName = prefNomFitxerCORRECCIO + "13_DF_CORRECCIO_FACTURES_COMPRA.csv"

        logic_comu.desaCSV(dfCorrecioFacturesCompra, fileName, carpetaHC)

    return dfCorreccioComandesCompra, dfCorrecioAlbaransCompra, dfCorrecioFacturesCompra


"""

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


def uneixDataFrames(df_real_filtrada, df_ped, df_alb, df_fac, prefNomFitxerCorreccio):

    df_real_ped = logic_comu.unionDataFrames(
        df_real_filtrada,
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

    df_real_filtrada_clauUnica = logic_comu.unionDataFrames(
        df_real_filtrada,
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
    filename_df_real_filtrada_clauUnica = (
        prefNomFitxerCorreccio + "df_real_filtrada_clauUnica.csv"
    )
    logic_comu.desaCSV(
        df_real_filtrada_clauUnica, filename_df_real_filtrada_clauUnica, carpetaDesti
    )

    # Ja podem fer merge entre df_real i df_alb, aplicant clau única,
    # però abans cal reanomenar la columna _merge (creada en el merge
    # anterior) per evitar problemes:

    df_real_filtrada_clauUnica.rename(columns={"_merge": "_merge_01"}, inplace=True)

    df_real_alb = logic_comu.unionDataFrames(
        df_real_filtrada_clauUnica,
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
        df_real_filtrada_clauUnica,
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

    return df_real_ped, df_real_filtrada_clauUnica, df_real_alb, df_real_fac


# ==============================================================================
# 3.1.7 RESEARCH OF ORPHAN OPERATIONS
# ==============================================================================


def researchOrphanOperations(
    df_real_filtrada_clauUnica, df_ped, df_alb, df_fac, prefNomFitxerCorreccio
):

    # OBTENIM COMANDES ALUMNES ORFES.
    # Es a dir, un alumne ha introduit una comanda, la qual no
    # apareix en les dades reals df_real

    df_comandesOrfes = logic_comu.unionDataFrames(
        df_ped,
        df_real_filtrada_clauUnica,
        "A_NUMERO_CP",
        "R_NUMERO_CP",
        "left",
        "_ped",
        "_real",
        True,
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
        df_real_filtrada_clauUnica,
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
        df_real_filtrada_clauUnica,
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
            "Num. Comanda compra": row["R_NUMERO_CP"],
            "Real Empresa": row["R_EMPRESA_C"],
            "Alumn@ Empresa": row["A_EMPRESA_CP"],
            "Empreses ==": "✅",
            "Real Proveïdor": row["R_PROVEEDOR_C"],
            "Alumn@ Proveïdor": row["A_PROVEEDOR_CP"],
            "Proveïdors ==": "✅",
            "Real Data emisió": row["R_FECHA_EMISION_C"],
            "Alumn@ Data emisió": row["A_FECHA_EMISION_CP"],
            "Dates emisió ==": "✅",
            "Real Num. Comanda": row["R_NUMERO_CP"],
            "Alumn@ Num. Comanda": row["A_NUMERO_CP"],
            "Num. Comanda ==": "✅",
            "Real Import": row["R_IMPORTE_C"],
            "Alumn@ Import": row["A_IMPORTE_CP"],
            "Import ==": "✅",
            "Estat Comanda": row["A_ESTADO_CP"],
            "Estat Comanda OK": "❌",
            "Data Entrega Tasca": row["R_FECHA_ENTREGA"],
            "Data Factura Compra Disponible": pd.to_datetime(row["R_FECHA_EMISION_C"])
            + timedelta(days=1),
            "Estat Fact. Comanda": row["A_ESTADO_FACTURACION_CP"],
            "Estat Fact. Comanda OK": "❌",
        }

        if (
            str(row["R_EMPRESA_C"]).strip().upper()
            != str(row["A_EMPRESA_CP"]).strip().upper()
        ):
            info_pedidos["Empreses =="] = "❌"

        if (
            str(row["R_PROVEEDOR_C"]).strip().upper()
            != str(row["A_PROVEEDOR_CP"]).strip().upper()
        ):
            info_pedidos["Proveïdors =="] = "❌"

        if row["R_FECHA_EMISION_C"] != row["A_FECHA_EMISION_CP"]:
            info_pedidos["Dates emisió =="] = "❌"

        if row["R_NUMERO_CP"] != row["A_NUMERO_CP"]:
            info_pedidos["Num. Comanda =="] = "❌"

        if row["R_IMPORTE_C"] != row["A_IMPORTE_CP"]:
            info_pedidos["Import =="] = "❌"

        if row["A_ESTADO_CP"] == "Pedido de compra":
            info_pedidos["Estat Comanda OK"] = "✅"

        # DETERMINAM SI FACTURA DE COMPRA ESTÀ DISPONIBLE
        dataEntregaTasca = pd.to_datetime(row["R_FECHA_ENTREGA"])
        dataDisponibleFactura = pd.to_datetime(row["R_FECHA_EMISION_C"]) + timedelta(
            days=1
        )
        if dataEntregaTasca >= dataDisponibleFactura:
            estatFactEsperat = "TOTALMENTE FACTURADO"
            if str(row["A_ESTADO_FACTURACION_CP"]).strip().upper() == estatFactEsperat:
                info_pedidos["Estat Fact. Comanda OK"] = "✅"
            else:
                info_pedidos["Estat Fact. Comanda OK"] = "❌"
        else:
            estatFactEsperat = "FACTURAS EN ESPERA"
            if str(row["A_ESTADO_FACTURACION_CP"]).strip().upper() == estatFactEsperat:
                info_pedidos["Estat Fact. Comanda OK"] = "✅"
            else:
                info_pedidos["Estat Fact. Comanda OK"] = "❌"

        informe_pedidos.append(info_pedidos)

    # CREAM DF CORRECCIO COMANDES COMPRA
    dfCorrecioComandesCompra = pd.DataFrame(informe_pedidos)

    fileName = prefNomFitxerCorreccio + "InformeCorreccióComandesCompra.csv"

    logic_comu.desaCSV(dfCorrecioComandesCompra, fileName, "HISTORIC_CORRECCIONS")

    return dfCorrecioComandesCompra


# ==============================================================================
# 3.1.9 CORRECCIO D'OPERACIONS - ALBARANS
# ==============================================================================


def correccioAlbarans(df_real_alb, prefNomFitxerCorreccio):

    informe_albarans = []

    for index, row in df_real_alb.iterrows():
        info_albarans = {
            "Num. Comanda compra": row["R_NUMERO_CP"],
            "Real Empresa": row["R_EMPRESA_C"],
            "Alumn@ Empresa": row["A_EMPRESA_CA"],
            "Empreses ==": "✅",
            "Real Proveïdor": row["R_PROVEEDOR_C"],
            "Alumn@ Proveïdor": row["A_PROVEEDOR_CA"],
            "Proveïdors ==": "✅",
            "Real Data emisió": row["R_FECHA_EMISION_C"],
            "Alumn@ Data emisió": row["A_FECHA_EMISION_CA"],
            "Dates emisió ==": "✅",
            "Real Num. Comanda": row["R_NUMERO_CA"],
            "Alumn@ Num. Comanda": row["A_NUMERO_CA"],
            "Num. Albarà ==": "✅",
            "Real Import": row["R_IMPORTE_C"],
            "Alumn@ Import": row["A_IMPORTE_CA"],
            "Import ==": "✅",
            "Estat Albarà": row["A_ESTADO_CA"],
            "Estat Albarà OK": "❌",
        }

        if (
            str(row["R_EMPRESA_C"]).strip().upper()
            != str(row["A_EMPRESA_CA"]).strip().upper()
        ):
            info_albarans["Empreses =="] = "❌"

        if (
            str(row["R_PROVEEDOR_C"]).strip().upper()
            != str(row["A_PROVEEDOR_CA"]).strip().upper()
        ):
            info_albarans["Proveïdors =="] = "❌"

        if row["R_FECHA_EMISION_C"] != row["A_FECHA_EMISION_CA"]:
            info_albarans["Dates emisió =="] = "❌"

        if row["R_NUMERO_CA"] != row["A_NUMERO_CA"]:
            info_albarans["Num. Albarà =="] = "❌"

        if row["R_IMPORTE_C"] != row["A_IMPORTE_CA"]:
            info_albarans["Import =="] = "❌"

        if str(row["A_ESTADO_CA"]).strip().upper() == "HECHO":
            info_albarans["Estat Albarà OK"] = "✅"

        informe_albarans.append(info_albarans)

    # CREAM DF CORRECCIO ALBARANS COMPRA
    dfCorrecioAlbaransCompra = pd.DataFrame(informe_albarans)

    fileName = prefNomFitxerCorreccio + "InformeCorreccióAlbaransCompra.csv"

    logic_comu.desaCSV(dfCorrecioAlbaransCompra, fileName, "HISTORIC_CORRECCIONS")

    return dfCorrecioAlbaransCompra


# ==============================================================================
# 3.1.10 CORRECCIO D'OPERACIONS - FACTURES
# ==============================================================================


def correccioFactures(df_real_fac, prefNomFitxerCorreccio):

    informe_factures = []

    for index, row in df_real_fac.iterrows():
        info_factures = {
            "Num. Comanda compra": row["R_NUMERO_CP"],
            "Data entrega tasca": row["R_FECHA_ENTREGA"],
            "Fra. compra disponible en data entrega": "",
            "Fra. compra registrada en ODOO": "",
            "Real Empresa": row["R_EMPRESA_C"],
            "Alumn@ Empresa": row["A_EMPRESA_CF"],
            "Empreses ==": "✅",
            "Real Proveïdor": row["R_PROVEEDOR_C"],
            "Alumn@ Proveïdor": row["A_PROVEEDOR_CF"],
            "Proveïdors ==": "✅",
            "Real Data emisió": row["R_FECHA_EMISION_C"],
            "Alumn@ Data emisió": row["A_FECHA_EMISION_CF"],
            "Dates emisió ==": "✅",
            "Real Num. Factura": row["R_NUMERO_CF"],
            "Alumn@ Num. Factura": row["A_NUMERO_CF"],
            "Num. Factura ==": "✅",
            "Real Import": row["R_IMPORTE_C"],
            "Alumn@ Import": row["A_IMPORTE_CF"],
            "Import ==": "✅",
        }

        # FACTURA DE COMPRA REGISTRADA EN ODOO
        if (
            str(row["A_EMPRESA_CF"]).strip().upper() == "NAN"
            and str(row["A_PROVEEDOR_CF"]).strip().upper() == "NAN"
            and str(row["A_FECHA_EMISION_CF"]).strip().upper() == "NAT"
            and str(row["A_NUMERO_CF"]).strip().upper() == "NAN"
            and str(row["A_IMPORTE_CF"]).strip().upper() == "NAN"
        ):
            info_factures["Fra. compra registrada en ODOO"] = "NO - ❌"
            info_factures["Alumn@ Empresa"] = "❌ - SENSE DADES"
            info_factures["Alumn@ Proveïdor"] = "❌ - SENSE DADES"
            info_factures["Alumn@ Data emisió"] = "❌ - SENSE DADES"
            info_factures["Alumn@ Num. Factura"] = "❌ - SENSE DADES"
            info_factures["Alumn@ Import"] = "❌ - SENSE DADES"

        else:
            info_factures["Fra. compra registrada en ODOO"] = "SI - ✅"

        dataEntregaTasca = row["R_FECHA_ENTREGA"]
        dataDisponibleFactura = row["R_FECHA_EMISION_C"] + timedelta(days=1)
        if dataEntregaTasca >= dataDisponibleFactura:
            info_factures["Fra. compra disponible en data entrega"] = "SI - ✅"
            if (
                str(row["R_EMPRESA_C"]).strip().upper()
                != str(row["A_EMPRESA_CF"]).strip().upper()
            ):
                info_factures["Empreses =="] = "❌"

            if (
                str(row["R_PROVEEDOR_C"]).strip().upper()
                != str(row["A_PROVEEDOR_CF"]).strip().upper()
            ):
                info_factures["Proveïdors =="] = "❌"

            if row["R_FECHA_EMISION_C"] != row["A_FECHA_EMISION_CF"]:
                info_factures["Dates emisió =="] = "❌"

            if row["R_NUMERO_CF"] != row["A_NUMERO_CF"]:
                info_factures["Num. Factura =="] = "❌"

            if row["R_IMPORTE_C"] != row["A_IMPORTE_CF"]:
                info_factures["Import =="] = "❌"

        else:
            info_factures["Fra. compra disponible en data entrega"] = "NO - ❌"
            print(str(row["A_EMPRESA_CF"]).strip().upper())
            print(str(row["A_PROVEEDOR_CF"]).strip().upper())
            print(str(row["A_FECHA_EMISION_CF"]).strip().upper())
            print(str(row["A_NUMERO_CF"]).strip().upper())
            print(str(row["A_IMPORTE_CF"]).strip().upper())
            print("--------------------------------")
            if str(row["A_EMPRESA_CF"]).strip().upper() != "NAN":
                info_factures["Empreses =="] = "❌"

            if str(row["A_PROVEEDOR_CF"]).strip().upper() != "NAN":
                info_factures["Proveïdors =="] = "❌"

            if str(row["A_FECHA_EMISION_CF"]).strip().upper() != "NAT":
                info_factures["Dates emisió =="] = "❌"

            if str(row["A_NUMERO_CF"]).strip().upper() != "NAN":
                info_factures["Num. Factura =="] = "❌"

            if str(row["A_IMPORTE_CF"]).strip().upper() != "NAN":
                info_factures["Import =="] = "❌"

        informe_factures.append(info_factures)

    # CREAM DF CORRECCIO FACTURES COMPRA
    dfCorrecioFacturesCompra = pd.DataFrame(informe_factures)

    fileName = prefNomFitxerCorreccio + "InformeCorreccióFacturesCompra.csv"

    logic_comu.desaCSV(dfCorrecioFacturesCompra, fileName, "HISTORIC_CORRECCIONS")

    return dfCorrecioFacturesCompra
"""
