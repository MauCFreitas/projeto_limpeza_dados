##### DATA WRANGLING!

O objetivo deste projeto consiste em gerar, e trabalhar dados sujos, gerados aleatóriamente, para chegar em uma conclusão de analise

### Ferramentas

As ferramentas usadas serão:   
    - Microsoft Copilot: para a geração das tabelas aleatórias;  
    - Python: para o tratamento dos dados e automatização do serviço;   
    - PostgreSQL: para registrar as tabelas limpas e raceber os acessos;  
    - Excel: para criação de dashboards e apresentações sobre o projeto.  

### Geração dos dados

As tabelas foram geradas a partir do seguinte script gerado pelo Microsoft Copilot:  


[Gerador de Tabela](DATA/RAW/GERADOR%20DE%20TABELA%20RAW/generate_data.py)  

A partir deste código, 4 tabelas foram geradas:  
1- [Tabela clientes](DATA/RAW/clientes.csv) - Tabela que mostrava os registros de cadastros dos clientes desta suposta loja;  
2- [Tabela produtos](DATA/RAW/produtos.csv) - Tabela que represetava a disponibilidade de produtos cadastrados pela loja;  
3- [Tabela pedidos](DATA/RAW/pedidos.csv) - Tabela que relacionada a entrega dos pedidos que foram feitos;  
4- [Tabela pedidos](DATA/RAW/itens_pedido.csv) - Tabela que demonstrava os pedidos dos produtos cadastrados feitos pelos clientes cadastrados.  

### Correção das tabelas

Como as tabelas foram geradas por informações aleatórias, alguns dados ficaram desconexos do que eu precisava para montar uma analise. 
Além disso, alguns dados também não seguiam um padrão, o que poderia complicar uma futura analise em uma outra ferramenta.

Para organizar os dados, precisei usar basicamente a bibliotecas Pandas e Numpy para buscar padrões e fazer a leitura adequada destas tabelas.

Sendo assim, iniciei a organização destas informações em:  

## [Tabela Clientes](SRC/transform_clientes.py)  

Os dados nesta tabela eram referentes aos clientes cadastrados nesta loja, e se apresentava em 7 colunas, sendo elas: id_cliente, nome, email, cidade, estado, idade, data_cadastro.

Passo 1 - Remover cadastros duplicados:  
Ter mais de um cliente com o mesmo cadastro poderia atrapalhar minhas analises futuras, então não poderia deixar mais de um cliente com o mesmo ID, por exemplo.

Passo 2 - Tratamento da coluna idade:  
Como o código de geração me gerou dados de idade em formato float, que é um formato não apropriado para idade, fiz a correção para um formato int.
Além disso, como se tratava de cadastros de uma loja, decidi que só usaria os clientes que tivesse idade entre 18 e 100 anos.
Para não perder alguns cadastros, e como esta tabela é fictícia, decidi corrigir os valores nulos, que também foram anulados pelo tratamento anterior, e substitui os valores de idade nula pela média de idades dos clientes cadastrados com idades validas.

Passo 3 - Tratamento dos emails:  
Os emails precisavam ter um formato específico, então para manter os dados desta coluna adequados, eu usei uma função que reconhecia os padrões de formato de emails, e desconsiderei os cadastros que não tinham email adequado.

Passo 4 - Tratamento de cidades:  
No código de geração, o aleatorizador contava com uma problematização na digitação da cidade, que incluia abreviações, letras maiúsculas e minúsculas. 
Para resolver este problema, precisei usar um código que compreendesse as strings de forma adequada e convertesse os resultados da coluna em um formato padrão.
Também precisei limpar os cadastros que não possuiam atribuição para o valor cidade.

Passo 5 - Tratamento dos nomes:  
Assim como nas outras colunas, a falta de padrão nos nomes era um fator que atrapalhava esta coluna. Além destre problema, também tinha a questão de titulos pessoais, como "Sr.", "Sra.", "Dr.", "Dra." que precisavam ser removidos para não poluírem os dados.

Passo 6 - Remoção de colunas auxiliares:  
Durante os processos anteriores, algumas colunas e tabelas extras foram geradas, e precisavam ser removidas.

Passo 7 - Relatório de qualidade:  
Gerei um relatório de qualidade desta tabela para me ajudar a compreender quantos dos cadastros foram mantidos duante o processo de limpeza.

Passo 8 - Salvar tabela limpa:  
Com todos os erros resolvidos, só restava salvar a tabela na pasta da tabela clean.

------- Fim do tratamento dos dados desta tabela. -------

## [Tabela produtos](SRC/transform_produtos.py)  

Nesta tabela, os dados cadastrados se referiam aos produtos cadastrados na loja, e estavam separados em 4 colunas: id_produto, categoria, produto, preco.

Passo 1 - Reconhecimento dos dados e remoção das duplicatas:  
Apesar de não apresentar duplicatas de produtos, eu precisava reconhecer os dados que estavam presentes nesta tabela e como os erros poderiam se apresentar.

Passo 2 - Tratamento das categorias:  
Neste modelo de tabela, as categorias se demonstravam sem um padrão, algumas com erro de digitação, e outras sem padrão.
Para uma consulta futura, isto poderia atrapalhar o desenvolvimento da analise.

Passo 3 - Salvar tabela limpa:  
Como esta tabela apresentava poucas colunas, e os dados já estavam de certa forma, concisos e prontos para uso, considerei que todos os erros resolvidos, só restava salvar a tabela na pasta da tabela clean.

------- Fim do tratamento dos dados desta tabela. -------

## [Tabela itens](SRC/transform_itens.py)  

Esta era a primeira tabela que eu precisaria trabalhar os dados em conjunto com uma outra tabela trabalhada previamente, a tabela produtos_clean.
Nesta tabela, haviam 5 colunas: id_item, id_pedido, id_produto, quantidade, valor_unitario.

Passo 1 - Reconhecimento dos dados e remoção das duplicatas:  
Como já foi dito e feito antes, as tabelas não deveriam apresentar dados duplicados para não gerar erros na analise.

Passo 2 - Tratamento de quantidades:  
Esta coluna não poderia ser apresentada com valores negativos ou equivalentes a 0, pois indicaria que o pedido não havia sido realizado.

Passo 3 - Tratamento dos preços:  
Como a tabela foi gerada através do aleatório, eu precisava que os preços fossem equivalentes aos preços cadastrados na tabela de produtos, então fiz a correção desta coluna, importando os valores da outra tabela me baseando na coluna de id_produto.

Passo 4 - Criação da coluna valor_total:  
Enquanto tratava estes dados, decidi que ter mais uma coluna que apontava o valor total da compra poderia ser util para a analise, então incluí esta coluna.

Passo 5 - Salvar tabela limpa:  
Com os dados já tratados, agora era hora de salvar a tabela em formato clean.

------- Fim do tratamento dos dados desta tabela. -------

## [Tabela de pedidos](SRC/transform_pedidos.py)  

Esta tabela foi a ultima a ser tratada, pois precisaria que os dados batessem com todos os dados de todas as outras tabelas anteriores.
Ela apresentava 4 colunas: id_pedido, id_cliente, data_pedido, status.

Passo 1 - Tratamento de datas(1):  
Nesta tabela, eu não vi como problema haverem dados duplicados, pois era uma tabela para identificar o status dos pedidos, apenas.
Entretanto, encontrei um problema com a padronização do formato das datas.

Passo 2 - Tratamento dos status:  
Os status estavam cadastrados de formas variadas, sem um padrão, o que poderia atrapalhar nossas futuras analises.

Passo 3 - Tratamento de datas(2):  
Como a geração foi aleatória, as datas dos pedidos também estavam aleatórias. Então decidi fazer com que as datas dos pedidos feitos por clientes não fossem menores que as datas de cadastro destes mesmos clientes.
Sendo assim, quando a data_pedido era menor que a data_cadastro do cliente, a data_pedido se tornava igual a data_cadastro.

Passo 4 - Salvar tabela limpa:  
Com os dados já tratados, agora era hora de salvar a tabela em formato clean.

------- Fim do tratamento dos dados desta tabela. -------

### Criação das tabelas em formato SQL
As tabelas limpas ja estavam geradas, e agora eu precisava usar o PostgreSQL para cadastrar os dados destas tabelas.
Para isso, usei as bibliotecas Python sqlalchemy e psychopg para reconhecer a conexão com o SQL e cadastrar as tabelas as tabelas.  

[Importação das tabelas para o SQL](SRC/load_postgres.py)  

Mas este código não fará isto de uma forma descritiva. Então será necessário apontar para ele de forma posterior quais são as chaves primárias e chaves estrangeiras, por exemplo.  

Para isso, usei este comando

[Configuração das tabelas SQL](SQL/config_tables.sql)

Agora tenho as minhas tabelas configuradas, com as definições adequadas de PK e FK corrigidas. Além disso, também configurei os formatos dos dados de cada coluna das tabelas.  

### Criação das views
Antes de criar as views das tabelas SQL, preciso organizar meus pensamentos sobre quais tipos de analises eu preciso fazer. Para esta documentação, farei uma lista, que me auxiliará  com os próximos passos.  

## Objetivos da analise:
1) Analise de crescimento - Esta analise parte da pergunta inicial "estamos crescendo?" e tem como objetivo analisar, cronologicamente os status de entregas, com objetivo de compreender se a entrada de dinheiro foi superior aos meses anteriores;

2) Estudo dos clientes - Aqui a analise consistirá em avaliar os clientes que continuam comprando com esta loja com o objetivo de fidelizar os clientes e/ou encontrar o público alvo;

3) Estudo de produtos que mais vendem - Nesta analise, o objetivo agora é estudar como a loja é vista por seus clientes, através de uma analise dos produtos;

4) Operação dos pedidos - Por fim, irei avaliar como os pedidos se comportaram nestas tabelas.

## Analise exploratória de dados:
Com meus objetivos definidos, farei uma analise exploratória de dadospara compreender se eu alcançarei as respostas para estas perguntas.  

1) Analise de crescimento da loja:
Iniciei estas analises com a pergunta principal: "A loja está crescendo? Está obtendo mais lucros que antes?"  
Então eu inicio a analise com:  
[Analise exploratória](notebooks/analise_exploratoria.py)

[Analise de crescimento](NOTEBOOK/analise_exploratória/crescimento.py)

Com esta analise, pude avaliar, nos meses em que foram registrados pedidos, todo o faturamento de pedidos com status equivalente a 'Entregue'. Dessa forma, toda compra que estivesse concluída, estaria no meu calculo.

Ao separar os meses e realizar os somatórios, plotei um gráfico para uma melhor compreensão:  
<img src="DASHBOARD\IMAGENS\evolução faturamento mensal.png" alt="Evolução do Faturamento Mensal" width="300">  

E com isso, pude avaliar que houve sim um aumento do faturamento ao longo dos meses, principalmente após o mês de Outubro de 2024.

Decidi também plotar mais um gráfico que pudesse me mostrar valores referentes ao faturamento anual:  
<img src="DASHBOARD\IMAGENS\evolução faturamento anual.png" alt="Evolução do Faturamento Anual" width="300">  

E pude ver com mais clareza a curva crescente referente ao faturamento desta loja ao longo dos anos, de uma forma quase que exponencial.

2) Estudo dos clientes da loja:
Nesta analise, eu queria identificar quem é o publico que mais compra nessa loja, separando eles por: idade e região(cidade), que foram os dados cadastrados nas tabelas.

[Analise dos clientes](NOTEBOOK/analise_exploratória/clientes.py)

Foi realizado também um teste de assimetria para identificar qual o melhor valor a ser avaliado, a média ou a mediana dos valores de idade. Por apresentar um valor dentro do intervalo [-1, 1] (valor apresentado equivalente a -0,13), a média de idade se tornou um valor confiavel.

Sendo assim, avaliei e calculei a idade média, a moda e a mediana dentre clientes que registraram pedidos nesta loja, e assim, eu poderia identificar a idade do público alvo.  

<img src="DASHBOARD\IMAGENS\distribuição idade clientes.png" alt="Distribuição da Idade dos clientes da Loja" width="300">  

E com este estudo, pude notar que a média de idade dos clientes desta loja é de 45 anos, e portanto, o público alvo se enquadraria nesta faixa de idade.

Agora, ao tratar da cidade, precisei compreender quais eram as cidades que apareciam de forma mais recorrente dentre os pedidos feitos. E pude plotar este gráfico, que apontava as 5 cidades mais comuns na minha lista:  

<img src="DASHBOARD\IMAGENS\5 cidades com mais clientes.png" alt="TOP 5 Cidades Compradoras" width="300">  

Nesta avaliação, percebi que Salvador, Belo Horizonte, Porto Alegre, Recife e Curitiba eram as cidades que mais compravam na loja.

Além destas avaliações, também precisei avaliar os clientes que faziam a recompra e os clientes que compravam apenas 1x na loja.

[Analise de recompra](NOTEBOOK/analise_exploratória/recompra.py)

A partir deste script, pude compreender melhor quem eram os clientes fidelizados desta loja, aqueles que compravam os produtos com frequencia.

Após essa avaliação, encontrei os valores:  

<img src="DASHBOARD\IMAGENS\taxa de recompra.png" alt="Taxa de Recompra/compra unitária" width="300">  

E com estes dados, pude perceber que para esta loja fictícia, que os dados foram gerados aleatóriamente, a recompra era muito mais alta que o esperado, e reprensetava um valor acima de 99% das compras.

Mesmo com este valor irreal, decidi seguir minha analise, para ver até onde poderia chegar, e calculei também o tempo que levava para um cliente, que ja realizou uma compra, fazer a recompra na mesma loja:  

<img src="DASHBOARD\IMAGENS\distribuição tempo de recompra.png" alt="Tempo para realizar recompra" width="300">  

com a analise ralizada, pude concluir que o tempo médio para recompra dos clientes desta loja era de aproximadamente 110 dias após a compra anterior.

3) Analise de quais categorias mais saem:
Aqui, o objetivo era entender quais as categorias estão mais presentes nos pedidos feitos pelos clientes.

[Analise de categorias](NOTEBOOK/analise_exploratória/categorias.py)

Sendo assim, foi necessário organizar um ranking para esta avaliação:

<img src="DASHBOARD\IMAGENS\ranking de saída de categorias.png" alt="Ranking de saída de categorias" width="300">  

Pude observar que existe sim uma categoria que destoa dentre as outras é a categoria de produtos Eletrônicos, tendo uma faixa de saída equivalente a:  

<img src="DASHBOARD\IMAGENS\porcentagem de saída de categorias.png" alt="Porcentagem de saída de categorias" width="300">  

Também foi avaliado nesta analise, a taxa de saída de cada categoria de produto por mês, separando a categoria que lidera o ranking e a categoria que fica em segundo lugar.  

<img src="DASHBOARD\IMAGENS\principais categorias vendidas no mes.png" alt="Principais categorias vendidas no mes" width="300">  

E com esta tabela, pude perceber que a categoria de Eletrônicos domina as vendas na maioria dos meses, e é seguido pela categoria Casa, que alcança o segundo lugar em vendas entre as categorias na maioria dos meses.

4) Operação dos pedidos:
Nesta última analise, o objetivo foi encontrar um padrão entre os pedidos, para tentar compreender como os clientes pensam ao realizarem os pedidos. Para isso, será avaliado a quantidade média de produtos por pedido, e o valor médio dos pedidos.

[Analise de pedidos](NOTEBOOK/analise_exploratória/operacao.py)

A analise retornou uma média de 5 itens por pedido, com uma média de R$ 13.743,37 por pedido.

