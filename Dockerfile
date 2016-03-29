FROM alpine:3.3

ENV CONFIGS_DJANGO_STATIC_ROOT /srv/static

WORKDIR /srv
RUN mkdir logs static
VOLUME ["/srv/logs", "/srv/static"]

COPY configs /srv/configs
COPY requirements.txt /srv/configs/requirements.txt

RUN apk --no-cache add python3 pcre mailcap libpq libxml2 libxslt openssl && \
    apk --no-cache add --virtual build-dependencies \
        python3-dev build-base postgresql-dev libxml2-dev \
        libxslt-dev linux-headers openssl-dev pcre-dev git && \
    python3 -m ensurepip --default-pip && \
    pip3 install -U pip && \
    pip3 install -r /srv/configs/requirements.txt && \
    apk del build-dependencies

COPY docker/app/docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
