# TESTE PRÁTICO - ANALISTA DE INFRAESTRUTURA

### Apresentação
Olá, seja bem vindo ao teste de analista de infraestrutura. Vou realizar a apresentação de todo o processo seguindo as partes solicitadas na documentação enviada.

## PARTE 1 - Construção de imagens de containers
Na parte de construção da imagem, eu inicialmente instalei e rodei a aplicação em minha máquina, para entender os requisitos e como, de maneira geral, a aplicação funcionava, e nesse ponto identifiquei a necessidade de um servidor MySQL para efetuar a migration dos dados. O servidor foi instalado em minha máquina para os testes iniciais.

### Explicando o Dockerfile
O Dockerfile foi criado com base na análise préviamente explicada, todas as linhas foram devidamente comentadas, facilitando o entendimento:

[![Dockerfile](images/dockerfile.png?raw=true)](Dockerfile)

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

## PARTE 2 - Orquestração de Containers
Na segunda parte, é o momento onde mais gosto de atuar, pois entendo que o Kubernetes revolucionou o modo de gerenciamento de containers.

Realizei a criação dos manifestos abaixo:

```
├── app
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── namespace.yaml
│   ├── secrets.yaml
│   └── service.yaml
└── bd
    ├── namespace.yaml
    ├── secrets.yaml
    ├── service.yaml
    ├── statefulset.yaml
    └── volumes.yaml

```
Como o banco de dados é uma dependência importante para o funcionamento da aplicação, resolvi também criar os artefatos para ele.
Explicando melhor:

- **configmap**: Arquivo importante para fazer o mapeamento dos dados de configuração para a aplicação, resolvi adicionar apenas o endereço do serviço responsável por expor internamente o pod de banco de dados (StateFulSet)
- **deployment**: É o principal arquivo de manifesto do Kubernetes, pois ele é responsável pela criação da aplicação em si, bem como suas configurações. Adicionei nesse arquivo também as configurações de recursos de memória e cpu.
- **namespace**: Artefato que realiza a criação do namespace que irá acoplar em um ambiente isolado os dois serviços (aplicação e banco de dados).
- **secrets**: Para este projeto, criei um secrets para armazenar as informações sigilosas de banco. Lembrando que especificamente para este projeto utilizei os secrets dessa maneira. Existem muitas outras maneiras mais seguras de realizar este processo, como a utilização do Vault ou mesmo através do armazenamento de segredos em pipelines do Github ou Jenkins.
- **service**: Para o reconhecimento e comunicação entre os dois pods faz-se necessário a utilização de um serviço, que posteriormente poderá ser utilizado através de um LoadBalancer (ALB ou ELB, da AWS, como exemplo).
- **statefulset**: Criei o banco de dados como statefulset para manter os dados de banco persistentes, no caso de haver algum problema com o pod, ou mesmo em sua reinicialização, os dados fiquem seguros em um volume próprio.
- **volumes**: E por último, porém não menos importante, criei o PVC para acoplar o volume ao pod, mantendo assim a persistência de dados.

**Obs.:**: Como primeiro projeto, criei esses artefatos para deixar a aplicação funcionando, porém reitero a necessidade de análise de um ambiente onde haja outras formas de melhoria, como a utilização do Helm, do Vault, e limitação de utilização por parte dos usuários do Kubernetes e a criação de usuários de serviço internos do kubernetes (SA). Com isso, a melhoria contínua dos processos e políticas de segurança, trariam mais estabilidade e segurança à aplicação.


## PARTE 3 - Pipeline de integração contínua e entrega contínua (CI/CD)
Para a integração de novas funcionalidades e entrega contínua da aplicação, faz-se necessária a implantação de um pipeline. Apostando na robustez e na versatilidade do Jenkins, eu criaria um pipeline através dele, seguindo os passos:
- **Build**: para a criação e manutenção dos arquivos necessários para o funcionamento da aplicação
- **Testes**: Toda aplicação precisa passar por uma esteira de testes, a fim de verificar a possibilidade de melhoria, aproveitamento de código e análise de vulnerabilidades. O Sonar Qube é uma das melhores ferramentas para isso, e tem uma boa integração com o Jenkins.
- **deploy**: O deploy precisa ser rápido e a prova de falhas, em todos os ambientes (DEV, QA e PROD), agilizando todo o processo de melhoria e resolução de bugs.
- **Notificação**: Todo o processo da esteira, precisa ser notificado, seja para os desenvolvedores, seja para a equipe responsáel pela infraestutura, a fim de trazer o feedback necessário em cada passo.
- **Monitoramento**: Os logs de execução da Pipeline e da aplicação precisam estar concentrados em um local seguro e de fácil acesso, bem como as métricas, utilizando o Prometheus para a coleta desses dados e o Grafana para a exposição e análise dos dados coletados, bem como a criação de dashboards que facilitam a tomada de decisão. É claro que não poderia deixar de faltar um APM, para análise dos traces da aplicação, a fim de facilitar a melhora do desempenho de queries ou algum outro trace que esteja atrapalhando o desempenho da aplicação.


## PARTE BONUS - Script de automação
Para automatizar as partes 1 e 2, criei um script em python para automatizar o deploy da aplicação, seja em docker (docker-compose), seja em kubernetes. Ao rodar o script, será questionado em qual plataforma deseja que seja feito o deploy e qual a versão da aplicação, para casos de atualização da mesma.
Utiliei o Python devido sua versatilidade e facilidade em gerar scripts e até aplicaões robustas. É uma linguagem de fácil compreensão e com uma curva de aprendizado muito pequena. Para rodar o script, basta fazer o clone do repositório e rodar o comando abaixo, na raiz do projeto:
`python build.py`
A partir daí o script irá perguntar em qual plataforma deseja fazer o deploy e qual a versão deseja utilizar.