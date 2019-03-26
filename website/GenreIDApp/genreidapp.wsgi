#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/GenreIDApp/")

from GenreIDApp import app as application

#from werkzeug.debug import DebuggedApplication 
#application = DebuggedApplication(app, True)

application.secret_key = 'Add your secret key'
