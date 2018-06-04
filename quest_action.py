"""
Handles creating, rendering and editing 'quest actions': links between nodes.

Quest action may be:
 * transition from one node to another (Link): one of the good or bad answers;
 * free form answer or other sentence (Question): password with two or more
   possible outcomes;
 * general transformation (Action): test against quest item and some
   transformation of the item and/or hero.

What do actions have in common:
 * unique id;
 * the node they are attached to;
 * few node ids used as an arguments to a decision-making function (below);
 * additional parameters and functions: Python data/code, of course;
 * transition effects: pop-up dialog, etc; these are Javascript/HTML.
"""

import os
import uuid
import pprint

import tornado.web

import quest

__all__ = ["game_action_routes", "make_html"]


def _load_action(action_id):
    data = eval(open("stages/game_actions/action_%s.dat" % action_id,
                     encoding="utf-8").read())
    data['id'] = action_id
    return data


def _save_action(action_id, data):
    with open("stages/game_actions/action_%s.dat" % action_id, "w",
              encoding="utf-8") as output_stream:
        pprint.pprint(data, output_stream)


class ActionHandler(tornado.web.RequestHandler):
    def get(self, action_id):
        data = eval(open("stages/game_actions/action_%s.dat" % action_id,
                         encoding="utf-8").read())
        data['nik'] = action_id
        self.render("game_action.html", data=data)


class EditActionHandler(tornado.web.RequestHandler):
    def get(self, node_id, action_id):
        print("Editing action '{action_id:.5}...' @ '{node_id}'"
              .format(**locals()))
        action = _load_action(action_id)
        action['node_id'] = node_id
        self.render("game_action_editor.html", action=action)

    def post(self, node_id, action_id):
        args = {}
        for k, v in self.request.arguments.items():
            args[k] = v
            if isinstance(v, list) and len(v) == 1:
                args[k] = v[0]
            args[k] = args[k].decode('utf8')
        del args["_xsrf"]
        output_stream = open("stages/game_actions/action_%s.dat" % action_id,
                             "w",
                             encoding="utf-8")
        pprint.pprint(args, output_stream)
        self.redirect("%s" % action_id)


class NewActionHandler(tornado.web.RequestHandler):
    def get(self):
        args = {}
        for k, v in self.request.arguments.items():
            args[k] = v
            if isinstance(v, list) and len(v) == 1:
                args[k] = v[0]
            args[k] = args[k].decode('utf8')
        # TODO: add protection against xsrf attack.
        # del args["_xsrf"]
        action_id = uuid.uuid4().hex
        output_stream = open("stages/game_actions/action_%s.dat" % action_id,
                             "w",
                             encoding="utf-8")
        pprint.pprint(args, output_stream)
        quest.link_action(args['node_id'], action_id)
        self.redirect("../game_node/%s" % args['node_id'])


def render_to_html(action_id):
    return "DUMMY_MAKE({})".format(action_id)


game_action_routes = [
    (r"/action/(.*)", ActionHandler),
    (r"/action_new", NewActionHandler),
    (r"/action_edit/([^/]*)/(.*)", EditActionHandler),
]
