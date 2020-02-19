# Online Education

## Процесс установки на сервер

### Загрузка online_education на компьютер
Требуется, чтобы на сервер был установлен приложение `git`.

```sh
$ git clone "https://github.com/NaurizAitbai/online_education.git"
$ cd online_education
```
Необходимо будет ввести данные учетного записа, у которого есть доступ к этому репозиторию.

### Установка пакетов для Linux
В терминале ввести следующую команду:

```sh
$ sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
```

### Установка Docker
TODO: В РАЗРАБОТКЕ

### Включить доступ к Docker через TCP
Создайте папку в `/lib/systemd/system/` под названием `docker.service.d`. Внутри создайте файл `override.conf`.

```sh
sudo mkdir /lib/systemd/system/docker.service.d
sudo vim /lib/systemd/system/docker.service.d/override.conf
```

`/lib/systemd/system/docker.service.d/override.conf`

```
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2376
```

### Установка Nginx
Инструкция по установке `nginx` доступен по следующему адресу: [Install NGINX](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)

Для установки `nginx` необходимо ввести в терминале следующие команды:

```sh
$ sudo add-apt-repository ppa:nginx/stable
$ sudo apt-get update
$ sudo apt-get install nginx
```

### Создание базы и пользователя в PostgreSQL
В терминале зайди под юзером `postgres` и в приложение `psql` ввести SQL-запросы.

```
$ sudo -u postgres psql

postgres=# CREATE DATABASE online_education;
postgres=# CREATE USER имя_пользователя WITH PASSWORD 'пароль';
postgres=# ALTER ROLE имя_пользователя SET client_encoding TO 'utf8';
postgres=# ALTER ROLE имя_пользователя SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE имя_пользователя SET timezone TO 'Asia/Aqtau';
postgres=# GRANT ALL PRIVILEGES ON DATABASE online_education TO имя_пользователя;
postgres=# \q
```

### Создание виртуального окружения Python
Необходимо установить приложение `pipenv` для создания виртуального окружения Python.

```sh
$ sudo pip3 install pipenv
$ sudo chown -R пользователь:пользователь ~/.cache
$ export PIPENV_VENV_IN_PROJECT=1
$ pipenv --python python3
$ pipenv shell
$ pipenv install
$ pipenv install gunicorn psycopg2
```

### Поменять настройки сайта
Внутри проекта расположение файл `onlie_education/settings.py`. Необходимо рядом с ним создать файл `local_settings.py`, и редактировать этот файл:

```sh
$ vim online_education/local_settings.py
```
`~/online_education/online_education/local_settings.py`
```
from os.path

from django.conf import settings

SECRET_KEY = 'секретный ключ'

# Разрешенные хосты:
ALLOWED_HOSTS = ['Имя домена сайта', 'Публичный IP_адрес сайта', 'Локальный IP-адрес сайта']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'online_education',
        'USER': 'имя_пользователя',
        'PASSWORD': 'пароль',
        'HOST': 'localhost',
    }
}

# Подключение к Docker Daemon
DOCKER_HOST = 'IP-адрес Docker-сервера'
DOCKER_PORT = 'Порт Docker-сервера'

# Когда Docker контейнер создается, ему присваивается URL-адрес имя_проекта.DOCKER_BASE_DOMAIN
DOCKER_BASE_DOMAIN = 'Домен сайта'
```

### Мигрирование и создание директории static
```sh
$ python manage.py migrate
$ python manage.py collectstatic
```

### Создание сервиса Gunicorn
Создаем и редактируем файл `/etc/systemd/system/online_education.service`.
```sh
$ sudo vim /etc/systemd/system/online_education.service
```

`/etc/systemd/system/online_education.service`
```
[Unit]
Description=Online Education (Gunicorn Daemon)
After=network.target

[Service]
User=пользователь
Group=пользователь
WorkingDirectory=/home/пользователь/online_education
ExecStart=/home/пользователь/online_education/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/пользователь/online_education/online_education.sock online_education.wsgi:application

[Install]
WantedBy=multi-user.target
```

Запустить сервис с помощью команды:
```sh
$ sudo systemctl enable online_education
$ sudo systemctl start online_education
```

### Настройка Nginx
Создать конфигурационный файл для нашего сайта в директории nginx.
```sh
$ sudo vim /etc/nginx/conf.d/online_education.conf
```

`/etc/nginx/conf.d/online_education.conf`
```
server {
    listen 80;
    server_name имя_домена;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/пользователь/online_education;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/пользователь/online_education/online_education.sock;
    }

    location /ws/ {
        include proxy_params;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://unix:/home/пользователь/online_education/online_education.sock;
    }
}
```

Также создать папку `/etc/nginx/apps`, и сделать владельцем данной папки текущего пользователя.

```sh
sudo mkdir /etc/nginx/apps
sudo chown -R пользователь:пользователь /etc/nginx/apps
```

В файле `/etc/nginx/nginx.conf` внутри `http` добавить строку `include apps/*;`

```sh
sudo vim /etc/nginx/nginx.conf
```

`/etc/nginx/nginx.conf`
```
http {
    ...
    include apps/*;
}
```

После сохранение файла, выполнить следующие команды
```sh
$ sudo nginx -t
$ sudo systemctl restart nginx
```

### Дать права текущему пользователю сделать перезапуск Nginx сервиса
TODO: В РАЗРАБОТКЕ