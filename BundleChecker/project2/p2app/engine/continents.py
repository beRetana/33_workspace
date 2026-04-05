
# continents.py

import sqlite3
import p2app.events.continents as event_continents

def search(connection: sqlite3.Connection, event: event_continents.StartContinentSearchEvent) -> list[event_continents.ContinentSearchResultEvent]:
    """Executes a sqlite action and returns a list of all continents that match the search criteria."""
    continent_name = event.name()
    continent_code = event.continent_code()

    if continent_name and not continent_code:
        cursor = connection.execute('SELECT * FROM continent WHERE name = ?', [continent_name])
    elif continent_code and not continent_name:
        cursor = connection.execute('SELECT * FROM continent WHERE continent_code = ?', [continent_code] )
    else:
        cursor = connection.execute('SELECT * FROM continent WHERE name = ? and continent_code = ?',
                                    (continent_name, continent_code))

    continents = cursor.fetchall()
    cursor.close()

    return [event_continents.ContinentSearchResultEvent(event_continents.Continent(continent[0], continent[1], continent[2])) for continent in continents]

def load_search(connection: sqlite3.Connection, event: event_continents.LoadContinentEvent) -> list[event_continents.ContinentLoadedEvent]:
    """Searches a specified continent and returns an event with that information"""
    continent_id = event.continent_id()
    cursor = connection.execute('SELECT * FROM continent WHERE continent_id = ?', [continent_id])
    continent = cursor.fetchone()
    cursor.close()

    return [event_continents.ContinentLoadedEvent(event_continents.Continent(*continent))]

def save_new(connection: sqlite3.Connection, event: event_continents.SaveNewContinentEvent) -> list[event_continents.ContinentSavedEvent | event_continents.SaveContinentFailedEvent]:
    """Create a new continent and save it to the database"""
    continent_id, continent_code, continent_name = event.continent()
    try:
        cursor = connection.execute('INSERT INTO continent (continent_code, name) VALUES (?, ?)',
                           (continent_code, continent_name))
    except sqlite3.Error as error:
        return [event_continents.SaveContinentFailedEvent(error.__str__())]
    else:
        connection.commit()
        new_continent = event_continents.Continent(cursor.lastrowid, continent_code, continent_name)
        cursor.close()
        return [event_continents.ContinentSavedEvent(new_continent)]

def save_modified(connection: sqlite3.Connection, event: event_continents.SaveContinentEvent)-> list[event_continents.ContinentSavedEvent | event_continents.SaveContinentFailedEvent]:
    """Saves the given changes from the event and persists them through the database."""
    continent_id = event.continent().continent_id
    continent_name = event.continent().name
    continent_code = event.continent().continent_code

    try:
        connection.execute('UPDATE continent SET name = ?, continent_code = ? WHERE continent_id = ?',
                                (continent_name, continent_code, continent_id))
    except sqlite3.Error as error:
        return [event_continents.SaveContinentFailedEvent(error.__str__())]
    else:
        connection.commit()
        return [event_continents.ContinentSavedEvent(event_continents.Continent(continent_id, continent_code, continent_name))]

