import streamlit as st

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
