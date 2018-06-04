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

__all__ = "game_action_routes make_html package_resources".split()


def package_resources(include_separators=True):
    """List of actions; used here and in the node editor."""
    icons = "random record check --- wrench --- edit".split()
    links = "simple radio  check --- code   --- input".split()
    labels = '''
        Варианты выбора: простые переходы
        Варианты выбора: радио-кнопки
        Варианты выбора: чек-боксы
        ---
        Игровая логика на Питоне
        ---
        Вопрос со свободным ответом (проверка тьютором)
    '''.strip('\n').split('\n')
    pkg = zip(icons, links, labels)
    if not include_separators:
        pkg = [x for x in pkg if x[0] != "---"]
    return pkg


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
        self.render("game_action_editor.html",
                    action=action,
                    actions=package_resources(include_separators=False))

    def post(self, node_id, action_id):
        args = _load_action(action_id)
        for k, v in self.request.arguments.items():
            args[k] = v
            if isinstance(v, list) and len(v) == 1:
                args[k] = v[0]
            args[k] = args[k].decode('utf8')
        del args["_xsrf"]
        _save_action(action_id, args)
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


class NewSimpleActionHandler(tornado.web.RequestHandler):
    def get(self, node_id):
        action_id = uuid.uuid4().hex
        action = {
            'type': 'simple',
            'id': action_id,
            'node_id': node_id
        }
        _save_action(action_id, action)
        quest.link_action(node_id, action_id)
        self.redirect("/action_edit/simple/%s/%s" % (node_id, action_id))


class EditSimpleActionHandler(tornado.web.RequestHandler):
    def get(self, node_id, action_id):
        action = _load_action(action_id)
        action['node_id'] = node_id
        self.render("game_simple_action_editor.html",
                    action=action)

    def post(self, node_id, action_id):
        args = _load_action(action_id)
        for k, v in self.request.arguments.items():
            args[k] = v
            if isinstance(v, list) and len(v) == 1:
                args[k] = v[0]
            args[k] = args[k].decode('utf8')
        del args["_xsrf"]
        _save_action(action_id, args)
        self.redirect("/game_node_editor/%s" % node_id)


def render_to_html(action_id):
    return "DUMMY_MAKE({})".format(action_id)


def load_actions(actions):
    icons, links, _ = zip(*package_resources(include_separators=False))
    pack = dict(zip(links, icons))
    res = dict((_id, _load_action(_id)) for _id in actions)
    for k in res:
        res[k]['icon'] = pack[res[k]['type']]
    return res


game_action_routes = [
    (r"/action/(.*)", ActionHandler),
    (r"/action_new/simple/(.*)", NewSimpleActionHandler),
    (r"/action_edit/simple/([^/]*)/(.*)", EditSimpleActionHandler),
    (r"/action_edit/([^/]*)/(.*)", EditActionHandler),
]
