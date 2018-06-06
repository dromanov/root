'''
Handles creating, rendering and editing nodes of the text based game.
'''
import os
import glob
import pprint

import tornado.web

import quest_action

__all__ = ["game_routes"]


def list_nodes():
    """List all nodes for the drop-down menus, etc."""
    res = {}
    for name in glob.glob( "stages/game_nodes/node_*.dat"):
        node_id = name[len("stages/game_nodes/node_"):-4]
        res[node_id] = _load_node(node_id)
    return res


def _load_node(node_id):
    filename = "stages/game_nodes/node_%s.dat" % node_id
    data = {}
    if os.path.isfile(filename):
        data = eval(open("stages/game_nodes/node_%s.dat" % node_id,
                         encoding="utf-8").read())
    data['nik'] = node_id
    return data


def _save_node(node_id, data):
    with open("stages/game_nodes/node_%s.dat" % node_id, "w",
              encoding="utf-8") as output_stream:
        pprint.pprint(data, output_stream)


class GameNodeHandler(tornado.web.RequestHandler):
    def get(self, node_id):
        data = _load_node(node_id)
        action_details = quest_action.load_actions(data.get('actions', []))
        self.render("game_node.html", data=data, action_details=action_details)


class GameNodeEditorHandler(tornado.web.RequestHandler):
    def get(self, node_id):
        data = _load_node(node_id)
        action_details = quest_action.load_actions(data.get('actions', []))
        self.render("game_node_editor.html", data=data,
                    action_menu=quest_action.package_resources(),
                    action_details=action_details,
                    nodes=list_nodes())

    def post(self, node_id):
        args = _load_node(node_id)
        for _key in self.request.arguments.keys():
            v = self.get_arguments(_key)
            if isinstance(v, list) and len(v) == 1:
                v = v[0]
            args[_key] = v
        del args["_xsrf"]
        _save_node(node_id, args)
        self.redirect(node_id)


def link_action(node_id, action_id):
    data = _load_node(node_id)
    data['actions'] = data.get('actions', []) + [action_id]
    _save_node(node_id, data)


game_routes = [
    (r"/game_node/(.*)", GameNodeHandler),
    (r"/game_node_editor/(.*)", GameNodeEditorHandler),
]
