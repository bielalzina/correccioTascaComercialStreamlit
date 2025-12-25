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
    st.info("ℹ️ Puja l'arxiu CSV en cada secció")


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

           
    