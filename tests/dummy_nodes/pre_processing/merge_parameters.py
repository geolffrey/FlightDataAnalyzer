from analysis_engine.node import (
    A, M, P, S, KPV, KTI,
    aeroplane, App, helicopter,
    DerivedParameterNode, FlightPhaseNode, KeyTimeInstanceNode,
    KeyPointValueNode, ApproachNode, FlightAttributeNode,
    MultistateDerivedParameterNode
)
from analysis_engine.key_time_instances import (
    MinsToTouchdown, DistanceFromThreshold, AltitudeWhenDescending
)
from analysis_engine.library import any_of, all_of, all_deps, any_one_of, lookup_table, any_deps
from analysis_engine.derived_parameters import CoordinatesStraighten
from flightdatautilities import aircrafttables as at
from analysis_engine.settings import (
    AIRSPEED_THRESHOLD, NAME_VALUES_ENGINE, NAME_VALUES_LEVER,
    NAME_VALUES_CONF, NAME_VALUES_RANGES, NAME_VALUES_DISTANCE,
    NAME_VALUES_CLIMB, NAME_VALUES_DESCENT
)


class Groundspeed(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_deps(cls, available)

    def derive(self,
               source_A=P('Groundspeed (1)'),
               source_B=P('Groundspeed (2)')):
        pass


class LongitudePrepared(DerivedParameterNode, CoordinatesStraighten):
    name = 'Longitude Prepared'

    def derive(self,
               lon=P('Longitude'), lat=P('Latitude'),
               ac_type=A('Aircraft Type')):
        pass


class LatitudePrepared(DerivedParameterNode, CoordinatesStraighten):
    name = 'Latitude Prepared'

    def derive(self,
               lon=P('Longitude'),
               lat=P('Latitude'),
               ac_type=A('Aircraft Type')):
        pass


class Latitude(DerivedParameterNode):
    name = 'Latitude'

    @classmethod
    def can_operate(cls, available):
        return any_of(('Latitude (1)', 'Latitude (2)', 'Latitude (3)'),
                      available)

    def derive(self,
               src_1=P('Latitude (1)'),
               src_2=P('Latitude (2)'),
               src_3=P('Latitude (3)')):
        pass


class Longitude(DerivedParameterNode):
    name = 'Longitude'

    @classmethod
    def can_operate(cls, available):
        return any_of(('Longitude (1)', 'Longitude (2)', 'Longitude (3)'),
                      available)

    def derive(self,
               src_1=P('Longitude (1)'),
               src_2=P('Longitude (2)'),
               src_3=P('Longitude (3)')):
        pass
