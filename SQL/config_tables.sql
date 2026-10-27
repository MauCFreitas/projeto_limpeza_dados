-- tabela clientes
-- pk
ALTER TABLE clientes_sql
ADD CONSTRAINT pk_cliente PRIMARY KEY (id_cliente);
-- configurando valores para as outras colunas da tabela clientes
ALTER TABLE clientes_sql
    ALTER COLUMN id_cliente TYPE INTEGER USING id_cliente::INTEGER,
    ALTER COLUMN nome TYPE VARCHAR(100) USING nome::VARCHAR(100),
    ALTER COLUMN email TYPE VARCHAR(254) USING email::VARCHAR(254),
    ALTER COLUMN cidade TYPE VARCHAR(100) USING cidade::VARCHAR(100),
    ALTER COLUMN estado TYPE VARCHAR(2) USING estado::VARCHAR(2),
    ALTER COLUMN idade TYPE INTEGER USING idade::INTEGER,
    ALTER COLUMN data_cadastro TYPE VARCHAR(20) USING data_cadastro::VARCHAR(20);


-- tabela produtos
-- pk
ALTER TABLE produtos_sql
ADD CONSTRAINT pk_produto PRIMARY KEY (id_produto);
-- configurando valores para as outras colunas da tabela produtos
ALTER TABLE produtos_sql
    ALTER COLUMN id_produto TYPE INT USING id_produto::INT,
    ALTER COLUMN categoria TYPE VARCHAR(50) USING categoria::VARCHAR(50),
    ALTER COLUMN produto TYPE VARCHAR(30) USING produto::VARCHAR(30),
    ALTER COLUMN preco TYPE DECIMAL(20, 2) USING preco::DECIMAL(20, 2);


-- tabela itens
-- pk
ALTER TABLE itens_sql 
ADD CONSTRAINT pk_itens PRIMARY KEY (id_item);
--configurando valores para as outras colunas da tabela itens
ALTER TABLE itens_sql
    ALTER COLUMN id_item TYPE INT USING id_item::INT,
    ALTER COLUMN id_pedido TYPE INT USING id_pedido::INT,
    ALTER COLUMN id_produto TYPE INT USING id_produto::INT,
    ALTER COLUMN quantidade TYPE INT USING quantidade::INT,
    ALTER COLUMN valor_unitario TYPE INT USING valor_unitario::INT,
    ALTER COLUMN valor_total TYPE INT USING valor_total::INT;
-- fk
ALTER TABLE itens_sql
ADD CONSTRAINT fk_itens_pedidos
FOREIGN KEY (id_pedido) REFERENCES pedidos_sql(id_pedido)
ON DELETE CASCADE;


-- tabela pedidos
-- pk
ALTER TABLE pedidos_sql
ADD CONSTRAINT pk_pedido PRIMARY KEY (id_pedido);
ALTER TABLE pedidos_sql
    ALTER COLUMN id_pedido TYPE INT USING id_pedido::INT,
    ALTER COLUMN id_cliente TYPE INT USING id_cliente::INT,
    ALTER COLUMN data_pedido TYPE VARCHAR(20) USING data_pedido::VARCHAR(20),
    ALTER COLUMN status TYPE VARCHAR(50) USING status::VARCHAR(50);
-- fk
ALTER TABLE pedidos_sql
ADD CONSTRAINT fk_pedidos_clientes
FOREIGN KEY (id_cliente) REFERENCES clientes_sql(id_cliente)
ON DELETE CASCADE;


