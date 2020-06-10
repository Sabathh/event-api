from event_handler import EventHandler

def getAllEvents():
    
    eHandler = EventHandler()

    all_events = eHandler.getAllEvents()

    return all_events


def getEventsByFilter(query_parameters):

    eHandler = EventHandler()

    events = eHandler.getEventByFilter(query_parameters)

    return events

