# countries.py
import sqlite3
import p2app.events.countries as event_countries

def search(connection: sqlite3.Connection, event: event_countries.StartCountrySearchEvent) -> list[event_countries.CountrySearchResultEvent]:
    """Executes a sqlite action and returns a list of all continents that match the search criteria."""
    country_name = event.name()
    country_code = event.country_code()

    if country_name and not country_code:
        cursor = connection.execute('SELECT * FROM country WHERE name = ?', [country_name])
    elif country_code and not country_name:
        cursor = connection.execute('SELECT * FROM country WHERE country_code = ?', [country_code] )
    else:
        cursor = connection.execute('SELECT * FROM country WHERE name = ? and country_code = ?',
                                    (country_name, country_code))

    countries = cursor.fetchall()
    cursor.close()

    return [event_countries.CountrySearchResultEvent(
        event_countries.Country(country[0], country[1], country[2], country[3], country[4], country[5])) for country in countries]

def load(connection: sqlite3.Connection, event: event_countries.LoadCountryEvent) -> list[event_countries.CountryLoadedEvent]:
    """Searches a specified continent and returns an event with that information"""
    country_id = event.country_id()

    cursor = connection.execute('SELECT * FROM country WHERE country_id = ?', [country_id])

    country = cursor.fetchone()
    cursor.close()

    return [event_countries.CountryLoadedEvent(event_countries.Country(*country))]

def save_new(connection: sqlite3.Connection, event: event_countries.SaveNewCountryEvent) -> list[event_countries.CountrySavedEvent | event_countries.SaveCountryFailedEvent]:
    """Create a new continent and save it to the database"""

    try:
        cursor = connection.execute('INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords) VALUES (?,?,?,?,?,?)',
                           event.country())
    except sqlite3.Error as error:
        connection.rollback()
        return [event_countries.SaveCountryFailedEvent(error.__str__())]
    else:
        connection.commit()
        new_country = event_countries.Country(cursor.lastrowid, event.country().country_code,
                                              event.country().name, event.country().continent_id,
                                              event.country().wikipedia_link, event.country().keywords)
        cursor.close()
        return [event_countries.CountrySavedEvent(new_country)]

def save_modified(connection: sqlite3.Connection, event: event_countries.SaveCountryEvent)-> list[event_countries.CountrySavedEvent | event_countries.SaveCountryFailedEvent]:
    """Saves the given changes from the event and persists them through the database."""
    country_id = event.country().country_id
    country_name = event.country().name
    country_code = event.country().country_code
    continent_id = event.country().continent_id
    wikipedia_link = event.country().wikipedia_link
    keywords = event.country().keywords

    try:
        connection.execute('UPDATE country SET name = ?, country_code = ?, continent_id = ?, wikipedia_link = ?, keywords = ? WHERE country_id = ?',
                                (country_name, country_code, continent_id, wikipedia_link, keywords, country_id))
    except sqlite3.Error as error:
        connection.rollback()
        return [event_countries.SaveCountryFailedEvent(error.__str__())]
    else:
        connection.commit()
        return [event_countries.CountrySavedEvent(event.country())]
