Step 1
======

$ mkvirtualenv tornado_timetable
$ mkdir tornado_timetable
$ cd tornado_timetable
$ pip install tornado
$ python
>>> import tornado
>>> tornado.version
4.3

Step 2
======
$ workon peopleware

(!) Make absolute path (after all symbolic links stripped) to be unicode free,
    otherwise one can get UnicodeDecodeError.

    If you want to work in Russian-named-folder, create real folder in clean
    place and place the symlink into Russian folder to work there.

Step 3
======
Freeze and install the requirements:
    $ pip freeze > requirements.txt
    $ pip install -r requirements.txt
