#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid

from time import time, sleep

from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line

from remote_mouse_cursor import PointerNewUserHandler, \
    PointerDropUserHandler, PointerNewPositionHandler, PointerUpdateHandler

from quest import game_routes, LoginHandler, GraphHandler


define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

TIME_ROOT = 1495539784.0


def checkpoint(msg):
    print("%7.3f: %s" % (time() - TIME_ROOT, msg))
    sleep(1.0)
    assert False, "no one should have called me"


class MessageBuffer(object):
    def __init__(self):
        self.waiters = set()
        self.cache = []
        self.cache_size = 200

    def wait_for_messages(self, cursor=None):
        # Construct a `Future` to return to our caller. This allows
        # `wait_for_messages` to be yielded from a coroutine even though
        # it is not a coroutine itself.  We will set the result of the
        # `Future when` results are available.
        result_future = Future()
        if cursor:
            new_count = 0
            for msg in reversed(self.cache):
                if msg["id"] == cursor:
                    break
                new_count += 1
            if new_count:
                result_future.set_result(self.cache[-new_count:])
                return result_future
        self.waiters.add(result_future)
        return result_future

    def cancel_wait(self, future):
        self.waiters.remove(future)
        # Set an empty result to unblock any waiting coroutines.
        future.set_result([])

    def new_messages(self, messages):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        # checkpoint(">>> new_messages(%r)" % messages)
        for future in self.waiters:
            future.set_result(messages)
        self.waiters = set()
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]


# Making this a non-singleton is left as an exercise for the reader.
global_message_buffer = MessageBuffer()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        args = {}
        for k, v in self.request.arguments.items():
            args[k] = v
            if isinstance(v, list) and len(v) == 1:
                args[k] = v[0]
            args[k] = args[k].decode('utf8')
        # cursor = self.get_argument("cursor", None)
        if 'name' in args:
            pupils[args['name']] = 'finals'

        self.render("index.html", messages=global_message_buffer.cache)


class MessageNewHandler(tornado.web.RequestHandler):
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body"),
        }
        # 'to_basestring' is necessary for Python 3's json encoder, which
        # doesn't accept byte strings.
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        global_message_buffer.new_messages([message])


class MessageUpdatesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        cursor = self.get_argument("cursor", None)
        # checkpoint(">>> MsgUpdateHandler(%r)" % cursor)
        # Save the future returned by wait_for_messages so we can cancel
        # it in wait_for_messages
        self.future = global_message_buffer.wait_for_messages(cursor=cursor)
        # checkpoint(">>> MsgUpdateHandler - before yield...")
        messages = yield self.future
        # checkpoint(">>> MsgUpdateHandler - after yield, messages = %r" %
        #            messages)
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        global_message_buffer.cancel_wait(self.future)


pupils = {
}


class QuestHandler(tornado.web.RequestHandler):
    def get(self, milestone):
        # checkpoint(">>> Quest %s" % milestone)
        args = {}
        for k, v in self.request.arguments.items():
            args[k] = v
            if isinstance(v, list) and len(v) == 1:
                args[k] = v[0]
            args[k] = args[k].decode('utf8')
        # cursor = self.get_argument("cursor", None)
        if 'name' in args:
            pupils[args['name']] = milestone
        self.render("quest_%s.html" % milestone, args=args)


class TeacherMapHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("teacher_map.html", pupils=pupils)


class TeacherMapDataHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({'pupils': list(pupils.items())})
        

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/quest/(.*)", QuestHandler),
            (r"/teacher", TeacherMapHandler),
            (r"/login", LoginHandler),
            (r"/graph", GraphHandler),
            (r"/a/teacher", TeacherMapDataHandler),
            (r"/a/message/new", MessageNewHandler),
            (r"/a/message/updates", MessageUpdatesHandler),
            (r"/a/pointer/updates", PointerUpdateHandler),
            (r"/a/pointer/new_user", PointerNewUserHandler),
            (r"/a/pointer/drop_user", PointerDropUserHandler),
            (r"/a/pointer/new_position", PointerNewPositionHandler),
        ]
        + game_routes,
        cookie_secret=uuid.uuid4().hex,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        login_url=r"/login",
        xsrf_cookies=True,
        debug=options.debug,
    )
    print("App is listening to the port", options.port)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
