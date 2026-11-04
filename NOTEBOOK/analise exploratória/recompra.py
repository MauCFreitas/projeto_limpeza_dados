import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (12, 5)

engine = create_engine("postgresql+psycopg://postgres:@127.0.0.1:5432/analise_vendas")

pedidos = pd.read_sql("SELECT data_pedido, id_cliente, status FROM pedidos_sql", engine)
clientes = pd.read_sql("SELECT id_cliente FROM clientes_sql", engine)

pedidos['data_pedido'] = pd.to_datetime(pedidos["data_pedido"], format="%Y-%m-%d")

pedidos = pedidos.drop(pedidos[pedidos['status'] == 'Cancelado'].index)
# Clientes recorrentes:
df_clientes = pedidos.copy()
df_clientes['recorrencia'] = df_clientes['id_cliente'].map(df_clientes['id_cliente'].value_counts())

df_clientes = df_clientes.sort_values(by=['recorrencia', 'id_cliente', 'data_pedido'], ascending=[True, True, True])

df_clientes = df_clientes.drop_duplicates(subset=['id_cliente']).reset_index(drop=True)

def classificar_faixa(linhas):
    recorrencia = linhas['recorrencia']
    if recorrencia == 1:
        return '1x'
    elif 2 <= recorrencia <= 5:
        return '2 a 5x'
    elif 5 < recorrencia <= 10:
        return '6 a 10x'
    elif recorrencia > 10:
        return 'Mais de 10x'

df_clientes['faixa_compras'] = df_clientes.apply(classificar_faixa, axis=1)

clientes_unicos = df_clientes[df_clientes['faixa_compras'] == '1x']
clientes_recorrentes_2_5x = df_clientes[df_clientes['faixa_compras'] == '2 a 5x']
clientes_recorrentes_6_10x = df_clientes[df_clientes['faixa_compras'] == '6 a 10x']
clientes_recorrentes_10x = df_clientes[df_clientes['faixa_compras'] == 'Mais de 10x']

resumo_faixas = df_clientes['faixa_compras'].value_counts()
porcentagens = df_clientes['faixa_compras'].value_counts(normalize=True) * 100
ordem_faixas = ['2 a 5x', '6 a 10x', '1x', 'Mais de 10x']
porcentagens = porcentagens.reindex(ordem_faixas).fillna(0)

df_pct_1x = porcentagens['1x']
df_pct_2_5x = porcentagens['2 a 5x']
df_pct_6_10x = porcentagens['6 a 10x']
df_pct_10x = porcentagens['Mais de 10x']

plt.figure(figsize=(8, 6))

plt.pie(porcentagens.values, 
        labels=porcentagens.index, 
        startangle=90, 
        colors=sns.color_palette("Set2"),
        autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
        textprops=dict(color="w", weight="bold"),
    )
plt.title("Taxa de recompra", fontsize=14, pad=15)
plt.legend(porcentagens.index, loc="upper right", bbox_to_anchor=(1.2, 1))
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()

# Tempo que leva até a recompra
df_recompra = pedidos.copy()
df_recompra = df_recompra.sort_values(by=["id_cliente", "data_pedido"])

df_recompra['data_pedido'] = pd.to_datetime(df_recompra["data_pedido"], format="%Y-%m-%d")

df_recompra['diferenca'] = df_recompra.groupby('id_cliente')['data_pedido'].diff().dt.days
tempo_medio_recompra = df_recompra.groupby('id_cliente')['diferenca'].mean()
media_recompra = tempo_medio_recompra.mean()

print(media_recompra)

sns.histplot(
    data=df_recompra,
    x="diferenca",
    bins=155,
    kde=True,
    stat="count",
    color="teal",
    edgecolor="black",
    line_kws={"color": "royalblue", "linewidth": 3},
)

plt.title("Tempo médio para recompra", fontsize=14, pad=15)
plt.xlabel("Dias", fontsize=10)
plt.ylabel("Frequencia de pedidos", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.xlim(0, 225)
plt.xticks(list(range(0, 226, 25)), rotation=90)
plt.tight_layout()
plt.show()
