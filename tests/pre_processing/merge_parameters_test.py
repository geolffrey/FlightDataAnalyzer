# -*- coding: utf-8 -*-

from flightdatautilities import masked_array_testutils as ma_test
import numpy as np
import unittest

from analysis_engine.node import A, P

from analysis_engine.pre_processing.merge_parameters import (
    Groundspeed,
    LatitudePrepared,
    LongitudePrepared,
)

from analysis_engine.derived_parameters import CoordinatesStraighten


class TestGroundspeed(unittest.TestCase):

    def setUp(self):
        self.node_class = Groundspeed

    def test_can_operate(self):
        combinations = self.node_class.get_operational_combinations()
        self.assertEqual(len(combinations), 3)  # 2**2-1

    def test_basic(self):
        one = P('Groundspeed (1)', np.ma.array([100, 200, 300]), frequency=0.5, offset=0.0)
        two = P('Groundspeed (2)', np.ma.array([150, 250, 350]), frequency=0.5, offset=1.0)
        gs = Groundspeed()
        gs.derive(one, two)
        # Note: end samples are not 100 & 350 due to method of merging.
        ma_test.assert_masked_array_equal(gs.array[1:-1], np.ma.array([150, 200, 250, 300]))
        self.assertEqual(gs.frequency, 1.0)
        self.assertEqual(gs.offset, 0.0)


class TestLatitudePrepared(unittest.TestCase):
    def test_can_operate(self):
        combinations = LatitudePrepared.get_operational_combinations()
        expected_combinations = [('Longitude', 'Latitude', 'Aircraft Type')]
        self.assertEqual(combinations, expected_combinations)

    @unittest.skip('Test Does Not Work')
    def test_upsample(self):
        lat = P('Latitude', np.ma.array(data=[1, 0, 0, 0, 0, 2.0],
                                        mask=[0,1,1,1,1,0]),
                frequency=0.25)
        lon = P('Longitude', np.ma.array(data=[0,0,0,2,2,2.0],
                                        mask=[1,1,1,0,0,0]),
                frequency=0.25)
        ac_type = A('Aircraft Type', 'aeroplane')
        lp = LatitudePrepared()
        lp.derive(lon, lat, ac_type)
        self.assertEqual(len(lp.array), 24)
        self.assertEqual(lp.frequency, 1.0)

    def test_derive(self):
        # Check with partially masked data
        lat = P('Latitude', np.ma.array(data=[0,0,0,3,0,3.0],
                                        mask=[1,1,1,0,1,0]))
        lon = P('Longitude', np.ma.array(data=[0,0,0,2,2,2.0],
                                        mask=[1,1,1,0,0,0]))
        ac_type = A('Aircraft Type', 'aeroplane')
        lp = LatitudePrepared()
        expected = np.ma.array([3,3,3,3,3,3])
        lp.derive(lon, lat, ac_type)
        ma_test.assert_masked_array_equal(lp.array, expected)
        # And the fully masked data should give the same result
        lon = P('Latitude', np.ma.array(data=[0,0,0,3,0,3.0],
                                        mask=[1,1,1,1,1,1]))
        lp.derive(lon, lat, ac_type)
        ma_test.assert_masked_array_equal(lp.array, expected)


class TestLongitudePrepared(unittest.TestCase):
    def test_can_operate(self):
        combinations = LongitudePrepared.get_operational_combinations()
        expected_combinations = [('Longitude', 'Latitude', 'Aircraft Type')]
        self.assertEqual(combinations, expected_combinations)

    def test_derive(self):
        lat = P('Latitude', np.ma.array(data=[0,0,0,3,3,3.0],
                                        mask=[1,1,1,0,0,0]))
        lon = P('Longitude', np.ma.array(data=[0,0,0,2,2,2.0],
                                        mask=[1,1,1,0,0,0]))
        ac_type = A('Aircraft Type', 'helicopter')
        lp = LongitudePrepared()
        expected = np.ma.array([2,2,2,2,2,2])
        # Try with partially masked data
        lp.derive(lon, lat, ac_type)
        ma_test.assert_masked_array_equal(lp.array, expected)
        # And the fully masked data should give the same result
        lon = P('Longitude', np.ma.array(data=[0,0,0,2,2,2.0],
                                        mask=[1,1,1,1,1,1]))
        lp.derive(lon, lat, ac_type)
        ma_test.assert_masked_array_equal(lp.array, expected)
