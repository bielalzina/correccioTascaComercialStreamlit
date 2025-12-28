import pandas as pd
import os


def carregaCSV(fileName):
    # obtenim ruta actual
    rutaActual = os.getcwd()
    rutaFitxer = rutaActual + "/LLISTATS_CSV/" + fileName
    # Carga CSV estándar: Separador coma, decimal punto, fechas ISO.
    # Leemos forzando que los IDs sean texto para no perder ceros o precisión
    df = pd.read_csv(rutaFitxer, sep=",", encoding="utf-8", dtype=str)
    return df


def exportToExcel(df, fileName):
    # obtenim ruta actual
    rutaActual = os.getcwd()
    rutaFitxer = rutaActual + "/HISTORIC_CORRECCIONS/" + fileName
    try:
        df.to_excel(rutaFitxer, index=False)
        print(f"✅ Exportacio a Excel correcta: {fileName}")
    except Exception as e:
        print(f"❌ Error al exportar a Excel: {e}")
