import pandas as pd
from datetime import datetime, timedelta
import os
import logic_comu

# CARREGA ARXIUS
# 9_DATOS_INVENTARIO_ALUMNO.csv


"""
df_resum_stock= logic_comu.carregaCSV("9_DATOS_INVENTARIO_ALUMNO.csv")

if any(dadesCarregades is None for dadesCarregades in [df_resum_stock]):
  print("NO ES POT SEGUIR EXECUTANT EL PROGRAMA PER FALTA DE DADES")
  exit()

# print("✅ Dades carregades correctament. Continuam correcció")
# print(df_resum_stock)
# print()

# 10_HISTORIAL_E_S_INVENTARIO_ALUMNO.csv

df_hes_inventari= logic_comu.carregaCSV("10_HISTORIAL_E_S_INVENTARIO_ALUMNO.csv")

if any(dadesCarregades is None for dadesCarregades in [df_hes_inventari]):
  print("NO ES POT SEGUIR EXECUTANT EL PROGRAMA PER FALTA DE DADES")
  exit()

# print("✅ Dades carregades correctament. Continuam correcció")
# print(df_hes_inventari)
# print()

# 2 COLUMNES DATAFRAMES
print("9_DATOS_INVENTARIO_ALUMNO.csv")
print("\n".join(df_resum_stock  .columns.tolist()))
print()
print("10_HISTORIAL_E_S_INVENTARIO_ALUMNO.csv")
print("\n".join(df_hes_inventari.columns.tolist()))
print()

# 3. NETEJA DADES

# NUMERIQUES
df_resum_stock['A_COST_UNITARI_I'] = pd.to_numeric(df_resum_stock['A_COST_UNITARI_I'], 
                                        errors='coerce').fillna(0.00)
df_resum_stock['A_IMPORT_I'] = pd.to_numeric(df_resum_stock['A_IMPORT_I'], 
                                        errors='coerce').fillna(0.00)
df_resum_stock['A_UNITATS_REALS_I'] = pd.to_numeric(df_resum_stock['A_UNITATS_REALS_I'], 
                                        errors='coerce').fillna(0.00)
df_resum_stock['A_UNITATS_DISPONIBLES_I'] = pd.to_numeric(df_resum_stock['A_UNITATS_DISPONIBLES_I'], 
                                        errors='coerce').fillna(0.00)
df_resum_stock['A_UNITATS_PENDENTS_ENTRAR_I'] = pd.to_numeric(df_resum_stock['A_UNITATS_PENDENTS_ENTRAR_I'], 
                                        errors='coerce').fillna(0.00)
df_resum_stock['A_UNITATS_PENDENTS_SORTIR_I'] = pd.to_numeric(df_resum_stock['A_UNITATS_PENDENTS_SORTIR_I'], 
                                        errors='coerce').fillna(0.00)

# NUMERIQUES
df_hes_inventari['A_UNITATS_HES'] = pd.to_numeric(df_hes_inventari['A_UNITATS_HES'], 
                                        errors='coerce').fillna(0.00)
df_hes_inventari['A_IN_HES'] = pd.to_numeric(df_hes_inventari['A_IN_HES'], 
                                        errors='coerce').fillna(0.00)
df_hes_inventari['A_OUT_HES'] = pd.to_numeric(df_hes_inventari['A_OUT_HES'], 
                                        errors='coerce').fillna(0.00)
df_hes_inventari['A_STOCK_HES'] = pd.to_numeric(df_hes_inventari['A_STOCK_HES'], 
                                        errors='coerce').fillna(0.00)

# DATES

df_hes_inventari['A_DATA_HES'] = pd.to_datetime(df_hes_inventari['A_DATA_HES'])


# CREA CLAU UNICA = EXPEDIENT + PRODUCTEP
df_resum_stock['CLAU_UNICA'] = df_resum_stock['A_EXPEDIENT_I'] + df_resum_stock['A_PRODUCTE_I']
df_hes_inventari['CLAU_UNICA'] = df_hes_inventari['A_EXPEDIENT_HES'] + df_hes_inventari['A_PRODUCTE_HES']

# CREAM NOU DF A PARTIR DE df_hes_inventari AMB NOMES
# STOCK FINALS (A_OPERACIO_HES = 'OP_FINAL')
df_hes_inventari_stocks_finals = df_hes_inventari.loc[df_hes_inventari['A_OPERACIO_HES'] == 'OP_FINAL']

# print(df_hes_inventari_stocks_finals)

# CREAM NOU DF A PARTIR DE df_hes_inventari AMB NOMES
# STOCKS NEGATIUS (A_STOCK_HES < 0)
df_hes_inventari_stocks_negatius = df_hes_inventari.loc[df_hes_inventari['A_STOCK_HES'] < 0]

# print(df_hes_inventari_stocks_negatius)

# UNIO df_resum_stock i df_hes_inventari_stocks_finals 
# D'AQUESTA MANERA PODEM DETERMINAR SI LLISTAT HES INVENTARI
# INCLOU TOTS ELS REGISTRES

df_inventari_final = pd.merge(df_resum_stock, df_hes_inventari_stocks_finals, on='CLAU_UNICA', how='left', suffixes=('', '_HES'))

# print(df_inventari_final)

# INICIAM CORRECCIO INVENTARI A NIVELL D'EMPRESA - PRODUCTE
# ASPECTES A COMPROVAR PER CADA EMPRESA-PRODUCTE:
# 1. NUM. UNITATS FINALS COINCIDEIX EN ELS DOS LLISTATS: 
#    9_DATOS_INVENTARIO_ALUMNO.csv i 10_HISTORIAL_E_S_INVENTARIO_ALUMNO.csv
# 2. UNITATS PENDENTS ENTRAR
# 3. UNITATS PENDENTS SORTIR
# 4. STOCKS NEGATIUS

informe = []

for idx, row in df_inventari_final.iterrows():
  empresa = row['A_EMPRESA_I']
  expedient = row['A_EXPEDIENT_I']
  producte = row['A_PRODUCTE_I']

  info = {
    'EMPRESA': empresa,
    'EXPEDIENT': expedient,
    'PRODUCTE': producte,
    'STOCK FINAL - UNITATS - INFORME STOCK': row['A_UNITATS_REALS_I'],
    'STOCK FINAL - UNITATS - HISTORIAL OPERACIONS': row['A_STOCK_HES'],
    'UNITATS FINALS COINCIDEIXEN': '',
    'UNITATS PENDENTS ENTRAR': row['A_UNITATS_PENDENTS_ENTRAR_I'],
    'ESTAT PENDENTS ENTRAR': '',
    'UNITATS PENDENTS SORTIR': row['A_UNITATS_PENDENTS_SORTIR_I'],
    'ESTAT PENDENTS SORTIR': '',
    'STOCKS NEGATIUS':  '✅',
    'RESULTAT': '',
    'OBSERVACIONS': ''
  }

  observacions = ""  

  # 'UNITATS FINALS COINCIDEIXEN'
  if row['A_UNITATS_REALS_I'] == row['A_STOCK_HES']:
    info['UNITATS FINALS COINCIDEIXEN'] = '✅'
  else:
    info['UNITATS FINALS COINCIDEIXEN'] = '❌'
    observacions += "El numero de unitats finals no coincideixen en els llistats aportats\n"

  # 'ESTAT PENDENTS ENTRAR'
  if row['A_UNITATS_PENDENTS_ENTRAR_I'] > 0:
    info['ESTAT PENDENTS ENTRAR'] = '❌'
    observacions += "Unitats pendents entrar > 0 -> Hi ha albarans de compra no validats?\n"
  else:
    info['ESTAT PENDENTS ENTRAR'] = '✅'

  # 'ESTAT PENDENTS SORTIR'
  if row['A_UNITATS_PENDENTS_SORTIR_I'] > 0:
    info['ESTAT PENDENTS SORTIR'] = '❌'
    observacions += "Unitats pendents sortir > 0 -> Hi ha albarans de venda no validats?\n"
  else:
    info['ESTAT PENDENTS SORTIR'] = '✅'

# 'CHECK STOCK NEGATIU'
    # Comprovam si empresa ha tingut stocks negatius

  if not df_hes_inventari_stocks_negatius.empty:
    error = df_hes_inventari_stocks_negatius[
      (df_hes_inventari_stocks_negatius['A_EMPRESA_HES'] == empresa) &
      (df_hes_inventari_stocks_negatius['A_PRODUCTE_HES'] == producte)
    ]
    if not error.empty:
      info['STOCKS NEGATIUS'] = '❌'
      observacions += "Per aquest producte hi ha operacions registrades que han generat stocks negatius"


  # 'RESULTAT'
  if all([info['STOCKS NEGATIUS'] == '✅', 
          info['UNITATS FINALS COINCIDEIXEN'] == '✅', 
          info['ESTAT PENDENTS ENTRAR'] == '✅', 
          info['ESTAT PENDENTS SORTIR'] == '✅']):
    info['RESULTAT'] = '✅ - ENHORABONA'
  else:
    info['RESULTAT'] = '❌ - REVISAR'

  # 'OBSERVACIONS'
  if observacions:
    info['OBSERVACIONS'] = observacions
  else:
    info['OBSERVACIONS'] = '✅'

  informe.append(info)

# CREAM DF INFORME
df_informe = pd.DataFrame(informe)

# GUARDEM INFORME
fileName = "Correccio_Inventari_Empresa_Producte.xlsx"

rutaActual = os.getcwd()

rutaFitxer = rutaActual + "/HISTORIC_CORRECCIONS/" + fileName

try:
    df_informe.to_excel(rutaFitxer, index=False)
    print(f"✅ Corrección Inventario generada: {fileName}")
except Exception as e:
    print(f"❌ Error al guardar: {e}")

# CONTINUAM CORRECCIO INVENTARI A NIVELL D'EMPRESA
# ASPECTES A COMPROVAR PER CADA EMPRESA:
# 1. VALOR FINAL NO SUPERIOR A 1.000 €
# 
# AQUESTA CORRECCIO NO ES FA A NIVELL DE PRODUCTE,
# SINO QUE ES FA A NIVELL D'EMPRESA, PER LA QUAL COSA
# HEM DE CREAR UN NOU DF AMB AGRUPAMENT PER EMPRESA AMB 
# SUMA DE LA COLUMNA IMPORT

# PRIMER PAS: CREAM DF REDUIT AMB LES COLUNNES QUE ENS INTERESSEN

df_reduit = df_inventari_final[['A_EMPRESA_I', 'A_IMPORT_I']]

# print(df_reduit)

# SEGON PAS: CREAM DF AGRUPAT PER EMPRESA AMB SUMA IMPORT

df_agrupat = df_reduit.groupby('A_EMPRESA_I').sum().reset_index()

# print(df_agrupat)

informe02 = []

for idx, row in df_agrupat.iterrows():
  empresa = row['A_EMPRESA_I']
  valor_stock_final = row['A_IMPORT_I']

  info02 = {
    'EMPRESA': empresa,
    'VALOR STOCK FINAL': valor_stock_final,
    'VALOR STOCK FINAL NO SUPERIOR A 1.000 €': '',
    'RESULTAT': '',
    'OBSERVACIONS': ''
  }

  observacions02 = ""

  # 'CHECK VALOR STOCK NO SUPERIOR A 1.000 €'
  # Comprovam si el valor del stock és superior a 1.000 €
  
  if info02['VALOR STOCK FINAL'] > 1000:
    info02['VALOR STOCK FINAL NO SUPERIOR A 1.000 €'] = '❌'
    observacions02 += "El valor dels articles en magatzem supera el límit de 1.000 €"
  else:
    info02['VALOR STOCK FINAL NO SUPERIOR A 1.000 €'] = '✅'

  # 'RESULTAT'
  if info02['VALOR STOCK FINAL NO SUPERIOR A 1.000 €'] == '✅':
    info02['RESULTAT'] = '✅ - ENHORABONA'
  else:
    info02['RESULTAT'] = '❌ - REVISAR'

  # 'OBSERVACIONS'
  if observacions02:
    info02['OBSERVACIONS'] = observacions02
  else:
    info02['OBSERVACIONS'] = '✅'

  informe02.append(info02)

# CREAM DF INFORME
df_informe02 = pd.DataFrame(informe02)

# GUARDEM INFORME
fileName02 = "Correccio_Inventari_valor_stock_final.xlsx"

rutaActual = os.getcwd()

rutaFitxer = rutaActual + "/HISTORIC_CORRECCIONS/" + fileName02

try:
    df_informe02.to_excel(rutaFitxer, index=False)
    print(f"✅ Corrección Inventario generada: {fileName02}")
except Exception as e:
    print(f"❌ Error al guardar: {e}")

"""
