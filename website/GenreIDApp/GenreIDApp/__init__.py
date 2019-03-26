from flask import Flask

app = Flask(__name__)
from GenreIDApp import routes

app.debug = True

