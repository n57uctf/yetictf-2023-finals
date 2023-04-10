# store-api

## Необходиме переменные окружения:
```
DJANGO_SECRET_KEY=<INSERT_YOUR_DJANGO_SECRET_KEY_HERE>

JWT_SECRET_KEY=<INSERT_YOUR_JWT_SECRET_KEY_HERE>

SWAGGER_URL=http://127.0.0.1:8000/

POSTGRES_DB=postgres
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
DB_HOST=db
DB_PORT=5432
```

### Хранить их нужно в файле `.env` в корне проекта

## Сборка проекта осуществляется командой:
```sudo docker-compose up --build```

## Интерфейс для API доступен по адресу
`http://127.0.0.1:8080/swagger/`


## Админ панель доступна по адресу
`http://127.0.0.1:8080/admin/`

### Стандартные данные для входа
```
login: admin
password: admin
```

