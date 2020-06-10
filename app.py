import flask
from flask import render_template, request, jsonify, redirect

from event_handler import EventHandler
import events_api

app = flask.Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Home page. Displays page to visualize all events and handles addition of new events.
    """
    if request.method == 'POST':
        eventType = request.form['eventType']
        eventTitle = request.form['eventTitle']
        eventDescription = request.form['eventDescription']

        try:
            events_api.insertEvent(eventType, eventTitle, eventDescription)
            return redirect('/')
        except:
            return 'There was an issue adding your event'

    else:
        events = events_api.getAllEvents()
        return render_template('home.html', events=events)

@app.route('/api/events/all', methods=['GET'])
def api_all():
    """
    Returns all events in database in JSON format.
    """
    return jsonify(events_api.getAllEvents())

@app.route('/api/events', methods=['GET'])
def api_filter():
    """
    Returns events, filtered by the specified parameters, in JSON format.
    Only the keys 'date', 'eventType' and 'eventTitle' will be processed.
    """
    query_parameters = request.args

    # If no filter criteria is specified then all events are returned.
    if not query_parameters:
        return api_all()

    results = events_api.getEventsByFilter(query_parameters)

    if not results:
            return page_not_found(404)

    return jsonify(results)

@app.errorhandler(404)
def page_not_found(e):
    """
    Handles unexpected requests.
    """
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()