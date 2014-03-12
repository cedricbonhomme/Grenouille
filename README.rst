++++++++++
Grenouille
++++++++++

Presentation
============

This project was inspired by the project `Grenouille <https://github.com/tarekziade/grenouille/>`_
from `Tarek Ziadé <http://ziade.org/>`_.

It is intended to be running on a `Raspberry Pi <http://www.raspberrypi.org/>`_
with a `Yoctopuce <http://www.yoctopuce.com>`_ sensor.

The station is connected to `OpenWeatherMap <http://openweathermap.org/>`_, main goal of this *fork*.


Usage
=====

Deployment
----------

This application can be deployed on Heroku.

Deploying the application on Heroku
'''''''''''''''''''''''''''''''''''

.. code:: bash

    $ git clone https://bitbucket.org/cedricbonhomme/grenouille.git
    $ cd grenouille
    $ heroku create
    $ heroku addons:add heroku-postgresql:dev
    $ git push heroku master
    $ heroku open

Deploying the application on a traditional server
'''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: bash

    $ sudo -u postgres createuser
    $ createdb grenouille
    $ sudo -u postgres createuser
    postgres=# ALTER USER username WITH ENCRYPTED PASSWORD 'password';
    postgres=# GRANT ALL PRIVILEGES ON DATABASE grenouille TO username;
    postgres=# \q
    $ export SQLALCHEMY_DATABASE_URI="postgres://username:password@127.0.0.1:5432/grenouille"

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
