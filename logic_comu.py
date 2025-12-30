import pandas as pd
import os


def obtenir_expedient(nom_empresa):
    try:
        if pd.isna(nom_empresa):
            return "UNKNOWN"
        parts = str(nom_empresa).split(" ")
        if len(parts) >= 2:
            return parts[1]
        else:
            return "UNKNOWN"
    except:
        return "ERROR"


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


def unionDataFrames(
    dfleft, dfright, clauleft, clauright, com, suffleft, suffright, resultat
):

    df_union = pd.merge(
        dfleft,
        dfright,
        left_on=clauleft,
        right_on=clauright,
        how=com,
        suffixes=(suffleft, suffright),
        indicator=resultat,
    )

    return df_union


# ==============================================================================
# FUNCIONS PER A LA CORRECCIO DE COMPRES
# ==============================================================================


# INSERIM LA DATA DE ENTREGA EN EL DF DESTI
def insereixDataEntregaEnDFDesti(
    df_desti, columnaDataEntrega, columnaEmpresa, df_fechas
):
    # CONVERTIM df_fechas['EMPRESA_ALUMNO'] i df_fechas['FECHA_ENTREGA'] en un diccionari
    mapaDatesEntrega = dict(
        zip(df_fechas["EMPRESA_ALUMNO"], df_fechas["FECHA_ENTREGA"])
    )

    # print(mapaDatesEntrega)

    # INSERIM LA DATA EN df_desti
    df_desti[columnaDataEntrega] = df_desti[columnaEmpresa].map(mapaDatesEntrega)

    # for fila in df_desti.itertuples():
    #     print(f"EMPRESA: {fila.A_EMPRESA_CF} - DATA: {fila.A_FECHA_ENTREGA_FV}")

    return df_desti


# NETEJA TIPUS DE DADES EN df_real
def netejaTipusDadesDFReal(df_real):
    df_real["R_FECHA_EMISION_C"] = pd.to_datetime(df_real["R_FECHA_EMISION_C"])
    df_real["R_FECHA_ENTREGA"] = pd.to_datetime(df_real["R_FECHA_ENTREGA"])
    df_real["R_IMPORTE_C"] = pd.to_numeric(
        df_real["R_IMPORTE_C"], errors="coerce"
    ).fillna(0.00)
    df_real["R_ACUMULADO_C"] = pd.to_numeric(
        df_real["R_ACUMULADO_C"], errors="coerce"
    ).fillna(0.00)
    return df_real


# NETEJA TIPUS DE DADES EN df_ped
def netejaTipusDadesDFPed(df_ped):
    df_ped["A_FECHA_ALTA_ODOO_CP"] = pd.to_datetime(df_ped["A_FECHA_ALTA_ODOO_CP"])
    df_ped["A_FECHA_EMISION_CP"] = pd.to_datetime(df_ped["A_FECHA_EMISION_CP"])
    df_ped["A_IMPORTE_CP"] = pd.to_numeric(
        df_ped["A_IMPORTE_CP"], errors="coerce"
    ).fillna(0.00)
    df_ped["A_ACUMULADO_CP"] = pd.to_numeric(
        df_ped["A_ACUMULADO_CP"], errors="coerce"
    ).fillna(0.00)

    return df_ped


# NETEJA TIPUS DE DADES EN df_alb
def netejaTipusDadesDFAlb(df_alb):
    df_alb["A_FECHA_ALTA_ODOO_CA"] = pd.to_datetime(df_alb["A_FECHA_ALTA_ODOO_CA"])
    df_alb["A_FECHA_EMISION_CA"] = pd.to_datetime(df_alb["A_FECHA_EMISION_CA"])
    df_alb["A_IMPORTE_CA"] = pd.to_numeric(
        df_alb["A_IMPORTE_CA"], errors="coerce"
    ).fillna(0.00)
    df_alb["A_ACUMULADO_CA"] = pd.to_numeric(
        df_alb["A_ACUMULADO_CA"], errors="coerce"
    ).fillna(0.00)
    return df_alb


# NETEJA TIPUS DE DADES EN df_fac
def netejaTipusDadesDFFac(df_fac):
    df_fac["A_FECHA_EMISION_CF"] = pd.to_datetime(df_fac["A_FECHA_EMISION_CF"])
    df_fac["A_FECHA_ENTREGA_CF"] = pd.to_datetime(df_fac["A_FECHA_ENTREGA_CF"])
    df_fac["A_IMPORTE_CF"] = pd.to_numeric(
        df_fac["A_IMPORTE_CF"], errors="coerce"
    ).fillna(0.00)
    df_fac["A_ACUMULADO_CF"] = pd.to_numeric(
        df_fac["A_ACUMULADO_CF"], errors="coerce"
    ).fillna(0.00)
    return df_fac


# OBTENCIÓ DUPLICATS
def obtenirDuplicats(df, columna):
    return df[df.duplicated(columna, keep=False)]
