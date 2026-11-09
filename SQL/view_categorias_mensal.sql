-- Active: 1792696188799@@127.0.0.1@5432@analise_vendas
CREATE OR REPLACE VIEW vw_categorias_mensal AS
SELECT 
    pr.categoria,
    EXTRACT(YEAR FROM p.data_pedido::DATE) AS ano,
    EXTRACT(MONTH FROM p.data_pedido::DATE) AS mes,
    SUM(i.quantidade) AS qtd_itens_vendidos,
    SUM(i.valor_total) AS faturamento
FROM itens_sql i 
JOIN produtos_sql pr ON i.id_produto = pr.id_produto
JOIN pedidos_sql p ON i.id_pedido = p.id_pedido
GROUP BY EXTRACT(YEAR FROM p.data_pedido::DATE), EXTRACT(MONTH FROM p.data_pedido::DATE), pr.categoria
ORDER BY ano, mes, faturamento DESC;