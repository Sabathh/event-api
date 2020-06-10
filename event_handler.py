import sqlite3
from datetime import datetime

class EventHandler():
    """
    Class responsible for interacting with SQLite database containing events occuring within the company
    """
    
    def __init__(self, dbFile:str = 'events.db'):
        """
        Constructor

        Args:
            dbFile (str, optional): Absolute or relative path to the database. Defaults to 'events.db'.
        """
        self.dbPath = dbFile
        
        self.tableName = 'events'
        self.date = 'date'
        self.eventType = 'eventType'
        self.eventTitle = 'eventTitle'
        self.eventDescription = 'eventDescription'

    def createDatabase(self, dropTable:bool = False):
        """
        Creates the events table in the database if it does not exist. 
        Can optionally clear previously existing table.

        Args:
            dropTable (bool, optional): Set to true to clear previously existing table. Defaults to False.
        """
        conn = sqlite3.connect(self.dbPath)

        if dropTable:
            conn.execute(f'''DROP TABLE IF EXISTS {self.tableName}''')

        conn.execute(f'''
                        CREATE TABLE IF NOT EXISTS {self.tableName}
                            ({self.date} text, {self.eventType} text, {self.eventTitle} text, {self.eventDescription} text)
                        ''')
        conn.commit()

    def insertEvent(self, eventType:str, eventTitle:str, eventDescription:str):
        """
        Inserts an event into the events table.

        Args:
            eventType (str): Type of the event
            eventTitle (str): Title of the event
            eventDescription (str): Description of the event
        """ 
        conn = sqlite3.connect(self.dbPath)

        eventDate = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
        
        conn.execute(f'''
                        INSERT INTO {self.tableName}
                            VALUES ('{eventDate}', '{eventType}', '{eventTitle}', '{eventDescription}')
        ''')
        conn.commit()

    def _dict_factory(self, cursor, row) -> dict:
        """
        Converts SQL query result into a dictionary to facilitate processing into JSON

        Args:
            cursor : Cursor object
            row : Tuple containing the original row of the query

        Returns:
            dict: Dictionary containing the data of the provided row
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def getAllEvents(self) -> list:
        """
        Retrieves all the events stored in the table

        Returns:
            list: List containing the events stored in the table. Each event is a dictionary
        """
        conn = sqlite3.connect(self.dbPath)
        conn.row_factory = self._dict_factory
        cur = conn.cursor()

        return cur.execute(f'SELECT * FROM {self.tableName} ORDER BY {self.date} DESC;').fetchall()

    def getEventByFilter(self, query_parameters: dict) -> list:
        """
        Retrieves all the events matching the specified filters 
        for the 'date', 'eventType' and 'eventTitle' parameters.

        Args:
            query_parameters (dict): Dictionary containing the filter specifications. 
                                     Only the keys 'date', 'eventType' and 'eventTitle' will be processed.

        Returns:
            list: List of containing the events stored in the table. Each event is a dictionary
        """
        date = query_parameters.get(self.date)
        eventType = query_parameters.get(self.eventType)
        eventTitle = query_parameters.get(self.eventTitle)

        # Assemble SQL query based on the specified parameters
        query = f"SELECT * FROM {self.tableName} WHERE"
        to_filter = []

        if date:
            query += f' {self.date}=? AND'
            to_filter.append(date)
        if eventType:
            query += f' {self.eventType}=? AND'
            to_filter.append(eventType)
        if eventTitle:
            query += f' {self.eventTitle}=? AND'
            to_filter.append(eventTitle)
        if not (date or eventType or eventTitle):
            return {}

        # Remove trailing ' AND' from the query assembled
        query = query[:-4] + f'ORDER BY {self.date} DESC;'

        conn = sqlite3.connect(self.dbPath)
        conn.row_factory = self._dict_factory
        cur = conn.cursor()

        return cur.execute(query, to_filter).fetchall()
        