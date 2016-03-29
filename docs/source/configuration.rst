=============
configuration
=============

.. _`configuration`:


confi.gs comes with various configuration options that can be set in different
ways. Configuration can be passed as OS environment variables or in form of a
configuration file in /etc/configs/configs.ini. OS environment variables have
higher priority than settings from the configuration file. If neither is
present, internal defaults *NOT SUITABLE FOR PRODUCTION* will be used.

environment variables
=====================

**CONFIGS_CONFIGS_ENCDATA_FIELDS**
  Space separated list of field names for the external node classifier.

  *Default*: 'location role flavor'


**CONFIGS_DATABASE_HOST**
  IP or hostname of the postgresql database server.

  *Default*: '127.0.0.1'


**CONFIGS_DATABASE_SCHEMA**
  Name of the database.

  *Default*: 'configs'


**CONFIGS_DATABASE_PASSWORD**
  Password to connect to the database.

  *Default*: 'configs'


**CONFIGS_DATABASE_PORT**
  Port of the postgresql database server.

  *Default*: '5432'


**CONFIGS_DATABASE_USER**
  User to connect to the database.

  *Default*: 'configs'


**CONFIGS_DJANGO_DEBUG**
  Wheter or not to enable DEBUG mode. *NEVER* enable in production deployments

  *Default*: True


**CONFIGS_DJANGO_STATIC_ROOT**
  Where collected static files (images, css, js, etc.) from the application
  should be deployed to when django-admin collectstatic is run.

  *Default*: None


**CONFIGS_SECURITY_ALLOWED_HOSTS**
  Space separated list of host names the application should answer for. Raises
  an HTTP 400 (bad request) if the request is for a host name not in this list.

  *Default*: '*'


**CONFIGS_SECURITY_CSRF_COOKIE_SECURE**
  Whether to use a secure cookie for the CSRF cookie. If this is set to True,
  the cookie will be marked as *secure*, which means browsers may ensure that
  the cookie is only sent under an HTTPS connection.

  *Default*: False


**CONFIGS_SECURITY_SESSION_COOKIE_SECURE**
  Whether to use a secure cookie for the session cookie. If this is set to True,
  the cookie will be marked as *secure*, which means browsers may ensure that
  the cookie is only sent under an HTTPS connection.

  *Default*: False


**CONFIGS_SECURITY_SECRET_KEY**
  A secret key for a particular Django installation. This is used to provide
  cryptographic signing, and should be set to a unique, unpredictable value.

  *Default*: 'InSecureDefaultNeverUseItInProduction'

  https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY


configuration file
==================

The configuration file is a INI-style file /etc/configs/configs.ini.

It supports the same configuration options as the environment variables.

A few examples:

To set *CONFIGS_DJANGO_DEBUG*:

.. code-block:: ini

    [django]
    debug = True

To set *CONFIGS_CONFIGS_ENCDATA_FIELDS*

.. code-block:: ini

    [configs]
    encdata_fields = 'field1 field2 field3'

