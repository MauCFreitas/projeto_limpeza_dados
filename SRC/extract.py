import pandas as pd


# clientes = pd.read_csv(f'projeto_limpeza_dados\DATA\RAW\clientes.csv')
# itens = pd.read_csv(f'projeto_limpeza_dados\DATA\RAW\clientes.csv')
# pedidos =  pd.read_csv(f'projeto_limpeza_dados\DATA\RAW\clientes.csv')
# produtos =  pd.read_csv(f'projeto_limpeza_dados\DATA\RAW\clientes.csv')

pedidos = pd.read_csv(f'DATA\CLEAN\pedidos_clean.csv')

duplicados = pedidos[pedidos.duplicated(subset=['id_pedido'], keep=False)]
print(duplicados)