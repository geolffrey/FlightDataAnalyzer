# -*- coding: utf-8 -*-

import numpy as np
import unittest

from analysis_engine.node import P, A

from analysis_engine.pre_processing.merge_parameters import (
    Groundspeed,
    Latitude,
    LatitudePrepared,
    Longitude,
    LongitudePrepared,
)
from numpy.ma.testutils import assert_array_equal


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
        assert_array_equal(gs.array[1:-1], np.array([150, 200, 250, 300]))
        self.assertEqual(gs.frequency, 1.0)
        self.assertEqual(gs.offset, 0.0)


class TestLatitudePrepared(unittest.TestCase):
    def test_can_operate(self):
        combinations = LatitudePrepared.get_operational_combinations()
        expected_combinations = [('Longitude', 'Latitude', 'Aircraft Type')]
        self.assertEqual(combinations, expected_combinations)

    def test_derive(self):
        longitude = P('Longitude', array=np.ma.arange(10, 20, 0.01))
        latitude = P('Latitude', array=np.ma.arange(40, 50, 0.01))
        latitude.array[100:800] = np.ma.masked
        node = LatitudePrepared()
        node.derive(longitude, latitude, A('Aircraft Type', 'aeroplane'))

        expected_mask = np.zeros(1_000, dtype=np.bool)
        expected_mask[100:800] = 1
        np.testing.assert_array_equal(node.array.mask, expected_mask)


class TestLongitudePrepared(unittest.TestCase):
    def test_can_operate(self):
        combinations = LongitudePrepared.get_operational_combinations()
        expected_combinations = [('Longitude', 'Latitude', 'Aircraft Type')]
        self.assertEqual(combinations, expected_combinations)

    @unittest.skip('Test Not Implemented')
    def test_derive(self):
        self.assertTrue(False, msg='Test not implemented')


class TestLatitude:
    def test_1_source(self):
        lat1 = P(
            'Latitude (1)',
            array=np.ma.arange(-10, 10),
            frequency=0.5,
            offset=0.25
        )
        lat1.array[5:8] = np.ma.masked

        latitude = Latitude()
        latitude.get_derived((lat1, None, None))

        expected = np.ma.arange(-10, 10)

        np.testing.assert_array_equal(latitude.array, expected)
        np.testing.assert_array_equal(latitude.array.mask, expected.mask)
        assert latitude.offset == 0.25
        assert latitude.frequency == 0.5

    def test_2_sources(self):
        lat1 = P(
            'Latitude (1)',
            array=np.ma.arange(-10, 10),
            frequency=0.5,
            offset=0.25
        )
        lat1.array[5:8] = np.ma.masked
        lat2 = P(
            'Latitude (2)',
            array=np.ma.arange(-9.5, 10),
            frequency=0.5,
            offset=0.75
        )
        lat2.array[5:8] = np.ma.masked
        latitude = Latitude()
        latitude.get_derived((lat1, lat2, None))

        expected = np.ma.arange(-9.75, 10, 0.5)
        expected[-1] = np.ma.masked

        np.testing.assert_array_equal(latitude.array, expected)
        np.testing.assert_array_equal(latitude.array.mask, expected.mask)
        assert latitude.offset == 0.5
        assert latitude.frequency == 1


class TestLongitude:
    def test_1_source(self):
        long1 = P(
            'Longitude (1)',
            array=np.ma.concatenate((
                np.arange(160, 180),
                np.arange(-180, -170)
            )),
            frequency=0.5,
            offset=0.25
        )
        long1.array[5:8] = np.ma.masked

        longitude = Longitude()
        longitude.get_derived((long1, None, None))

        expected = np.ma.concatenate((
            np.arange(160, 180),
            np.arange(-180, -170)
        ))

        np.testing.assert_array_equal(longitude.array, expected)
        np.testing.assert_array_equal(longitude.array.mask, expected.mask)
        assert longitude.offset == 0.25
        assert longitude.frequency == 0.5

    def test_2_sources(self):
        long1 = P(
            'Longitude (1)',
            array=np.ma.concatenate((
                np.arange(160, 180),
                np.arange(-180, -170)
            )),
            frequency=0.5,
            offset=0.25
        )
        long1.array[5:8] = np.ma.masked
        long2 = P(
            'Longitude (2)',
            array=np.ma.concatenate((
                np.arange(160.5, 180),
                np.arange(-179.5, -170)
            )),
            frequency=0.5,
            offset=0.75
        )
        long2.array[5:8] = np.ma.masked
        longitude = Longitude()
        longitude.get_derived((long1, long2, None))

        expected = np.ma.concatenate((
            np.arange(160.25, 180, 0.5),
            np.arange(-179.75, -170, 0.5)
        ))
        expected[-1] = np.ma.masked

        np.testing.assert_array_equal(longitude.array, expected)
        np.testing.assert_array_equal(longitude.array.mask, expected.mask)
        assert longitude.offset == 0.5
        assert longitude.frequency == 1
