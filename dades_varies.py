import streamlit as st



# VARIABLES GLOBALES

# ARXIUS LLISTATS_INPUT

fitxerInput00 = "00_DATOS_COMPRAS_REALES.csv"
fitxerInput01 = "01_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv"
fitxerInput02 = "02_DATOS_ALBARANES_COMPRA_ALUMNOS.csv"
fitxerInput03 = "03_DATOS_FACTURAS_COMPRA_ALUMNOS.csv"
fitxerInput04 = "04_FECHA_ENTREGA_TRABAJOS.csv"
fitxerInput05 = "05_DATOS_VENTAS_REALES.csv"
fitxerInput06 = "06_DATOS_PEDIDOS_VENTAS_ALUMNOS.csv"
fitxerInput07 = "07_DATOS_ALBARANES_VENTAS_ALUMNOS.csv"
fitxerInput08 = "08_DATOS_FACTURAS_VENTAS_ALUMNOS.csv"
fitxerInput09 = "09_RESUM_DADES_INVENTARI_ALUMNE.csv"
fitxerInput10 = "10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv"

# ARXIUS LLISTATS_OUTPUT

fitxerOutput11 = "COMPRES_11_DF_CORRECCIO_COMANDES_COMPRA.csv"
fitxerOutput12 = "COMPRES_12_DF_CORRECCIO_ALBARANS_COMPRA.csv"
fitxerOutput13 = "COMPRES_13_DF_CORRECCIO_FACTURES_COMPRA.csv"
fitxerOutput14 = ""
fitxerOutput15 = ""
fitxerOutput16 = ""
fitxerOutput06 = ""
fitxerOutput07 = ""
fitxerOutput08 = ""
fitxerOutput40 = "INVENTARI_40_CORRECCIO_INVENTARI_EMPRESA_PRODUCTE.csv"
fitxerOutput41 = "INVENTARI_41_CORRECCIO_INVENTARI_EMPRESA.csv"

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
