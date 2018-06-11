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
    filename = "stages/game_actions/action_%s.dat" % action_id
    data = {}
    if os.path.isfile(filename):
        data = eval(open(filename, encoding="utf-8").read())
    data['id'] = action_id
    return data


def save_action(action_id, data):
    with open("stages/game_actions/action_%s.dat" % action_id, "w",
              encoding="utf-8") as output_stream:
        pprint.pprint(data, output_stream)


def update_action(action_id, patch):
    action = _load_action(action_id)
    action.update(patch)
    save_action(action_id, action)


class NewSimpleActionHandler(tornado.web.RequestHandler):
    def get(self, node_id):
        action_id = uuid.uuid4().hex
        action = {
            'type': 'simple',
            'id': action_id,
            'node_id': node_id
        }
        save_action(action_id, action)
        quest.link_action(node_id, action_id)
        self.redirect("/action_edit/simple/%s/%s" % (node_id, action_id))


class EditSimpleActionHandler(tornado.web.RequestHandler):
    def get(self, node_id, action_id):
        action = _load_action(action_id)
        action['node_id'] = node_id
        self.render("game_simple_action_editor.html",
                    action=action, nodes=quest.list_nodes())

    def post(self, node_id, action_id):
        args = _load_action(action_id)
        for _key in self.request.arguments.keys():
            v = self.get_arguments(_key)
            if isinstance(v, list) and len(v) == 1:
                v = v[0]
            args[_key] = v
        # TODO: does tornado check the _xsfr token automatically for me?
        del args["_xsrf"]

        new_node_name = args.get("make_new_node", "")
        if new_node_name:
            if new_node_name.isalnum():
                self.redirect("/game_node_editor/%s" % new_node_name)
            else:
                self.redirect("/game_node_editor/%s" % node_id)
            return

        save_action(action_id, args)
        self.redirect("/game_node_editor/%s" % node_id)


def render_to_html(action_id):
    return "DUMMY_MAKE({})".format(action_id)


def load_actions(actions):
    """Packs actions with full data for external renderer @ node editor."""
    icons, links, _ = zip(*package_resources(include_separators=False))
    pack = dict(zip(links, icons))
    res = dict((_id, _load_action(_id)) for _id in actions)
    for k in res:
        res[k]['icon'] = pack[res[k]['type']]
    return res


game_action_routes = [
    (r"/action_new/simple/(.*)", NewSimpleActionHandler),
    (r"/action_edit/simple/([^/]*)/(.*)", EditSimpleActionHandler),
]
