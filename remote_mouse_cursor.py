#!/usr/bin/env python

"""
API to manage several mouse pointers on single page.

Engine structure is taken from tornado example `chat`, long poll version:
    https://github.com/tornadoweb/tornado/tree/master/demos/chat
"""

import logging
import uuid

import tornado.web


from tornado.concurrent import Future
from tornado import gen


class PointersStorage(object):
    def __init__(self):
        self.positions = {}
        self.waiters = set()
        self.version = 0

    def wait_for_positions(self, version=0):
        # Construct a Future to return to our caller.  This allows
        # wait_for_messages to be yielded from a coroutine even though
        # it is not a coroutine itself.  We will set the result of the
        # Future when results are available.
        result_future = Future()
        if version < self.version:
            result_future.set_result({'positions': list(self.positions.items()),
                                      'version': self.version})
            return result_future
        self.waiters.add(result_future)
        return result_future

    def cancel_wait(self, future):
        self.waiters.remove(future)
        # Set an empty result to unblock any coroutines waiting.
        future.set_result({})

    def __send_all_futures(self):
        for future in self.waiters:
            future.set_result({'positions': list(self.positions.items()),
                               'version': self.version})
        self.waiters = set()

    def new_position(self, user, position):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        self.version += 1
        self.positions.update({user: position})
        self.__send_all_futures()

    def new_user(self, user, position):
        logging.info("Adding new user: %s", user)
        self.version += 1
        self.positions.update({user: position})
        self.__send_all_futures()

    def drop_user(self, user):
        logging.info("Forgetting user: %s", user)
        self.version += 1
        del self.positions[user]
        self.__send_all_futures()


# Making this a non-singleton is left as an exercise for the reader.
pointers = PointersStorage()


class PointerNewUserHandler(tornado.web.RequestHandler):
    def post(self):
        if not self.get_secure_cookie("pointer_user"):
            user = uuid.uuid4().hex
            self.set_secure_cookie("pointer_user", user)
            self.write(user)
            pointers.new_user(user, self.get_argument("position", {'x': 0,
                                                                   'y': 0}))
        else:
            self.write("You are here already!")


class PointerDropUserHandler(tornado.web.RequestHandler):
    def post(self):
        user = self.get_secure_cookie("pointer_user")
        if user:
            self.clear_cookie("pointer_user")
            self.write("Bye!")
            pointers.drop_user(user)
        else:
            self.write("Who are you?!")


class PointerNewPositionHandler(tornado.web.RequestHandler):
    def post(self):
        user = self.get_secure_cookie("pointer_user").decode("utf-8")
        if user:
            x, y = [int(self.get_argument(k)) for k in "x y".split()]
            logging.debug("received new coordinates: %s", (x, y))
            pointers.new_position(user, {'x': x, 'y': y})
        else:
            self.write("You are not registered!")


class PointerUpdateHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        if not self.get_secure_cookie("pointer_user"):
            logging.critical("unregistered user polls the data!")
        version = int(self.get_argument("version", 0))
        logging.debug("version: %d", version)
        # Save the future returned by `wait_for_positions` so we can cancel
        # it in `wait_for_positions`.
        self.future = pointers.wait_for_positions(version=version)
        positions = yield self.future
        if self.request.connection.stream.closed():
            return
        self.write(positions)

    def on_connection_close(self):
        pointers.cancel_wait(self.future)
