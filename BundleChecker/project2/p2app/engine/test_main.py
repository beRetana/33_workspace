# test_main.py
import unittest
from main import *
from pathlib import Path

# Testing the functionality and accuracy of main.

class TestMain(unittest.TestCase):

    def setUp(self):
        self._path = Path("/Users/brandon__lii/Downloads/UCI/2024-2025/Invierno/ICS_33/Projects/Project2/p2app/database/airport.db")
        self._engine = Engine()
        self._engine.process_event(event_database.OpenDatabaseEvent(self._path))

    def tearDown(self):
        #self._engine.process_event(event_database.CloseDatabaseEvent())
        pass

    def test_process_event_close_app(self):
        result = self._engine.process_event(event_app.QuitInitiatedEvent())
        expected = event_app.EndApplicationEvent()

        self.assertEqual(1, len(list(result)))

        result = self._engine.process_event(event_app.QuitInitiatedEvent())

        self.assertEqual(type(expected), type(result.__next__()))

    def test_process_event_open_data_base_success(self):
        result = self._engine.process_event(event_database.OpenDatabaseEvent(self._path))
        expected = event_database.DatabaseOpenedEvent(self._path)

        self.assertEqual(1, len(list(result)))

        result = self._engine.process_event(event_database.OpenDatabaseEvent(self._path))

        self.assertEqual(type(expected), type(result.__next__()))

    def test_process_event_open_data_base_failure(self):
        fake_path = Path("")
        result = self._engine.process_event(event_database.OpenDatabaseEvent(fake_path))
        expected = event_database.DatabaseOpenFailedEvent("Not a database")

        self.assertEqual(1, len(list(result)))

        result = self._engine.process_event(event_database.OpenDatabaseEvent(fake_path))

        self.assertEqual(type(expected), type(result.__next__()))

    def test_process_event_unrecognized_event(self):

        result = self._engine.process_event("Not an Event")
        expected = event_app.ErrorEvent("Unrecognized event")

        self.assertEqual(1, len(list(result)))

        result = self._engine.process_event("Not an Event")

        self.assertEqual(type(expected), type(result.__next__()))

if __name__ == '__main__':
    unittest.main()