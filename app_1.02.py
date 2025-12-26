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
        
        if st.button("⚙️ PROCESSAR I DESAR CORRECCIÓ", type="primary"):
            # Comoprovam si s'han adjuntat tots els arxius per INICIAR la pujada al servidor
            if  file_compres_real and file_fecha_entrega_trabajos and file_dades_compra_comandes_alumne and file_dades_compra_albarans_alumne and file_dades_compra_factures_alumne:
                if nom_correccio == "":
                    st.error("Cal que indiquis un nom per aquesta correcció")     
                else:
                    st.write("⏳ Aplicant algoritme de correcció")

                    # --- 1. IMPORTAR LÒGICA CORRECCIÓ COMPRES ---
                    # Esto carga el archivo logic_compras.py que creamos antes
                    import logic_compres 
                    
                    # --- 2. LLAMADA A LA FUNCIÓN MAESTRA ---
                    # Le pasamos los 5 archivos que has subido a la web
                    """
                    df_notas, df_h_alb, df_h_fac, df_h_ped, error_msg = logic_compres.procesar_correccion_compras(
                                file_compres_real, 
                                file_dades_compra_comandes_alumne, 
                                file_dades_compra_albarans_alumne, 
                                file_dades_compra_factures_alumne, 
                                file_fecha_entrega_trabajos
                    )                    

                    # --- 3. GESTIÓN DE RESULTADOS ---
                    if error_msg:
                        st.error(f"❌ MERDA, ALGUNA COSA NO FUNCIONA. HO MIRAM {error_msg}")
                    else:
                        st.success("✅ CORRECCIÓ REALITZADA AMB Éxit")
                    """
                    logic_compres.procesar_correccion_compras(
                                file_compres_real, 
                                file_dades_compra_comandes_alumne, 
                                file_dades_compra_albarans_alumne, 
                                file_dades_compra_factures_alumne, 
                                file_fecha_entrega_trabajos
                    )                   
                    st.success("✅ CORRECCIÓ REALITZADA AMB ÉXIT")
        
            else:
                st.error("Cal que adjuntis tots els arxius per poder processar la correcció")
        
                 
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
        modulo_consulta = st.selectbox("Selecciona: ", ["COMPRES", "VENDES", "INVENTARI"])


    with col_sel2:
        # Buscamos en la carpeta qué archivos hay de ese módulo
        archivos_disponibles = [f for f in os.listdir(CARPETA_HISTORICO) if f.startswith(modulo_consulta) and f.endswith(".xlsx")]
        # Los ordenamos para que salga el último primero
        archivos_disponibles.sort(reverse=True)

        seleccio_tasca = st.selectbox("Selecciona la entrega: ", archivos_disponibles)  

    if seleccio_tasca:
        # Cargamos el archivo seleccionado desde el disco duro
        ruta_archivo = os.path.join(CARPETA_HISTORICO, seleccio_tasca)
        try:
            df_notas = pd.read_excel(ruta_archivo)
            
            # Selector de Alumno
            lista_empresas = sorted(df_notas['EMPRESA'].unique().astype(str))
            empresa_seleccionada = st.selectbox("Selecciona la teva empresa:", lista_empresas)
            
            if empresa_seleccionada:
                st.divider()
                st.subheader(f"Resultados: {empresa_seleccionada} - {seleccio_tasca}")
                
                # Filtrar y mostrar
                # Convertimos a string por si acaso pandas leyó el expediente como número
                df_alumno = df_notas[df_notas['EMPRESA'].astype(str) == str(empresa_seleccionada)]
                
                st.dataframe(
                    df_alumno, 
                    use_container_width=True, 
                    hide_index=True
                )
                
                # Resumen visual
                errores = df_alumno[df_alumno['RESULTAT'] != 'OK']
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


