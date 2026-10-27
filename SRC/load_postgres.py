from sqlalchemy import create_engine
import pandas as pd


clientes = pd.read_csv(f'DATA\CLEAN\clientes_clean.csv')
itens = pd.read_csv(f'DATA\CLEAN\itens_clean.csv')
produtos = pd.read_csv(f'DATA\CLEAN\produtos_clean.csv')
pedidos = pd.read_csv(f"DATA\CLEAN\pedidos_clean.csv")

engine = create_engine(
    "postgresql+psycopg://postgres:@127.0.0.1:5432/analise_vendas"
)

clientes.to_sql(
    name="clientes_sql",
    con=engine,
    if_exists="replace",
    index=False
)

itens.to_sql(
    name="itens_sql",
    con=engine,
    if_exists="replace",
    index=False
)

pedidos.to_sql(
    name="pedidos_sql",
    con=engine,
    if_exists="replace",
    index=False
)

produtos.to_sql(
    name="produtos_sql",
    con=engine,
    if_exists="replace",
    index=False
)


