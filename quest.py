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
    """Complex handler with GET and POST channels.
    GET:
        the operation is set in parameter `do` and handles action editing.

    POST:
        receives the data and updates the node and the action being edited.
    """
    def get(self, node_id):
        data = _load_node(node_id)
        action_details = quest_action.load_actions(data.get('actions', []))
        if self.get_argument('do', '') == 'delete':
            _id = self.get_argument('action_id')
            data['actions'].pop(data['actions'].index(_id))
            _save_node(node_id, data)
            self.redirect(node_id)
            return
        elif self.get_argument('do', '') == 'edit':
            data['action_to_edit'] = self.get_argument('action_id')

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

        # Optionally create new location (node).
        new_node_name = args.get("make_new_node", "")
        if new_node_name:
            if new_node_name.isalnum():
                self.redirect("/game_node_editor/%s" % new_node_name)
            else:
                self.redirect("/game_node_editor/%s" % node_id)
            return

        if self.get_argument('do', '') == 'save_edited_simple_action':
            args = {k.split(".")[1]: v for k, v in args.items()
                    if k.startswith("action.")}
            print(args)
            self.redirect(node_id)
            return

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
