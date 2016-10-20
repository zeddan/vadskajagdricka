import os
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for

app = Flask(__name__)
app.config.from_object('src.settings')
app.url_map.strict_slashes = False
handler = RotatingFileHandler('errors.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)

import src.controllers
