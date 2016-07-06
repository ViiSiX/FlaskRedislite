import flask
import pytest
import time
import flask_redislite
from os import remove, path
from redislite import Redis, StrictRedis


@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.config.update({
        'REDISLITE_PATH': 'frl.rdb',
        'REDISLITE_WORKER_PID': 'worker.pid',
        'RL_PATH': 'worker1.rdb'
    })

    try:
        remove(app.config.get('REDISLITE_PATH'))
    except OSError:
        pass

    try:
        remove(app.config.get('RL_PATH'))
    except OSError:
        pass

    return app


@pytest.fixture
def simple_job():
    return '224a-ff43-6a2gF'


def test_constructor(app):
    """
    - Test if the connection is created and using Redis class
    """
    rdb = flask_redislite.FlaskRedis(app)
    with app.app_context():
        assert isinstance(rdb.connection, Redis)
        assert rdb.connection.socket_file is not None


def test_constructor_strict(app):
    """
    - Test if the connection is created and using StrictRedis class
    """
    rdb = flask_redislite.FlaskRedis(app, strict=True)
    with app.app_context():
        assert isinstance(rdb.connection, StrictRedis)
        assert rdb.connection.socket_file is not None


def test_constructor_redis_collections(app):
    """
    - Test if the connection is created and using StrictRedis class
    - Check if the collection is created
    """
    rdb = flask_redislite.FlaskRedis(app, collections=True)
    with app.app_context():
        assert isinstance(rdb.connection, StrictRedis)
        assert rdb.connection.socket_file is not None
        assert rdb.collection is not None


def test_constructor_rq(app):
    """
    - Test if the connection is created and using Redis class
    - Check if the worker process is created
    - Check if the worker pid file is created
    - Check if the worker pid file is cleaned up after terminated
    """
    rdb = flask_redislite.FlaskRedis(app, rq=True)
    assert not path.isfile(app.config.get('REDISLITE_WORKER_PID'))

    with app.app_context():
        assert isinstance(rdb.connection, Redis)
        assert rdb.connection.socket_file is not None

        rdb.start_worker()
        assert rdb.worker_process.is_alive()
        assert path.isfile(app.config.get('REDISLITE_WORKER_PID'))

    # Simulate the app termination
    time.sleep(0.5)
    rdb.worker_process.terminate()
    time.sleep(0.5)
    assert not path.isfile(app.config.get('REDISLITE_WORKER_PID'))


def test_config_prefix(app):
    """
    - If the constructor is called without app object, no connection
    """
    rdb = flask_redislite.FlaskRedis(config_prefix='RL')

    with app.app_context():
        assert isinstance(rdb.connection, Redis)
        assert rdb.connection.socket_file is not None


def test_commit(app):
    """
    - If commit, check if rdb file exists
    """
    rdb = flask_redislite.FlaskRedis()

    with app.app_context():
        rdb.commit()
        time.sleep(0.5)
        assert path.isfile(app.config.get('REDISLITE_PATH'))


def test_redis_set_get(app):
    """
    - Test if we can set and get values from Redislite
    """
    rdb = flask_redislite.FlaskRedis(app)

    with app.app_context():
        rdb.connection.set('foo1', 'aiKjq91jUyq3r')
        assert rdb.connection.get('foo1') == 'aiKjq91jUyq3r'


def test_redis_collections(app):
    """
    - Test if we can set and get values using Redis-Collections
    """
    rdb = flask_redislite.FlaskRedis(app, collections=True)

    with app.app_context():
        collection = rdb.collection

        # Dict
        d = collection.dict('foo_dict')
        d['foo2'] = '28bH-76R-26A'
        assert not isinstance(d, dict)
        assert d == {'foo2': '28bH-76R-26A'}

        # List
        l = collection.list('foo_list')
        l.append('foo3 is kua3D')
        assert not isinstance(l, list)
        assert l[0] == 'foo3 is kua3D'


def test_rq(app):
    """
    - Test if we can enqueue a simple job and get result from it
    """
    rdb = flask_redislite.FlaskRedis(app, rq=True)

    with app.app_context():
        rdb.start_worker()

    # Simulate the request
    with app.app_context():
        queue = rdb.queue
        job = queue.enqueue(simple_job, ttl=60, result_ttl=60, job_id='foo4')
        assert job.result is None
        time.sleep(1)
        assert job.result == simple_job()

    # Another request
    time.sleep(0.5)
    with app.app_context():
        queue = rdb.queue
        assert queue.fetch_job('foo4').result == simple_job()

    # Clean up
    rdb.worker_process.terminate()
