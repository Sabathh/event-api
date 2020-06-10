from event_handler import EventHandler

def initDatabase(clearDatabase:bool = False):
    """
    Initializes events database. 
    Can optionally clear previously existing data.

    Args:
        clearDatabase (bool, optional): to true to clear previously existing data. Defaults to False.
    """
    eHandler = EventHandler()
    eHandler.createDatabase(clearDatabase)

def getAllEvents():
    """
    Retrieves all the events stored in the database.add()

    Returns:
        list: List containing the events stored in the table. Each event is a dictionary
    """
    eHandler = EventHandler()

    all_events = eHandler.getAllEvents()

    return all_events


def getEventsByFilter(query_parameters):
    """
    Retrieves all the events matching the specified filters 
    for the 'date', 'eventType' and 'eventTitle' parameters.

    Args:
        query_parameters (dict): Dictionary containing the filter specifications. 
                                 Only the keys 'date', 'eventType' and 'eventTitle' will be processed.

    Returns:
        list: List of containing the events stored in the table. Each event is a dictionary
    """
    eHandler = EventHandler()

    events = eHandler.getEventByFilter(query_parameters)

    return events


def insertEvent(eventType:str, eventTitle:str, eventDescription:str):
    """
    Inserts an event into the database.

    Args:
        eventType (str): Type of the event
        eventTitle (str): Title of the event
        eventDescription (str): Description of the event
    """
    eHandler = EventHandler()

    eHandler.insertEvent(eventType, eventTitle, eventDescription)
