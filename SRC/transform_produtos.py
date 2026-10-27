import pandas as pd
import numpy as np
import re

produtos = pd.read_csv(f'DATA\RAW\produtos.csv')

# como foi feito com a tabela de clientes, iniciarei tentando compreender o que havia de errado com esta tabela

print(produtos.head())
print(produtos.info())
print(produtos.isna().sum())

# além destas analises, preciso reconhecer se os valores dos produtos estão com valores negativos e as duplicatas

print(produtos[produtos["preco"] <= 0].shape[0])
produtos = produtos.drop_duplicates()

# um dos erros notados nesta tabela foi a falta de padrão na escrita

produtos["categoria"] = (
    produtos["categoria"]
    .str.title()
    .str.strip()
)

produtos["categoria"] = produtos["categoria"].replace({
    "Cas" : "Casa",
    "Eletrônico" : "Eletrônicos",
    "Livro" : "Livros"
})


print(produtos.head(49))


# agora com a correção de todos os erros, hora de salvar a nova tabela

produtos.to_csv(
r"projeto_limpeza_dados\DATA\CLEAN\produtos_clean.csv",
index=False,
encoding="utf-8-sig"
)