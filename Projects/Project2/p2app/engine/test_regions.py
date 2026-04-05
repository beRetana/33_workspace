# test_regions.py

import unittest
from regions import *
import sqlite3
from pathlib import Path

class TestRegions(unittest.TestCase):

    def setUp(self):
        self._path = Path(
            "/Users/brandon__lii/Downloads/UCI/2024-2025/Invierno/ICS_33/Projects/Project2/p2app/database/airport.db")

        self._connection = sqlite3.connect(self._path)
        self._connection.execute("PRAGMA foreign_keys = ON")

    def test_search_regions(self):
        def testing(code, region_local_code, name):
            result = search(self._connection, event_regions.StartRegionSearchEvent(code, region_local_code, name))
            expected_region = event_regions.Region(303286, "BY-VI", "VI", "Vitebsk Region", 4, 302678,
                                                   "https://en.wikipedia.org/wiki/Vitebsk_Region",
                                                   "Vicebskaja voblasc', Ві́цебская во́бласць, Vitsebsk Voblast")
            self.assertEqual(event_regions.RegionSearchResultEvent(expected_region).__repr__(), result[0].__repr__())

        region_code = "BY-VI"
        local_code = "VI"
        region_name = "Vitebsk Region"
        testing(region_code, local_code, region_name)
        testing(None, local_code, region_name)
        testing(None, None, region_name)
        testing(None, local_code, None)
        testing(region_code, None, region_name)
        testing(region_code, None, None)
        testing(region_code, local_code, None)

    def test_load_regions(self):
        region_id = 303286
        result = load_search(self._connection, event_regions.LoadRegionEvent(region_id))

        self.assertEqual(1, len(result))
        region = event_regions.Region(region_id, "BY-VI", "VI", "Vitebsk Region", 4, 302678,
                                                   "https://en.wikipedia.org/wiki/Vitebsk_Region",
                                                   "Vicebskaja voblasc', Ві́цебская во́бласць, Vitsebsk Voblast")
        self.assertEqual(event_regions.RegionLoadedEvent(region).__repr__(), result[0].__repr__())

    def test_save_regions(self):
        region_id = 303286
        region = event_regions.Region(region_id, "BY-VI", "V8", "Region", 5, 302678,
                                      "https://wiki/Vitebsk_Region",
                                      "Vicebskaja voblasc', Voblast")
        results = save_modified(self._connection, event_regions.SaveRegionEvent(region))
        self.assertEqual(1, len(results))
        self.assertEqual(event_regions.RegionSavedEvent(region).__repr__(), results[0].__repr__())

        region = event_regions.Region(region_id, "BY-VI", "VI", "Vitebsk Region", 4, 302678,
                                      "https://en.wikipedia.org/wiki/Vitebsk_Region",
                                      "Vicebskaja voblasc', Ві́цебская во́бласць, Vitsebsk Voblast")
        save_modified(self._connection, event_regions.SaveRegionEvent(region))

    def test_save_new_region(self):
        region_id = 400000
        region = event_regions.Region(region_id, "BY-VI2", "V8", "Region", 6, 302682,
                                      "https://wiki/Vitebsk_Region",
                                      "Vicebskaja voblasc', Voblast")
        results = save_new(self._connection, event_regions.SaveNewRegionEvent(region))
        self.assertEqual(1, len(results))
        self.assertEqual(event_regions.RegionSavedEvent(region).__repr__(), results[0].__repr__())

        self._connection.execute('DELETE FROM region WHERE region_id = ?', (region_id,))
        self._connection.commit()

if __name__ == '__main__':
    unittest.main()