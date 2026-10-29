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

pedidos = pd.read_sql("SELECT id_pedido, data_pedido, id_cliente FROM pedidos_sql", engine)
itens   = pd.read_sql("SELECT id_pedido, valor_total, quantidade FROM itens_sql", engine)
clientes = pd.read_sql("SELECT id_cliente, idade, cidade FROM clientes_sql", engine)

# itens_agrupados = itens.groupby("id_pedido", as_index=False)["valor_total"].sum()
# df_data = pedidos.merge(itens_agrupados, on="id_pedido", how="left")

# df_data["data_pedido"] = pd.to_datetime(df_data["data_pedido"], errors="coerce")
# df_data["ano_mes"] = df_data["data_pedido"].dt.to_period("M")

# resumo = df_data.groupby("ano_mes")["valor_total"].agg(
#     Faturamento="sum",
#     Media="mean",
#     Desvio_Padrao="std",
#     Qtd_Pedidos="count"
# ).reset_index()


# Crescimento --- o faturamento está aumentando?

# ano = []
# mes = []
# for data in df['ano_mes']:
#     ano.append(data.year)
#     mes.append(data.month)


# df_data['ano'] = ano
# df_data['mes'] = mes

# periodos = df_data.groupby(['ano', 'mes'])
# periodo_anual = df_data.groupby(['ano'])

# print(periodos)
# for (ano, mes), valor_mes in periodos:
#     soma_vendas = valor_mes['valor_total'].sum()
#     # print(f"Soma das Vendas em {mes} de {ano}: R$ {soma_vendas:.2f}")
#     soma_pedidos = len(valor_mes)
#     # print(f"Quantidade de Pedidos em {mes} de {ano}: {soma_pedidos}")

# for ano, valor_ano in periodo_anual:
#     soma_anual = valor_ano['valor_total'].sum()
#     soma_pedidos_ano = len(valor_ano)

# # Crescimento (mensal) --- plotando em um grafico

# plot_crescimento = df_data.groupby(['ano', 'mes'])['valor_total'].agg(
#     Faturamento='sum',
#     Qtd_Pedidos='count'
# ).reset_index()

# plot_crescimento['periodo'] = plot_crescimento['ano'].astype(str) + '-' + plot_crescimento['mes'].astype(str).str.zfill(2)

# plt.plot(plot_crescimento['periodo'], plot_crescimento['Faturamento'], 
#          marker='o',
#          linestyle='-',
#          color='b',
#          linewidth=2)

# plt.title('Evolução do Faturamento Mensal', fontsize=16) #titulo
# plt.xlabel('Ano-Mês', fontsize=12) #eixo x
# plt.ylabel('Faturamento (dezenas de milhões de R$)', fontsize=12) #eixo y
# plt.xticks(rotation=90, ha='right') #girando nomes para não sobrepor
# plt.grid(True, linestyle='--', alpha=0.6) #grade para facilitar leitura do gráfico

# plt.show()

# # Crescimento (anual) --- plotando em um grafico

# plot_crescimento_ano = df_data.groupby(['ano'])['valor_total'].agg(
#     Faturamento='sum',
#     Qtd_Pedidos='count'
# ).reset_index()

# plot_crescimento_ano['periodo'] = plot_crescimento_ano['ano'].astype(str).str.zfill(2)

# plt.plot(plot_crescimento_ano['periodo'], plot_crescimento_ano['Faturamento'], 
#          marker='o',
#          linestyle='-',
#          color='b',
#          linewidth=2)

# plt.title('Evolução do Faturamento Anual', fontsize=16) #titulo
# plt.xlabel('Ano', fontsize=12) #eixo x
# plt.ylabel('Faturamento (centenas de milhões de R$)', fontsize=12) #eixo y
# plt.xticks(rotation=90, ha='right') #girando nomes para não sobrepor
# plt.grid(True, linestyle='--', alpha=0.6) #grade para facilitar leitura do gráfico

# plt.show()

# Estudo de clientes --- Quem continua comprando? Qual a média de idade dos clientes? Qual cidade mais compra?
# Idades:
# dados_clientes = clientes.groupby('id_cliente')['idade'].mean()
# df_idade = pedidos.merge(dados_clientes, on='id_cliente', how='left')

# df_idade = df_idade.drop(columns=['data_pedido', 'id_pedido'])

# soma_idades = df_idade['idade'].sum()
# qtd_pedidos = len(df_idade)

# idade_media = int(df_idade['idade'].mean())
# idade_mediana = int(df_idade['idade'].median())
# idade_moda = df_idade['idade'].mode()[0]


# plt.figure(figsize=(10, 5))
# plt.hist(df_idade['idade'], bins=20, color='lightgreen', edgecolor='black')
# plt.title('Distribuição de Idade dos Clientes', fontsize=14)
# plt.xlabel('Idade', fontsize=12)
# plt.ylabel('Frequência', fontsize=12)
# plt.axvline(idade_media, color='red', linestyle='dashed', linewidth=2, label=f'Média: {idade_media}')
# plt.axvline(idade_mediana, color='blue', linestyle='dashed', linewidth=2, label=f'Mediana: {idade_mediana}')
# plt.axvline(idade_moda, color='green', linestyle='dashed', linewidth=2, label=f'Moda: {idade_moda}')
# plt.legend()
# plt.show()


# Cidades:
# df_cidade = pedidos.merge(clientes[['id_cliente', 'cidade']], on='id_cliente', how='left')

# print(df_cidade)

# top_cidades = df_cidade['cidade'].value_counts().head(5)

# plt.figure(figsize=(10, 5))
# top_cidades.sort_values().plot(kind='barh', color='yellow', edgecolor='black')
# plt.title('Top 5 Cidades com mais Clientes', fontsize=14)
# plt.xlabel('Quantidade de Clientes', fontsize=12)
# plt.ylabel('Cidade', fontsize=12)
# plt.show()

# Clientes recorrentes:
df_cliente = pedidos
compras_por_cliente = df_cliente.groupby('id_cliente')['id_pedido'].count().reset_index()
compras_por_cliente.columns = ['id_cliente', 'qtd']

def frequencia(qtd):
    if qtd == 1: return '1x'
    elif qtd == 2: return '2x'
    elif qtd == 3: return '3x'
    elif qtd == 4: return '4x'
    elif qtd == 5: return '5x'
    elif qtd == 6: return '6x'
    elif qtd == 7: return '7x'
    elif qtd == 8: return '8x'
    elif qtd == 9: return '9x'
    elif qtd == 10: return '10x'
    elif qtd == 11: return '11x'
    elif qtd == 12: return '12x'
    elif qtd == 13: return '13x'
    elif qtd == 14: return '14x'
    elif qtd == 15: return '15x'
    elif qtd == 16: return '16x'
    elif qtd == 17: return '17x'
    elif qtd == 18: return '18x'
    elif qtd == 19: return '19x'
    elif qtd == 20: return '20x'
    elif qtd == 21: return '21x'

compras_por_cliente['faixa'] = compras_por_cliente['qtd'].apply(frequencia)
distribuicao = compras_por_cliente['faixa'].value_counts().reindex(['1x', '2x', '3x', '4x', '5x a 9x', '10x ou +'])

for value in compras_por_cliente['faixa']:
    '1x' == '1x',
    '2x' == '2x',
    '3x' == '3x',
    '4x' == '4x',
    '5x', '6x', '7x', '8x', '9x' == '5x a 9x',
    '10x', '11x', '12x', '13x', '14x', '15x', '16x', '17x', '18x', '19x', '20x', '21x' == '10x ou mais'

tamanho_tabela = len(compras_por_cliente)
# qtd_pedidos = cliente

print(compras_por_cliente['faixa'])

# plt.figure(figsize=(10, 5))
# bars = plt.bar(distribuicao.index, distribuicao.values, color='skyblue', edgecolor='black')
# plt.title('Quantas vezes cada cliente comprou?', fontsize=14)
# plt.xlabel('Número de Compras', fontsize=12)
# plt.ylabel('Quantidade de Clientes', fontsize=1)

# for bar in bars:
#     yval = bar.get_height()
#     plt.text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha='center', va='bottom')
# plt.show()