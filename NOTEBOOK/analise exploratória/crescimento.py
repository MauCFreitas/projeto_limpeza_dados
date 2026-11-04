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

pedidos = pd.read_sql("SELECT id_pedido, data_pedido, id_cliente, status FROM pedidos_sql", engine)
itens   = pd.read_sql("SELECT id_pedido, valor_total, quantidade FROM itens_sql", engine)
clientes = pd.read_sql("SELECT id_cliente, idade, cidade FROM clientes_sql", engine)

pedidos = pedidos.drop(pedidos[pedidos['status'] == 'Cancelado'].index)
pedidos['data_pedido'] = pd.to_datetime(pedidos["data_pedido"], format="%Y-%m-%d")

itens_agrupados = itens.groupby("id_pedido", as_index=False)["valor_total"].sum()
df_data = pedidos.merge(itens_agrupados, on="id_pedido", how="left")

df_data["data_pedido"] = pd.to_datetime(df_data["data_pedido"], errors="coerce")
df_data["ano_mes"] = df_data["data_pedido"].dt.to_period("M")


resumo = df_data.groupby("ano_mes")["valor_total"].agg(
    Faturamento="sum",
    Media="mean",
    Desvio_Padrao="std",
    Qtd_Pedidos="count"
).reset_index()


# Crescimento --- o faturamento está aumentando?

ano = []
mes = []
for data in df_data['ano_mes']:
    ano.append(data.year)
    mes.append(data.month)


df_data['ano'] = ano
df_data['mes'] = mes

periodos = df_data.groupby(['ano', 'mes'])
periodo_anual = df_data.groupby(['ano'])

print(periodos)
for (ano, mes), valor_mes in periodos:
    soma_vendas = valor_mes['valor_total'].sum()
    # print(f"Soma das Vendas em {mes} de {ano}: R$ {soma_vendas:.2f}")
    soma_pedidos = len(valor_mes)
    # print(f"Quantidade de Pedidos em {mes} de {ano}: {soma_pedidos}")

for ano, valor_ano in periodo_anual:
    soma_anual = valor_ano['valor_total'].sum()
    soma_pedidos_ano = len(valor_ano)

# Crescimento (mensal) --- plotando em um grafico

plot_crescimento = df_data.groupby(['ano', 'mes'])['valor_total'].agg(
    Faturamento='sum',
    Qtd_Pedidos='count'
).reset_index()

plot_crescimento['periodo'] = plot_crescimento['ano'].astype(str) + '-' + plot_crescimento['mes'].astype(str).str.zfill(2)

plt.plot(plot_crescimento['periodo'], plot_crescimento['Faturamento'], 
         marker='o',
         linestyle='-',
         color='blue',
         linewidth=2)

plt.title('Evolução do Faturamento Mensal', fontsize=16) #titulo
plt.xlabel('Ano-Mês', fontsize=10) #eixo x
plt.ylabel('Faturamento', fontsize=12) #eixo y
plt.xticks(rotation=90, ha='right') #girando nomes para não sobrepor
plt.grid(True, linestyle='--', alpha=0.6) #grade para facilitar leitura do gráfico
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"R$ {x:,.0f}".replace(",", "."))
)

plt.show()

# Crescimento (anual) --- plotando em um grafico

plot_crescimento_ano = df_data.groupby(['ano'])['valor_total'].agg(
    Faturamento='sum',
    Qtd_Pedidos='count'
).reset_index()

plot_crescimento_ano['periodo'] = plot_crescimento_ano['ano'].astype(str).str.zfill(2)

plt.plot(plot_crescimento_ano['periodo'], plot_crescimento_ano['Faturamento'], 
         marker='o',
         linestyle='-',
         color='b',
         linewidth=2)

plt.title('Evolução do Faturamento Anual', fontsize=16) #titulo
plt.xlabel('Ano', fontsize=10) #eixo x
plt.ylabel('Faturamento', fontsize=12) #eixo y
plt.xticks(rotation=90, ha='right') #girando nomes para não sobrepor
plt.grid(True, linestyle='--', alpha=0.6) #grade para facilitar leitura do gráfico
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"R$ {x:,.0f}".replace(",", "."))
)

plt.show()
