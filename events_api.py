from event_handler import EventHandler

def initDatabase(clearDatabase:bool = False):

    eHandler = EventHandler()

    eHandler.createDatabase(clearDatabase)

def getAllEvents():
    
    eHandler = EventHandler()

    all_events = eHandler.getAllEvents()

    return all_events


def getEventsByFilter(query_parameters):

    eHandler = EventHandler()

    events = eHandler.getEventByFilter(query_parameters)

    return events


def insertEvent(eventType:str, eventTitle:str, eventDescription:str):

    eHandler = EventHandler()

    eHandler.insertEvent(eventType, eventTitle, eventDescription)
