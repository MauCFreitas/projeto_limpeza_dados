import pandas as pd
import numpy as np
import re

itens = pd.read_csv(f'DATA\RAW\itens_pedido.csv')
produtos = pd.read_csv(f'DATA\CLEAN\produtos_clean.csv')
pedidos = pd.read_csv(f'DATA\RAW\pedidos.csv')

# após corrigir problemas da tabela de produtos, vou utiliza-la para arrumar as inconsistencias da tabela de pedidos
# uma vez que precisarei usar valores atualizados da tabela produtos para corrigir alguns valores na tabela de pedidos

# assim como nas tabelas de clientes e produtos, preciso compreender o que ha de errado com esta tabela, e ja remover os itens duplicados

print(itens.head())
print(itens.info())
print(itens.isna().sum())
itens_antes = len(itens)
itens = itens.drop_duplicates()
duplicados_removidos = itens_antes - len(itens)

# além disso, quero remover os pedidos que tiveram erros e que a quantidade foi 0 ou inferior

itens = itens[itens["quantidade"] > 0]

# considerando que as tabelas foram geradas aleatóriamente, e que as tabelas não apresentam relação, encontrei uma inconsistencia relacional em relação aos pedidos e aos produtos em relação ao preço
# para que eu siga o trabalho nestas tabelas, precisarei corrigir os valores para conseguir fazer uma comparação adequada no futuro

itens_validos = itens[itens["id_produto"].isin(produtos["id_produto"])]
print( f'estes são os itens validos {itens_validos}')
itens = itens[itens["id_produto"].isin(produtos["id_produto"])]

itens = itens.merge(
    produtos[["id_produto", "preco"]],
    on="id_produto",
    how="left"
)

itens["valor_unitario"] = itens["preco"]

# agora os valores dos produtos na tabela de pedidos estão compatíveis com os preços dos produtos na tabela de produtos

# quero adicionar mais uma coluna a tabela para avaliar o valor total das compras efetuadas

itens["valor_total"] = itens["valor_unitario"] * itens["quantidade"]


itens = itens.drop(columns="preco")
print(itens.head(15))




itens.to_csv(
r"DATA\CLEAN\itens_clean.csv",
index=False,
encoding="utf-8-sig"
)