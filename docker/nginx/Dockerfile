FROM nginx:alpine

ENV UWSGI_PASS app:8000
MAINTAINER Andre Keller

COPY nginx.conf /etc/nginx/nginx.conf
RUN touch /etc/nginx/uwsgi-upstream.conf && \
    chown nginx:nginx /etc/nginx/uwsgi-upstream.conf
COPY docker-entrypoint.sh /

USER nginx
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]
