# p2app/engine/main.py
#
# ICS 33 Winter 2025
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.

"""p2app/events.__init__.py"""

import sqlite3

import p2app.engine.continents as engine_continents
import p2app.engine.countries as engine_countries
import p2app.engine.regions as engine_regions

import p2app.events.app as event_app
import p2app.events.continents as event_continents
import p2app.events.countries as event_countries
import p2app.events.database as event_database
import p2app.events.regions as event_regions



class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self._connection = None

    def _create_connection(self, event: event_database.OpenDatabaseEvent)-> list[event_database.DatabaseOpenFailedEvent] | list[event_database.DatabaseOpenedEvent]:
        """Takes in an event and tries to connect to the database. If successful, returns
        an event to notify success or failure."""
        database_directory = event.path()
        cursor = None
        try:
            self._connection = sqlite3.connect(database_directory)
            # This is simply to check if the file given is a database.
            cursor = self._connection.execute('PRAGMA foreign_keys = ON;')
            cursor = self._connection.execute('SELECT name FROM sqlite_master WHERE type=\'table\' ORDER BY name;')
        except sqlite3.Error as e:
            return [event_database.DatabaseOpenFailedEvent(str(e))]
        else:
            return [event_database.DatabaseOpenedEvent(database_directory)]
        finally:
            if cursor:
                cursor.close()

    def _close_connection(self)-> list[event_database.DatabaseClosedEvent]:
        """Closes the connection to the database and returns an event DatabaseClosedEvent"""

        self._connection.close()
        self._connection = None
        return [event_database.DatabaseClosedEvent()]

    def _close_application(self):
        """CLoses the application."""
        if self._connection:
            self._connection.close()
            self._connection = None
        return [event_app.EndApplicationEvent()]

    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        # Recognize the event
        match type(event):
            case event_database.OpenDatabaseEvent:
                yield from self._create_connection(event)
            case event_database.CloseDatabaseEvent:
                yield from self._close_connection()
            case event_app.QuitInitiatedEvent:
                yield from self._close_application()
            # Continents Section
            case event_continents.StartContinentSearchEvent:
                yield from engine_continents.search(self._connection, event)
            case event_continents.LoadContinentEvent:
                yield from engine_continents.load_search(self._connection, event)
            case event_continents.SaveContinentEvent:
                yield from engine_continents.save_modified(self._connection, event)
            case event_continents.SaveNewContinentEvent:
                yield from engine_continents.save_new(self._connection, event)
            # Countries Section
            case event_countries.StartCountrySearchEvent:
                yield from engine_countries.search(self._connection, event)
            case event_countries.LoadCountryEvent:
                yield from engine_countries.load(self._connection, event)
            case event_countries.SaveCountryEvent:
                yield from engine_countries.save_modified(self._connection, event)
            case event_countries.SaveNewCountryEvent:
                yield from engine_countries.save_new(self._connection, event)
            # Regions Section
            case event_regions.StartRegionSearchEvent:
                yield from engine_regions.search(self._connection, event)
            case event_regions.LoadRegionEvent:
                yield from engine_regions.load_search(self._connection, event)
            case event_regions.SaveRegionEvent:
                yield from engine_regions.save_modified(self._connection, event)
            case event_regions.SaveNewRegionEvent:
                yield from engine_regions.save_new(self._connection, event)
            case _:
                yield from [event_app.ErrorEvent("Unrecognized Event")]



