import logic_comu
import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import logic_compres_1_03

# import logic_vendes_1_03
import logic_inventari_1_03
import logic_estructura_1_03
import logic_comu
import time
import glob

from dades_varies import *

# ==============================================================================
# 1. CONFIGURACIÓN Y GESTIÓN DE CARPETAS
# ==============================================================================

# Aquestes instruccions sempre han d'estar en l'inici
# Definim el títol de la pàgina (pipella browser)

st.set_page_config(
    page_title="Corrector DC",
    page_icon="🎓",
    layout="wide",
)

# CARPERTA ON DESAM LES CORRECCIONS

CARPETA_HISTORICO = "HISTORIC_CORRECCIONS"

# Creem la carpeta si no existeix
if not os.path.exists(CARPETA_HISTORICO):
    os.makedirs(CARPETA_HISTORICO)

# ==============================================================================
# 2. BARRA LATERAL (ROLES)
# ==============================================================================

# 2. MENÚ LATERAL I ROLS
with st.sidebar:
    st.title("TAULER DE CONTROL")
    rol = st.selectbox("Identifica't com a: ", ["Alumne", "Professor"])

    acces_professor = False
    if rol == "Professor":
        password = st.text_input("Contrasenya: ", type="password")
        if password == "1234":
            st.success("🔓 GRANTED ACCESS")
            acces_professor = True
        else:
            st.error("🚫 ACCESS DENIED")

# ==============================================================================
# 3. VISTA PROFESOR (GENERAR Y GUARDAR)
# ==============================================================================

if rol == "Professor" and acces_professor:

    st.title("👨‍🏫 GESTIÓ DE CORRECCIONS")

    st.header("NOVA CORRECCIÓ COMPRES")
    st.subheader("Indica el grup, la tasca i la data de venciment")

    colA, colB, colC = st.columns(3)

    # Definim dades identificatives de la tasca que volem corregir

    with colA:
        grup = st.selectbox(
            "Selecciona el grup: ",
            ["ADG21O", "ADG32O"],
            index=None,
            placeholder="Selecciona el grup...",
        )

    with colB:
        tasca = st.selectbox(
            "Selecciona la tasca: ",
            llista_num_tasques,
            index=None,
            placeholder="Selecciona la tasca...",
        )

    with colC:
        dataVto = st.date_input(
            "Indica la data de venciment de la tasca: ",
            value=None,
            format="DD/MM/YYYY",
        )

    if grup is None:
        st.error("Per continuar, cal indicar el grup que ha fet la tasca")
        st.stop()

    if tasca is None:
        st.error("Per continuar, cal indicar la tasca objecte de correcció")
        st.stop()

    if dataVto is None:
        st.error("Per continuar, cal indicar la data de venciment de la tasca")
        st.stop()

    tab_estat_correcio, tab_compres, tab_vendes, tab_inventari = st.tabs(
        ["ESTAT CORRECCIÓ", "COMPRES", "VENDES", "INVENTARI"]
    )

    # DECLARAM UNA SERIE DE VARIABLES COMUNS PER A COMPRES, VENDES I INVENTARI

    # El grup i la tasca vendran informats com a parametres de la funció,
    # d'aquesta manera definirem dos prefixos pels arxius:

    # prefNomFitxerSOURCES = grup + "_" + tasca + "_"
    # prefNomFitxerSOURCES = "ADG32O_02.12_"

    # prefNomFitxerCORRECCIO = grup + "_" + tasca
    # pefNomFitxerCORRECCIO = "ADG32O_02.12"

    # Carpeta LLISTATS_INPUT
    carpetaINPUT = "LLISTATS_INPUT"

    # Carpeta LLISTATS_OUTPUT
    carpetaOUTPUT = "LLISTATS_OUTPUT"

    # ====================================================================
    # 3.0 VISTA PROFESOR - TAB ESTAT CORRECCIÓ
    # ====================================================================

    with tab_estat_correcio:
        st.subheader("ESTAT ACTUAL DE LA CORRECCIÓ")

        # Comprovem si existeix el directori INPUT
        # La carpeta INPUT es on desam els arxius que contenen la tasca dels
        # alumnes que hem de corregir
        st.subheader("COMPROVACIÓ EXISTENCIA CARPETA INPUT")

        existeixCarpetaInput = logic_estructura_1_03.existeixDirectori(
            "INPUT", grup + "_" + tasca
        )

        if existeixCarpetaInput:
            
            missatge = (
                "✅ El directori LLISTATS_INPUT/" + grup + "_" + tasca + " existeix"
            )
            st.success(missatge)

            # Comprovam si existeixen els documents adequats en el directori INPUT

            llistaArxiusTeoricsInput, disponibilitatArxiuInput = logic_estructura_1_03.relacioArxiusPresents("INPUT", grup, tasca)

            relacioArxiusInput = {
                "ARXIU": llistaArxiusTeoricsInput,
                "DISPONIBLE": disponibilitatArxiuInput,
            }

            st.dataframe(
                relacioArxiusInput,
                width="stretch",
                column_config={
                    "ARXIU": "Arxiu",
                    "DISPONIBLE": "Disponible",
                },
            )

        else:
            
            missatge = (
                "❌ El directori LLISTATS_INPUT/" + grup + "_" + tasca + " NO existeix"
            )
            st.error(missatge)
            creaCarpetaInput = st.checkbox("Activa el check si vols crear el directori LLISTATS_INPUT/" + grup + "_" + tasca)
            if creaCarpetaInput:
                novaCarpetaInput = logic_estructura_1_03.creaDirectori("INPUT", grup, tasca)
                missatge = "✅ El directori LLISTATS_INPUT/" + grup + "_" + tasca + " ha estat creat amb èxit"
                st.success(missatge)
                if st.button("Refresca la pàgina"):
                    st.rerun()

        st.subheader("COMPROVACIÓ EXISTENCIA CARPETA OUTPUT")
        # Comprovem si existeix el directori OUTPUT
        # La carpeta OUTPUT es on desam els arxius amb la correcció de les tasques dels alumnes
        existeixCarpetaOutput = logic_estructura_1_03.existeixDirectori(
            "OUTPUT", grup + "_" + tasca
        )
        if existeixCarpetaOutput:
            missatge = (
                "✅ El directori LLISTATS_OUTPUT/" + grup + "_" + tasca + " existeix"
            )
            st.success(missatge)

            # Comprovam si existeixen els documents adequats en el directori OUTPUT

            llistaArxiusTeoricsOutput, disponibilitatArxiuOutput = logic_estructura_1_03.relacioArxiusPresents("OUTPUT", grup, tasca)

            relacioArxiusOutput = {
                "ARXIU": llistaArxiusTeoricsOutput,
                "DISPONIBLE": disponibilitatArxiuOutput,
            }

            st.dataframe(
                relacioArxiusOutput,
                width="stretch",
                column_config={
                    "ARXIU": "Arxiu",
                    "DISPONIBLE": "Disponible",
                },
            )

        else:
            missatge = (
                "❌ El directori LLISTATS_OUTPUT/" + grup + "_" + tasca + " NO existeix"
            )
            st.error(missatge)


    # ====================================================================
    # 3.1 VISTA PROFESOR - TAB COMPRES
    # ====================================================================

    with tab_compres:

        st.subheader("CORRECCIÓ COMPRES")

        # Abans de fer la correcció, comprovem si hi ha correccions anteriors:
        prefixNomFitxerCorreccioCompres = grup + "_" + tasca + "_COMPRES_"
        rutaHistoricsCorreccions = (
            os.getcwd() + "/" + carpetaOUTPUT + "/" + prefixNomFitxerCorreccioCompres
        )
        patro = rutaHistoricsCorreccions + "*"
        # la variable 'patro' a més de contenir la ruta a la carpeta, també
        # inclou la part comé del nom del fitxer, i amb l'asterisc (*),
        # obtindrem tots els arxius que compleixen el patró

        llistaFitxersCorreccio = glob.glob(patro)

        calCorregirCompres = False

        if len(llistaFitxersCorreccio) > 0:
            st.warning("Hi ha correccions anteriors per a aquesta tasca")
            opcioCorreccio = st.selectbox(
                "Les compres han estat corregides anteriorment. Vols repetir la correcció?",
                ("Sí", "No"),
                index=None,
                placeholder="Selecciona una opció...",
            )
            if opcioCorreccio is None:
                st.error("❌ Per continuar, cal seleccionar una opció")
                # st.stop()
            elif opcioCorreccio == "Sí":
                calCorregirCompres = True
                st.success("✅ CORRECCIÓ ACTIVADA")
                # Aquí va el resto del código de compres corregides
            elif opcioCorreccio == "No":
                calCorregirCompres = False
                st.info("ℹ️ CORRECCIÓ DESACTIVADA")
                # Código alternativo si no corregir
        elif len(llistaFitxersCorreccio) == 0 or len(llistaFitxersCorreccio) is None:
            calCorregirCompres = True
            st.success("✅ CORRECCIÓ ACTIVADA")

        if calCorregirCompres:
            # Cridam a la funció de correcció de compres
            # Creamos el contenedor visual
            with st.spinner(
                "⏳ S'ESTA CORREGINT LES OPERACIONS DE COMPRES... Cal tenir una mica de paciencia (entre 10 i 15 segons)"
            ):
                # La ejecución se detiene aquí hasta que la función hace el return
                (
                    dfCorreccioComandesCompra,
                    dfCorrecioAlbaransCompra,
                    dfCorrecioFacturesCompra,
                ) = logic_compres_1_03.correccioCompres(
                    grup, tasca, carpetaINPUT, carpetaOUTPUT
                )

            # Una vez fuera del bloque 'with', el spinner desaparece solo
            st.success("✅ CORRECCIÓN COMPLETADA")

        if calCorregirCompres == False:
            # Recuperem les dades de la correcció anterior
            # carregaCSV(fileName, carpeta)

            fileName01 = (
                grup
                + "_"
                + tasca
                + "_"
                + "COMPRES_"
                + "11_DF_CORRECCIO_COMANDES_COMPRA.csv"
            )

            dfCorreccioComandesCompra = logic_comu.carregaCSV(fileName01, carpetaOUTPUT)

            fileName02 = (
                grup
                + "_"
                + tasca
                + "_"
                + "COMPRES_"
                + "12_DF_CORRECCIO_ALBARANS_COMPRA.csv"
            )

            dfCorrecioAlbaransCompra = logic_comu.carregaCSV(fileName02, carpetaOUTPUT)

            fileName03 = (
                grup
                + "_"
                + tasca
                + "_"
                + "COMPRES_"
                + "13_DF_CORRECCIO_FACTURES_COMPRA.csv"
            )

            dfCorrecioFacturesCompra = logic_comu.carregaCSV(fileName03, carpetaOUTPUT)

        if dfCorreccioComandesCompra is not None:
            st.subheader("Comandes corregides")
            # Num. Comanda compra
            # Empreses ==
            # Proveïdors ==
            # Dates emisió ==
            # Num. Comanda ==
            # Import ==
            # Estat Comanda OK
            # Estat Fact. Comanda OK
            columnesMostrar = [
                "Real Empresa",
                "Num. Comanda compra",
                "Empreses ==",
                "Proveïdors ==",
                "Dates emisió ==",
                "Num. Comanda ==",
                "Import ==",
                "Estat Comanda OK",
                "Estat Fact. Comanda OK",
            ]

            st.dataframe(dfCorreccioComandesCompra[columnesMostrar])
            st.divider()
        elif dfCorreccioComandesCompra is None:
            st.subheader("No s'han trobat comandes per corregir")
            st.divider()

        if dfCorrecioAlbaransCompra is not None:
            st.subheader("Albarans corregits")
            st.dataframe(dfCorrecioAlbaransCompra)
            st.divider()
        elif dfCorrecioAlbaransCompra is None:
            st.subheader("No s'han trobat albarans per corregir")
            st.divider()

        if dfCorrecioFacturesCompra is not None:
            st.subheader("Factures corregides")
            st.dataframe(dfCorrecioFacturesCompra)
            st.divider()
        elif dfCorrecioFacturesCompra is None:
            st.subheader("No s'han trobat factures per corregir")
            st.divider()

    with tab_vendes:
        st.subheader("CORRECCIÓ VENDES")

    # ====================================================================
    # 3.3 VISTA PROFESOR - TAB INVENTARI
    # ====================================================================

    with tab_inventari:
        st.subheader("CORRECCIÓ INVENTARI")

        # Abans de fer la correcció, comprovem si hi ha correccions anteriors:
        prefixNomFitxerCorreccioInventari = grup + "_" + tasca + "_INVENTARI_"
        rutaLlistatsOutputInventari = (
            os.getcwd() + "/" + carpetaOUTPUT + "/" + prefixNomFitxerCorreccioInventari
        )
        patro = rutaLlistatsOutputInventari + "*"
        # la variable 'patro' a més de contenir la ruta a la carpeta, també
        # inclou la part comé del nom del fitxer, i amb l'asterisc (*),
        # obtindrem tots els arxius que compleixen el patró

        llistaFitxersCorreccioInventari = glob.glob(patro)

        _ = """
        st.warning("*******************************************************")
        # Ruta específica al directori LLISTATS_OUTPUT
        ruta = os.getcwd() + "/" + carpetaOUTPUT

        # Todos los archivos del directorio (cualquier extensión)
        todos_archivos = glob.glob(os.path.join(ruta, "*"))
        nombres_todos = [
            os.path.basename(f) for f in todos_archivos if os.path.isfile(f)
        ]
        # print("Archivos en la carpeta:", nombres_todos)

        # ADG32O_02.12_INVENTARI_40_CORRECCIO_INVENTARI_EMPRESA_PRODUCTE.csv
        # ADG32O_02.12_INVENTARI_41_CORRECCIO_INVENTARI_EMPRESA.csv

        fitxer40 = (
            grup
            + "_"
            + tasca
            + "_INVENTARI_"
            + "40_CORRECCIO_INVENTARI_EMPRESA_PRODUCTE.csv"
        )
        fitxer41 = (
            grup + "_" + tasca + "_INVENTARI_" + "41_CORRECCIO_INVENTARI_EMPRESA.csv"
        )

        if fitxer40 in nombres_todos:
            missatge = "✅ S'HA TROBAT L'ARXIU DE CORRECCIÓ: " + fitxer40
            st.success(missatge)
            existeixFitxer40 = True
        else:
            missatge = "❌ NO S'HA TROBAT L'ARXIU DE CORRECCIÓ: " + fitxer40
            st.error(missatge)
            existeixFitxer40 = False

        if fitxer41 in nombres_todos:
            missatge = "✅ S'HA TROBAT L'ARXIU DE CORRECCIÓ: " + fitxer41
            st.success(missatge)
            existeixFitxer41 = True
        else:
            missatge = "❌ NO S'HA TROBAT L'ARXIU DE CORRECCIÓ: " + fitxer41
            st.error(missatge)
            existeixFitxer41 = False

        if existeixFitxer40 and existeixFitxer41:
            st.success("AQUI ESTA LA CORRECCIÓ DESADA")
        else:
            st.error("❌ CAL TORNAR REALITZAR LA CORRECCIÓ")

        st.warning("*******************************************************")

        """

        calCorregirInventari = False

        if len(llistaFitxersCorreccioInventari) > 0:
            st.warning("Hi ha correccions anteriors per a aquesta tasca")
            opcioCorreccio = st.selectbox(
                "L'inventari ja ha estat corregit anteriorment. Vols repetir la correcció?",
                ("Sí", "No"),
                index=None,
                placeholder="Selecciona una opció...",
            )
            if opcioCorreccio is None:
                st.error("❌ Per continuar, cal seleccionar una opció")
                # st.stop()
            elif opcioCorreccio == "Sí":
                calCorregirInventari = True
                st.success("✅ CORRECCIÓ ACTIVADA")
                # Aquí va el resto del código de compres corregides
            elif opcioCorreccio == "No":
                calCorregirInventari = False
                st.info("ℹ️ CORRECCIÓ DESACTIVADA")
                # Código alternativo si no corregir

        elif (
            len(llistaFitxersCorreccioInventari) == 0
            or len(llistaFitxersCorreccioInventari) is None
        ):
            calCorregirInventari = True
            st.success("✅ CORRECCIÓ ACTIVADA")

        if calCorregirInventari:
            # Cridam a la funció de correcció de l'inventari
            # Creamos el contenedor visual
            with st.spinner(
                "⏳ S'ESTA CORREGINT L'INVENTARI... Cal tenir una mica de paciencia (entre 10 i 15 segons)"
            ):
                # La ejecución se detiene aquí hasta que la función hace el return
                (
                    df_correccio_inventari_empresa_producte,
                    df_correccio_inventari_empresa,
                ) = logic_inventari_1_03.correccioInventari(
                    grup, tasca, carpetaINPUT, carpetaOUTPUT
                )

            # Una vez fuera del bloque 'with', el spinner desaparece solo
            st.success("✅ CORRECCIÓN COMPLETADA")

        if calCorregirInventari == False:
            # Recuperem les dades de la correcció anterior
            # carregaCSV(fileName, carpeta)

            fileName01 = (
                grup
                + "_"
                + tasca
                + "_INVENTARI_"
                + "31_DF_CORRECCIO_INVENTARI_EMPRESA_PRODUCTE.csv"
            )

            df_correccio_inventari_empresa_producte = logic_comu.carregaCSV(
                fileName01, carpetaOUTPUT
            )

            fileName02 = (
                grup
                + "_"
                + tasca
                + "_INVENTARI_"
                + "32_DF_CORRECCIO_INVENTARI_EMPRESA.csv"
            )

            df_correccio_inventari_empresa = logic_comu.carregaCSV(
                fileName02, carpetaOUTPUT
            )

        if df_correccio_inventari_empresa_producte is not None:
            st.subheader("CORRECCIÓ INVENTARI PER EMPRESA - PRODUCTE")
            st.dataframe(df_correccio_inventari_empresa_producte)
            st.divider()
        else:
            st.info(
                "ℹ️ No hi ha correcció de l'inventari per empresa-producte per a aquesta tasca"
            )

        if df_correccio_inventari_empresa is not None:
            st.subheader("CORRECCIÓ INVENTARI PER EMPRESA")
            st.dataframe(df_correccio_inventari_empresa)
            st.divider()
        else:
            st.info(
                "ℹ️ No hi ha correcció de l'inventari per empresa per a aquesta tasca"
            )


# ==============================================================================
# 4. VISTA ALUMNO (LECTURA DEL HISTÓRICO)
# ==============================================================================

elif rol == "Alumne":

    col_sel1, col_sel2 = st.columns(2)

    with col_sel1:
        modulo_consulta = st.selectbox(
            "Selecciona: ", ["COMPRES", "VENDES", "INVENTARI"]
        )

    with col_sel2:
        # Buscamos en la carpeta qué archivos hay de ese módulo
        archivos_disponibles = [
            f
            for f in os.listdir(CARPETA_HISTORICO)
            if f.startswith(modulo_consulta) and f.endswith(".xlsx")
        ]
        # Los ordenamos para que salga el último primero
        archivos_disponibles.sort(reverse=True)

        seleccio_tasca = st.selectbox("Selecciona la entrega: ", archivos_disponibles)

    if seleccio_tasca:
        # Cargamos el archivo seleccionado desde el disco duro
        ruta_archivo = os.path.join(CARPETA_HISTORICO, seleccio_tasca)
        try:
            df_notas = pd.read_excel(ruta_archivo)

            # Selector de Alumno
            lista_empresas = sorted(df_notas["EMPRESA"].unique().astype(str))
            empresa_seleccionada = st.selectbox(
                "Selecciona la teva empresa:", lista_empresas
            )

            if empresa_seleccionada:
                st.divider()
                st.subheader(f"Resultados: {empresa_seleccionada} - {seleccio_tasca}")

                # Filtrar y mostrar
                # Convertimos a string por si acaso pandas leyó el expediente como número
                df_alumno = df_notas[
                    df_notas["EMPRESA"].astype(str) == str(empresa_seleccionada)
                ]

                st.dataframe(df_alumno, width="stretch", hide_index=True)

                # Resumen visual
                errores = df_alumno[df_alumno["RESULTAT"] != "OK"]
                if errores.empty:
                    st.success("🎉 ¡Excelente! Sin errores detectados.")
                else:
                    st.error(f"⚠️ Tienes {len(errores)} líneas para revisar.")

        except Exception as e:
            st.error(f"Error al cargar el archivo histórico: {e}")

    else:
        st.info("No hay correcciones publicadas para este módulo todavía.")

# ==============================================================================
# 5. BLOQUEO
# ==============================================================================
elif rol == "Profesor" and not acceso_profesor:
    st.error("⛔ Acceso denegado.")
