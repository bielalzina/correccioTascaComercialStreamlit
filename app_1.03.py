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

    tab_compres, tab_vendes, tab_inventari = st.tabs(["COMPRES", "VENDES", "INVENTARI"])

    st.session_state.fase01 = True
    st.session_state.fase15 = True

    print("DESPRES DE INICIAR LES ETAPES DE CORRECCIÓ")
    print(st.session_state.fase01)
    print(st.session_state.fase15)

    # ====================================================================
    # 3.1 VISTA PROFESOR - TAB COMPRES
    # ====================================================================

    with tab_compres:

        # ====================================================================
        # 3.1.1 CARREGA LLISTATS - ARXIUS AMB DADES REALS i DADES ALUMNAT
        # ====================================================================

        if st.session_state.fase01:
            st.subheader("TAB COMPRES")

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
