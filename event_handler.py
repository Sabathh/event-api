import sqlite3
from datetime import datetime

class EventHandler(object):
    
    def __init__(self, dbFile:str = 'events.db'):

        self.dbPath = dbFile
        
        self.tableName = 'events'
        self.date = 'date'
        self.eventType = 'eventType'
        self.eventTitle = 'eventTitle'
        self.eventDescription = 'eventDescription'

    def createDatabase(self, dropTable:bool = False):

        conn = sqlite3.connect(self.dbPath)

        if dropTable:
            conn.execute(f'''DROP TABLE {self.tableName}''')

        conn.execute(f'''
                        CREATE TABLE IF NOT EXISTS {self.tableName}
                            ({self.date} text, {self.eventType} text, {self.eventTitle} text, {self.eventDescription} text)
                        ''')
        conn.commit()

    def insertEvent(self, eventType:str, eventTitle:str, eventDescription:str):
        
        conn = sqlite3.connect(self.dbPath)

        eventDate = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
        
        conn.execute(f'''
                        INSERT INTO {self.tableName}
                            VALUES ('{eventDate}', '{eventType}', '{eventTitle}', '{eventDescription}')
        ''')
        conn.commit()

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def getAllEvents(self) -> dict:

        conn = sqlite3.connect(self.dbPath)
        conn.row_factory = self._dict_factory
        cur = conn.cursor()

        return cur.execute(f'SELECT * FROM {self.tableName} ORDER BY {self.date} DESC;').fetchall()

    def getEventByFilter(self, query_parameters: dict) -> dict:
        
        date = query_parameters.get(self.date)
        eventType = query_parameters.get(self.eventType)
        eventTitle = query_parameters.get(self.eventTitle)

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
        