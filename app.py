import flask
from flask import request, jsonify
import sqlite3

from event_handler import EventHandler

import events_api

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Event Reader</h1>
              <p>API for reading events</p>
           '''

@app.route('/api/events/all', methods=['GET'])
def api_all():

    return jsonify(events_api.getAllEvents())

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/events', methods=['GET'])
def api_filter():
    query_parameters = request.args

    if not query_parameters:
        return api_all()

    results = events_api.getEventsByFilter(query_parameters)

    if not results:
            return page_not_found(404)

    return jsonify(results)

app.run()