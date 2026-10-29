import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
from pathlib import Path

# ----------------------------------
# Configuração
# ----------------------------------

fake = Faker("pt_BR")
np.random.seed(42)
random.seed(42)

N_CLIENTES = 1000
N_PRODUTOS = 50
N_PEDIDOS = 10000
N_ITENS = 30000

Path("data").mkdir(exist_ok=True)

# ----------------------------------
# CLIENTES
# ----------------------------------

clientes = []

cidades = [
    "Rio de Janeiro",
    "São Paulo",
    "Belo Horizonte",
    "Curitiba",
    "Porto Alegre",
    "Salvador",
    "Recife",
    "Fortaleza"
]

for i in range(1, N_CLIENTES + 1):

    cidade = random.choice(cidades)

    # inconsistências de cidade
    if random.random() < 0.10:
        cidade = random.choice([
            cidade.lower(),
            cidade.upper(),
            cidade.replace("São", "S."),
            cidade.replace("Rio de Janeiro", "RJ")
        ])

    email = fake.email()

    # emails inválidos
    if random.random() < 0.05:
        email = random.choice([
            email.replace("@", ""),
            email.replace(".com", ""),
            email.replace("@", "@@")
        ])

    idade = random.randint(18, 70)

    # idades inválidas
    if random.random() < 0.02:
        idade = random.choice([-10, 150, 999])

    cliente = {
        "id_cliente": i,
        "nome": fake.name(),
        "email": email,
        "cidade": cidade,
        "estado": fake.estado_sigla(),
        "idade": idade,
        "data_cadastro": fake.date_between(
            start_date="-5y",
            end_date="today"
        )
    }

    clientes.append(cliente)

clientes = pd.DataFrame(clientes)

# nulos
for col in ["email", "cidade", "idade"]:
    mask = np.random.rand(len(clientes)) < 0.08
    clientes.loc[mask, col] = np.nan

# duplicados
duplicados = clientes.sample(frac=0.05)
clientes = pd.concat([clientes, duplicados], ignore_index=True)

clientes.to_csv(
    "data/clientes.csv",
    index=False,
    encoding="utf-8-sig"
)

# ----------------------------------
# PRODUTOS
# ----------------------------------

categorias = [
    "Eletrônicos",
    "Casa",
    "Esporte",
    "Livros",
    "Informática"
]

produtos = []

for i in range(1, N_PRODUTOS + 1):

    categoria = random.choice(categorias)

    # categorias inconsistentes
    if random.random() < 0.10:
        categoria = random.choice([
            categoria.lower(),
            categoria.upper(),
            categoria[:-1]
        ])

    preco = round(random.uniform(10, 5000), 2)

    # preço inválido
    if random.random() < 0.02:
        preco = random.choice([0, -100, -500])

    produtos.append({
        "id_produto": i,
        "categoria": categoria,
        "produto": f"Produto {i}",
        "preco": preco
    })

produtos = pd.DataFrame(produtos)

produtos.to_csv(
    "data/produtos.csv",
    index=False,
    encoding="utf-8-sig"
)

# ----------------------------------
# PEDIDOS
# ----------------------------------

status_validos = [
    "Entregue",
    "Cancelado",
    "Em Transporte"
]

pedidos = []

for i in range(1, N_PEDIDOS + 1):

    status = random.choice(status_validos)

    # status inconsistentes
    if random.random() < 0.10:
        status = random.choice([
            status.lower(),
            status.upper(),
            "delivered"
        ])

    cliente = random.randint(1, N_CLIENTES)

    # chave inválida
    if random.random() < 0.03:
        cliente = 999999

    data_pedido = fake.date_between(
        start_date="-2y",
        end_date="today"
    )

    pedidos.append({
        "id_pedido": i,
        "id_cliente": cliente,
        "data_pedido": data_pedido,
        "status": status
    })

pedidos = pd.DataFrame(pedidos)

# datas inválidas
mask = np.random.rand(len(pedidos)) < 0.02

datas_invalidas = [
    "32/01/2024",
    "2024-15-01",
    "99/99/9999"
]

pedidos.loc[mask, "data_pedido"] = np.random.choice(
    datas_invalidas,
    mask.sum()
)

pedidos.to_csv(
    "data/pedidos.csv",
    index=False,
    encoding="utf-8-sig"
)

# ----------------------------------
# ITENS PEDIDO
# ----------------------------------

itens = []

for i in range(1, N_ITENS + 1):

    pedido_id = random.randint(1, N_PEDIDOS)
    produto_id = random.randint(1, N_PRODUTOS)

    # chave inválida
    if random.random() < 0.03:
        produto_id = 99999

    quantidade = random.randint(1, 10)

    # quantidade inválida
    if random.random() < 0.02:
        quantidade = random.choice([0, -2, -10])

    valor = round(random.uniform(10, 5000), 2)

    itens.append({
        "id_item": i,
        "id_pedido": pedido_id,
        "id_produto": produto_id,
        "quantidade": quantidade,
        "valor_unitario": valor
    })

itens = pd.DataFrame(itens)

itens.to_csv(
    "data/itens_pedido.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Arquivos gerados com sucesso!")