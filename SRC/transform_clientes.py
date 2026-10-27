import pandas as pd
import numpy as np
import re

clientes = pd.read_csv(f'DATA\RAW\clientes.csv')

# para compreender exatamente o que esta acontecendo de errado com a tabela:

print(clientes.head())
print(clientes.info())
print(clientes.isna().sum())

# então existem 83 erros na coluna de emails, 88 erros na coluna de cidades e 100 erros na coluna de idade relacionados a valor em branco

# agora precisamos verificar se há cadastros duplicados

clientes_antes = len(clientes)
clientes = clientes.drop_duplicates()
duplicados_removidos = clientes_antes - len(clientes)

# com esta verificação 50 cadastros foram removidos


######### TRATAMENTO DE IDADE:
# apenas clientes com idade entre 18 e 100 continuarão cadastrados

clientes[
    (clientes["idade"] < 18)
    | (clientes["idade"] > 100)
]

# para não atrapalhar a analise de dados, substituirei idades nulas pela média das outras idades

clientes.loc[
    (clientes["idade"] < 18)
    | (clientes["idade"] > 100),
    "idade"
] = np.nan

clientes["idade"] = clientes["idade"].fillna(
    clientes["idade"].median()
)

# as idades ficaram em formato float, e idade não se mede assim. por isso irei substituir o formato para int

clientes["idade"] = clientes["idade"].astype(int)
######### TRATAMENTO DAS DATAS:

# primeiro eu preciso padronizar o formato das datas quanto ao texto, logo em seguida, irei organizar a ordem dos detalhes
clientes["data_cadastro"] = pd.to_datetime(clientes["data_cadastro"], errors="coerce")
clientes["data_cadastro"] = clientes["data_cadastro"].dt.strftime('%d/%m/%Y')

######### TRATAMENTO DOS EMAILS:

# neste momento precisamos invalidar os emails que não estão adequados

def validar_email(email):
    if pd.isna(email):
        return False
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return bool(re.match(padrao, str(email)))

clientes["email_valido"] = clientes["email"].apply(validar_email)


clientes.loc[
    clientes["email_valido"] == False,
    "email"
] = np.nan

clientes = clientes.dropna(
    subset=["email"]
)


######### TRATAMENTO DAS CIDADES:

clientes["cidade"] = clientes["cidade"].astype(str)

clientes["cidade"] = (
    clientes["cidade"]
    .str.upper()
    .str.strip()
)

clientes["cidade"] = clientes["cidade"].replace({
    "RJ": "RIO DE JANEIRO",
    "RIO JANEIRO": "RIO DE JANEIRO",
    "S. PAULO": "SAO PAULO",
    "SAO PAULO": "SAO PAULO"
})

# para os cadastros com cidade em branco, selecionarei a moda (valor mais comum) das cidades para substituir 

cidade_mais_comum = clientes["cidade"].mode()[0]

clientes["cidade"] = clientes["cidade"].fillna(
    cidade_mais_comum
)

# com isso, limpamos todos os cadastros com valores vazios

######### TRATAMENTO DOS NOMES:

# apesar dos nomes não estarem em branco, eles não seguem um padrão

clientes["nome"] = (
    clientes["nome"]
    .str.title()
    .str.strip()
)

# agora todos os nomes iniciam com letra maiúscula e seguem em letras minusculas

# mas ainda tem um problema de cadastro em clientes que cadastraram um titulo prévio ao nome (Sr., Dr., Sra., Dra., Srta.)
clientes["nome"] = clientes["nome"].str.replace(
    r"^(Sr\.|Dr\.|Sra\.|Dra\.|Srta\.)\s*",
    "",
    regex=True
)

######### REMOVER COLUNAS AUXILIARES

# enquanto o tratamento foi produzido, colunas auxiliares foram adicionadas. agora é o momento de remove-las para não atrapalhar a leitura

clientes = clientes.drop(
    columns=["email_valido"]
)


######### RELATÓRIO DE QUALIDADE

quality_report = {
    "total_registros": len(clientes), \
    "emails_nulos": clientes["email"].isna().sum(), \
    "cidades_nulas": clientes["cidade"].isna().sum(), \
    "idade_nulas": clientes["idade"].isna().sum()
}

print(quality_report)

######### SALVANDO A TABELA LIMPA

# clientes.to_csv(
# r"projeto_limpeza_dados\DATA\CLEAN\clientes_clean.csv",
# index=False,
# encoding="utf-8-sig"
# )