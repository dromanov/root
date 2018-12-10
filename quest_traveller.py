"""
Helper class to manage all transformation of the user when (s)he travels.

"""
import os
import glob
import uuid

# Folder for all users to store their images in.
__UPLOADS__ = './images/'


class TravellerAPI:
    """API exposed to the actions."""
    sessions = {}

    def __init__(self, name):
        self.score = 0
        self.story = []
        self.new_location = "0_plan"  # `0_plan` is the start of the quest.
        self.name = name
        self._history = []

    def goto(self, place):
        self.new_location = place

    def pop_location(self):
        return self.new_location

    def remember(self, item):
        self._history.append(item)

    def get_history(self):
        return self._history

    def save_image(self, node_id, fileinfo):
        fname = fileinfo['filename']
        extn_name, extn_type = os.path.splitext(fname)
        cname = '_'.join([node_id, self.name, extn_name,
                          uuid.uuid4().hex, extn_type])
        open(os.path.join(__UPLOADS__, cname), 'wb').write(fileinfo['body'])

    def list_saved_images(self, node_id):
        print(os.path.join(__UPLOADS__, '_'.join([node_id, self.name])))
        filenames = glob.glob(os.path.join(__UPLOADS__,
                                           '_'.join([node_id,
                                                     self.name,
                                                     '*'])))
        # I use relative path here, but the site requires the absolute path.
        return [f.lstrip('.') for f in filenames]

    def to_txt(self):
        dump = [self.score, self.story, self.name, self._history, self.story,
                self.new_location]
        return repr(dump)

    def update_from_txt(self, dump_):
        (self.score, self.story, self.name, self._history, self.story,
         self.new_location) = eval(dump_)
