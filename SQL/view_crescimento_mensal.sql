-- Active: 1792696188799@@127.0.0.1@5432@analise_vendas
CREATE OR REPLACE VIEW vw_crescimento_mensal AS
SELECT 
    EXTRACT(YEAR FROM p.data_pedido) AS ano,
    EXTRACT(MONTH FROM p.data_pedido) AS mes,
    COUNT(DISTINCT p.id_pedido) AS qtd_pedidos,
    SUM(i.valor_total) AS faturamento
FROM pedidos_sql p
JOIN itens_sql i ON p.id_pedido = i.id_pedido
WHERE p.status = 'Entregue'
GROUP BY EXTRACT(YEAR FROM p.data_pedido), EXTRACT(MONTH FROM p.data_pedido)
ORDER BY ano, mes;