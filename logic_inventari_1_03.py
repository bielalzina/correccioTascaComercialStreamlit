import pandas as pd
from datetime import datetime, timedelta
import os
import logic_comu
import glob


def correccioInventari(grup, tasca, carpetaINPUT, carpetaOUTPUT):

    # CARREGA ARXIUS
    # ADG32O_02.12_09_RESUM_DADES_INVENTARI_ALUMNE.csv
    # ADG32O_02.12_10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv

    # Abans de recuperar les fonts de dades, per fer les correccions, eliminarem tots els arxius existents relacionats amb l'INVENTARI:

    # Definim ruta y patró
    # El asterisco (*) actúa como comodín para cualquier carácter posterior

    rutaOUTPUT = (
        os.getcwd() + "/" + carpetaOUTPUT + "/" + grup + "_" + tasca + "_INVENTARI_"
    )
    patro = rutaOUTPUT + "*"

    # patro = C:\Users\GABRIEL\Documents\GitHub\correccioTascaComercialStreamlit\LLISTATS_OUTPUT\ADG32O_02.12_INVENTARI_*

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

    fileNameResumInventari = (
        grup + "_" + tasca + "_" + "09_RESUM_DADES_INVENTARI_ALUMNE.csv"
    )
    fileNameHESInventari = (
        grup + "_" + tasca + "_" + "10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv"
    )

    try:
        df_resum_inventari = logic_comu.carregaCSV(fileNameResumInventari, carpetaINPUT)
        df_hes_inventari = logic_comu.carregaCSV(fileNameHESInventari, carpetaINPUT)

    except Exception as e:
        print(f"Error carregant els arxius: {e}")

    # print(df_resum_inventari)
    # print(df_hes_inventari)

    print("✅ Dades carregades correctament. Continuam correcció")
    # print()

    # 2 COLUMNES DATAFRAMES
    # print("LLISTATS COLUMNES 09_RESUM_DADES_INVENTARI_ALUMNE.csv")
    # print("\n".join(df_resum_inventari.columns.tolist()))
    # print()
    # print("LLISTATS COLUMNES 10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv")
    # print("\n".join(df_hes_inventari.columns.tolist()))
    # print()

    # 3. NETEJA DADES

    # Netejem tipus de dades en df_resum_inventari
    df_resum_inventari = logic_comu.netejaTipusDadesDFResumInventari(df_resum_inventari)

    # Netejem tipus de dades en df_hes_inventari
    df_hes_inventari = logic_comu.netejaTipusDadesDFHesInventari(df_hes_inventari)

    print("✅ Dades netejas correctament. Continuam correcció")
    # print()
    # print(df_resum_inventari)
    # print(df_hes_inventari)
    # print()

    # CREAM NOU DF A PARTIR DE df_hes_inventari AMB NOMES
    # STOCK FINALS ON A_OPERACIO_HES = 'OP_FINAL'
    df_hes_inventari_stocks_finals = df_hes_inventari.loc[
        df_hes_inventari["A_OPERACIO_HES"] == "OP_FINAL"
    ]

    print("✅ STOCKS FINALS EN DF_HES_INVENTARI")
    print(df_hes_inventari_stocks_finals)

    # CREAM NOU DF A PARTIR DE df_hes_inventari AMB NOMES
    # STOCKS NEGATIUS ON A_STOCK_HES < 0

    df_hes_inventari_stocks_negatius = df_hes_inventari.loc[
        df_hes_inventari["A_STOCK_HES"] < 0
    ]

    if not df_hes_inventari_stocks_negatius.empty:
        print("✅ STOCKS NEGATIUS EN DF_HES_INVENTARI")
        # print(df_hes_inventari_stocks_negatius)
    else:
        print("✅ No hi han stocks negatius en df_hes_inventari")

    # UNIO df_resum_inventari i df_hes_inventari_stocks_finals
    # D'AQUESTA MANERA PODEM DETERMINAR SI LLISTAT HES INVENTARI
    # INCLOU TOTS ELS REGISTRES (totes les entrades i sortides dels productes)
    # I SI COINCIDEIXEN ELS STOCKS FINALS EN ELS DOS LLISTATS

    df_inventari_final = logic_comu.unionDataFrames(
        df_resum_inventari,
        df_hes_inventari_stocks_finals,
        "A_CLAU_UNICA_I",
        "A_CLAU_UNICA_HES",
        "left",
        "_resum",
        "_hes",
        True,
    )

    print("✅ INVENTARI FINAL")
    # print(df_inventari_final)

    # INICIAM CORRECCIO INVENTARI A NIVELL D'EMPRESA - PRODUCTE
    # ASPECTES A COMPROVAR PER CADA EMPRESA-PRODUCTE:
    # 1. NUM. UNITATS FINALS COINCIDEIX EN ELS DOS LLISTATS:
    #    09_RESUM_DADES_INVENTARI_ALUMNE.csv
    #    10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv
    # 2. UNITATS PENDENTS ENTRAR
    # 3. UNITATS PENDENTS SORTIR
    # 4. STOCKS NEGATIUS

    informe = []

    for idx, row in df_inventari_final.iterrows():
        empresa = row["A_EMPRESA_I"]
        expedient = row["A_EXPEDIENT_I"]
        producte = row["A_PRODUCTE_I"]

        info = {
            "EMPRESA": empresa,
            "EXPEDIENT": expedient,
            "PRODUCTE": producte,
            "UF - RESUM INVENTARI": row["A_UNITATS_REALS_I"],
            "UF - HES INVENTARI": row["A_STOCK_HES"],
            "UF COINCIDEIXEN": "",
            "PENDENTS ENTRAR": row["A_UNITATS_PENDENTS_ENTRAR_I"],
            "PENDENTS ENTRAR = 0": "",
            "PENDENTS SORTIR": row["A_UNITATS_PENDENTS_SORTIR_I"],
            "PENDENTS SORTIR = 0": "",
            "STOCKS NEGATIUS": "✅",
            "RESULTAT": "",
            "OBSERVACIONS": "",
        }

        observacions = ""

        # 'UNITATS FINALS COINCIDEIXEN'
        if row["A_UNITATS_REALS_I"] == row["A_STOCK_HES"]:
            info["UF COINCIDEIXEN"] = "✅"
        else:
            info["UF COINCIDEIXEN"] = "❌"
            observacions += (
                "El numero de unitats finals no coincideixen en els llistats aportats\n"
            )

        # 'ESTAT PENDENTS ENTRAR'
        if row["A_UNITATS_PENDENTS_ENTRAR_I"] > 0:
            info["PENDENTS ENTRAR = 0"] = "❌"
            observacions += (
                "Unitats pendents entrar > 0 -> Hi ha albarans de compra no validats?\n"
            )
        else:
            info["PENDENTS ENTRAR = 0"] = "✅"

        # 'ESTAT PENDENTS SORTIR'
        if row["A_UNITATS_PENDENTS_SORTIR_I"] > 0:
            info["PENDENTS SORTIR = 0"] = "❌"
            observacions += (
                "Unitats pendents sortir > 0 -> Hi ha albarans de venda no validats?\n"
            )
        else:
            info["PENDENTS SORTIR = 0"] = "✅"

        # 'CHECK STOCK NEGATIU'
        # Comprovam si empresa ha tingut stocks negatius

        if not df_hes_inventari_stocks_negatius.empty:
            error = df_hes_inventari_stocks_negatius[
                (df_hes_inventari_stocks_negatius["A_EMPRESA_HES"] == empresa)
                & (df_hes_inventari_stocks_negatius["A_PRODUCTE_HES"] == producte)
            ]
            if not error.empty:
                info["STOCKS NEGATIUS"] = "❌"
                observacions += "Per aquest producte hi ha operacions registrades que han generat stocks negatius"

        # 'RESULTAT'
        if all(
            [
                info["STOCKS NEGATIUS"] == "✅",
                info["UF COINCIDEIXEN"] == "✅",
                info["PENDENTS ENTRAR = 0"] == "✅",
                info["PENDENTS SORTIR = 0"] == "✅",
            ]
        ):
            info["RESULTAT"] = "✅ - ENHORABONA"
        else:
            info["RESULTAT"] = "❌ - REVISAR"

        # 'OBSERVACIONS'
        if observacions:
            info["OBSERVACIONS"] = observacions
        else:
            info["OBSERVACIONS"] = "✅"

        informe.append(info)

    # CREAM DF INFORME
    df_correccio_inventari_empresa_producte = pd.DataFrame(informe)

    # GUARDEM INFORME
    fileName = (
        grup
        + "_"
        + tasca
        + "_INVENTARI_"
        + "40_CORRECCIO_INVENTARI_EMPRESA_PRODUCTE.csv"
    )

    logic_comu.desaCSV(df_correccio_inventari_empresa_producte, fileName, carpetaOUTPUT)

    print("✅ INFORME GUARDAT")
    # print(df_correccio_inventari_empresa_producte)

    # CONTINUAM CORRECCIO INVENTARI A NIVELL D'EMPRESA
    # ASPECTES A COMPROVAR PER CADA EMPRESA:
    # 1. VALOR FINAL NO SUPERIOR A 1.000 €

    # AQUESTA CORRECCIO NO ES FA A NIVELL DE PRODUCTE,
    # SINO QUE ES FA A NIVELL D'EMPRESA, PER LA QUAL COSA
    # HEM DE CREAR UN NOU DF AMB AGRUPAMENT PER EMPRESA AMB
    # SUMA DE LA COLUMNA IMPORT

    # PRIMER PAS: CREAM DF REDUIT AMB LES COLUNNES QUE ENS INTERESSEN

    df_inventari_final_reduit = df_inventari_final[["A_EMPRESA_I", "A_IMPORT_I"]]

    # print(df_reduit)

    # SEGON PAS: CREAM DF AGRUPAT PER EMPRESA AMB SUMA IMPORT

    df_inventari_final_agrupat = (
        df_inventari_final_reduit.groupby("A_EMPRESA_I").sum().reset_index()
    )

    # print(df_agrupat)

    informe02 = []

    for idx, row in df_inventari_final_agrupat.iterrows():
        empresa = row["A_EMPRESA_I"]
        valor_stock_final = row["A_IMPORT_I"]

        info02 = {
            "EMPRESA": empresa,
            "VALOR STOCK FINAL": valor_stock_final,
            "VALOR STOCK FINAL NO SUPERIOR A 1.000 €": "",
            "RESULTAT": "",
            "OBSERVACIONS": "",
        }

        observacions02 = ""

        # 'CHECK VALOR STOCK NO SUPERIOR A 1.000 €'
        # Comprovam si el valor del stock és superior a 1.000 €

        if info02["VALOR STOCK FINAL"] > 1000:
            info02["VALOR STOCK FINAL NO SUPERIOR A 1.000 €"] = "❌"
            observacions02 += (
                "El valor dels articles en magatzem supera el límit de 1.000 €"
            )
        else:
            info02["VALOR STOCK FINAL NO SUPERIOR A 1.000 €"] = "✅"

        # 'RESULTAT'
        if info02["VALOR STOCK FINAL NO SUPERIOR A 1.000 €"] == "✅":
            info02["RESULTAT"] = "✅ - ENHORABONA"
        else:
            info02["RESULTAT"] = "❌ - REVISAR"

        # 'OBSERVACIONS'
        if observacions02:
            info02["OBSERVACIONS"] = observacions02
        else:
            info02["OBSERVACIONS"] = "✅"

        informe02.append(info02)

    # CREAM DF INFORME
    df_correccio_inventari_empresa = pd.DataFrame(informe02)

    # GUARDEM INFORME
    fileName = grup + "_" + tasca + "_INVENTARI_" + "41_CORRECCIO_INVENTARI_EMPRESA.csv"

    try:
        logic_comu.desaCSV(df_correccio_inventari_empresa, fileName, carpetaOUTPUT)
        print(f"✅ Corrección Inventario generada: {fileName}")
    except Exception as e:
        print(f"❌ Error al guardar: {e}")

    print("✅ INFORME GUARDAT")
    # print(df_correccio_inventari_empresa)

    return df_correccio_inventari_empresa_producte, df_correccio_inventari_empresa
