Flask-Redislite
===============

.. image:: https://travis-ci.org/scattm/FlaskRedislite.svg?branch=master
    :target: https://travis-ci.org/scattm/FlaskRedislite
.. image:: https://coveralls.io/repos/github/scattm/FlaskRedislite/badge.svg?branch=master
    :target: https://coveralls.io/github/scattm/FlaskRedislite?branch=master
.. image:: https://landscape.io/github/scattm/FlaskRedislite/master/landscape.svg?style=flat
   :target: https://landscape.io/github/scattm/FlaskRedislite/master
   :alt: Code Health

Using Flask with Redislite, also redis-collections.

Installation
------------
Using pip

.. code-block:: bash

    pip install Flask-Redislite

Usage
-----
Choose the path for your Redislite data file, then include to your application config

.. code-block:: python

    REDISLITE_PATH = '<path/to/redis/file.rdb>'
    
Create new redis instance within your application

.. code-block:: python

    from flask import Flask
    from flask_redislite import FlaskRedislite
    
    app = Flask(__name__)
    
    rdb = FlaskRedislite(app)
    # with redis-collections:
    # rdb = FlaskRedislite(app, collection = True)
    
Then use it on your view

.. code-block:: python

    rdb.connection.set('foo1', 'bar1')
    print rdb.connection.get('foo1')
    
    # redis-collections
    collection = rdb.collection
    d = collection.dict('123456')
    d['foo'] = 'bar'
    print d

RQ
-----
To use Flask-Redislite with RQ, you need to start RQ worker as a new process

.. code-block:: python

    from flask import Flask
    from flask_redislite import FlaskRedislite

    app = Flask(__name__)

    rdb = FlaskRedislite(app, rq=True)

    # Your other extensions load here
    # ex: lm = LoginManager()
    # ...

    with app.app_context():
        rdb.start_worker()

    # your codes
    # ex: views function

    app.run()

Then within your view enqueue the jobs:

.. code-block:: python

    import time

    def simple_job():
        time.sleep(2)
        return 12345

    queue = rdb.queue
    queue['default'].enqueue(simple_job, ttl=60, result_ttl=60, job_id='321')
    sleep(5)
    print queue['default'].fetch_job('321').result
