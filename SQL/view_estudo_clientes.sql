-- Active: 1792696188799@@127.0.0.1@5432@analise_vendas
CREATE OR REPLACE VIEW vw_estudo_clientes AS
SELECT 
    c.id_cliente,
    c.idade,
    c.cidade,
    COUNT(DISTINCT p.id_pedido) AS total_pedidos,
    SUM(i.valor_total) AS total_gasto,
    MIN(p.data_pedido::DATE) AS primeira_compra,
    MAX(p.data_pedido::DATE) AS ultima_compra
FROM clientes_sql c
LEFT JOIN pedidos_sql p ON c.id_cliente = p.id_cliente
LEFT JOIN itens_sql i ON p.id_pedido = i.id_pedido
GROUP BY c.id_cliente, c.idade, c.cidade;
