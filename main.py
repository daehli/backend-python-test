"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app, db
from alayatodo.fixtures import init_fixture

if __name__ == '__main__':
    args = docopt(__doc__)  
    if args['initdb']:
        db.create_all()
        init_fixture()
        print "AlayaTodo: Database initialized."
    else:
        app.run(use_reloader=True)
