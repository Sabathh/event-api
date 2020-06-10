# Event Handler API

API developed to store and query events that happened in the company. The events can be retrieved both via a Python API or REST API.

For more details please refer to the documentation available in the source code

## Database Schema

The Database contains a single table responsible for storing the event data. It is organized in the following format:

 - date (text) : Date the event was inserted. Format is DD/MM/YYYY, hh:mm:ss
 - eventType (text) : Type of the event
 - eventTitle (text) : Title of the event
 - eventDescription (text) : Brief description of the event

## Python API

The Python API has the following methods:

- initDatabase : Initializes the events table in the database. Can optionally clear the existing data.
- getAllEvents : Returns all events in the database
- getEventsByFilter: Returns events according to specified filters
- insertEvent : Inserts a new event

## Webpage

The main page contains a list of all events in the database organized in a table, as well as a field to add new events.

In order to start the webserver run the file _app.py_. The main page will be available at http://localhost:5000/

The following routes can be used to interact with the database:

- _/api/events_ : Returns events filtered according to the specified parameters in JSON format (e.g. /api/events?eventType=Release returns a JSON with all events containing eventType='Release').
- _/api/events/all_ : Returns all events in the database in JSON format
