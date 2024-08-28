# TESTE PRÁTICO - ANALISTA DE INFRAESTRUTURA

### Apresentação
> Olá, seja bem vindo ao teste de analista de infraestrutura. Vou realizar a apresentação de todo o processo seguindo as partes solicitadas na documentação enviada.

## PARTE 1 - Construção de imagens de containers
> Na parte de construção da imagem, eu inicialmente instalei e rodei a aplicação em minha máquina, para entender os requisitos e como, de maneira geral, a aplicação funcionava, e nesse ponto identifiquei a necessidade de um servidor MySQL para efetuar a migration dos dados. O servidor foi instalado em minha máquina para os testes iniciais.

### Explicando o Dockerfile
O Dockerfile foi criado com base na análise préviamente explicada, todas as linhas foram devidamente comentadas, facilitando o entendimento:

[![Dockerfile](images/dockerfile.png?raw=true)](images/dockerfile.png)

A partir daí, basta fazer o buil da imagem, utilizando o Dockerfile acima. Rodando o comando:
`docker build -t cesarbgoncalves/infra-challenge:1.0.0 .`

com o build pronto, basta rodar o docker com as configurações de banco, dependência importante para a aplicação funcionar corretamente:
``` shell
docker run --rm -it -p 8000:8000 \
-e DB_HOST=172.17.0.1 \
-e DB_PORT=3306 \
-e DB_DATABASE=challenge \
-e DB_USERNAME=root \
-e DB_PASSWORD=debian \
cesarbgoncalves/infra-challenge:1.0.0
```
