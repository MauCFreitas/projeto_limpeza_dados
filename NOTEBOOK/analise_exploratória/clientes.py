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

pedidos = pd.read_sql("SELECT id_pedido, id_cliente FROM pedidos_sql", engine)
clientes = pd.read_sql("SELECT id_cliente, idade, cidade FROM clientes_sql", engine)


# Estudo de clientes --- Quem continua comprando? Qual a média de idade dos clientes? Qual cidade mais compra?
# Idades:

dados_clientes = clientes.groupby('id_cliente')['idade'].mean()
df_idade = pedidos.merge(dados_clientes, on='id_cliente', how='left')

df_idade = df_idade.drop(columns=['id_pedido'])

soma_idades = df_idade['idade'].sum()
qtd_pedidos = len(df_idade)

# Teste para saber qual variável é a mais confiável
print(df_idade['idade'].skew()) # valor apresentado equivalente a 


idade_media = int(df_idade['idade'].mean())
idade_mediana = int(df_idade['idade'].median())
idade_moda = df_idade['idade'].mode()[0]


plt.figure(figsize=(10, 5))
plt.hist(df_idade['idade'], bins=20, color='lightgreen', edgecolor='black')
plt.title('Distribuição de Idade dos Clientes', fontsize=14)
plt.xlabel('Idade', fontsize=12)
plt.ylabel('Frequência', fontsize=12)
plt.axvline(idade_media, color='red', linestyle='dashed', linewidth=2, label=f'Média: {idade_media}')
plt.axvline(idade_mediana, color='blue', linestyle='dashed', linewidth=2, label=f'Mediana: {idade_mediana}')
plt.axvline(idade_moda, color='green', linestyle='dashed', linewidth=2, label=f'Moda: {idade_moda}')
plt.legend()
plt.show()


# # Cidades:
df_cidade = pedidos.merge(clientes[['id_cliente', 'cidade']], on='id_cliente', how='left')

top_cidades = df_cidade['cidade'].value_counts().head(5)

plt.figure(figsize=(10, 5))
top_cidades.sort_values().plot(kind='barh', color='yellow', edgecolor='black')
plt.title('Top 5 Cidades com mais Clientes', fontsize=14)
plt.xlabel('Quantidade de Clientes', fontsize=12)
plt.ylabel('Cidade', fontsize=12)
plt.show()