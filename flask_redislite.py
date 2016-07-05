from redislite import Redis, StrictRedis
from redis_collections import Dict as RC_Dict, List as RC_List
from rq import Queue, Worker
from flask import current_app
from multiprocessing import Process


try:
    from flask import _app_ctx_stack as stack
except ImportError:
    # fall back
    from flask import _request_ctx_stack as stack


class Collection(object):
    def __init__(self, redis):
        self._redis = redis

    def dict(self, key=None):
        return RC_Dict(key=key, redis=self._redis)

    def get_dict(self, key=None):
        return RC_Dict(key=key, redis=self._redis)

    def list(self, key=None):
        return RC_List(key=key, redis=self._redis)

    def get_list(self, key=None):
        return RC_List(key=key, redis=self._redis)


class FlaskRedis(object):
    def __init__(self, app=None, **kwargs):
        self.app = app
        self.include_collections = kwargs.get('collections', False)
        self.include_rq = kwargs.get('rq', False)
        self.queues = kwargs.get('rq_queues', ['default'])
        strict = self.include_collections or kwargs.get('strict', False)

        self.redis_class = StrictRedis if strict else Redis
        self._connection = None

        self.config_prefix = kwargs.get('config_prefix', 'REDISLITE')

        if app is not None:
            self.init_app(app)

    def connect(self):
        if self._connection is None:
            self._connection = self.redis_class(
                current_app.config["{}_PATH".format(self.config_prefix)]
            )
        return self._connection

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self._teardown)
        else:
            # fall back
            app.teardown_request(self._teardown)

    def _teardown(self, exception):
        if exception is not None:
            print exception

    @property
    def connection(self):
        return self.connect()

    @property
    def collection(self):
        if not self.include_collections:
            return None
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'redislite_collection'):
                ctx.redislite_collection = Collection(redis=self.connection)
            return ctx.redislite_collection

    @property
    def queue(self):
        if not self.include_rq:
            return None
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'redislite_queue'):
                ctx.redislite_queue = Queue(connection=self.connection)
            return ctx.redislite_queue

    def get_worker(self):
        if not self.include_rq:
            return None
        print self.connection
        return Worker(queues=self.queues,
                      connection=self.connection)

