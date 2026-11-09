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

pedidos = pd.read_sql("SELECT id_pedido, data_pedido, status FROM pedidos_sql", engine)
itens = pd.read_sql("SELECT id_pedido, id_produto, valor_total FROM itens_sql", engine)
produtos = pd.read_sql("SELECT id_produto, categoria FROM produtos_sql", engine)

pedidos['data_pedido'] = pd.to_datetime(pedidos['data_pedido'], format='%Y-%m-%d', errors="coerce")
pedidos = pedidos.drop(pedidos[pedidos['status'] == 'Cancelado'].index)
pedidos = pedidos.drop(columns='status')

# A pergunta central aqui é sobre qual categoria de produto mais sai

A = pd.merge(pedidos, itens, on='id_pedido', how='left')
B = pd.merge(A, produtos, on='id_produto', how='left')
df_categorias = B.copy()

quantidades = df_categorias['categoria'].value_counts()

plt.figure(figsize=(10, 5))
quantidades.sort_values().plot(kind='barh', color='blue', edgecolor='black')
plt.title('Ranking de saída das categorias dos produtos', fontsize=14)
plt.xlabel('Quantidade de pedidos', fontsize=12)
plt.ylabel('Categorias', fontsize=12)
plt.show()


# Porcentagem de saída
porcentagens = df_categorias['categoria'].value_counts(normalize=True) * 100

plt.figure(figsize=(10, 5))
porcentagens.sort_values().plot(kind='barh', color='green', edgecolor='red')
plt.title('Porcentagem de saída das categorias dos produtos', fontsize=14)
plt.xlabel('Porcentagem', fontsize=12)
plt.ylabel('Categorias', fontsize=12)
plt.show()

# Avaliação de categorias mais vendidas por mês
pedidos_itens = pedidos.merge(itens, on='id_pedido', how='left')
df_mes = pedidos_itens.merge(produtos, on='id_produto', how='left')
df_mes["ano_mes"] = df_mes["data_pedido"].dt.to_period("M").astype(str)

vendas_categoria = (
    df_mes.groupby(['ano_mes', 'categoria'])['valor_total']
    .sum()
    .reset_index()
)

vendas_categoria['ranking'] = (vendas_categoria.groupby('ano_mes')['valor_total'].rank(ascending=False, method='first')).astype(int)

top_2 = vendas_categoria[vendas_categoria['ranking'].isin([1, 2])]

matriz_ranking = top_2.pivot(index='categoria', columns='ano_mes', values='ranking')

plt.figure(figsize=(14, 5))

sns.heatmap(
    matriz_ranking, 
    annot=True,         
    cmap="Greens_r",     
    cbar=False,          
    linewidths=.5,       
    fmt='g'              
)

plt.title('Principais categorias por mês', fontsize=14, weight='bold', pad=15)
plt.xlabel('Meses', fontsize=12)
plt.ylabel('Categorias', fontsize=12)
plt.xticks(rotation=90, ha='right')

plt.tight_layout()
plt.show()
