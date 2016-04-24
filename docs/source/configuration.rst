=============
configuration
=============

.. _`configuration`:


confi.gs reads its configuration from OS environment variables.

confi.gs comes with some insecure internal defaults (marked below) in order
to ease development and testing of the application. confi.gs refuses to start
if these internal defaults are not overridden in a production environment!

environment variables
=====================

**CONFIGS_DATABASE_HOST**
  IP or hostname of the postgresql database server.

  *Default*: '127.0.0.1'


**CONFIGS_DATABASE_SCHEMA**
  Name of the database.

  *Default*: 'configs'


**CONFIGS_DATABASE_PASSWORD**
  Password to connect to the database.

  *INSECURE DEFAULT, DO NOT USE IN PRODUCTION*

  *Default*: 'configs'


**CONFIGS_DATABASE_PORT**
  Port of the postgresql database server.

  *Default*: '5432'


**CONFIGS_DATABASE_USER**
  User to connect to the database.

  *Default*: 'configs'


**CONFIGS_DJANGO_DEBUG**
  Wheter or not to enable DEBUG mode.

  *INSECURE DEFAULT, DO NOT USE IN PRODUCTION*

  *Default*: True


**CONFIGS_DJANGO_STATIC_ROOT**
  Where collected static files (images, css, js, etc.) from the application
  should be deployed to when django-admin collectstatic is run.

  *Default*: None


**CONFIGS_ENCDATA_FIELDS**
  Space separated list of field names for the external node classifier.

  *Default*: 'location role flavor'


**CONFIGS_SECURITY_ALLOWED_HOSTS**
  Space separated list of host names the application should answer for. Raises
  an HTTP 400 (bad request) if the request is for a host name not in this list.

  *INSECURE DEFAULT, DO NOT USE IN PRODUCTION*

  *Default*: '*'


**CONFIGS_SECURITY_CSRF_COOKIE_SECURE**
  Whether to use a secure cookie for the CSRF cookie. If this is set to True,
  the cookie will be marked as *secure*, which means browsers may ensure that
  the cookie is only sent under an HTTPS connection.

  *INSECURE DEFAULT, DO NOT USE IN PRODUCTION*

  *Default*: False


**CONFIGS_SECURITY_SESSION_COOKIE_SECURE**
  Whether to use a secure cookie for the session cookie. If this is set to True,
  the cookie will be marked as *secure*, which means browsers may ensure that
  the cookie is only sent under an HTTPS connection.

  *INSECURE DEFAULT, DO NOT USE IN PRODUCTION*

  *Default*: False


**CONFIGS_SECURITY_SECRET_KEY**
  A secret key for a particular Django installation. This is used to provide
  cryptographic signing, and should be set to a unique, unpredictable value.

  *INSECURE DEFAULT, DO NOT USE IN PRODUCTION*

  *Default*: 'InSecureDefaultNeverUseItInProduction'

  https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY


**CONFIGS_USE_INSECURE_DEFAULTS**
  Wheter to accept insecure defaults. If this is set to True, the application
  will run regardless of insecure internal default values.

  This defaults to False, unless confi.gs is started via its `manage.py` script.

  *ONLY TOUCH THIS IF YOU ARE REALLY SURE WHAT YOU ARE DOING*
