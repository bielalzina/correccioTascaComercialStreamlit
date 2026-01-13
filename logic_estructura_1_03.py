from pathlib import Path
import os
import shutil
import glob


# Carpeta LLISTATS_INPUT
rutaCarpetaINPUT = os.getcwd() + "/LLISTATS_INPUT/"

# Carpeta LLISTATS_OUTPUT
rutaCarpetaOUTPUT = os.getcwd() + "/LLISTATS_OUTPUT/"


def existeixDirectori(in_out, grup_tasca):
    if in_out == "INPUT":
        ruta = Path(rutaCarpetaINPUT + grup_tasca)
    elif in_out == "OUTPUT":
        ruta = Path(rutaCarpetaOUTPUT + grup_tasca)
    if ruta.exists():
        return True
    else:
        return False


def existeixFitxersDirectori(in_out, grup_tasca):
    if in_out == "INPUT":
        ruta = Path(rutaCarpetaINPUT + grup_tasca)
    elif in_out == "OUTPUT":
        ruta = Path(rutaCarpetaOUTPUT + grup_tasca)
    if ruta.exists():
        return True
    else:
        return False


def llistaFitxersDirectori(in_out, grup_tasca):
    if in_out == "INPUT":
        ruta = Path(rutaCarpetaINPUT + grup_tasca)
    elif in_out == "OUTPUT":
        ruta = Path(rutaCarpetaOUTPUT + grup_tasca)

    arxius = glob.glob(os.path.join(ruta, "*"))
    nomsArxius = [os.path.basename(f) for f in arxius if os.path.isfile(f)]
    return nomsArxius


def arxiuDisponible(nomArxiu, llistaArxius):
    if nomArxiu in llistaArxius:
        return "✅"
    else:
        return "❌"


nomCurtArxiusTeoricsInput = [
    "00_DATOS_COMPRAS_REALES.csv",
    "01_DATOS_PEDIDOS_COMPRA_ALUMNOS.csv",
    "02_DATOS_ALBARANES_COMPRA_ALUMNOS.csv",
    "03_DATOS_FACTURAS_COMPRA_ALUMNOS.csv",
    "04_FECHA_ENTREGA_TRABAJOS.csv",
    "05_DATOS_VENTAS_REALES.csv",
    "06_DATOS_PEDIDOS_VENTAS_ALUMNOS.csv",
    "07_DATOS_ALBARANES_VENTAS_ALUMNOS.csv",
    "08_DATOS_FACTURAS_VENTAS_ALUMNOS.csv",
    "09_RESUM_DADES_INVENTARI_ALUMNE.csv",
    "10_HISTORIAL_E_S_INVENTARI_ALUMNE.csv",
]

nomCurtArxiusTeoricsOutput = [
    "COMPRES_11_DF_CORRECCIO_COMANDES_COMPRA.csv",
    "COMPRES_12_DF_CORRECCIO_ALBARANS_COMPRA.csv",
    "COMPRES_13_DF_CORRECCIO_FACTURES_COMPRA.csv",
    "COMPRES_14_DF_CORRECCIO_ENTREGA_TRABAJOS.csv",
    "VENDES_30_DF_CORRECCIO_COMANDES_VENDES.csv",
    "VENDES_31_DF_CORRECCIO_ALBARANS_VENDES.csv",
    "VENDES_32_DF_CORRECCIO_FACTURES_VENDES.csv",
    "INVENTARI_19_DF_CORRECCIO_INVENTARI_EMPRESA_PRODUCTE.csv",
    "INVENTARI_20_DF_CORRECCIO_INVENTARI_EMPRESA.csv",
]


def llistaArxiusTeorics(in_out, grup, tasca):
    if in_out == "INPUT":
        llistaArxiusTeoricsInput = [
            f"{grup}_{tasca}_{arxiu}" for arxiu in nomCurtArxiusTeoricsInput
        ]
        return llistaArxiusTeoricsInput
    elif in_out == "OUTPUT":
        llistaArxiusTeoricsOutput = [
            f"{grup}_{tasca}_{arxiu}" for arxiu in nomCurtArxiusTeoricsOutput
        ]
        return llistaArxiusTeoricsOutput


# 3. Crear el directorio
# parents=True crea carpetas intermedias si no existen
# exist_ok=True evita errores si alguien lo creó justo antes
# ruta.mkdir(parents=True, exist_ok=True)
# print(f"Directorio '{ruta}' creado con éxito.")


# 4. Eliminar el directorio
# Opción A: Solo si está vacío
# ruta.rmdir()

# Opción B: Eliminar la carpeta y TODO su contenido (archivos y subcarpetas)
# shutil.rmtree(ruta)
