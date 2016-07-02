Flask-Redislite
===============

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
