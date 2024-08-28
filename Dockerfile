# Instalando a versão do PHP que não possui vulnerabilidades e foi escolhido SO Alpine por conta do tamanho
FROM php:8.3-rc-alpine

# Definindo candidato para análise via docker inspect
LABEL candidato="Cesar Barbosa Goncalves"

# Instalando as dependências do PHP para rodar a aplicação
RUN apk add --update bash libzip-dev libmcrypt-dev libpng-dev libjpeg-turbo-dev &&\
    libxml2-dev icu-dev mysql-dev curl-dev libmemcached-dev &&\
    apk add --update --virtual build-dependencies build-base gcc wget autoconf && \
    docker-php-ext-install gd && \
    docker-php-ext-install zip &&\
    docker-php-ext-install xml &&\
    docker-php-ext-install mysqli pdo pdo_mysql

# Removendo arquivos de cache, para deixar a imagem o mais enxuta possível
RUN apk del build-dependencies &&\
    rm -rf /var/cache/apk/*

# Baixando e instalando o composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/bin --filename=composer 

# copiando todos os arquivos para a imagem
COPY . .

# Definindo o diretório de trabalho como /main
WORKDIR /main

# Rodando o comando do composer install
RUN composer install

# Criando variável de ambiente para a porta utilizada
ENV PORT=8000

# Marcando o run.sh como executável
RUN chmod +x /run.sh

# Expondo a porta 8000
EXPOSE ${PORT}

# Definindo o ponto de entrada com o run.sh
ENTRYPOINT ["sh", "/run.sh"]

