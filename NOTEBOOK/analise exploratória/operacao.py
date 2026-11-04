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

pedidos = pd.read_sql("SELECT id_pedido, status FROM pedidos_sql", engine)
itens = pd.read_sql("SELECT id_pedido, valor_total, quantidade FROM itens_sql", engine)

pedidos = pedidos.drop(pedidos[pedidos['status'] == 'Cancelado'].index)
pedidos = pedidos.drop(columns='status')

df_operacao = pd.merge(pedidos, itens, on='id_pedido', how='left')

qtd_media = df_operacao['quantidade'].copy()
qtd_media = qtd_media.mean()

valor_medio = df_operacao['valor_total'].copy()
valor_medio = valor_medio.mean()

print(df_operacao, qtd_media, valor_medio)

