import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓ INICIAL DE LA PÀGINA
# Aquestes instruccions sempre han d'estar en l'inici.ArithmeticError
# Definim el títol de la pàgina (pipella browser)

st.set_page_config(
    page_title="Corrector DC",
    page_icon="🎓",
    layout="wide",  
)

st.title("🎓 CORRECTOR TASQUES DEPARTAMENT COMERCIAL - EMPRESAULA")
st.markdown("---") # Línia separadora

# 2. MENÚ LATERAL (SIDEBAR)
with st.sidebar:
    st.header("MENÚ")
    opcion = st.radio("Módulo: ", ["COMPRES", "VENDES", "INVENTARI"])
    st.info("ℹ️ Puja l'arxiu CSV en cada secció

# 3. LOGICA INTERFICIE
# En funció de la opció seleccionada (Compres, Vendes...), mostrarà un contingut diferent

if opcion == "COMPRES":
    st.header("🛒 CORRECCIÓ DE COMPRES" )

    # ---- A. CONFIGURACIO ----
    st.subheader("1. Configuración")
    # Dividim la pant alla en dues columnes
    col1, col2 = st.columns(2)
    
    with col1:
        # Selector de data
        fecha_entrega = st.date_input("📅 Fecha Límite de Entrega (Viernes):", 
                            value=pd.to_datetime("today"))

    with col2:
        st.write("Aquesta data es fara servir per determinar si les factures estven disponibles (+1 dia)")
        st.markdown("---")
       
    # ---- B. PUJADA ARXIUS ----
    st.subheader("2. Carrega d'arxius")

    # Es fan servir 'expanders' per no ocupar tanta pantalla
    with st.expander("📂 DADES REALS COMPRES - EMPRESAULA", expanded=True):
        file_compra_real = st.file_uploader("Subir 0_DATOS_COMPRAS_REALES.csv", type=["csv"])

    with st.expander("📂 DADES APORTADES PELS ALUNNES", expanded=True):
        col_izq, col_der = st.columns(2)
        with col_izq:
            file_compra_pedido_alumne = st.file_uploader("Subir 1_PEDIDOS.csv", type=["csv"])
            file_compra_albaran_alumne = st.file_uploader("Subir 2_ALBARANES.csv", type=["csv"])
        with col_der:
            file_compra_factura_alumne = st.file_uploader("Subir 3_FACTURAS.csv", type=["csv"])
            file_fechas_entrega = st.file_uploader("Subir 4_FECHS_ENTREGA.csv", type=["csv"])