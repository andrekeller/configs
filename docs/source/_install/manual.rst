Manual setup (Ubuntu 16.04 LTS)
===============================

This guide will walk you through the manual setup process of confi.gs on an
existing ubuntu 16.04 LTS machine.

All commands stated on the next lines are run while logged in as root (i.e.
sudo -i).


Perform system update and install needed packages
-------------------------------------------------

::

    apt-get -y update
    apt-get dist-upgrade
    apt-get install python3-dev python3-venv build-essential \
                    libpq-dev libpcre3-dev libyaml-dev libssl-dev \
                    postgresql-9.5 postgresql-client-9.5 \
                    ssl-cert nginx-full git
    apt-get autoremove
    apt-get clean

Setup user/group and permissions for configs
--------------------------------------------

::

    groupadd -r configs
    useradd -r -m -k /dev/null -s /bin/bash -d /home/configs -g configs configs
    gpasswd -a www-data configs

Fetch the configs source
------------------------

::

    sudo -iu configs
    git clone -b devel https://github.com/configs-app/configs.git ~/app
    exit

Populate the python virtualenv
------------------------------

::

    sudo -iu configs
    python3 -m venv ~/pyvenv
    source ~/pyvenv/bin/activate
    exit


Setup postgresql database
-------------------------

::

    sudo -iu postgres psql template1

.. code:: sql

    CREATE DATABASE configs;
    CREATE USER configs WITH PASSWORD 'SecureDatabasePassword';
    GRANT ALL PRIVILEGES ON DATABASE "configs" to configs;
    \c configs
    CREATE EXTENSION IF NOT EXISTS hstore;

Setup configuration for configs app
-----------------------------------

The configuration of confi.gs is done via environment variables.

.. code-block:: bash
    :caption: /etc/default/configs

    DJANGO_SETTINGS_MODULE=configs.settings
    CONFIGS_DATABASE_PASSWORD=SecureDatabasePassword
    CONFIGS_DJANGO_DEBUG=no
    CONFIGS_DJANGO_STATIC_ROOT=/home/configs/static
    CONFIGS_SECURITY_ALLOWED_HOSTS=configs.example.org
    CONFIGS_SECURITY_CSRF_COOKIE_SECURE=yes
    CONFIGS_SECURITY_SESSION_COOKIE_SECURE=yes
    CONFIGS_SECURITY_SECRET_KEY=LongUnpredictableSecureString


Setup service for configs
-------------------------

.. code-block:: ini
    :caption: /etc/systemd/system/configs.service

    [Unit]
    Description=confi.gs app
    Requires=nginx.service postgresql.service
    Before=nginx.service
    After=postgresql.service

    [Service]
    WorkingDirectory=/home/configs/app/configs
    EnvironmentFile=/etc/default/configs
    ExecStartPre=/home/configs/pyvenv/bin/python \
                    /home/configs/app/configs/manage.py collectstatic --noinput
    ExecStartPre=/home/configs/pyvenv/bin/python \
                    /home/configs/app/configs/manage.py migrate
    ExecStart=/home/configs/pyvenv/bin/uwsgi --chdir /home/configs/app/configs \
                    --die-on-term \
                    --need-app \
                    --env DJANGO_SETTINGS_MODULE=configs.settings \
                    --enable-threads \
                    --master \
                    --processes 2 \
                    --socket 127.0.0.1:8000 \
                    --wsgi-file configs/wsgi.py

::

    systemctl daemon-reload
    systemctl start configs
    systemctl status configs

Setup nginx
-----------

::

    openssl dhparam -out /etc/ssl/dh4096.pem 4096


.. code-block:: nginx
    :caption: /etc/nginx/sites-available/configs.conf

    server {

        listen [::]:80 ipv6only=off;
        server_name configs.example.org;

        return 301 https://$server_name$request_uri;

    }

    server {

        listen [::]:443 ipv6only=off ssl;
        server_name configs.example.net

        ssl on;
        ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
        ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;
        ssl_dhparam /etc/ssl/dh4096.pem;

        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:50m;
        ssl_session_tickets off;

        ssl_protocols TLSv1.2;
        ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256';
        ssl_prefer_server_ciphers on;

        add_header Strict-Transport-Security max-age=15768000;

        access_log /var/log/nginx/configs_access.log;
        error_log /var/log/nginx/configs_error.log;

        location / {
            include uwsgi_params;
            uwsgi_param Host $host;
            uwsgi_param X-Real-IP $remote_addr;
            uwsgi_param X-Forwarded-For $proxy_add_x_forwarded_for;
            uwsgi_param X-Forwareded-Proto $http_x_forwarded-proto;
            uwsgi_pass 127.0.0.1:8000;
        }

        location ^~ /static {
            alias /home/configs/static;
        }

    }

::

    ln -s /etc/nginx/sites-available/configs.conf /etc/nginx/sites-enabled/
    rm /etc/nginx/sites-enabled/default
    systemctl restart nginx

