from pathlib import Path
import os
import shutil
import glob

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


nomArxiusTeoricsInputCOMPRES = [
    "00_DATOS_COMPRAS_REALES.csv",
    "01_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv",
    "02_DATOS_ALBARANES_COMPRA_ALUMNOS.csv",
    "03_DATOS_FACTURAS_COMPRA_ALUMNOS.csv",
    "04_FECHA_ENTREGA_TRABAJOS.csv",
]
nomArxiusTeoricsInputVENDES = [
    "05_DATOS_VENTAS_REALES.csv",
    "06_DATOS_PEDIDOS_VENTAS_ALUMNOS.csv",
    "07_DATOS_ALBARANES_VENTAS_ALUMNOS.csv",
    "08_DATOS_FACTURAS_VENTAS_ALUMNOS.csv",
]
nomArxiusTeoricsInputINVENTARI = [
    "09_RESUM_DADES_INVENTARI_ALUMNE.csv",
    "10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv",
]

nomArxiusTeoricsInput = (
    nomArxiusTeoricsInputCOMPRES
    + nomArxiusTeoricsInputVENDES
    + nomArxiusTeoricsInputINVENTARI
)


nomArxiusTeoricsOutputCOMPRES = [
    "11_DF_CORRECCIO_COMANDES_COMPRA.csv",
    "12_DF_CORRECCIO_ALBARANS_COMPRA.csv",
    "13_DF_CORRECCIO_FACTURES_COMPRA.csv",
]
nomArxiusTeoricsOutputVENDES = [
    "21_DF_CORRECCIO_COMANDES_VENDES.csv",
    "22_DF_CORRECCIO_ALBARANS_VENDES.csv",
    "23_DF_CORRECCIO_FACTURES_VENDES.csv",
]
nomArxiusTeoricsOutputINVENTARI = [
    "31_DF_CORRECCIO_INVENTARI_EMPRESA_PRODUCTE.csv",
    "32_DF_CORRECCIO_INVENTARI_EMPRESA.csv",
]
nomArxiusTeoricsOutput = (
    nomArxiusTeoricsOutputCOMPRES
    + nomArxiusTeoricsOutputVENDES
    + nomArxiusTeoricsOutputINVENTARI
)

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


# Carpeta LLISTATS_INPUT
rutaCarpetaINPUT = os.getcwd() + "/LLISTATS_INPUT/"

# Carpeta LLISTATS_OUTPUT
rutaCarpetaOUTPUT = os.getcwd() + "/LLISTATS_OUTPUT/"


def pujaArxiu(arxiu, nomArxiu, rutaDirectori):
    try:
        # 1. Construir la ruta completa
        rutaCompleta = os.path.join(rutaDirectori, nomArxiu)

        # 2. Desar l'arxiu en mode binari ("wb")
        with open(rutaCompleta, "wb") as f:
            f.write(arxiu.getbuffer())
            retornat = True
    except Exception as e:
        print(f"Error al desar l'arxiu {nomArxiu}: {str(e)}")
        retornat = False
    return retornat


def relacioArxiusPresents(in_out, rutaDirectori):
    if in_out == "INPUT":
        # Recuperem els arxius existents en el directori INPUT
        llistaArxiusExistentsInput = llistaFitxersDirectori(rutaDirectori)
        # print("ARXIUS QUE HI HA EN EL DIRECTORI INPUT")
        # print(llistaArxiusExistentsInput)

        # Recuperem la llista d'arxius teorics
        llistaArxiusTeoricsInput = nomArxiusTeoricsInput

        # Comprovem si els arxius teorics existen en el directori INPUT
        disponibilitatArxiuInput = []
        for arxiu in llistaArxiusTeoricsInput:
            if arxiu not in llistaArxiusExistentsInput:
                disponibilitat = "❌ NO DISPONIBLE"
            else:
                disponibilitat = "✅ DISPONIBLE"
            disponibilitatArxiuInput.append(disponibilitat)
        return llistaArxiusTeoricsInput, disponibilitatArxiuInput

    elif in_out == "OUTPUT":
        # Recuperem els arxius existents en el directori OUTPUT
        llistaArxiusExistentsOutput = llistaFitxersDirectori(rutaDirectori)
        # print("ARXIUS QUE HI HA EN EL DIRECTORI OUTPUT")
        # print(llistaArxiusExistentsOutput)

        # Recuperem la llista d'arxius teorics
        llistaArxiusTeoricsOutput = nomArxiusTeoricsOutput

        # Comprovem si els arxius teorics existen en el directori OUTPUT
        disponibilitatArxiuOutput = []
        for arxiu in llistaArxiusTeoricsOutput:
            if arxiu not in llistaArxiusExistentsOutput:
                disponibilitat = "❌ NO DISPONIBLE"
            else:
                disponibilitat = "✅ DISPONIBLE"
            disponibilitatArxiuOutput.append(disponibilitat)
        return llistaArxiusTeoricsOutput, disponibilitatArxiuOutput


def llistaFitxersDirectori(rutaDirectori):
    arxius = glob.glob(os.path.join(rutaDirectori, "*"))
    nomsArxius = [os.path.basename(f) for f in arxius if os.path.isfile(f)]
    return nomsArxius


def llistaArxiusTeorics(in_out, grup, tasca):
    if in_out == "INPUT":
        llistaArxiusTeoricsInput = [
            f"{grup}_{tasca}_{arxiu}" for arxiu in nomArxiusTeoricsInput
        ]
        return llistaArxiusTeoricsInput
    elif in_out == "OUTPUT":
        llistaArxiusTeoricsOutput = [
            f"{grup}_{tasca}_{arxiu}" for arxiu in nomArxiusTeoricsOutput
        ]
        return llistaArxiusTeoricsOutput


def existeixFitxersDirectori(in_out, grup_tasca):
    if in_out == "INPUT":
        ruta = Path(rutaCarpetaINPUT + grup_tasca)
    elif in_out == "OUTPUT":
        ruta = Path(rutaCarpetaOUTPUT + grup_tasca)
    if ruta.exists():
        return True
    else:
        return False


def arxiuDisponible(nomArxiu, llistaArxius):
    if nomArxiu in llistaArxius:
        return "✅"
    else:
        return "❌"


def creaDirectori(in_out, grup, tasca):
    if in_out == "INPUT":
        ruta = Path(rutaCarpetaINPUT + grup + "_" + tasca)
    elif in_out == "OUTPUT":
        ruta = Path(rutaCarpetaOUTPUT + grup + "_" + tasca)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def comprovaDisponibilitatArxiusperTipus(in_out, rutaDirectori, llista):

    if in_out == "INPUT":
        # Recuperem els arxius existents en el directori INPUT
        llistaArxiusExistentsInput = llistaFitxersDirectori(rutaDirectori)
        # print("LLISTA EXISTENT")
        # print(llistaArxiusExistentsInput)
        for llistat in llista:
            if llistat not in llistaArxiusExistentsInput:
                return False  # Termina la ejecución aquí si falla
        return True  # Si termina el bucle, todos estaban presentes
    elif in_out == "OUTPUT":
        # Recuperem els arxius existents en el directori OUTPUT
        llistaArxiusExistentsOutput = llistaFitxersDirectori(rutaDirectori)
        # print("LLISTA EXISTENT")
        # print(llistaArxiusExistentsOutput)
        for llistat in llista:
            if llistat not in llistaArxiusExistentsOutput:
                return False  # Termina la ejecución aquí si falla
        return True  # Si termina el bucle, todos estaban presentes
    else:
        return False


def existeixDirectori(in_out, grup_tasca):
    if in_out == "INPUT":
        ruta = Path(rutaCarpetaINPUT + grup_tasca)
    elif in_out == "OUTPUT":
        ruta = Path(rutaCarpetaOUTPUT + grup_tasca)
    if ruta.exists():
        return True
    else:
        return False


# 4. Eliminar el directorio
# Opción A: Solo si está vacío
# ruta.rmdir()

# Opción B: Eliminar la carpeta y TODO su contenido (archivos y subcarpetas)
# shutil.rmtree(ruta)
