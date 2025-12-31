import streamlit as st
import pandas as pd
import os

# INICIALITZACIO DELS ESTATS DE LES ETAPES DE CORRECCIÓ
if "compres_carrega_llistats" not in st.session_state:
    st.session_state.compres_carrega_llistats = False
if "compres_insercio_dates_entrega_neteja" not in st.session_state:
    st.session_state.compres_insercio_dates_entrega_neteja = False


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

        st.subheader("NOVA CORRECCIÓ COMPRES")

        colA, colB = st.columns(2)

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

        # ====================================================================
        # 3.1.1 CARREGA LLISTATS - ARXIUS AMB DADES REALS i DADES ALUMNAT
        # ====================================================================

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("DADES REALS")
            file_compres_real = st.file_uploader(
                "Adjunta el fitxer 0_DATOS_COMPRAS_REALES.csv",
                type=["csv"],
                key="real_c",
            )
            file_dates_entrega_treballs = st.file_uploader(
                "Adjunta el fitxer 4_FECHA_ENTREGA_TRABAJOS.csv",
                type=["csv"],
                key="fec_c",
            )

        with col2:
            st.subheader("DADES ALUMNAT")
            file_dades_compra_comandes_alumne = st.file_uploader(
                "Subir 1_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv", type=["csv"], key="ped_c"
            )
            file_dades_compra_albarans_alumne = st.file_uploader(
                "Subir 2_DATOS_ALBARANES_COMPRA_ALUMNOS.csv", type=["csv"], key="alb_c"
            )
            file_dades_compra_factures_alumne = st.file_uploader(
                "Subir 3_DATOS_FACTURAS_COMPRA_ALUMNOS.csv", type=["csv"], key="fac_c"
            )

        # ====================================================================
        # 3.1.2 ENVIAMENT ARXIUS PER AL SEU TRACTAMENT
        # ===================================================================

        if st.button("⚙️ PUJAR I PROCESSAMENT INICIAL DE LLISTATS", type="primary"):
            # Comprovam si s'ha seleccionat el grup i la tasca
            # Si no es selecciona cap, mostrem un missatge d'error i aturem la execucio
            if grup is None:
                st.error("Per continuar, cal indicar el grup que ha fet la tasca")
                st.stop()

            if tasca is None:
                st.error("Per continuar, cal indicar la tasca objecte de correcció")
                st.stop()

            # Comoprovam si s'han adjuntat tots els arxius per INICIAR la pujada al servidor
            if not (
                file_compres_real
                and file_dates_entrega_treballs
                and file_dades_compra_comandes_alumne
                and file_dades_compra_albarans_alumne
                and file_dades_compra_factures_alumne
            ):
                st.error(
                    "No podrem continuar fins que no hagis adjuntat tots els llistats sol·licitats"
                )
                # ATURAM L'EXECUCIO DEL PROGRAMA. EL CODI POSTERIOR NO
                # S'EXECUTARA, DE TAL FORMA QUE NO NECESSITEM USAR ELSE
                st.stop()

            st.write("⏳ Pujant arxius al servidor... ⏳")

            # --- 1. IMPORTAR LÒGICA CORRECCIÓ COMPRES ---
            # Esto carga el archivo logic_compras.py que creamos antes
            import logic_compres
            import logic_comu

            # --- 2. PUJAM ELS ARXIUS AMB FUNCIO carregaArxius() ---
            # Li passam els 5 arxius que hem pujat a la WEB

            df_real, df_ped, df_alb, df_fac, df_fechas = logic_compres.carregaArxius(
                file_compres_real,
                file_dades_compra_comandes_alumne,
                file_dades_compra_albarans_alumne,
                file_dades_compra_factures_alumne,
                file_dates_entrega_treballs,
            )

            listaDFs01 = [df_real, df_ped, df_alb, df_fac, df_fechas]

            if any(dadesCarregades is None for dadesCarregades in listaDFs01):
                st.error("NO ES POT SEGUIR EXECUTANT EL PROGRAMA PER FALTA DE DADES")
                # ATURAM L'EXECUCIO DEL PROGRAMA. EL CODI POSTERIOR NO
                # S'EXECUTARA, DE TAL FORMA QUE NO NECESSITEM USAR ELSE
                st.stop()

            st.success(
                "✅ LA CÀRREGA DELS LLISTATS I LA SEVA CONVERSIÓ A DATAFRAMES HA ESTAT EXITOSA"
            )
            st.session_state.compres_carrega_llistats = True

            st.divider()

            # ==========================================================
            # 3.1.3 DATA ENTREGA TREBALL I NETEJA VARIABLES
            # ==========================================================

            if st.session_state.compres_carrega_llistats:

                st.write(
                    "Com ja sabem les factures de compra estan disponibles al dia següent d'haver fet la comanda. Per determinar si l'alumnat ha d'haver registrat o no les factures de compra, cal introduir les dates d'entrega dels treballs i comparar-les amb la dates en que la factures de compra estan disponibles."
                )

                if st.session_state.compres_carrega_llistats:
                    st.write(
                        "També cal realitzar una serie d'operacions dirigidaes a la neteja i homogenitzacio de les dades incloses en els llistats (dates, valors numerics...)"
                    )

                if st.session_state.compres_carrega_llistats:
                    if st.button(
                        "⚙️ INSERCIÓ DATA ENTREGA i NETEJA DE VALORS", type="primary"
                    ):

                        # Executam funció

                        st.write(
                            "Iniciant procés de neteja i inserció de data d'entrega..."
                        )
                        st.write(
                            "Aquest procés pot tardar uns minuts, si la tasca te molta dades"
                        )
                        st.write(
                            "Si no tens paciència, puc parar el procés amb el botó 'Parar procés'"
                        )

                        df_real, df_ped, df_alb, df_fac = (
                            logic_compres.insertaDataEntrega_netejaTipusDades(
                                df_real, df_ped, df_alb, df_fac, df_fechas
                            )
                        )

                        listaDFs02 = [df_real, df_ped, df_alb, df_fac]

                        if any(
                            dadesCarregades is None for dadesCarregades in listaDFs02
                        ):
                            st.error(
                                "NO ES POT SEGUIR EXECUTANT EL PROGRAMA PER FALTA DE DADES"
                            )
                            # ATURAM L'EXECUCIO DEL PROGRAMA. EL CODI POSTERIOR NO
                            # S'EXECUTARA, DE TAL FORMA QUE NO NECESSITEM USAR ELSE
                            st.stop()

                        st.success(
                            "✅ LA INSERCIÓ DE LA DATA DE ENTREGA I LA NETEJA DELS TIPUS DE DADES HA ESTAT EXITOSA"
                        )
                        st.session_state.compres_insercio_dates_entrega_neteja = True

                        st.write("PROVAM CODI ABANS DE CONTINUAR")
                    else:
                        st.error("MERDA No s'han carregat tots els arxius necessaris")
                        st.stop()

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
