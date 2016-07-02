from redislite import Redis, StrictRedis
from redis_collections import Dict as RC_Dict, List as RC_List
from flask import current_app


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
        strict = self.include_collections or kwargs.get('strict', False)

        self.redis_class = StrictRedis if strict else Redis

        self.config_prefix = kwargs.get('config_prefix','REDISLITE_')

        if app is not None:
            self.init_app(app)

    def _connect(self):
        return self.redis_class(current_app.config["{}PATH".format(self.config_prefix)])

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self._teardown)
        else:
            # fall back
            app.teardown_request(self._teardown)

    def _teardown(self, exception):
        ctx = stack.top
        if exception is not None:
            print exception
        if hasattr(ctx, 'redislite_db'):
            ctx.redislite_db.shutdown()

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'redislite_db'):
                ctx.redislite_db = self._connect()

                if self.include_collections:
                    ctx.redislite_collection = Collection(ctx.redislite_db)
            return ctx.redislite_db

    @property
    def collection(self):
        if not self.include_collections:
            return None
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'redislite_collection'):
                ctx.redislite_collection = Collection(self.connection)
            return ctx.redislite_collection
