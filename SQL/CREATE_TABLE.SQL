-- Active: 1792696188799@@127.0.0.1@5432@analise_vendas
CREATE TABLE ITENS (
    id_item INT PRIMARY KEY,
    id_pedido INT,
    id_produto INT,
    quantidade INT,
    valor_unitario INT,
    valor_total INT
);