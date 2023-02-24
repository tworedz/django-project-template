# {{ project_name }}

# Local development


## Initial requirements

With default configs project requires:
 - `redis` running on default `6379` localhost port for worker.
 - `postgres` running on default `5432` localhost port with
    `POSTGRES_PASSWORD=postgres` `POSTGRES_USER=postgres` for project itself.

Project uses `poetry` for dependency management:
```shell
poetry install
```

`pre-commit` used for code formatting and holding source code similarity:
```shell
pre-commit install
```

## Running

Run server:
```shell
python manage.py runserver
```

Run worker:
```shell
python manage.py run_huey
```

## Testing

Project uses `pytest` for testing purposes
```shell
pytest src --vvrs -n auto
```


# Production deployment

Project was dockerized with love and pain.

## Initial requirements

* docker
* docker compose
* make

Tested on:
```shell
> docker --version
Docker version 20.10.17, build 100c701

> docker compose version
Docker Compose version v2.10.2
```


## Deployment

// TODO
Eventually, Gitlab CI/CD will be configured here.


### Manual deployment

1. Copy and configure `.env.prod` file.
```shell
cp .env.example .env.prod
```
2. `make`
