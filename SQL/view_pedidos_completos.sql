CREATE OR REPLACE VIEW vw_pedidos_completos AS
SELECT 
    p.id_pedido,
    p.id_cliente,
    p.data_pedido,
    p.status,
    COALESCE(SUM(i.valor_total), 0) AS valor_total_pedido,
    COUNT(i.id_item) AS qtd_itens,
    COALESCE(SUM(i.quantidade), 0) AS qtd_unidades
FROM 
    pedidos_sql p
LEFT JOIN 
    itens_sql i ON p.id_pedido = i.id_pedido
GROUP BY 
    p.id_pedido, p.id_cliente, p.data_pedido, p.status;