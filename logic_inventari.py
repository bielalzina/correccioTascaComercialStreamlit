import pandas as pd
from datetime import datetime, timedelta
import os
import logic_comu

# 1. CARREGA ARXIUS 
# 9_DATOS_INVENTARIO_ALUMNO.csv

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

# Agrupamos el resumen por empresa para calcular el valor total del almacén
# (Aunque revisaremos línea a línea, necesitamos el total para la regla de los 1000€)
valor_stock_final_per_empresa = df_resum_stock.groupby('A_EMPRESA_I')['A_IMPORT_I'].sum()

# print(valor_stock_final_per_empresa)

# UNIO df_resum_stock i df_hes_inventari_stocks_finals 
# D'AQUESTA MANERA PODEM DETERMINAR SI LLISTAT HES INVENTARI
# INCLOU TOTS ELS REGISTRES

df_inventari_final = pd.merge(df_resum_stock, df_hes_inventari_stocks_finals, on='CLAU_UNICA', how='left', suffixes=('', '_HES'))

# print(df_inventari_final)

# CREAM INFORME FINAL
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
    'STOCKS FINALS COINCIDEIXEN': '',
    'UNITATS PENDENTS ENTRAR': row['A_UNITATS_PENDENTS_ENTRAR_I'],
    'ESTAT PENDENTS ENTRAR': '',
    'UNITATS PENDENTS SORTIR': row['A_UNITATS_PENDENTS_SORTIR_I'],
    'ESTAT PENDENTS SORTIR': '',
    'STOCKS NEGATIUS':  '✅',
    'VALOR STOCK FINAL': valor_stock_final_per_empresa.get(empresa, 0),
    'VALOR STOCK NO SUPERIOR A 1.000 €': '✅',
    'RESULTAT': '',
    'OBSERVACIONS': ''
  }

  observacions = []

  # 'CHECK STOCK NEGATIU'
    # Comprovam si empresa ha tingut stocks negatius

  if not df_hes_inventari_stocks_negatius.empty:
    error = df_hes_inventari_stocks_negatius[
      (df_hes_inventari_stocks_negatius['EMPRESA'] == empresa) &
      (df_hes_inventari_stocks_negatius['PRODUCTO'] == producto)
    ]
    if not error.empty:
      info['STOCKS NEGATIUS'] = '❌'
      observacions.append(error.iloc[0]['OBSERVACIONS'])

  # 'STOCKS FINALS COINCIDEIXEN'
  if row['A_UNITATS_REALS_I'] == row['A_STOCK_HES']:
    info['STOCKS FINALS COINCIDEIXEN'] = '✅'
  else:
    info['STOCKS FINALS COINCIDEIXEN'] = '❌'
    observacions.append("Stocks finals no coincideixen. Llistat HES incomplet ¿?")

  # 'ESTAT PENDENTS ENTRAR'
  if row['A_UNITATS_PENDENTS_ENTRAR_I'] > 0:
    info['ESTAT PENDENTS ENTRAR'] = '❌'
    observacions.append("Unitats pendents entrar > 0 (Albarans de compra no validats ¿?)")
  else:
    info['ESTAT PENDENTS ENTRAR'] = '✅'

  # 'ESTAT PENDENTS SORTIR'
  if row['A_UNITATS_PENDENTS_SORTIR_I'] > 0:
    info['ESTAT PENDENTS SORTIR'] = '❌'
    observacions.append("Unitats pendents sortir > 0 (Albarans de venda no validats ¿?)")
  else:
    info['ESTAT PENDENTS SORTIR'] = '✅'

  # 'CHECK VALOR STOCK NO SUPERIOR A 1.000 €'
  # Comprovam si el valor del stock és superior a 1.000 €
  
  if info['VALOR STOCK FINAL'] > 1000:
    info['VALOR STOCK NO SUPERIOR A 1.000 €'] = '❌'
    observacions.append("Valor dels articles en magatzem excessiu")
  else:
    info['VALOR STOCK NO SUPERIOR A 1.000 €'] = '✅'

  # 'RESULTAT'
  if all([info['STOCKS NEGATIUS'] == '✅', 
          info['STOCKS FINALS COINCIDEIXEN'] == '✅', 
          info['ESTAT PENDENTS ENTRAR'] == '✅', 
          info['ESTAT PENDENTS SORTIR'] == '✅', 
          info['VALOR STOCK NO SUPERIOR A 1.000 €'] == '✅']):
    info['RESULTAT'] = '✅ - ENHORABONA'
  else:
    info['RESULTAT'] = '❌ - REVISAR'

  # 'OBSERVACIONS'
  if observacions:
    info['OBSERVACIONS'] = '\n'.join(observacions)
  else:
    info['OBSERVACIONS'] = '✅'

  informe.append(info)

# CREAM DF INFORME
df_informe = pd.DataFrame(informe)

# GUARDEM INFORME
fileName = "Correccio_Inventari_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".xlsx"

rutaActual = os.getcwd()

rutaFitxer = rutaActual + "/HISTORIC_CORRECCIONS/" + fileName

try:
    df_informe.to_excel(rutaFitxer, index=False)
    print(f"✅ Corrección Inventario generada: {fileName}")
except Exception as e:
    print(f"❌ Error al guardar: {e}")


