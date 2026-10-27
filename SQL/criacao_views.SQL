-- view união completa
CREATE VIEW vw_vendas_completa AS SELECT
    p.id_pedido,
    p.status AS status_pedido,
    c.id_cliente,
    c.nome AS nome_cliente,
    c.cidade,
    c.estado,
    pr.id_produto AS nome_produto,
    pr.categoria,
    i.quantidade,
    pr.preco AS valor_unitario,
    i.valor_total
FROM itens_sql i, clientes_sql c, produtos_sql pr, pedidos_sql p
JOIN pedidos_sql ON i.id_pedido = i.id_pedido
JOIN clientes_sql c ON p.id_cliente = c.id_cliente
JOIN produtos_sql pr ON i.id_produto = pr.id_produto;