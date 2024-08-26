## About project infra-challenge

This is an example api project for the technical test to the application infrastructure team.

### Setup

1. The project requires:
```shell
PHP 8.3
MySQL 8.0.36
```
2. After clonning the project, install dependencies
```shell
composer install
```
3. Configure the credentials in .env file
```shell
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=
DB_USERNAME=
DB_PASSWORD=
```
4. Run migrations with seeders
```shell
php artisan migrate --seed
```
5. Access the example endpoint
```shell
curl http://127.0.0.1:8000/api/v1/products
```
