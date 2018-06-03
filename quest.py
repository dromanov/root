'''
Handles creating, rendering and editing nodes of the text based game.
'''

import os
import pprint

import tornado.web


__all__ = ["game_routes"]

class GameNodeHandler(tornado.web.RequestHandler):
    def get(self, node_id):
        data = eval(open("stages/game_nodes/node_%s.dat" % node_id,
                         encoding="utf-8").read())
        data['nik'] = node_id
        self.render("game_node.html", data=data)


class GameNodeEditorHandler(tornado.web.RequestHandler):
    def get(self, node_id):
        data = {}
        datafile = "stages/game_nodes/node_%s.dat" % node_id
        if os.path.isfile(datafile):
            data = eval(open(datafile,
                             encoding="utf-8").read())
        data['nik'] = node_id
        self.render("game_node_editor.html", data=data)

    def post(self, node_id):
        args = {}
        for k, v in self.request.arguments.items():
            args[k] = v
            if isinstance(v, list) and len(v) == 1:
                args[k] = v[0]
            args[k] = args[k].decode('utf8')
        del args["_xsrf"]
        output_stream = open("stages/game_nodes/node_%s.dat" % node_id, "w",
                             encoding="utf-8")
        pprint.pprint(args, output_stream)
        self.redirect("%s" % node_id)


game_routes = [
    (r"/game_node/(.*)", GameNodeHandler),
    (r"/game_node_editor/(.*)", GameNodeEditorHandler),
]
