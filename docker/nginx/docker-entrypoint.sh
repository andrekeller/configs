#!/bin/sh

cat > /etc/nginx/uwsgi-upstream.conf << EOF
upstream uwsgi { 
    server $UWSGI_PASS;
}
EOF
exec nginx -g 'daemon off;'
