"""
Flask-Redislite
---------------

Add Redislite support to Flask with addition redis-collections
and RQ.
"""
from redislite import Redis, StrictRedis
from redis_collections import Dict as RC_Dict, List as RC_List
from rq import Queue, Worker
from flask import current_app
from multiprocessing import Process


__version__ = '0.0.4'


try:
    from flask import _app_ctx_stack as stack
except ImportError:
    # fall back
    from flask import _request_ctx_stack as stack


class Collection(object):
    """
    Wrapper class for redis-collections
    """

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
    """
    Main class for Flask-Redislite
    """

    def __init__(self, app=None, **kwargs):
        """
        :param app: Flask's app
        :param kwargs: strict, config_prefix, collections, rq, rq_queues
        """
        self.app = app

        self.include_collections = kwargs.get('collections', False)
        strict = self.include_collections or kwargs.get('strict', False)

        self.redis_class = StrictRedis if strict else Redis

        self.include_rq = kwargs.get('rq', False)
        if self.include_rq:
            self.queues = kwargs.get('rq_queues', ['default'])
            self.worker_process = None

        self.config_prefix = kwargs.get('config_prefix', 'REDISLITE')

        self._connection = None

    def connect(self):
        self._connection = self.redis_class(
            current_app.config["{}_PATH".format(self.config_prefix)]
        )

    @property
    def connection(self):
        if self._connection is None:
            self.connect()
        return self._connection

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

    def start_worker(self):
        """
        Trigger new process as a RQ worker.
        """
        if not self.include_rq:
            return None
        worker = Worker(queues=self.queues,
                        connection=self.connection)
        worker_pid_path = current_app.config.get(
            "{}_WORKER_PID".format(self.config_prefix), 'rl_worker.pid'
        )

        try:
            worker_pid_file = open(worker_pid_path)
            worker_pid = int(worker_pid_file.read())
            print "Worker already started with PID=%d" % worker_pid
            worker_pid_file.close()
        except (IOError, TypeError):
            def worker_wrapper(worker_instance, pid_path):
                """
                A wrapper to start RQ worker as a new process.
                :param worker_instance: RQ's worker instance
                :param pid_path: A file to check if the worker
                    is running or not
                """
                import atexit
                import signal
                from os import remove

                def exit_handler():
                    """
                    Remove pid file on exit (Windows)
                    """
                    remove(pid_path)

                def signal_handler(*args):
                    """
                    Remove pid file on exit (*nix)
                    """
                    print "Exit py signal {signal}".format(signal=args[0])
                    remove(pid_path)

                atexit.register(exit_handler)
                signal.signal(signal.SIGINT, signal_handler)
                signal.signal(signal.SIGTERM, signal_handler)

                worker_instance.work()

                # Remove pid file if the process can not catch signals
                remove(pid_path)

            self.worker_process = Process(target=worker_wrapper, kwargs={
                'worker_instance': worker,
                'pid_path': worker_pid_path
            })
            self.worker_process.start()
            worker_pid_file = open(worker_pid_path, 'w')
            worker_pid_file.write("%d" % self.worker_process.pid)
            worker_pid_file.close()

            print "Start a worker process with PID=%d" % \
                  self.worker_process.pid

    def commit(self):
        """
        Saving data from memory to disk.
        """
        self.connection.bgsave()
