FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir /etc/nginx/ssl
COPY dhparam.pem /etc/nginx/ssl/dhparam.pem
COPY ssl-cert.pem /etc/nginx/ssl/ssl-cert.pem
COPY ssl-key.pem /etc/nginx/ssl/ssl-key.pem
