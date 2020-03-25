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


class EnterTransitionFlightToHover(KeyTimeInstanceNode):

    def derive(self, holds=S('Transition Flight To Hover')):
        pass


class ExitTransitionFlightToHover(KeyTimeInstanceNode):

    def derive(self, holds=S('Transition Flight To Hover')):
        pass


class ExitTransitionHoverToFlight(KeyTimeInstanceNode):

    def derive(self, holds=S('Transition Hover To Flight')):
        pass
