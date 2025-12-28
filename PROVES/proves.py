import pandas as pd
import os

df_ventas_importe = pd.DataFrame(
    {
        "id_pedido": [101, 102, 103],
        "importe": [100, 200, 150],
        "tienda": ["Barcelona", "Madrid", "Valencia"],
        "descuento": [10, 20, 15],
    }
)

df_ventas_cliente = pd.DataFrame(
    {"id_pedido": [101, 102, 102, 103], "cliente": ["Juan", "Teresa", "Roberto", "Eva"]}
)

df_ventas = pd.merge(
    df_ventas_importe,
    df_ventas_cliente,
    on="id_pedido",
    how="outer",
    indicator=True,
    suffixes=("_importe", "_cliente"),
)


print(df_ventas)
