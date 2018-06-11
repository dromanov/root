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
import pprint


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


def load_actions(actions):
    """Packs actions with full data for external renderer @ node editor."""
    icons, links, _ = zip(*package_resources(include_separators=False))
    pack = dict(zip(links, icons))
    res = dict((_id, _load_action(_id)) for _id in actions)
    for k in res:
        res[k]['icon'] = pack[res[k]['type']]
    return res
