import streamlit as st

# 1. CONFIGURACIÓ INICIAL DE LA PÀGINA
# Aquestes instruccions sempre han d'estar en l'inici.ArithmeticError
# Definim el títol de la pàgina (pipella browser)

st.set_page_config(
    page_title="Corrector DC",
    page_icon="🎓",
    layout="wide",  
)

# 2. TÍTOL PRINCIPAL DE LA PÀGINA
st.title("🎓 CORRECTOR TASQUES DEPARTAMENT COMERCIAL - EMPRESAULA")
st.markdown("---") # Línia separadora

# 3. MENÚ LATERAL (SIDEBAR)
with st.sidebar:
    st.header("Menú de Navegació")
    opcion = st.radio(
        "Que vols corregir?",
        options = ["COMPRES", "VENDES", "INVENTARI"]
    )
    
    st.info("ℹ️ Selecciona una opció per a continuar.")    

# 4. CONTINGUT DINÀMIC DE LA PÀGINA
# En funció de la opció seleccionada (Compres, Vendes...), mostrarà un contingut diferent

if opcion == "COMPRES":
    st.header("🛒 CORRECCIÓ DE COMPRES" )
    st.write("Aquí aparecerán los botones para subir pedidos, albaranes y facturas de compra.")

if opcion == "VENDES":
    st.header("💰 CORRECCIÓ DE VENDES" )
    st.write("Aquí aparecerán los botones para interactuar amb les VENDES")

if opcion == "INVENTARI":
    st.header(" CORRECCIÓ DE INVENTARI" )
    st.write("Aquí aparecerán los botones para interactuar amb INVENTARI")