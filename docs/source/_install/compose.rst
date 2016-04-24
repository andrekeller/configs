Docker compose
==============

The easiest and fastest way to get confi.gs up and running is to use the
supplied `docker-compose.yml` configuration.

Make sure you change the insecure default values, otherwise confi.gs will refuse
to start!

After that, run `docker-compose up` from the root directory in order to get a
basic setup. The basic setup consists of three containers:


**database**
    This runs the postgresql database server

**app**
    This runs the actual confi.gs application using uwsgi

**web**
    This runs the nginx reverse proxy for the application and the static files.
    confi.gs will be exposed on port 8080 by this container.


Whats left to do, make sure your loadbalancer points to port 8080 of the web
container and does proper SSL!
