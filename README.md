# chilli_report

O intuito deste código é gerar um relatório diário para monitorar acessos do [Hotel Chilli](https://www.hotelchilli.com.br/), que possui, em seu site, um contador de usuários do Hotel.

Todo o projeto é uma piada, mas serve para estudar tópicos como:

- Web Scrapping
- Doploy de aplicações em um ambiente serverless
- Construção de uma API REST para acesso de um banco de dados na nuvem
- Construção de relatórios automatizados e dashboards usando Python

## As etapas do projeto consistem em:

1) [X] Criar uma função lambda ativada de 5 em 5 minutos para coletar dados
2) [X] Criar um banco de dados no qual os dados são depositados
3) [X] Criar um interpretador dos dados
4) [X] Criar um dashboard para apresentação dos dados
5) [X] Criar uma API para automatizar a comunicação entre o ambiente de trabalho e a base de dados
6) [ ] Melhorar o Relatório com análise de projeção de clientes para cada dia mês

## Coisas a se fazer, ainda

- [ ] Alterar a função lambda para excluir o dado mais antigo da base de dados, sempre que um dado novo for inputado
- [ ] Esperar a base crescer o suficiente para estimarmos efeitos de feriados
- [ ] Analisar o crescimento da base de clientes ao longo do tempo