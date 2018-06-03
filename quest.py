'''
Handles creating, rendering and editing nodes of the text based game.
'''

import os
import pprint

import tornado.web


__all__ = ["game_routes"]


def _load_node(node_id):
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
        self.render("game_node.html", data=data)


class GameNodeEditorHandler(tornado.web.RequestHandler):
    def get(self, node_id):
        data = {}
        datafile = "stages/game_nodes/node_%s.dat" % node_id
        if os.path.isfile(datafile):
            data = eval(open(datafile,
                             encoding="utf-8").read())
        data['nik'] = node_id
        icons = "arrow-right record check --- wrench --- edit".split()
        links = "simple      radio  check --- code   --- input".split()
        labels = '''
            Варианты выбора: простой переход
            Варианты выбора: радио-кнопки
            Варианты выбора: чек-боксы
            ---
            Игровая логика на Питоне
            ---
            Вопрос со свободным ответом (проверка тьютором)
        '''.strip('\n').split('\n')
        self.render("game_node_editor.html", data=data,
                    action_menu=zip(icons, links, labels))

    def post(self, node_id):
        args = _load_node(node_id)
        for k, v in self.request.arguments.items():
            args[k] = v
            if isinstance(v, list) and len(v) == 1:
                args[k] = v[0]
            args[k] = args[k].decode('utf8')
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
