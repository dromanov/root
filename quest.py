'''
Handles creating, rendering and editing nodes of the text based game.
'''
import os
import glob
import uuid
import pprint

import tornado.web

import quest_action

import quest_traveller

__all__ = ["game_routes"]


traveller = quest_traveller.TravellerAPI()

users = {}


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("pointer_user")


class LoginHandler(BaseHandler):
    # `async` to handle a slow disk I/O?
    # https://github.com/tornadoweb/tornado/blob/stable/demos/blog/blog.py#L206
    def get(self):
        names = []
        filename = "stages/login.dat"
        if os.path.isfile(filename):
            # TODO: tell Victoria about the encoding bug here.
            names = eval(open(filename, encoding='utf-8').read())
        self.render("login.html", names=names)

    def post(self):
        name = self.get_argument("name")
        users[name] = quest_traveller.TravellerAPI()
        if not self.get_secure_cookie("pointer_user"):
            user = uuid.uuid4().hex
            # TODO: One should implement BaseClass::get_current_user()
            # and name the cookie below accordingly
            # [http://www.tornadoweb.org/en/stable/guide/security.html]
            self.set_secure_cookie("pointer_user", user)
        self.redirect("/game_node/start")


class GraphHandler(tornado.web.RequestHandler):
    def get(self):
        nodes = []
        for name in glob.glob( "stages/game_nodes/node_*.dat"):
           nodes.append(name[len("stages/game_nodes/node_"):-4])
        source = []
        target = []

        for name in glob.glob( "stages/game_actions/action_*.dat"):
            s = ''
            t = ''
            file = open(name)
            for _str in file:
                for node in nodes:
                    if _str.find(str(node)) != -1:
                         if _str.find("node_id") != -1:
                             s = node   
                         if _str.find("the_action") != -1:
                             t = node          
            source.append(s)
            target.append(t)
            # link[source] = target
            file.close()                
        self.render("graph.html", _nodes=nodes, _source=source, _target=target)


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


class GameNodeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, node_id):
        name = tornado.escape.xhtml_escape(self.current_user)
        print("User:", name)

        data = _load_node(node_id)

        _TODO = self.get_argument('do', '')
        if _TODO == 'execute':
            action_id = self.get_argument("action_id")
            assert action_id in data['actions'], "no such action here!"
            action = quest_action.load_action(action_id).get('the_action', '')
            exec(action, {'me': traveller})
            new_location = traveller.pop_location()
            if new_location:
                self.redirect("/game_node/" + new_location)
            else:
                self.redirect(node_id)
            return None

        action_details = quest_action.load_actions(data.get('actions', []))
        self.render("game_node.html", data=data, action_details=action_details)


class GameNodeEditorHandler(BaseHandler):
    """Complex handler with GET and POST channels.
    GET:
        the operation is set in parameter `do` and handles action editing.

    POST:
        receives the data and updates the node and the action being edited.
    """
    @tornado.web.authenticated
    def get(self, node_id):
        name = tornado.escape.xhtml_escape(self.current_user)
        print("User:", name)

        data = _load_node(node_id)
        _TODO = self.get_argument('do', '')
        if _TODO == 'delete':
            _id = self.get_argument('action_id')
            data['actions'].pop(data['actions'].index(_id))
            _save_node(node_id, data)
            self.redirect(node_id)
            return
        elif _TODO == 'edit':
            data['action_to_edit'] = self.get_argument('action_id')
        elif _TODO == "create_new_action":
            action_id = uuid.uuid4().hex
            action = {
                'type': self.get_argument("type"),
                'id': action_id,
                'node_id': node_id
            }
            quest_action.save_action(action_id, action)
            link_action(node_id, action_id)
            self.redirect("?do=edit&action_id=%s" % action_id)
            return
        elif _TODO == 'move_right':
            action_id = self.get_argument("action_id")
            _actions = data['actions']
            if action_id in _actions:
                i = _actions.index(action_id)
                _a = _actions.pop(i)
                _actions.insert(min(len(_actions), i+1), _a)
            _save_node(node_id, data)
        elif _TODO == 'move_left':
            action_id = self.get_argument("action_id")
            _actions = data['actions']
            if action_id in _actions:
                i = _actions.index(action_id)
                _a = _actions.pop(i)
                _actions.insert(max(0, i-1), _a)
            _save_node(node_id, data)

        action_details = quest_action.load_actions(data.get('actions', []))
        self.render("game_node_editor.html", data=data,
                    action_menu=quest_action.package_resources(),
                    action_details=action_details,
                    nodes=list_nodes())

    @tornado.web.authenticated
    def post(self, node_id):
        name = tornado.escape.xhtml_escape(self.current_user)
        print("User:", name)

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
            quest_action.update_action(args['id'], args)
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
