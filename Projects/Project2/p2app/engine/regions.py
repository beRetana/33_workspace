# regions.py
import sqlite3

import p2app.events.regions as event_regions

def search(connection: sqlite3.Connection, event: event_regions.StartRegionSearchEvent)-> list[event_regions.RegionSearchResultEvent]:
    """Searches through the data for the selections that meet the parameters."""
    region_code = event.region_code()
    local_code = event.local_code()
    region_name = event.name()

    if region_code and local_code and region_name:
        cursor = connection.execute('SELECT * FROM region WHERE region_code = ? AND local_code = ? AND name = ?',
                                    (region_code, local_code, region_name))
    elif not local_code and not region_code:
        cursor = connection.execute('SELECT * FROM region WHERE name = ?', (region_name,))
    elif not local_code and not region_name:
        cursor = connection.execute('SELECT * FROM region WHERE region_code = ?', (region_code,))
    elif not region_code and not region_code:
        cursor = connection.execute('SELECT * FROM region WHERE local_code = ?', (local_code,))
    elif not region_name:
        cursor = connection.execute('SELECT * FROM region WHERE region_code = ? AND local_code = ?', (region_code, local_code))
    elif not local_code:
        cursor = connection.execute('SELECT * FROM region WHERE region_code = ? AND name = ?',
                            (region_code, region_name))
    else:
        cursor = connection.execute('SELECT * FROM region WHERE local_code = ? AND name = ?',
                            (local_code, region_name))
    countries = cursor.fetchall()
    cursor.close()

    return [event_regions.RegionSearchResultEvent(event_regions.Region(*country)) for country in countries]

def load_search(connection: sqlite3.Connection, event: event_regions.LoadRegionEvent)-> list[event_regions.RegionLoadedEvent]:
    """Load the data from the database about the selected region."""
    region_id = event.region_id()

    cursor = connection.execute('SELECT * FROM region WHERE region.region_id = ?', (region_id,))
    region = cursor.fetchone()
    cursor.close()
    return [event_regions.RegionLoadedEvent(event_regions.Region(*region))]

def save_new(connection: sqlite3.Connection, event: event_regions.SaveNewRegionEvent) -> list[event_regions.RegionSavedEvent | event_regions.SaveRegionFailedEvent]:
    """Create a new continent and save it to the database"""
    region_code = event.region().region_code
    region_local_code = event.region().local_code
    region_name = event.region().name
    continent_id = event.region().continent_id
    country_id = event.region().country_id
    wikipedia_link = event.region().wikipedia_link
    keywords = event.region().keywords

    try:
        cursor = connection.execute('INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?,?,?,?,?,?,?,?)',
                           event.region())
    except sqlite3.Error as error:
        connection.rollback()
        return [event_regions.SaveRegionFailedEvent(error.__str__())]
    else:
        connection.commit()
        new_region = event_regions.Region(cursor.lastrowid, region_code, region_local_code, region_name, continent_id, country_id, wikipedia_link, keywords)
        cursor.close()
        return [event_regions.RegionSavedEvent(new_region)]

def save_modified(connection: sqlite3.Connection, event: event_regions.SaveRegionEvent)-> list[event_regions.RegionSavedEvent | event_regions.SaveRegionFailedEvent]:
    """Saves the given changes from the event and persists them through the database."""
    region_id = event.region().region_id
    region_code = event.region().region_code
    region_local_code = event.region().local_code
    region_name = event.region().name
    continent_id = event.region().continent_id
    country_id = event.region().country_id
    wikipedia_link = event.region().wikipedia_link
    keywords = event.region().keywords

    try:
        connection.execute('UPDATE region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? WHERE region_id = ?',
            (region_code, region_local_code, region_name, continent_id, country_id, wikipedia_link, keywords, region_id))
    except sqlite3.Error as error:
        connection.rollback()
        return [event_regions.SaveRegionFailedEvent(error.__str__())]
    else:
        connection.commit()
        return [event_regions.RegionSavedEvent(event.region())]