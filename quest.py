"""
Handles creating, rendering and editing nodes of the text based game.
"""
import atexit
import os
import re
import glob
import uuid
import pprint

from copy import deepcopy

import tornado.web

import quest_action
import quest_traveller

__all__ = ("game_routes LoginHandler ResetHandler GraphHandler "
           "TeacherMapHandler1 TeacherMapDataHandler1 "
           "UserStatisticHandler").split()

secret = 1
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
        self.set_secure_cookie("secret", str(secret + 1))
        print(secret)
        if os.path.isfile(filename):
            names = eval(open(filename, encoding='utf-8').read())
        self.render("login.html", names=names)

    def post(self):
        name = self.get_argument("name")
        if not self.get_secure_cookie("pointer_user"):
            # user = uuid.uuid4().hex
            # TODO: One should implement BaseClass::get_current_user()
            #   and name the cookie below to match the one in
            #   `BaseHandler::get_current_user` (line 23).
            #   [http://www.tornadoweb.org/en/stable/guide/security.html]
            self.set_secure_cookie("pointer_user", name)
        if name not in users:
            users[name] = quest_traveller.TravellerAPI(name)
        self.redirect(f"/game_node/{users[name].pop_location()}")


class ResetHandler(tornado.web.RequestHandler):
    def get(self):
        global secret
        secret += 1
        self.clear_cookie("point_user")
        self.redirect("/game_node/0_plan")


class TeacherMapHandler1(tornado.web.RequestHandler):
    def get(self):
        all_nodes = list_nodes()
        node_ids = list(all_nodes.keys())
        self.render("teacher_map1.html", users=users, _nodes=node_ids)


class TeacherMapDataHandler1(tornado.web.RequestHandler):
    def get(self):
        self.write({'users': list(users.items())})


class GraphHandler(tornado.web.RequestHandler):
    def get(self):
        level_types = ["easy_level", "medium_level", "hard_level",
                       "fine_level", "organizational"]

        all_nodes = list_nodes()
        node_ids = list(all_nodes.keys())
        levels = [all_nodes[node].get("level", "") for node in node_ids]
        if any([l not in level_types + [""] for l in levels]):
            print("Unknown levels: {}".format(set(levels) - set(level_types)))

        source = []
        target = []
        edge_class = []
        for node_id, node in all_nodes.items():
            actions = quest_action.load_actions(node.get("actions", []))
            for action_id in actions:
                def parse_action(action):
                    """Simple heuristic to get the purpose of the action:
                        score +=    True
                        score -=    False
                        goto(dest)  Transition
                    """
                    res = {
                        'edge': 'unknown',
                        'targets': [],
                    }
                    the_action = action.get("the_action", "")
                    if re.search(r"me\.score\s*\+", the_action):
                        res['edge'] = 'true'
                    elif re.search(r"me\.score\s*-", the_action):
                        res['edge'] = 'false'

                    for dest in re.findall(r'''me\.goto\s*\(['"](\w+)['"]\)''',
                                           the_action):
                        res['targets'].append(dest)
                    if len(res['targets']) > 1:
                        print("I need more brains here!")
                    return res

                the_path = parse_action(quest_action.load_action(action_id))
                for destination in the_path['targets']:
                    source.append(node_id)
                    target.append(destination)
                    edge_class.append(the_path['edge'])

        self.render("graph.html",
                    _nodes=node_ids,
                    _source=source,
                    _target=target,
                    node_classes=levels,
                    edge_classes=edge_class)


class TableHandler(tornado.web.RequestHandler):
    def get(self):
        level_types = ["easy_level", "medium_level", "hard_level",
                       "fine_level", "organizational"]

        all_nodes = list_nodes()
        node_ids = list(sorted(all_nodes.keys()))
        levels = [all_nodes[node].get("level", "") for node in node_ids]
        if any([l not in level_types + [""] for l in levels]):
            print("Unknown levels: {}".format(set(levels) - set(level_types)))

        def score(name):
            history = users[name].get_history()
            scores = (h['delta_score'] for h in history)
            positive = sum(h for h in scores if h > 0)
            negative = sum(h for h in scores if h < 0)
            return positive, negative

        pupils_scores = [(p, score(p)) for p in users]
        self.render("table.html",
                    nodes=node_ids,
                    titles={n: all_nodes[n].get("title") for n in node_ids},
                    user_names=sorted(users.keys()),
                    scores=pupils_scores,
                    user_data=users)


def list_nodes():
    """List all nodes for the drop-down menus, etc."""
    res = {}
    for name in glob.glob("stages/game_nodes/node_*.dat"):
        node_id = name[len("stages/game_nodes/node_"):-4]
        res[node_id] = _load_node(node_id)
    return res


def _load_node(node_id):
    filename = f"stages/game_nodes/node_{node_id}.dat"
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
        name_ = tornado.escape.xhtml_escape(self.current_user)
        traveller = users[name_]
        print("{} came to {}".format(traveller.name, node_id))

        data = _load_node(node_id)

        _TODO = self.get_argument('do', '')
        if _TODO == 'execute':
            action_id = self.get_argument("action_id")
            assert action_id in data['actions'], "no such action here!"
            action = quest_action.load_action(action_id).get('the_action', '')
            me_before = deepcopy(traveller)
            exec(action, {'me': traveller})
            traveller.remember({
                'node_id': node_id,
                'delta_score': traveller.score - me_before.score
            })
            new_location = traveller.pop_location()
            if new_location:
                self.redirect("/game_node/" + new_location)
            else:
                self.redirect(node_id)
            return None

        def hhmmss2sec(s):
            terms = s.split(":")
            res = 0
            while terms:
                res = res*60 + int(terms.pop(0))
            return res

        if data.get("youtube_from", "").strip():
            data["youtube_from"] = hhmmss2sec(data["youtube_from"])
        if data.get("youtube_to", "").strip():
            data["youtube_to"] = hhmmss2sec(data["youtube_to"])

        action_details = quest_action.load_actions(data.get('actions', []))
        self.render("game_node.html",
                    data=data,
                    traveller=traveller,
                    action_details=action_details,
                    images=traveller.list_saved_images(node_id))
        
    @tornado.web.authenticated
    def post(self, node_id):
        name = tornado.escape.xhtml_escape(self.current_user)
        traveller = users[name]
        fileinfo = self.request.files['filearg'][0]
        traveller.save_image(node_id, fileinfo)
        self.redirect(node_id)


class GameNodeEditorHandler(BaseHandler):
    """Complex handler with GET and POST channels.
    GET:
        the operation is set in parameter `do` and handles action editing.

    POST:
        receives the data and updates the node and the action being edited.
    """
    @tornado.web.authenticated
    def get(self, node_id):
        name_ = tornado.escape.xhtml_escape(self.current_user)
        traveller = users[name_]

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
        self.render("game_node_editor.html",
                    data=data,
                    action_menu=quest_action.package_resources(),
                    action_details=action_details,
                    nodes=list_nodes())

    @tornado.web.authenticated
    def post(self, node_id):
        name_ = tornado.escape.xhtml_escape(self.current_user)
        traveller = users[name_]
        print("User:", traveller.name)

        args = _load_node(node_id)
        for _key in self.request.arguments.keys():
            v = self.get_arguments(_key)
            if isinstance(v, list) and len(v) == 1:
                v = v[0]
            args[_key] = v
        del args["_xsrf"]

        _name = "require_img_uploader"
        args[_name] = (args.get(_name, False) == 'on')

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


class UserStatisticHandler(tornado.web.RequestHandler):
    def get(self, username):
        if username not in users:
            print(f"Unknown user: {username}")
            self.clear()
            self.set_status(400)
            self.finish(f"<html><head><meta charset='utf-8'/></head>"
                        f"<body>User `{username}` is not found.</body></html>")
            return

        all_nodes = list_nodes()
        node_ids = list(sorted(all_nodes.keys()))
        self.render("user_stat.html",
                    user_name=username,
                    user_path=users[username].get_history(),
                    titles={n: all_nodes[n].get("title") for n in node_ids})


class NodeStatisticHandler(tornado.web.RequestHandler):
    def get(self, node_id):
        def location_score(history):
            for h in history:
                if h['node_id'] == node_id:
                    return h['delta_score']
            return None

        location_stat = {k: location_score(v.get_history())
                         for k, v in users.items()
                         if location_score(v.get_history()) is not None}

        all_nodes = list_nodes()
        node_ids = list(sorted(all_nodes.keys()))
        self.render("node_stat.html",
                    node_id=node_id,
                    location_stat=location_stat,
                    titles={n: all_nodes[n].get("title") for n in node_ids})


def dump_database():
    with open('users.repr.txt', 'w') as fp:
        fp.write(repr({k: v.to_txt() for k, v in users.items()}))


def restore_from_database():
    try:
        with open('users.repr.txt') as fp:
            # TODO: Yes, yes, I know!
            data = eval(fp.read())
            for name, ascii_dump in data.items():
                users[name] = quest_traveller.TravellerAPI(name)
                users[name].update_from_txt(ascii_dump)
    except:
        pass


restore_from_database()
atexit.register(dump_database)

game_routes = [
    (r"/game_node/(.*)", GameNodeHandler),
    (r"/game_node_editor/(.*)", GameNodeEditorHandler),
]
