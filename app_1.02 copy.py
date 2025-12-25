import streamlit as st
import pandas as pd
import os


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
    with tab_compres:
        st.subheader("Nova correcció de compres")

        # Definim nom identificador de la correcció
        nom_correccio = st.text_input("Etiqueta identificativa de la correcció (ADG32_02.01, ADG32_02.02, ADG32_02.03, ...): ")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**DADES REALS**")
            file_compres_real = st.file_uploader("Adjunta el fitxer 0_DATOS_COMPRAS_REALES.csv", type=["csv"], key="real_c")
            file_fecha_entrega_trabajos = st.file_uploader("Adjunta el fitxer 4_FECHA_ENTREGA_TRABAJOS.csv", type=["csv"], key="fec_c")
           
        with col2:
            st.markdown("**DADES APORTADES ALUMNAT**")
            file_dades_compra_comandes_alumne = st.file_uploader("Subir 1_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv", type=["csv"], key="ped_c")
            file_dades_compra_albarans_alumne = st.file_uploader("Subir 2_DATOS_ALBARANES_COMPRA_ALUMNOS.csv", type=["csv"], key="alb_c")
            file_dades_compra_factures_alumne = st.file_uploader("Subir 3_DATOS_FACTURAS_COMPRA_ALUMNOS.csv", type=["csv"], key="fac_c")
        
        
    
    
    
    with tab_vendes:
        st.write("Gestió de correccions de vendes")
    with tab_inventari:
        st.write("Gestió de correccions d'inventari")

    opcion = st.radio("Módulo: ", ["COMPRES", "VENDES", "INVENTARI"])
    st.info("ℹ️ Puja l'arxiu CSV en cada secció")

st.title("🎓 CORRECTOR TASQUES DEPARTAMENT COMERCIAL - EMPRESAULA")
st.markdown("---") # Línia separadora




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
        st.write("Aquesta data es fara servir per determinar si les factures estaven disponibles (+1 dia)")
        st.markdown("---")
       
    # ---- B. PUJADA ARXIUS ----
    st.subheader("2. Carrega d'arxius")

    # Es fan servir 'expanders' per no ocupar tanta pantalla
    with st.expander("📂 DADES REALS COMPRES - EMPRESAULA", expanded=True):
        file_compres_real = st.file_uploader("Subir 0_DATOS_COMPRAS_REALES.csv", type=["csv"])

    with st.expander("📂 DADES APORTADES PELS ALUNNES", expanded=True):
        col_izq, col_der = st.columns(2)
        with col_izq:
            file_dades_compra_comandes_alumne = st.file_uploader("Subir 1_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv", type=["csv"])
            file_dades_compra_albarans_alumne = st.file_uploader("Subir 2_DATOS_ALBARANES_COMPRA_ALUMNOS.csv", type=["csv"])
        with col_der:
            file_dades_compra_factures_alumne = st.file_uploader("Subir 3_DATOS_FACTURAS_COMPRA_ALUMNOS.csv", type=["csv"])
            file_fecha_entrega_trabajos = st.file_uploader("Subir 4_FECHA_ENTREGA_TRABAJOS.csv", type=["csv"])  
        
        # ---- C. BOTONS ACCIÓ ----
        st.markdown("---")
        
        # Verificam que tots els arxius s'han carregat abans d'habilitar el boto per pujar-los
        arxius_carregats = [file_compres_real, 
                            file_dades_compra_comandes_alumne, 
                            file_dades_compra_albarans_alumne, 
                            file_dades_compra_factures_alumne, 
                            file_fecha_entrega_trabajos]
       
        if all(arxius_carregats):
            st.success("✅ Tots els arxius estan carregats!!, Procedim al seu processament")
            
            if st.button("🚀 CORREGIR COMPRES", type="primary"):
                st.write("⏳ Procesant arxius... (AQUÍ CONECTAREM LA LÒGICA QUE HEM TREBALLAT ABANS)")

                # --- PEQUEÑA PRUEBA PARA QUE VEAS QUE FUNCIONA ---
                # Vamos a leer el archivo real solo para demostrar que Streamlit lo ve
                try:
                    df_test = pd.read_csv(file_compres_real, sep=None, engine='python')
                    st.write("Vista previa de les dades carregades")
                    # Mostram taula interactiva amb només les primeres 20 files per no saturar la pantalla
                    st.dataframe(df_test.head(20))
                except Exception as e:
                    st.error(f"Error al processar l'arxiu: {str(e)}") 

        else:
            st.warning("⚠️ Hi ha arxius sense carregar, no es pot procedir amb el processament") 

elif opcion == "VENDES":
    st.header("💰 CORRECCIÓ DE VENDES")
    st.write("Aquesta funcionalitat encara no està implementada")

elif opcion == "INVENTARI":
    st.header("📦 CORRECCIÓ DE INVENTARI")
    st.write("Aquesta funcionalitat encara no està implementada")

           
    