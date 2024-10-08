#!/bin/bash

# Definindo o arquivo .env
ENV_FILE="/main/.env"

# Definindo a conexão como MySQL
echo 'DB_CONNECTION=mysql' > "$ENV_FILE"

# Definindo as variáveis de conexão com o BD a partir das variáveis em  tempo de execução do container.
for var in $(env | cut -d= -f1| grep -e ^DB); do
    echo "$var=$(printenv $var)" >> "$ENV_FILE"
done
# Acessando o diretório do projeto
cd /main

# Verificando se a migração já foi realizada
php artisan migrate:status | grep -q ERROR
if [ $? -eq 0 ]; then
    echo "Migrações não aplicadas. Executando php artisan migrate..."
    php artisan migrate --seed --force
else
    echo "Migrações já aplicadas."
fi

# Rodando o comando para iniciar o servidor
php artisan serve --host=0.0.0.0 --port=${PORT}
