import logic_comu
import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import logic_compres
import logic_comu
import time

# INICIALITZACIO DELS ESTATS DE LES ETAPES DE CORRECCIÓ
if "introduccio_grup_tasca_data" not in st.session_state:
    st.session_state.introduccio_grup_tasca_data = False
if "compres_insercio_data_entrega" not in st.session_state:
    st.session_state.compres_insercio_data_entrega = False
if "compres_preparacio_llistats" not in st.session_state:
    st.session_state.compres_preparacio_llistats = False
if "compres_carrega_llistats" not in st.session_state:
    st.session_state.compres_carrega_llistats = False
if "compres_neteja_tipus" not in st.session_state:
    st.session_state.compres_neteja_tipus = False
if "compres_duplicats" not in st.session_state:
    st.session_state.compres_duplicats = False
if "compres_merge_dataframes" not in st.session_state:
    st.session_state.compres_merge_dataframes = False
if "compres_operacions_orfes" not in st.session_state:
    st.session_state.compres_operacions_orfes = False

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

    tab_compres, tab_vendes, tab_inventari = st.tabs(["COMPRES", "VENDES", "INVENTARI"])

    # ====================================================================
    # 3.1 VISTA PROFESOR - TAB COMPRES
    # ====================================================================

    with tab_compres:

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
                [
                    "02.01",
                    "02.02",
                    "02.03",
                    "02.04",
                    "02.05",
                    "02.06",
                    "02.07",
                    "02.08",
                    "02.09",
                    "02.10",
                    "02.11",
                    "02.12",
                    "02.13",
                    "02.14",
                    "02.15",
                    "02.16",
                    "02.17",
                    "02.18",
                    "02.19",
                    "02.20",
                    "02.21",
                    "02.22",
                    "02.23",
                    "02.24",
                    "02.25",
                    "02.26",
                    "02.27",
                    "02.28",
                    "02.29",
                    "02.30",
                    "02.31",
                    "02.32",
                    "02.33",
                    "02.34",
                    "02.35",
                    "02.36",
                    "02.37",
                    "02.38",
                    "02.39",
                    "02.40",
                    "02.41",
                    "02.42",
                    "02.43",
                    "02.44",
                    "02.45",
                    "02.46",
                    "02.47",
                    "02.48",
                    "02.49",
                    "02.50",
                ],
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

        prefNomFitxerCorreccio = grup + "_" + tasca + "_"

        st.divider()

        st.session_state.introduccio_grup_tasca_data = True

        # ====================================================================
        # 2. INTRODUCIO DATA ENTREGA TASCA
        # ====================================================================

        if st.session_state.introduccio_grup_tasca_data:

            st.title(
                "Registre de les dates en que els alumnes han entregat les tasques"
            )

            # 1. Definim els expedients i noms de les empreses
            expedients = [
                5796,
                6265,
                6320,
                6352,
                6356,
                6366,
                6368,
                6369,
                6427,
                6428,
                6431,
                6467,
                6478,
                6702,
                6706,
                6707,
                6713,
                6734,
                6746,
                6777,
                6792,
                6844,
            ]
            empreses_predefinides = [
                "ADG32 5796 NSACARES SL",
                "ADG32 6265 SMORENO SL",
                "ADG32 6320 MNAVARRO SL",
                "ADG32 6352 SAANANOU SL",
                "ADG32 6356 WAANANOU SL",
                "ADG32 6366 JMORAGUES SL",
                "ADG32 6368 LPIZA SL",
                "ADG32 6369 VMASTRANGELO SL",
                "ADG32 6427 NANANOU SL",
                "ADG32 6428 ABOUBAL SL",
                "ADG32 6431 GZOUGGAGHI SL",
                "ADG32 6467 WCHANTAH SL",
                "ADG32 6478 CBAUZA SL",
                "ADG32 6702 NFORNES SL",
                "ADG32 6706 NSUIYHI SL",
                "ADG32 6707 MOUAZINE SL",
                "ADG32 6713 BCARBONELL SL",
                "ADG32 6734 LABOLAFIO SL",
                "ADG32 6746 ELLADO SL",
                "ADG32 6777 JGARCIA SL",
                "ADG32 6792 PCAPO SL",
                "ADG32 6844 TTRAMULLAS SL",
            ]

            with st.form("formulari_dates_entrega_tasca"):
                st.subheader(
                    "Indica les dates en que els alumnes han entregat les tasques"
                )

                # Creamos listas vacías para almacenar los inputs temporalmente
                datos_finales = []

                # 2. Generamos los 44 inputs (22 nombres + 4 fechas)
                for i in range(22):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        exp = st.text_input(
                            f"Expedient {i+1}",
                            value=expedients[i],
                            key=f"exp_{i}",
                        )
                    with col2:
                        nom = st.text_input(
                            f"Empresa {i+1}",
                            value=empreses_predefinides[i],
                            key=f"emp_{i}",
                        )
                    with col3:
                        data = st.date_input(
                            f"Data entrega {i+1}",
                            value=dataVto,
                            key=f"fec_{i}",
                        )
                    with col4:
                        est = st.selectbox(
                            f"Estat entrega {i+1}",
                            options=["ENTREGADA", "NO ENTREGADA"],
                            index=0,
                            key=f"est_{i}",
                        )

                    # Guardamos cada fila como un diccionario
                    datos_finales.append(
                        {
                            "Expediente": exp,
                            "Empresa": nom,
                            "Data entrega": data.strftime("%Y-%m-%d"),
                            "Estat entrega": est,
                        }
                    )

                st.markdown("---")

                # Botón de envío

                enviado = st.form_submit_button("ENVIAR FORMULARI")

            if enviado:
                st.success("✅ Ejecución reanudada. Datos procesados.")

            # 4. Creación del DataFrame
            df_data_entrega_tasca = pd.DataFrame(datos_finales)

            # Mostramos el resultado
            st.subheader("DataFrame Resultante")
            st.dataframe(df_data_entrega_tasca, use_container_width=True)

            # DESAM CSV
            carpetaDesti = "LLISTATS_CSV"
            filename_df_data_entrega_tasca = (
                prefNomFitxerCorreccio + "df_data_entrega_tasca.csv"
            )
            logic_comu.desaCSV(
                df_data_entrega_tasca, filename_df_data_entrega_tasca, carpetaDesti
            )

            # Inserim la data de entrega en df_real
            df_real = logic_comu.insereixDataEntregaEnDFDesti(
                df_real, "R_FECHA_ENTREGA", "R_EMPRESA_C", df_data_entrega_tasca
            )

            st.divider()
            st.session_state.compres_insercio_data_entrega = True
            

        # ====================================================================
        # 3.1.1 CARREGA LLISTATS - ARXIUS AMB DADES REALS i DADES ALUMNAT
        # ====================================================================

        if st.session_state.compres_insercio_data_entrega:
            st.subheader("Adjunta els llistats amb les dades per corregir la tasca")

            col1, col2 = st.columns(2)

            with col1:
                st.badge("DADES REALS FROM EMPRESAULA")
                file_compres_real = st.file_uploader(
                    "Adjunta el fitxer 0_DATOS_COMPRAS_REALES.csv",
                    type=["csv"],
                    key="real_c",
                )
                st.badge("DADES COMANDES FROM ALUMNAT")
                file_dades_compra_comandes_alumne = st.file_uploader(
                    "Subir 1_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv",
                    type=["csv"],
                    key="ped_c",
                )

            with col2:
                st.badge("DADES ALBARANS FROM ALUMNAT")
                file_dades_compra_albarans_alumne = st.file_uploader(
                    "Subir 2_DATOS_ALBARANES_COMPRA_ALUMNOS.csv",
                    type=["csv"],
                    key="alb_c",
                )
                st.badge("DADES FACTURES FROM ALUMNAT")
                file_dades_compra_factures_alumne = st.file_uploader(
                    "Subir 3_DATOS_FACTURAS_COMPRA_ALUMNOS.csv",
                    type=["csv"],
                    key="fac_c",
                )

            # Comprovam si s'han adjuntat tots els arxius per INICIAR la pujada al servidor
            if not (
                file_compres_real
                and file_dades_compra_comandes_alumne
                and file_dades_compra_albarans_alumne
                and file_dades_compra_factures_alumne
            ):
                st.error(
                    "No podrem continuar fins que no hagis adjuntat tots els llistats sol·licitats"
                )
                st.stop()

        st.session_state.compres_preparacio_llistats = True

        st.divider()

        # ====================================================================
        # 3.1.2 ENVIAMENT ARXIUS PER AL SEU TRACTAMENT
        # ===================================================================

        if st.session_state.compres_preparacio_llistats:

            # if st.button("⚙️ PUJAR I PROCESSAMENT INICIAL DE LLISTATS", type="primary"):

            st.subheader("Carrega inicial de les dades")

            st.write("⏳ Pujant arxius al servidor... ⏳")

            # --- 2. PUJAM ELS ARXIUS AMB FUNCIO carregaArxius() ---
            # Li passam els 5 arxius que hem pujat a la WEB

            df_real, df_ped, df_alb, df_fac = logic_compres.carregaArxius(
                file_compres_real,
                file_dades_compra_comandes_alumne,
                file_dades_compra_albarans_alumne,
                file_dades_compra_factures_alumne,
            )

            listaDFs01 = [df_real, df_ped, df_alb, df_fac]

            if any(dadesCarregades is None for dadesCarregades in listaDFs01):
                st.error("NO ES POT SEGUIR EXECUTANT EL PROGRAMA PER FALTA DE DADES")
                # ATURAM L'EXECUCIO DEL PROGRAMA. EL CODI POSTERIOR NO
                # S'EXECUTARA, DE TAL FORMA QUE NO NECESSITEM USAR ELSE
                st.stop()

            time.sleep(3)

            st.success(
                "✅ LA CÀRREGA DELS LLISTATS I LA SEVA CONVERSIÓ A DATAFRAMES HA ESTAT EXITOSA"
            )

            st.session_state.compres_carrega_llistats = True

            st.divider()

        """
        # ==========================================================
        # 3.1.3 DATA ENTREGA TREBALL
        # ==========================================================

        if st.session_state.compres_carrega_llistats:

            st.subheader(
                "Data de lliurament de la tasca i disponibilitat de les factures de compra per al seu registre en ODOO"
            )

            st.write(
                "Com ja sabem les factures de compra estan disponibles al dia següent d'haver fet la comanda. Per determinar si l'alumnat ha d'haver registrat o no les factures de compra, cal introduir les dates d'entrega dels treballs i comparar-les amb la dates en que la factures de compra estan disponibles."
            )

            # print(df_real)

            df_real = logic_compres.insertaDataEntregaTreball(df_real, grup, dataVto)

            if df_real is None:
                st.error(
                    "No ha estat possible inserir la data d'entrega en el dataframe df_real. finalitza la execució d'aquesta APP. Disculpeu les molesties."
                )
                # ATURAM L'EXECUCIO DEL PROGRAMA. EL CODI POSTERIOR NO
                # S'EXECUTARA, DE TAL FORMA QUE NO NECESSITEM USAR ELSE
                st.divider()
                st.stop()

            # df_real no es NONE, podem continuar
            st.success(
                "Les dates d'entrega s'han introduït en el dataframe (df_real) per cada empresa/operacio (DF_REAL recull totes les operacions de compra realitzades pels alumnes en EMPRESAULA)"
            )

            # Inserim la data de entrega en df_real
            df_real = logic_comu.insereixDataEntregaEnDFDesti(
                df_real, "R_FECHA_ENTREGA", "R_EMPRESA_C", df_editat
            )

            st.session_state.compres_insercio_data_entrega = True
            st.divider()
"""
        # ==========================================================
        # 3.1.4 NETEJA VARIABLES
        # ==========================================================

        if st.session_state.compres_carrega_llistats:
            st.subheader("Neteja de variables")
            st.write(
                "També cal realitzar una serie d'operacions dirigidaes a la neteja i homogenitzacio de les dades incloses en els llistats (dates, valors numerics...)"
            )

            df_real = logic_comu.netejaTipusDadesDFReal(df_real)
            df_ped = logic_comu.netejaTipusDadesDFPed(df_ped)
            df_alb = logic_comu.netejaTipusDadesDFAlb(df_alb)
            df_fac = logic_comu.netejaTipusDadesDFFac(df_fac)

            if df_real is None or df_ped is None or df_alb is None or df_fac is None:
                st.error(
                    "No es pot executar la neteja en el tipus de variable. Finalitza la execució d'aquesta APP"
                )
                # ATURAM L'EXECUCIO DEL PROGRAMA. EL CODI POSTERIOR NO
                # S'EXECUTARA, DE TAL FORMA QUE NO NECESSITEM USAR ELSE
                st.stop()

            st.success("✅ LA NETEJA DELS TIPUS DE DADES HA ESTAT EXITOSA")
            st.session_state.compres_neteja_tipus = True

            st.divider()

        # ==========================================================
        # 3.1.5 COMANDES DUPLICADES
        # ==========================================================

        if st.session_state.compres_neteja_tipus:

            st.subheader("COMANDES DUPLICADES")
            st.write(
                "A nivell de compres, les operacions que normalment es dupliquen son les comandes: l'alumne introdueix 2 cops la mateixa comanda o bé introdueix dues comandes diferents, introduint el mateix número de comanda. Per tot això, nomes tindrem en compte possibles duplicats en df_ped."
            )

            df_ped_duplicats = logic_comu.obtenirDuplicats(df_ped, "A_NUMERO_CP")

            if len(df_ped_duplicats) > 0:
                st.write("S'han trobat les següents comandes duplicades en df_ped:")
                st.dataframe(df_ped_duplicats)
                st.session_state.compres_duplicats = True
                st.divider()
                # DESAM CSV
                carpetaDesti = "HISTORIC_CORRECCIONS"
                filename = prefNomFitxerCorreccio + "df_ped_duplicats.csv"
                logic_comu.desaCSV(df_ped_duplicats, filename, carpetaDesti)
            elif len(df_ped_duplicats) == 0 or df_ped_duplicats is None:
                st.write("No s'han trobat comandes duplicades en df_ped")
                st.session_state.compres_duplicats = True
                st.divider()

        # ==========================================================
        # 3.1.6 UNIO DE DATAFRAMES (merge)
        # ==========================================================

        if st.session_state.compres_duplicats == True:
            st.subheader("Unio de DATAFRAMES (merge)")
            st.markdown(
                """
                Per poder corregir les operacions de compra, realitzarem 3 unions de dataframes:
                
                1. Unió entre df_real i df_ped
                2. Unió entre df_real i df_alb
                3. Unió entre df_real i df_fac
                
                En df_real es relacionen totes les operacions de compra que els alumnes han realitzat en EMPRESAULA, a nivell de comanda, albarà i factura. En els altres dataframes df_ped, df_alb i df_fac, es relacionen les operacions que l'alumne ha registrat a nivell de comanda (df_ped), albarà (df_alb) i factura (df_fac). 
                Per tant, si volem determinar si els registres dels alumnes son correctes, cal relacionar l'operació real amb l'operació registrada.
                """
            )

            # UNIO ENTRE df_real i df_ped
            df_real_ped, df_real, df_real_alb, df_real_fac = (
                logic_compres.uneixDataFrames(
                    df_real,
                    df_ped,
                    df_alb,
                    df_fac,
                )
            )

            if (
                df_real_ped is not None
                and df_real is not None
                and df_real_alb is not None
                and df_real_fac is not None
            ):
                st.success("Unió correcta entre els dataframes")
                st.session_state.compres_merge_dataframes = True
                st.divider()

            else:
                st.error("Error en la unió entre els dataframes")
                st.divider()
                st.stop()

        # ==========================================================
        # 3.1.7 RESEARCH OF ORPHAN OPERATIONS
        # ==========================================================

        if st.session_state.compres_merge_dataframes:
            st.subheader("Recerca d'operacions ORFES")
            st.markdown(
                """
                Es pot donar el cas que els alumnes hagin creat operacions, les quals no tenen una comanda real de referencia (quasevol operació de compra sempre està associada a una comanda real). Per exemple, pot haver registrat una comanda de compra indicant un numero de comanda equivocat, la qual cosa fa que no es pugui associar aquesta operació a cap comanda real, o per exemple, por haver introduit la factura de compra sense establir una relació a la comanda real que s'esta facturant.
                Els registres resultants son considerats ORFES, perque no tenen cap comanda real associada.
                
                """
            )

            df_nomesComandesOrfes, df_nomesAlbaransOrfes, df_nomesFacturesOrfes = (
                logic_compres.researchOrphanOperations(
                    df_real, df_ped, df_alb, df_fac, prefNomFitxerCorreccio
                )
            )

            if len(df_nomesComandesOrfes) > 0:
                st.subheader("Comandes orfes")
                st.dataframe(df_nomesComandesOrfes)
                st.divider()
            elif len(df_nomesComandesOrfes) == 0 or df_nomesComandesOrfes is None:
                st.subheader("No s'han trobat comandes orfes")

            if len(df_nomesAlbaransOrfes) > 0:
                st.subheader("Albarans orfes")
                st.dataframe(df_nomesAlbaransOrfes)
                st.divider()
            elif len(df_nomesAlbaransOrfes) == 0 or df_nomesAlbaransOrfes is None:
                st.subheader("No s'han trobat albarans orfes")

            if len(df_nomesFacturesOrfes) > 0:
                st.subheader("Factures orfes")
                st.dataframe(df_nomesFacturesOrfes)
                st.divider()
            elif len(df_nomesFacturesOrfes) == 0 or df_nomesFacturesOrfes is None:
                st.subheader("No s'han trobat factures orfes")

            st.divider()
            st.session_state.compres_operacions_orfes = True

        # ==========================================================
        # 3.1.8 CORRECCIO D'OPERACIONS - COMANDES
        # ==========================================================

        if st.session_state.compres_operacions_orfes:
            st.subheader("Correcció d'operacions")

            dfCorrecioComandesCompra = logic_compres.correccioComandes(
                df_real_ped, prefNomFitxerCorreccio
            )

            if dfCorrecioComandesCompra is not None:
                st.subheader("Comandes corregides")
                st.dataframe(dfCorrecioComandesCompra)
                st.divider()
            elif dfCorrecioComandesCompra is None:
                st.subheader("No s'han trobat comandes per corregir")
                st.divider()

            st.session_state.compres_operacions_corregides = True

    with tab_vendes:
        st.write("Gestió de correccions de vendes")

    with tab_inventari:
        st.write("Gestió de correccions d'inventari")

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

                st.dataframe(df_alumno, use_container_width=True, hide_index=True)

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
