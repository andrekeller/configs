============
Installation
============

.. _`install`:

Manual setup on Ubuntu 14.04 LTS
================================

confi.gs needs postgresql 9.4, as previous version do not have support
for inet\_ops GiST indexes.

Additional dependencies include supervisor (to run the confi.gs uwsgi
app), nginx (as a reverse proxy in front of the uwsgi app) and some
python build dependencies to built the modules used in the confi.gs
python virtualenv.

All commands stated on the next lines are run while logged in as root
(i.e. sudo -i).

Setup postgresql apt repository
-------------------------------

::

    cat > /etc/apt/sources.list.d/postgresql.list << 'EOF'
    deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main
    EOF
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys ACCC4CF8

Perform system update and install needed packages
-------------------------------------------------

::

    apt-get -y update
    apt-get -y dist-upgrade
    apt-get -y install python-virtualenv python3-dev libpq-dev libpcre3-dev \
                       postgresql-9.4 postgresql-client-9.4 \
                       supervisor ssl-cert nginx-full pwgen git
    apt-get -y autoremove
    apt-get -y clean

Setup user/group and permissions for configs
--------------------------------------------

::

    groupadd -r configs
    useradd -r -m -k /dev/null -s /bin/bash -d /home/configs -g configs configs
    mkdir /etc/configs
    chown -R configs:configs /etc/configs
    gpasswd -a www-data configs

Fetch the configs source
------------------------

::

    sudo -iu configs
    git clone https://github.com/andrekeller/configs.git ~/app
    cd ~/app
    git checkout devel
    exit

Populate the python virtualenv
------------------------------

::

    sudo -iu configs
    virtualenv --python python3.4 --prompt '(configs-venv)' ~/pyvenv
    source ~/pyvenv/bin/activate
    pip install --upgrade pip
    pip install pip-tools
    cd ~/app
    pip-sync
    exit

Setup postgresql database
-------------------------

::

    export DB_PASS=$(pwgen -s 20 1)
    sudo -EHu postgres psql template1 << EOF
    CREATE DATABASE configs;
    CREATE USER configs WITH PASSWORD '$DB_PASS';
    GRANT ALL PRIVILEGES ON DATABASE "configs" to configs;
    EOF

Setup configuration for configs app (django/uwsgi)
--------------------------------------------------

::

    sudo -EHsu configs
    SECRET_KEY="$(pwgen -s 100 1)"
    cat > /etc/configs/configs.ini << EOF
    [django]
    debug = false
    static_root = /home/configs/static

    [database]
    schema = configs
    user = configs
    password = $DB_PASS
    host = 127.0.0.1
    port = 5432

    [security]
    allowed_hosts = $(hostname -f)
    csrf_cookie_secure = true
    session_cookie_secure = true
    secret_key = $SECRET_KEY
    EOF

    cat > /etc/configs/uwsgi.ini << 'EOF'
    [uwsgi]
    chdir = /home/configs/app/configs
    home = /home/configs/pyvenv
    env = DJANGO_SETTINGS_MODULE=configs.settings
    enable-threads
    master
    processes = 2
    socket = /home/configs/uwsgi.sock
    chmod-socket = 660
    wsgi-file = configs/wsgi.py
    EOF
    exit
    unset DB_PASS

Initialize configs
------------------

::

    sudo -iu configs
    source ~/pyvenv/bin/activate
    ~/app/configs/manage.py collectstatic --noinput
    ~/app/configs/manage.py migrate
    ~/app/configs/
    exit

Supervisor configuration
------------------------

::

    cat > /etc/supervisor/conf.d/configs-uwsgi.conf << 'EOF'
    [program:configs-uwsgi]
    command=/home/configs/pyvenv/bin/uwsgi --ini /etc/configs/uwsgi.ini
    autostart=true
    autorestart=true
    directory=/home/configs/app/configs
    stdout_logfile=/var/log/supervisor/configs-uwsgi.log
    stdout_logfile_backups=10
    stdout_logfile_maxbytes=10MB
    stderr_logfile=NONE
    redirect_stderr=true
    stopsignal=QUIT
    user=configs
    EOF
    supervisorctl reload

Nginx configuration
-------------------

::

    openssl dhparam -out /etc/nginx/dhparam.pem 2048
    SSL_CIPHERS='ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:
    ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:
    DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:
    ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:
    ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:
    ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:
    DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:
    DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:ECDHE-RSA-DES-CBC3-SHA:
    ECDHE-ECDSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:
    AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:
    DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:
    !EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA'

    cat > /etc/nginx/sites-available/configs.conf << EOF
    server {

        listen [::]:80 ipv6only=off;
        server_name $(hostname -f);

        return 301 https://\$server_name\$request_uri;

    }

    server {

        listen [::]:443 ipv6only=off ssl;
        server_name $(hostname -f);

        ssl on;
        ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
        ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;
        ssl_dhparam /etc/nginx/dhparam.pem;
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:59m;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers '${SSL_CIPHERS//[[:space:]]}';
        ssl_prefer_server_ciphers on;
        add_header Strict-Transport-Security max-age=15768000;

        access_log /var/log/nginx/configs_access.log;
        error_log /var/log/nginx/configs_error.log;

        location / {
            include uwsgi_params;
            uwsgi_param Host \$host;
            uwsgi_param X-Real-IP \$remote_addr;
            uwsgi_param X-Forwarded-For \$proxy_add_x_forwarded_for;
            uwsgi_param X-Forwareded-Proto \$http_x_forwarded-proto;
            uwsgi_pass unix:///home/configs/uwsgi.sock;
        }

        location ^~ /static {
            alias /home/configs/static;
        }

    }
    EOF

    ln -s /etc/nginx/sites-available/configs.conf /etc/nginx/sites-enabled/
    rm /etc/nginx/sites-enabled/default
    service nginx restart

