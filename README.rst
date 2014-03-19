++++++++++
Grenouille
++++++++++

Presentation
============

Grenouille is an online service for weather data.  
All data can be obtained in JSON and displayed on a map.
The Web application is based on Flask and uses PostgreSQL.  
It can be deployed on Heroku. An example of a client for the Yocto-Meteo sensor 
is provided (inspired from `this code <https://github.com/tarekziade/grenouille/>`_).

The project is divided in two parts:

* the web service: a Flask application using PostgreSQL with an open API;
* a proof of concept station: a watcher running on a `Raspberry Pi <http://www.raspberrypi.org/>`_ with a `Yoctopuce <http://www.yoctopuce.com>`_ sensor. Of course you can implement your own client with the API documentation.

A demo instance is available `here <https://petite-grenouille.herokuapp.com/>`_.

Usage
=====

Deployment
----------

This application can be deployed on Heroku or on a traditional server.

Deploying the application on Heroku
'''''''''''''''''''''''''''''''''''

.. code:: bash

    $ git clone https://bitbucket.org/cedricbonhomme/grenouille.git
    $ cd grenouille
    $ heroku create
    $ heroku addons:add heroku-postgresql:dev
    $ git push heroku master
    $ heroku run init
    $ heroku ps:scale web=1

Deploying the application on a traditional server
'''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    $ git clone https://bitbucket.org/cedricbonhomme/grenouille.git
    $ cd grenouille
    $ sudo apt-get install postgresql postgresql-server-dev-9.1 postgresql-client
    $ sudo pip install --upgrade -r requirements.txt
    $ sudo -u postgres createuser
    Enter name of role to add: username
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) y
    Shall the new role be allowed to create more new roles? (y/n) n
    $ createdb grenouille
    $ sudo -u postgres psql
    postgres=# ALTER USER username WITH ENCRYPTED PASSWORD 'password';
    postgres=# GRANT ALL PRIVILEGES ON DATABASE grenouille TO username;
    postgres=# \q
    $ export DATABASE_URL="postgres://username:password@127.0.0.1:5432/grenouille"
    $ python db_create.py
    $ python runserver.py
     * Running on http://0.0.0.0:5000/
     * Restarting with reloader


Web services
------------

Send measures
'''''''''''''

This example shows how to send measures from a station to the platform.

.. code:: python

    >>> url = "https://petite-grenouille.herokuapp.com/weather.json/"
    >>> headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    >>> data = {'pression': 1023, 'api_key': 'VDZCF0aa1nUazxbCX2q01FKRWALxdIzCMNmg', 'temperature': 20, 'station_id': 2, 'humidity': 81}
    >>> r = requests.post(url, data=json.dumps(data), headers=headers, auth=('your-email@example.com', 'password'))
    >>> print r.content
    {
    "result": "OK"
    }


Donation
========

If you wish and if you like *Grenouille*, you can donate via bitcoin
`1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ <https://blockexplorer.com/address/1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ>`_.
Thank you!

License
=======

`Grenouille <https://bitbucket.org/cedricbonhomme/grenouille>`_
is under `GPLv3 <http://www.gnu.org/licenses/gpl-3.0.txt>`_ license.

Contact
=======

`My home page <http://cedricbonhomme.org/>`_.
