# Unit tests for core.py

import unittest

from core import *

class CoreTests(unittest.TestCase):
    def test_mph_to_fps(self):
        self.assertEqual(70*5280/3600, mph_to_fps(70))

    def test_feet_to_station(self):
        self.assertEqual(0, feet_to_station(0))
        self.assertEqual(5, feet_to_station(500))
        self.assertEqual(10, feet_to_station(1000))
        self.assertEqual(20, feet_to_station(2000))

    def test_round_to_5(self):
        self.assertEqual(5, round_to_5(4.9))
        self.assertEqual(10, round_to_5(9.9))


    def test_stopping_sight_distance(self):
        self.assertEqual(730, stopping_sight_distance(70))
        self.assertEqual(250, stopping_sight_distance(35, 0.0))

    def test_stopping_sight_distance_on_grade(self):
        self.assertEqual(85, stopping_sight_distance(15, -0.06))
        self.assertEqual(405, stopping_sight_distance(50,0.03))
        self.assertEqual(1250, stopping_sight_distance(85,-0.09))

    def test_clear_offset(self):
        self.assertAlmostEqual(3.07, clear_offset(2500, 50, 1, 12.0, 0.0),places=2)
        self.assertAlmostEqual(3.11, clear_offset(2500, 50, 2, 12.0, 0.0),places=2)
        self.assertAlmostEqual(19.28, clear_offset(3000, 75, 2, 12.0, 0.03),places=2)
        self.assertAlmostEqual(36.64, clear_offset(3000, 75, 2, 12.0, -0.09),places=2)

    def test_decision_sight_distance(self):
        self.assertEqual(780, decision_sight_distance(70, Maneuver.A))
        self.assertEqual(1410, decision_sight_distance(70, Maneuver.B))
        self.assertEqual(1105, decision_sight_distance(70, Maneuver.C))
        self.assertEqual(1275, decision_sight_distance(70, Maneuver.D))
        self.assertEqual(1445, decision_sight_distance(70, Maneuver.E))

    def test_inside_and_outside_agree(self):
        rad = 2000
        baserad = 1995
        self.assertAlmostEqual(clear_inside_shoulder(baserad, 70, 0.0, 5.0), clear_offset(rad, 70, 1, 12.0, 0.0), places=0)

if __name__ == '__main__':
    unittest.main()