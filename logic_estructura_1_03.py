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


def llistaFitxersDirectori(in_out, grup, tasca):
    if in_out == "INPUT":
        ruta = Path(rutaCarpetaINPUT + grup + "_" + tasca + "/")
        # print(ruta)
    elif in_out == "OUTPUT":
        ruta = Path(rutaCarpetaOUTPUT + grup + "_" + tasca + "/")
        # print(ruta)

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

nomCurtArxiusTeoricsInputCOMPRES = nomCurtArxiusTeoricsInput[:5]
nomCurtArxiusTeoricsInputVENDES = nomCurtArxiusTeoricsInput[5:9]
nomCurtArxiusTeoricsInputINVENTARI = nomCurtArxiusTeoricsInput[9:]

nomCurtArxiusTeoricsOutput = [
    "COMPRES_11_DF_CORRECCIO_COMANDES_COMPRA.csv",
    "COMPRES_12_DF_CORRECCIO_ALBARANS_COMPRA.csv",
    "COMPRES_13_DF_CORRECCIO_FACTURES_COMPRA.csv",
    "VENDES_21_DF_CORRECCIO_COMANDES_VENDES.csv",
    "VENDES_22_DF_CORRECCIO_ALBARANS_VENDES.csv",
    "VENDES_23_DF_CORRECCIO_FACTURES_VENDES.csv",
    "INVENTARI_31_DF_CORRECCIO_INVENTARI_EMPRESA_PRODUCTE.csv",
    "INVENTARI_32_DF_CORRECCIO_INVENTARI_EMPRESA.csv",
]

nomCurtArxiusTeoricsOutputCOMPRES = nomCurtArxiusTeoricsOutput[:3]
nomCurtArxiusTeoricsOutputVENDES = nomCurtArxiusTeoricsOutput[3:6]
nomCurtArxiusTeoricsOutputINVENTARI = nomCurtArxiusTeoricsOutput[6:]


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


def relacioArxiusPresents(in_out, grup, tasca):
    if in_out == "INPUT":
        # Recuperem els arxius existents en el directori INPUT
        llistaArxiusExistentsInput = llistaFitxersDirectori(in_out, grup, tasca)
        # print("ARXIUS QUE HI HA EN EL DIRECTORI INPUT")
        # print(llistaArxiusExistentsInput)

        # Recuperem la llista d'arxius teorics
        llistaArxiusTeoricsInput = llistaArxiusTeorics(in_out, grup, tasca)
        # print("ARXIUS QUE TEORICAMENT HAURIEN D'ESTAR EN EL DIRECTORI INPUT")
        # print(llistaArxiusTeoricsInput)

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
        llistaArxiusExistentsOutput = llistaFitxersDirectori(in_out, grup, tasca)
        # print("ARXIUS QUE HI HA EN EL DIRECTORI OUTPUT")
        # print(llistaArxiusExistentsOutput)

        # Recuperem la llista d'arxius teorics
        llistaArxiusTeoricsOutput = llistaArxiusTeorics(in_out, grup, tasca)
        # print("ARXIUS QUE TEORICAMENT HAURIEN D'ESTAR EN EL DIRECTORI OUTPUT")
        # print(llistaArxiusTeoricsOutput)

        # Comprovem si els arxius teorics existen en el directori OUTPUT
        disponibilitatArxiuOutput = []
        for arxiu in llistaArxiusTeoricsOutput:
            if arxiu not in llistaArxiusExistentsOutput:
                disponibilitat = "❌ NO DISPONIBLE"
            else:
                disponibilitat = "✅ DISPONIBLE"
            disponibilitatArxiuOutput.append(disponibilitat)
        return llistaArxiusTeoricsOutput, disponibilitatArxiuOutput


def creaDirectori(in_out, grup, tasca):
    if in_out == "INPUT":
        ruta = Path(rutaCarpetaINPUT + grup + "_" + tasca)
    elif in_out == "OUTPUT":
        ruta = Path(rutaCarpetaOUTPUT + grup + "_" + tasca)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def comprovaDisponibilitatArxiusperTipus(in_out, grup, tasca, llista):

    # Afegim prefix GRUP_TASCA_ als elements de la llista per poder comparar
    # amb la llista d'existents
    llista = [grup + "_" + tasca + "_" + arxiu for arxiu in llista]
    print("LLISTA TEORICA")
    print(llista)

    if in_out == "INPUT":
        # Recuperem els arxius existents en el directori INPUT
        llistaArxiusExistentsInput = llistaFitxersDirectori(in_out, grup, tasca)
        # print("LLISTA EXISTENT")
        # print(llistaArxiusExistentsInput)
        for llistat in llista:
            if llistat not in llistaArxiusExistentsInput:
                return False  # Termina la ejecución aquí si falla
        return True  # Si termina el bucle, todos estaban presentes
    elif in_out == "OUTPUT":
        # Recuperem els arxius existents en el directori OUTPUT
        llistaArxiusExistentsOutput = llistaFitxersDirectori(in_out, grup, tasca)
        # print("LLISTA EXISTENT")
        # print(llistaArxiusExistentsOutput)
        for llistat in llista:
            if llistat not in llistaArxiusExistentsOutput:
                return False  # Termina la ejecución aquí si falla
        return True  # Si termina el bucle, todos estaban presentes
    else:
        return False


# 4. Eliminar el directorio
# Opción A: Solo si está vacío
# ruta.rmdir()

# Opción B: Eliminar la carpeta y TODO su contenido (archivos y subcarpetas)
# shutil.rmtree(ruta)
