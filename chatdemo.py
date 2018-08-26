#!/usr/bin/env python
#
# Copyright (c) 2018 Victoria Isaeva, Dmitry V. Romanov
#

import uuid
import os.path

import tornado.escape
import tornado.ioloop
import tornado.web

from tornado.options import define, options, parse_command_line

from quest import (game_routes, LoginHandler, GraphHandler, TeacherMapHandler1,
                   TeacherMapDataHandler1, TableHandler)

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/graph", GraphHandler),
            (r"/table", TableHandler),
            (r"/teacher1", TeacherMapHandler1),
            (r"/a/teacher1", TeacherMapDataHandler1),            
            (r"/images/(.*)", tornado.web.StaticFileHandler,
                {'path': os.path.join(os.getcwd(), './images')}),
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
