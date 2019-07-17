from sys import path as moduleSearchPath
from os import chdir
from os.path import realpath
from pathlib import Path


applicationPath = str(Path(realpath(__file__)).parent.parent)
moduleSearchPath.insert(0, applicationPath)
chdir(applicationPath)


from wsgi.flask import app as application

