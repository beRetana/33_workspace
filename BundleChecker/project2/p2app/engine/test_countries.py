# test_countries.py
import unittest
from countries import *
from pathlib import Path
import sqlite3

class TestCountries(unittest.TestCase):

    def setUp(self):
        self._path = Path("/Users/brandon__lii/Downloads/UCI/2024-2025/Invierno/ICS_33/Projects/Project2/p2app/database/airport.db")
        self._connection = sqlite3.connect(self._path)
        self._connection.execute("PRAGMA foreign_keys = ON")

    def test_search_countries(self):

        def testing(country_name, country_code):
            result = search(self._connection, event_countries.StartCountrySearchEvent(country_code, country_name))

            self.assertEqual(1, len(result))
            country = event_countries.Country(302589, "MW", "Malawi",
                                              1, "https://en.wikipedia.org/wiki/Malawi", "Airports in Malawi")
            self.assertEqual(event_countries.CountrySearchResultEvent(country).__repr__(), result[0].__repr__())

        name = "Malawi"
        code = "MW"
        testing(name, code)
        testing(None, code)
        testing(name, None)

    def testing_load_countries(self):
        result = load(self._connection, event_countries.LoadCountryEvent(302682))
        self.assertEqual(1, len(result))
        country = event_countries.Country(302682, "DK", "Denmark", 4,
                                          "https://en.wikipedia.org/wiki/Denmark",
                                          "Lufthavnene i Danmark")
        expected = event_countries.CountryLoadedEvent(country)
        self.assertEqual(expected.__repr__(), result[0].__repr__())

    def testing_save_modified_countries(self):
        country = event_countries.Country(302682, "DK", "Denmark", 3, "fake news", "I do not understand")
        result = save_modified(self._connection, event_countries.SaveCountryEvent(country))
        self.assertEqual(1, len(result))
        self.assertEqual(event_countries.CountrySavedEvent(country).__repr__(), result[0].__repr__())

        country = event_countries.Country(302682, "DK", "Denmark", 4, "https://en.wikipedia.org/wiki/Denmark", "Lufthavnene i Danmark")
        save_modified(self._connection, event_countries.SaveCountryEvent(country))

    def testing_new_countries(self):
        new_country_id = 3502110
        country = event_countries.Country(new_country_id, "NEW", "My Country", 3, "MyWebsite", "New")
        result = save_new(self._connection, event_countries.SaveNewCountryEvent(country))
        self.assertEqual(1, len(result))
        self.assertEqual(event_countries.CountrySavedEvent(country).__repr__(), result[0].__repr__())

        self._connection.execute('DELETE FROM country WHERE country_id = ?', (new_country_id,))
        self._connection.commit()

if __name__ == '__main__':
    unittest.main()

