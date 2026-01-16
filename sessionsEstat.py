import streamlit as st
import os


def inicialitzaSessionsEstat():
    # Solo inicializa si no existen para no sobreescribir datos actuales
    if "grup" not in st.session_state:
        st.session_state.grup = None
    if "tasca" not in st.session_state:
        st.session_state.tasca = None
    if "dataVto" not in st.session_state:
        st.session_state.dataVto = None

    if "carpetaINPUT" not in st.session_state:
        st.session_state.carpetaINPUT = "LLISTATS_INPUT"
    if "carpetaOUTPUT" not in st.session_state:
        st.session_state.carpetaOUTPUT = "LLISTATS_OUTPUT"

    if "rutaFinsInput" not in st.session_state:
        st.session_state.rutaFinsInput = (
            os.getcwd() + "/" + st.session_state.carpetaINPUT
        )
    if "rutaFinsOutput" not in st.session_state:
        st.session_state.rutaFinsOutput = (
            os.getcwd() + "/" + st.session_state.carpetaOUTPUT
        )

    # ARXIUS IMPUT i OUTPUT
    # nomArxiusTeoricsInputCOMPRES
    # "00_DATOS_COMPRAS_REALES.csv"
    # "01_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv"
    # "02_DATOS_ALBARANES_COMPRA_ALUMNOS.csv"
    # "03_DATOS_FACTURAS_COMPRA_ALUMNOS.csv"
    # "04_FECHA_ENTREGA_TRABAJOS.csv"

    # nomArxiusTeoricsInputVENDES
    # "05_DATOS_VENTAS_REALES.csv"
    # "06_DATOS_PEDIDOS_VENTAS_ALUMNOS.csv"
    # "07_DATOS_ALBARANES_VENTAS_ALUMNOS.csv"
    # "08_DATOS_FACTURAS_VENTAS_ALUMNOS.csv"

    # nomArxiusTeoricsInputINVENTARI
    # "09_RESUM_DADES_INVENTARI_ALUMNE.csv"
    # "10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv"

    if "fileInputCompres00" not in st.session_state:
        st.session_state.fileInputCompres00 = "00_DATOS_COMPRAS_REALES.csv"
    if "fileInputCompres01" not in st.session_state:
        st.session_state.fileInputCompres01 = "01_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv"
    if "fileInputCompres02" not in st.session_state:
        st.session_state.fileInputCompres02 = "02_DATOS_ALBARANES_COMPRA_ALUMNOS.csv"
    if "fileInputCompres03" not in st.session_state:
        st.session_state.fileInputCompres03 = "03_DATOS_FACTURAS_COMPRA_ALUMNOS.csv"
    if "fileInputCompres04" not in st.session_state:
        st.session_state.fileInputCompres04 = "04_FECHA_ENTREGA_TRABAJOS.csv"

    if "fileInputVendes05" not in st.session_state:
        st.session_state.fileInputVendes05 = "05_DATOS_VENTAS_REALES.csv"
    if "fileInputVendes06" not in st.session_state:
        st.session_state.fileInputVendes06 = "06_DATOS_PEDIDOS_VENTAS_ALUMNOS.csv"
    if "fileInputVendes07" not in st.session_state:
        st.session_state.fileInputVendes07 = "07_DATOS_ALBARANES_VENTAS_ALUMNOS.csv"
    if "fileInputVendes08" not in st.session_state:
        st.session_state.fileInputVendes08 = "08_DATOS_FACTURAS_VENTAS_ALUMNOS.csv"

    if "fileInputInventari09" not in st.session_state:
        st.session_state.fileInputInventari09 = "09_RESUM_DADES_INVENTARI_ALUMNE.csv"
    if "fileInputInventari10" not in st.session_state:
        st.session_state.fileInputInventari10 = "10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv"

    # nomArxiusTeoricsOutputCOMPRES
    # "11_DF_CORRECCIO_COMANDES_COMPRA.csv"
    # "12_DF_CORRECCIO_ALBARANS_COMPRA.csv"
    # "13_DF_CORRECCIO_FACTURES_COMPRA.csv"

    # nomArxiusTeoricsOutputVENDES
    # "21_DF_CORRECCIO_COMANDES_VENDES.csv"
    # "22_DF_CORRECCIO_ALBARANS_VENDES.csv"
    # "23_DF_CORRECCIO_FACTURES_VENDES.csv"

    # nomArxiusTeoricsOutputINVENTARI
    # "31_DF_CORRECCIO_INVENTARI_EMPRESA_PRODUCTE.csv"
    # "32_DF_CORRECCIO_INVENTARI_EMPRESA.csv"

    if "fileOutputCompres11" not in st.session_state:
        st.session_state.fileOutputCompres11 = "11_DF_CORRECCIO_COMANDES_COMPRA.csv"
    if "fileOutputCompres12" not in st.session_state:
        st.session_state.fileOutputCompres12 = "12_DF_CORRECCIO_ALBARANS_COMPRA.csv"
    if "fileOutputCompres13" not in st.session_state:
        st.session_state.fileOutputCompres13 = "13_DF_CORRECCIO_FACTURES_COMPRA.csv"

    if "fileOutputVendes21" not in st.session_state:
        st.session_state.fileOutputVendes21 = "21_DF_CORRECCIO_COMANDES_VENDES.csv"
    if "fileOutputVendes22" not in st.session_state:
        st.session_state.fileOutputVendes22 = "22_DF_CORRECCIO_ALBARANS_VENDES.csv"
    if "fileOutputVendes23" not in st.session_state:
        st.session_state.fileOutputVendes23 = "23_DF_CORRECCIO_FACTURES_VENDES.csv"

    if "fileOutputInventari31" not in st.session_state:
        st.session_state.fileOutputInventari31 = (
            "31_DF_CORRECCIO_INVENTARI_EMPRESA_PRODUCTE.csv"
        )
    if "fileOutputInventari32" not in st.session_state:
        st.session_state.fileOutputInventari32 = "32_DF_CORRECCIO_INVENTARI_EMPRESA.csv"

    if "data_entrega" not in st.session_state:
        st.session_state.data_entrega = False
    if "arxiu_dades_reals" not in st.session_state:
        st.session_state.arxiu_dades_reals = False
    if "arxiu_dades_alumnat" not in st.session_state:
        st.session_state.arxiu_dades_alumnat = False
    if "arxiu_dades_alumnat" not in st.session_state:
        st.session_state.arxiu_dades_alumnat = False

    if "disponibilitatArxiusINPUTCompres" not in st.session_state:
        st.session_state.disponibilitatArxiusINPUTCompres = False
    if "disponibilitatArxiusINPUTVendes" not in st.session_state:
        st.session_state.disponibilitatArxiusINPUTVendes = False
    if "disponibilitatArxiusINPUTInventari" not in st.session_state:
        st.session_state.disponibilitatArxiusINPUTInventari = False

    if "disponibilitatArxiusOUTPUTCompres" not in st.session_state:
        st.session_state.disponibilitatArxiusOUTPUTCompres = False
    if "disponibilitatArxiusOUTPUTVendes" not in st.session_state:
        st.session_state.disponibilitatArxiusOUTPUTVendes = False
    if "disponibilitatArxiusOUTPUTInventari" not in st.session_state:
        st.session_state.disponibilitatArxiusOUTPUTInventari = False


def inicialitzaRutesFinsGrupTasca():
    # RUTES
    # Solo concatenamos si grup i tasca no son None
    if st.session_state.grup and st.session_state.tasca:
        st.session_state.rutaFinsLlistatsInputGrupTasca = f"{st.session_state.rutaFinsInput}/{st.session_state.grup}_{st.session_state.tasca}"
        st.session_state.rutaFinsLlistatsOutputGrupTasca = f"{st.session_state.rutaFinsOutput}/{st.session_state.grup}_{st.session_state.tasca}"


"""
# INICIALITZACIO DELS ESTATS DE LES ETAPES DE CORRECCIÓ

if "fase01" not in st.session_state:
    st.session_state.fase01 = False

# 2. INTRODUCIO DATA ENTREGA TASCA

if "fase02" not in st.session_state:
    st.session_state.fase02 = False

# 3.1.1 CARREGA LLISTATS - ARXIUS AMB DADES REALS i DADES ALUMNAT

if "fase03" not in st.session_state:
    st.session_state.fase03 = False

# 3.1.2 ENVIAMENT ARXIUS PER AL SEU TRACTAMENT

if "fase04" not in st.session_state:
    st.session_state.fase04 = False

# 3.1.4 NETEJA VARIABLES

if "fase05" not in st.session_state:
    st.session_state.fase05 = False

# 3.1.5 COMANDES DUPLICADES

if "fase06" not in st.session_state:
    st.session_state.fase06 = False

# 3.1.6 UNIO DE DATAFRAMES (merge)

if "fase07" not in st.session_state:
    st.session_state.fase07 = False

# 3.1.7 RESEARCH OF ORPHAN OPERATIONS

if "fase08" not in st.session_state:
    st.session_state.fase08 = False

# 3.1.8 CORRECCIO D'OPERACIONS - COMANDES

if "fase09" not in st.session_state:
    st.session_state.fase09 = False

# 3.1.9 CORRECCIO D'OPERACIONS - ALBARANS

if "fase10" not in st.session_state:
    st.session_state.fase10 = False

# 3.1.10 CORRECCIO D'OPERACIONS - FACTURES

if "fase11" not in st.session_state:
    st.session_state.fase11 = False

if "fase12" not in st.session_state:
    st.session_state.fase12 = False

if "fase13" not in st.session_state:
    st.session_state.fase13 = False

if "fase14" not in st.session_state:
    st.session_state.fase14 = False

if "fase15" not in st.session_state:
    st.session_state.fase15 = False

# inventari

if "fase16" not in st.session_state:
    st.session_state.fase16 = False

if "fase17" not in st.session_state:
    st.session_state.fase17 = False

if "fase18" not in st.session_state:
    st.session_state.fase18 = False

if "fase19" not in st.session_state:
    st.session_state.fase19 = False

if "fase20" not in st.session_state:
    st.session_state.fase20 = False

if "fase21" not in st.session_state:
    st.session_state.fase21 = False

if "fase22" not in st.session_state:
    st.session_state.fase22 = False

if "fase23" not in st.session_state:
    st.session_state.fase23 = False

if "fase24" not in st.session_state:
    st.session_state.fase24 = False

if "fase25" not in st.session_state:
    st.session_state.fase25 = False

if "fase26" not in st.session_state:
    st.session_state.fase26 = False

if "fase27" not in st.session_state:
    st.session_state.fase27 = False

if "fase28" not in st.session_state:
    st.session_state.fase28 = False

if "fase29" not in st.session_state:
    st.session_state.fase29 = False

if "fase30" not in st.session_state:
    st.session_state.fase30 = False

if "fase31" not in st.session_state:
    st.session_state.fase31 = False

if "fase32" not in st.session_state:
    st.session_state.fase32 = False

if "fase33" not in st.session_state:
    st.session_state.fase33 = False

if "fase34" not in st.session_state:
    st.session_state.fase34 = False

if "fase35" not in st.session_state:
    st.session_state.fase35 = False

if "fase36" not in st.session_state:
    st.session_state.fase36 = False


# VARIABLES GLOBALES

# LLISTA NUM. TASQUES PER SELECTBOX INICIAL

llista_num_tasques = [
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
]

# Llista expedients

llista_expedients_alumnes = [
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

# Llista empreses d'alumnes

llista_empreses_alumnes = [
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
"""
