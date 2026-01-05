import logic_comu
import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import logic_compres
import logic_comu
import time

from st_sessions_state import *

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

    prefNomFitxerCorreccio = grup + "_" + tasca + "_"

    print("ABANS DE INICIAR LES ETAPES DE CORRECCIÓ")
    print(st.session_state.fase01)
    print(st.session_state.fase15)

    st.session_state.fase01 = True
    st.session_state.fase15 = True

    print("DESPRES DE INICIAR LES ETAPES DE CORRECCIÓ")
    print(st.session_state.fase01)
    print(st.session_state.fase15)

    tab_compres, tab_vendes, tab_inventari = st.tabs(["COMPRES", "VENDES", "INVENTARI"])

    # ====================================================================
    # 3.1 VISTA PROFESOR - TAB COMPRES
    # ====================================================================

    with tab_compres:

        # ====================================================================
        # 3.1.1 CARREGA LLISTATS - ARXIUS AMB DADES REALS i DADES ALUMNAT
        # ====================================================================

        if st.session_state.fase01:
            check_llistats = st.checkbox(
                "Els llistats per correcció ja estan pujats al servidor"
            )

            if not check_llistats:

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

                st.session_state.fase02 = True

                st.divider()

                # ==============================================================
                # 3.1.2 ENVIAMENT ARXIUS PER AL SEU TRACTAMENT
                # ==============================================================

                if st.session_state.fase02:

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
                        st.error(
                            "NO ES POT SEGUIR EXECUTANT EL PROGRAMA PER FALTA DE DADES"
                        )
                        # ATURAM L'EXECUCIO DEL PROGRAMA. EL CODI POSTERIOR NO
                        # S'EXECUTARA, DE TAL FORMA QUE NO NECESSITEM USAR ELSE
                        st.stop()

                    time.sleep(3)

                    st.success(
                        "✅ LA CÀRREGA DELS LLISTATS I LA SEVA CONVERSIÓ A DATAFRAMES HA ESTAT EXITOSA"
                    )

                    st.session_state.fase03 = True

                    st.divider()

            else:
                # Cal indicar a quin grup i tasca corresponen les dades
                df_real = logic_comu.carregaCSV(
                    prefNomFitxerCorreccio + "00_DATOS_COMPRAS_REALES.csv",
                    "LLISTATS_CSV",
                )
                df_ped = logic_comu.carregaCSV(
                    prefNomFitxerCorreccio + "01_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv",
                    "LLISTATS_CSV",
                )
                df_alb = logic_comu.carregaCSV(
                    prefNomFitxerCorreccio + "02_DATOS_ALBARANES_COMPRA_ALUMNOS.csv",
                    "LLISTATS_CSV",
                )
                df_fac = logic_comu.carregaCSV(
                    prefNomFitxerCorreccio + "03_DATOS_FACTURAS_COMPRA_ALUMNOS.csv",
                    "LLISTATS_CSV",
                )

                if (
                    df_real is None
                    or df_ped is None
                    or df_alb is None
                    or df_fac is None
                ):
                    st.error("Error al carregar els llistats. Execucio cancelada")
                    st.stop()
                else:
                    st.success(
                        "✅ LA CÀRREGA DELS LLISTATS I LA SEVA CONVERSIÓ A DATAFRAMES HA ESTAT EXITOSA"
                    )
                    st.session_state.fase03 = True
                    st.divider()

        # ==================================================================
        # 2. INTRODUCIO DATA ENTREGA TASCA
        # ==================================================================

        if st.session_state.fase03:

            st.title(
                "Registre de les dates en que els alumnes han entregat les tasques"
            )

            check_data_entrega = st.checkbox(
                "El llistat d'alumnes amb la data que varen entregar la tasca ja està pujat al servidor"
            )

            if not check_data_entrega:

                # 1. Definim els expedients i noms de les empreses
                expedients = llista_expedients_alumnes

                empreses_predefinides = llista_empreses_alumnes

                with st.form("formulari_dates_entrega_tasca"):
                    st.subheader(
                        "Indica les dates en que els alumnes han entregat les tasques"
                    )
                    st.markdown(
                        '<hr style="border:2px solid #2596be">', unsafe_allow_html=True
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
                        st.markdown(
                            '<hr style="border:2px solid #2596be">',
                            unsafe_allow_html=True,
                        )

                    # Botón de envío

                    enviado = st.form_submit_button("ENVIAR DADES DEL FORMULARI")

                if not enviado:
                    st.info(
                        "NO frissam, quan hagis acabat d'emplenar el formulari, fes clic al boto 'ENVIAR DADES DEL FORMULARI i seguirem amb l'execució del programa."
                    )
                    st.stop()

                # 4. Creación del DataFrame
                df_data_lliurament_tasca = pd.DataFrame(datos_finales)

                # Mostramos el resultado
                # st.subheader("DataFrame Resultante")
                # st.dataframe(df_data_lliurament_tasca, width="stretch")

                # DESAM CSV
                carpetaDesti = "LLISTATS_CSV"
                filename = prefNomFitxerCorreccio + "data_lliurament_tasca.csv"
                logic_comu.desaCSV(df_data_lliurament_tasca, filename, carpetaDesti)

                st.divider()
                st.session_state.fase04 = True

            # Si el llistat no estava pujat en SERVIDOR, ara ja hi esta pq.
            # hem executat el FALSE del checkbox.
            # Si el llistat estava pujat en SERVIDOR, hem executat el TRUE del checkbox.
            # Ens trobem en la mateixa situacio que amb el FALSE
            # Tant d'una forma com de l'altre, el llistat ja hi esta pujat en el SERVIDOR

            # Recuperam el llistat de les dades de lliurament de la tasca
            # Cal indicar a quin grup i tasca corresponen les dades
            df_data_lliurament_tasca = logic_comu.carregaCSV(
                prefNomFitxerCorreccio + "data_lliurament_tasca.csv",
                "LLISTATS_CSV",
            )

            # Inserim la data de entrega en df_real
            # Si volem corregir les compres, cal disposar d'aquesta data en el
            # dataframe de dades reals, per podetr determinar si s'han
            # registrat les factures de compra a data de entrega
            df_real = logic_comu.insereixDataEntregaEnDFDesti(
                df_real, "R_FECHA_ENTREGA", "R_EMPRESA_C", df_data_lliurament_tasca
            )

            # També obtindrem un llistat dels alumnes que no han lliurat la tasca
            # No corregirem una tasca que no dsiposam
            df_alumnes_morosos = df_data_lliurament_tasca[
                df_data_lliurament_tasca["Estat entrega"] == "NO ENTREGADA"
            ]

            # Mostram el llistat dels alumnes que no han lliurat la tasca
            st.subheader("Alumnes que no han lliurat la tasca")
            st.dataframe(df_alumnes_morosos, width="stretch")

            # DESAM CSV MOROSOS
            carpetaDesti = "LLISTATS_CSV"
            filename = prefNomFitxerCorreccio + "alumnes_morosos.csv"
            logic_comu.desaCSV(df_alumnes_morosos, filename, carpetaDesti)

            st.divider()
            st.session_state.fase04 = True

        # ==========================================================
        # 3.1.4 NETEJA VARIABLES
        # ==========================================================

        if st.session_state.fase04:
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
            st.session_state.fase05 = True

            st.divider()

        # ==========================================================
        # 3.1.5 COMANDES DUPLICADES
        # ==========================================================

        if st.session_state.fase05:

            st.subheader("COMANDES DUPLICADES")
            st.write(
                "A nivell de compres, les operacions que normalment es dupliquen son les comandes: l'alumne introdueix 2 cops la mateixa comanda o bé introdueix dues comandes diferents, introduint el mateix número de comanda. Per tot això, nomes tindrem en compte possibles duplicats en df_ped."
            )

            df_ped_duplicats = logic_comu.obtenirDuplicats(df_ped, "A_NUMERO_CP")

            if len(df_ped_duplicats) > 0:
                st.write("S'han trobat les següents comandes duplicades en df_ped:")
                st.dataframe(df_ped_duplicats)
                st.session_state.fase06 = True
                st.divider()
                # DESAM CSV
                carpetaDesti = "HISTORIC_CORRECCIONS"
                filename = prefNomFitxerCorreccio + "df_ped_duplicats.csv"
                logic_comu.desaCSV(df_ped_duplicats, filename, carpetaDesti)
            elif len(df_ped_duplicats) == 0 or df_ped_duplicats is None:
                st.write("No s'han trobat comandes duplicades en df_ped")
                st.session_state.fase06 = True
                st.divider()

        # ==========================================================
        # 3.1.6 UNIO DE DATAFRAMES (merge)
        # ==========================================================

        if st.session_state.fase06:

            # Abans d'unir els DFs, cal netejar df_real. ASctualment, dins df_real
            # tenim totes les operacions de compra fetes per tots els alumnes en
            # EMPRESAULA, però no tots els alumnes han lliurat la tasca,
            # per tant, no cal corregir una tasca que no tenim, així que ens
            # podem limitar als alumnes que si varen entregar la tasca.
            # Filtrarem df_real perquè només inclogui les empreses dels alumnes
            # que varen entregar la tasca en temps i forma.

            df_real_filtrada = df_real.merge(
                df_data_lliurament_tasca[
                    df_data_lliurament_tasca["Estat entrega"] == "ENTREGADA"
                ],
                left_on="R_EXPEDIENT_C",
                right_on="Expediente",
                how="inner",
            )

            # DESAM CSV
            carpetaDesti = "LLISTATS_CSV"
            filename = prefNomFitxerCorreccio + "df_real_filtrada.csv"
            logic_comu.desaCSV(df_real_filtrada, filename, carpetaDesti)

            st.subheader("Unio de DATAFRAMES (merge)")
            st.markdown(
                """
                Per poder corregir les operacions de compra, realitzarem 3 unions de dataframes:
                
                1. Unió entre df_real_filtrada i df_ped
                2. Unió entre df_real_filtrada i df_alb
                3. Unió entre df_real_filtrada i df_fac
                
                En df_real es relacionen totes les operacions de compra que els alumnes han realitzat en EMPRESAULA, a nivell de comanda, albarà i factura. En els altres dataframes df_ped, df_alb i df_fac, es relacionen les operacions que l'alumne ha registrat a nivell de comanda (df_ped), albarà (df_alb) i factura (df_fac). 
                Per tant, si volem determinar si els registres dels alumnes son correctes, cal relacionar l'operació real amb l'operació registrada.
                """
            )

            # UNIO ENTRE df_real_filtrada i df_ped
            df_real_ped, df_real_filtrada_clauUnica, df_real_alb, df_real_fac = (
                logic_compres.uneixDataFrames(
                    df_real_filtrada,
                    df_ped,
                    df_alb,
                    df_fac,
                    prefNomFitxerCorreccio,
                )
            )

            if (
                df_real_ped is not None
                and df_real_filtrada_clauUnica is not None
                and df_real_alb is not None
                and df_real_fac is not None
            ):
                st.success("Unió correcta entre els dataframes")
                st.session_state.fase07 = True
                st.divider()

            else:
                st.error("Error en la unió entre els dataframes")
                st.divider()
                st.stop()

        # ==========================================================
        # 3.1.7 RESEARCH OF ORPHAN OPERATIONS
        # ==========================================================

        if st.session_state.fase07:
            st.subheader("Recerca d'operacions ORFES")
            st.markdown(
                """
                Es pot donar el cas que els alumnes hagin creat operacions, les quals no tenen una comanda real de referencia (quasevol operació de compra sempre està associada a una comanda real). Per exemple, pot haver registrat una comanda de compra indicant un numero de comanda equivocat, la qual cosa fa que no es pugui associar aquesta operació a cap comanda real, o per exemple, por haver introduit la factura de compra sense establir una relació a la comanda real que s'esta facturant.
                Els registres resultants son considerats ORFES, perque no tenen cap comanda real associada.
                
                """
            )

            df_nomesComandesOrfes, df_nomesAlbaransOrfes, df_nomesFacturesOrfes = (
                logic_compres.researchOrphanOperations(
                    df_real_filtrada_clauUnica,
                    df_ped,
                    df_alb,
                    df_fac,
                    prefNomFitxerCorreccio,
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
            st.session_state.fase08 = True

        # ==========================================================
        # 3.1.8 CORRECCIO D'OPERACIONS - COMANDES
        # ==========================================================

        if st.session_state.fase08:
            st.subheader("Correcció d'operacions - Comandes")

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

            st.session_state.fase09 = True

        # ==========================================================
        # 3.1.9 CORRECCIO D'OPERACIONS - ALBARANS
        # ==========================================================

        if st.session_state.fase09:
            st.subheader("Correcció d'operacions - Albarans")

            dfCorrecioAlbaransCompra = logic_compres.correccioAlbarans(
                df_real_alb, prefNomFitxerCorreccio
            )

            if dfCorrecioAlbaransCompra is not None:
                st.subheader("Albarans corregits")
                st.dataframe(dfCorrecioAlbaransCompra)
                st.divider()
            elif dfCorrecioAlbaransCompra is None:
                st.subheader("No s'han trobat albarans per corregir")
                st.divider()

            st.session_state.fase10 = True

        # ==========================================================
        # 3.1.10 CORRECCIO D'OPERACIONS - FACTURES
        # ==========================================================

        if st.session_state.fase10:
            st.subheader("Correcció d'operacions")

            dfCorrecioFacturesCompra = logic_compres.correccioFactures(
                df_real_fac, prefNomFitxerCorreccio
            )

            if dfCorrecioFacturesCompra is not None:
                st.subheader("Factures corregides")
                st.dataframe(dfCorrecioFacturesCompra)
                st.divider()
            elif dfCorrecioFacturesCompra is None:
                st.subheader("No s'han trobat factures per corregir")
                st.divider()

    with tab_vendes:
        st.write("Gestió de correccions de vendes")

    with tab_inventari:

        print("DINS TAB_INVENTARI")
        print(st.session_state.fase01)
        print(st.session_state.fase15)

        # ====================================================================
        # 3.1.1 CARREGA LLISTATS - ARXIUS AMB DADES REALS i DADES ALUMNAT
        # ====================================================================

        if st.session_state.fase15:
            st.write("Gestió de correccions d'inventari")

            check_llistats_inventari = st.checkbox(
                "Els llistats per correcció de l'inventari ja estan pujats al servidor"
            )

            if not check_llistats_inventari:

                st.subheader("Adjunta els llistats amb les dades per corregir la tasca")

                col1, col2 = st.columns(2)

                with col1:
                    st.badge("RESUM DADES INVENTARI")
                    file_resum_dades_inventari = st.file_uploader(
                        "Adjunta el fitxer 09_RESUM_DADES_INVENTARI_ALUMNE.csv",
                        type=["csv"],
                        key="res_in",
                    )

                with col2:
                    st.badge("HISTORIAL ENTRADES i SORTIDES INVENTARI")
                    file_hes_inventari = st.file_uploader(
                        "Adjunta el fitxer 10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv",
                        type=["csv"],
                        key="hes_in",
                    )

                # Comprovam si s'han adjuntat tots els arxius per INICIAR la pujada al servidor
                if not (file_resum_dades_inventari and file_hes_inventari):
                    st.error(
                        "No podrem continuar fins que no hagis adjuntat tots els llistats sol·licitats"
                    )
                    st.stop()

                st.session_state.fase16 = True

                st.divider()

                # ==============================================================
                # 3.1.2 ENVIAMENT ARXIUS PER AL SEU TRACTAMENT
                # ==============================================================

                if st.session_state.fase16:

                    st.subheader("Carrega inicial de les dades")

                    st.write("⏳ Pujant arxius al servidor... ⏳")

                    # --- 2. PUJAM ELS ARXIUS AMB FUNCIO carregaArxius() ---
                    # Li passam els 2 arxius que hem pujat a la WEB

                    df_resum_dades_inventari, df_hes_inventari = (
                        logic_compres.carregaArxius(
                            file_resum_dades_inventari,
                            file_hes_inventari,
                        )
                    )

                    if df_resum_dades_inventari is None or df_hes_inventari is None:
                        st.error(
                            "NO ES POT SEGUIR EXECUTANT EL PROGRAMA PER FALTA DE DADES"
                        )
                        # ATURAM L'EXECUCIO DEL PROGRAMA. EL CODI POSTERIOR NO
                        # S'EXECUTARA, DE TAL FORMA QUE NO NECESSITEM USAR ELSE
                        st.stop()

                    time.sleep(3)

                    st.success(
                        "✅ LA CÀRREGA DELS LLISTATS I LA SEVA CONVERSIÓ A DATAFRAMES HA ESTAT EXITOSA"
                    )

                    st.session_state.fase17 = True

                    st.divider()

            else:
                # Cal indicar a quin grup i tasca corresponen les dades que volem recupetrar
                df_resum_dades_inventari = logic_comu.carregaCSV(
                    prefNomFitxerCorreccio + "09_RESUM_DADES_INVENTARI_ALUMNE.csv",
                    "LLISTATS_CSV",
                )
                df_hes_inventari = logic_comu.carregaCSV(
                    prefNomFitxerCorreccio + "10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv",
                    "LLISTATS_CSV",
                )

                if df_resum_dades_inventari is None or df_hes_inventari is None:
                    st.error("Error al carregar els llistats. Execucio cancelada")
                    st.stop()
                else:
                    st.success(
                        "✅ LA CÀRREGA DELS LLISTATS I LA SEVA CONVERSIÓ A DATAFRAMES HA ESTAT EXITOSA"
                    )
                    st.session_state.fase17 = True
                    st.divider()

        if st.session_state.fase17:

            # NOM DE LES COLUMNES DELS 2 DF

            print("09_RESUM_DADES_INVENTARI_ALUMNE.csv")
            print("\n".join(df_resum_dades_inventari.columns.tolist()))
            print()
            print("10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv")
            print("\n".join(df_hes_inventari.columns.tolist()))
            print()

            st.title(
                "Registre de les dates en que els alumnes han entregat les tasques"
            )

            ###@#@@##@@@@@@@@ AQYI

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
