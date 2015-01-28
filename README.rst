++++++++++
Grenouille
++++++++++

Presentation
============

Grenouille is an online service for weather data.
All data can be obtained in JSON and displayed on a map.
The Web application is based on `Flask <http://flask.pocoo.org>`_.

An example of a client for the Yocto-Meteo sensor
(connected to a `Raspberry Pi <http://www.raspberrypi.org>`_)
is provided (inspired from `this code <https://github.com/tarekziade/grenouille>`_).
Of course you can implement your own client with the API documentation.

The official instance is running `here <https://petite-grenouille.herokuapp.com>`_.

Usage
=====

Deployment
----------

The platform can be deployed on Heroku or on a traditional server.

After installation, you will be able to connect with the email
*root@grenouille.localhost* and the password *password*.

Deploying the application on Heroku
'''''''''''''''''''''''''''''''''''

.. code:: bash

    $ git clone https://bitbucket.org/cedricbonhomme/grenouille.git
    $ cd grenouille
    $ heroku create
    $ heroku addons:add heroku-postgresql:dev
    $ heroku config:set HEROKU=1
    $ git push heroku master
    $ heroku run init
    $ heroku ps:scale web=1

Deploying the application on a traditional server
'''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    $ git clone https://bitbucket.org/cedricbonhomme/grenouille.git
    $ cd grenouille
    $ sudo pip install --upgrade -r requirements.txt
    $ cp conf/conf.cfg-sample conf/conf.cfg

If you want to use PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ sudo apt-get install postgresql postgresql-server-dev-9.3 postgresql-client
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

Edit the configuration file with the line:

.. code:: cfg

    [database]
    uri = postgres://username:password@127.0.0.1:5433/grenouille

If you want to use SQLite
~~~~~~~~~~~~~~~~~~~~~~~~~

Just edit the configuration file with the line:

.. code:: cfg

    [database]
    uri = sqlite+pysqlite:///grenouille.db


Finally:

.. code:: bash

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

You can use the provided client:

.. code:: bash

    $ ./grenouillecli.py --email your-email@example.com --password password --api-key qGWjgIybd1i8uh89o5 --station 4 --temperature 25.7 --pression 980 --humidity 84
    {
        "result": "OK"
    }


Get measures
''''''''''''

By country:

.. code:: bash

    $ curl https://petite-grenouille.herokuapp.com/weather.json/?q=FR
    {
        "result": [
            {
            "coord": {
                "lat": 49.115558,
                "lon": 6.175635
            },
            "country": "FR",
            "date": "Sat, 05 Apr 2014 21:17:43 GMT",
            "id": 1,
            "main": {
                "humidity": 84.0,
                "pression": 980.0,
                "temperature": 25.7
            },
            "name": "Metz"
            },
            {
            "coord": {
                "lat": 45.649781,
                "lon": 0.153623
            },
            "country": "FR",
            "date": "Thu, 03 Apr 2014 05:34:00 GMT",
            "id": 5,
            "main": {
                "humidity": 82.0,
                "pression": 980.0,
                "temperature": 23.2
            },
            "name": "Angoul\u00eame"
            }
        ]
    }


Donation
========

If you wish and if you like *Grenouille*, you can donate via bitcoin
`1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ <https://blockexplorer.com/address/1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ>`_.
Thank you!

License
=======

`Grenouille <https://bitbucket.org/cedricbonhomme/grenouille>`_
is under the `GNU Affero General Public License version 3 <https://www.gnu.org/licenses/agpl-3.0.html>`_.

Contact
=======

`My home page <https://www.cedricbonhomme.org>`_.
