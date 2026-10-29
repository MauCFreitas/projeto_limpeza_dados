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


[Gerador de Tabela](projeto_limpeza_dados/DATA/RAW/GERADOR%20DE%20TABELAS/generate_data.py)  

A partir deste código, 4 tabelas foram geradas:  
1- [Tabela clientes](projeto_limpeza_dados/DATA/RAW/clientes.csv) - Tabela que mostrava os registros de cadastros dos clientes desta suposta loja;  
2- [Tabela produtos](projeto_limpeza_dados/DATA/RAW/produtos.csv) - Tabela que represetava a disponibilidade de produtos cadastrados pela loja;  
3- [Tabela pedidos](projeto_limpeza_dados/DATA/RAW/pedidos.csv) - Tabela que relacionada a entrega dos pedidos que foram feitos;  
4- [Tabela pedidos](projeto_limpeza_dados/DATA/RAW/itens_pedido.csv) - Tabela que demonstrava os pedidos dos produtos cadastrados feitos pelos clientes cadastrados.  

### Correção das tabelas

Como as tabelas foram geradas por informações aleatórias, alguns dados ficaram desconexos do que eu precisava para montar uma analise. 
Além disso, alguns dados também não seguiam um padrão, o que poderia complicar uma futura analise em uma outra ferramenta.

Para organizar os dados, precisei usar basicamente a bibliotecas Pandas e Numpy para buscar padrões e fazer a leitura adequada destas tabelas.

Sendo assim, iniciei a organização destas informações em:  

## [Tabela Clientes](projeto_limpeza_dados/SRC/transform_clientes.py)  

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

## [Tabela produtos](projeto_limpeza_dados/SRC/transform_produtos.py)  

Nesta tabela, os dados cadastrados se referiam aos produtos cadastrados na loja, e estavam separados em 4 colunas: id_produto, categoria, produto, preco.

Passo 1 - Reconhecimento dos dados e remoção das duplicatas:  
Apesar de não apresentar duplicatas de produtos, eu precisava reconhecer os dados que estavam presentes nesta tabela e como os erros poderiam se apresentar.

Passo 2 - Tratamento das categorias:  
Neste modelo de tabela, as categorias se demonstravam sem um padrão, algumas com erro de digitação, e outras sem padrão.
Para uma consulta futura, isto poderia atrapalhar o desenvolvimento da analise.

Passo 3 - Salvar tabela limpa:  
Como esta tabela apresentava poucas colunas, e os dados já estavam de certa forma, concisos e prontos para uso, considerei que todos os erros resolvidos, só restava salvar a tabela na pasta da tabela clean.

------- Fim do tratamento dos dados desta tabela. -------

## [Tabela itens](projeto_limpeza_dados/SRC/transform_itens.py)  

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

## [Tabela de pedidos](projeto_limpeza_dados/SRC/transform_pedidos.py)  

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

[Importação das tabelas para o SQL](projeto_limpeza_dados/SRC/load_postgres.py)  

Mas este código não fará isto de uma forma descritiva. Então será necessário apontar para ele de forma posterior quais são as chaves primárias e chaves estrangeiras, por exemplo.  

Para isso, usei este comando

[Configuração das tabelas SQL](projeto_limpeza_dados/SQL/config_tables.sql)

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

Então eu inicio a analise com:  
[Analise exploratória](projeto_limpeza_dados/notebooks/analise_exploratoria.py)


