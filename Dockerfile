FROM alpine:3.3

MAINTAINER Andre Keller

ENV CONFIGS_DJANGO_STATIC_ROOT /srv/static


WORKDIR /srv
COPY configs /srv/configs
COPY requirements.txt /srv/configs/requirements.txt
RUN addgroup -S configs
RUN adduser -SDHh /srv/configs -s /sbin/nologin configs && \
    chown -R configs:configs /srv/configs

RUN apk --no-cache add python3 pcre mailcap libpq libxml2 libxslt openssl && \
    apk --no-cache add --virtual build-dependencies \
        python3-dev build-base postgresql-dev libxml2-dev \
        libxslt-dev linux-headers openssl-dev pcre-dev git && \
    python3 -m ensurepip --default-pip && \
    pip3 install -U pip && \
    pip3 install -r /srv/configs/requirements.txt && \
    apk del build-dependencies

RUN /srv/configs/manage.py collectstatic --noinput && \
    chown -R configs:configs /srv/static && \
    chmod -R a+w /srv/static
    
VOLUME /srv/static

COPY docker/app/docker-entrypoint.sh /docker-entrypoint.sh
USER configs
EXPOSE 8000
ENTRYPOINT ["/docker-entrypoint.sh"]
