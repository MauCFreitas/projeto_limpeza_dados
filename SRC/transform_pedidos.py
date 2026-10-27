import pandas as pd
import numpy as np
import re

# para esta correção de tabela, precisarei usar todas as outras tabelas ja organizadas

clientes = pd.read_csv(f'DATA\CLEAN\clientes_clean.csv')
itens = pd.read_csv(f'DATA\CLEAN\itens_clean.csv')
produtos = pd.read_csv(f'DATA\CLEAN\produtos_clean.csv')
pedidos = pd.read_csv(f"DATA\RAW\pedidos.csv")

print(pedidos.head())
print(pedidos.info())
print(pedidos.isna().sum())



# para iniciar, preciso corrigir todos os valores que estão incorretos

######### CORRIGINDO AS DATAS

pedidos["data_pedido"] = pd.to_datetime(pedidos["data_pedido"], errors="coerce")
pedidos["data_pedido"] = pedidos["data_pedido"].dt.strftime('%d/%m/%Y')

# algumas datas ficaram nulas neste processo e precisarão ser apagadas

pedidos = pedidos.dropna(
    subset=["data_pedido"]
)

######### CORRIGINDO OS STATUS

pedidos["status"] = pedidos["status"].replace({
    "delivered" : "entregue"
})


pedidos["status"] = (
    pedidos["status"]
    .str.title()
    .str.strip()
)

######### VERIFICANDO SE DATA PEDIDO E DATA DE CADASTRO

# as datas dos pedidos não podem preceder as datas de cadastro dos clientes, para isso, preciso fazer uma checagem

comparacao = pedidos.merge(
    clientes[["id_cliente", "data_cadastro"]],
    on="id_cliente",
    how="left"
)

pedidos_invalidos = comparacao.loc[
    comparacao["data_pedido"] < comparacao["data_cadastro"],
    "id_cliente"
] 

pedidos.loc[
    pedidos["id_pedido"].isin(pedidos_invalidos),
    "data_pedido"
] = clientes["data_cadastro"]

# eu pensei em cancelar todos os pedidos que apresentassem data inferior a data de cadastro, mas isto resultou em muitas datas invalidas
# então decidi corrigir as datas dos pedidos para que ficassem equivalentes as datas dos cadastros de clientes

# precisei corrigir os valores na coluna id_pedido (sem repetição dos valores, pois id_pedido é uma PK(replace=False))
ids = itens["id_pedido"].unique()
pedidos = pedidos.head(len(ids)).copy()
pedidos["id_pedido"] = np.random.choice(ids, size=len(pedidos), replace=False)


# atualizar a lista de id cliente (com repetição dos valores, pois id_cliente é uma FK(replace=True))
pedidos["id_cliente"] = np.random.choice(clientes["id_cliente"], size=len(pedidos), replace=True)


pedidos.to_csv(
r"DATA\CLEAN\pedidos_clean.csv",
index=False,
encoding="utf-8-sig"
)