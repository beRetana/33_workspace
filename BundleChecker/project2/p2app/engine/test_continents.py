
import unittest
from continents import *
from pathlib import Path

class TestContinents(unittest.TestCase):
    def setUp(self):
        self._path = Path("/Users/brandon__lii/Downloads/UCI/2024-2025/Invierno/ICS_33/Projects/Project2/p2app/database/airport.db")
        self._connection = sqlite3.connect(self._path)

    def test_search(self):
        def testing(name, code):
            result = search(self._connection, event_continents.StartContinentSearchEvent(code, name))

            self.assertEqual(1, len(result))
            continent = event_continents.Continent(1, "AF", "Africa")
            self.assertEqual(event_continents.ContinentSearchResultEvent(continent).__repr__(), result[0].__repr__())

        continent_name = "Africa"
        continent_code = "AF"
        testing(continent_name, continent_code)
        testing(None, continent_code)
        testing(continent_name, None)

        continent_name = "No NAME"
        continent_code = "NO valid"

        empty_result = search(self._connection, event_continents.StartContinentSearchEvent(continent_code, continent_name))

        self.assertEqual(0, len(empty_result))
        self.assertEqual([], empty_result)

    def test_load_continents(self):
        continent_id = 3
        result = load_search(self._connection, event_continents.LoadContinentEvent(continent_id))

        self.assertEqual(1, len(result))
        continent = event_continents.Continent(continent_id, "AS", "Asia")
        self.assertEqual(event_continents.ContinentLoadedEvent(continent).__repr__(), result[0].__repr__())

    def test_edit_continents(self):
        continent = event_continents.Continent(3, "AS", "Asiatica")
        result = save_modified(self._connection, event_continents.SaveContinentEvent(continent))

        self.assertEqual(1, len(result))
        self.assertEqual(event_continents.ContinentSavedEvent(continent).__repr__(), result[0].__repr__())

        #Reset changes
        continent = event_continents.Continent(3, "AS", "Asia")
        result = save_modified(self._connection, event_continents.SaveContinentEvent(continent))

    def test_add_continents(self):
        new_id = 8
        continent = event_continents.Continent(new_id, "AM", "AMÉRICA")
        result = save_modified(self._connection, event_continents.SaveContinentEvent(continent))
        self.assertEqual(1, len(result))
        self.assertEqual(event_continents.ContinentSavedEvent(continent).__repr__(), result[0].__repr__())

        #Reset the data
        self._connection.execute('DELETE FROM continent WHERE continent_id = ?', (new_id,))
        self._connection.commit()

if __name__ == '__main__':
    unittest.main()