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


class GearDown(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_deps(cls, available)

    def derive(self,
               gl=M('Gear (L) Down'),
               gn=M('Gear (N) Down'),
               gr=M('Gear (R) Down'),
               gc=M('Gear (C) Down')):
        pass


class GearUp(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_deps(cls, available)

    def derive(self,
               gl=M('Gear (L) Up'),
               gn=M('Gear (N) Up'),
               gr=M('Gear (R) Up'),
               gc=M('Gear (C) Up')):
        pass


class GearInTransit(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_deps(cls, available)

    def derive(self,
               gl=M('Gear (L) In Transit'),
               gn=M('Gear (N) In Transit'),
               gr=M('Gear (R) In Transit'),
               gc=M('Gear (C) In Transit')):
        pass


class GearDownInTransit(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_deps(cls, available)

    def derive(self,
               gear_L=M('Gear (L) Down In Transit'),
               gear_N=M('Gear (N) Down In Transit'),
               gear_R=M('Gear (R) Down In Transit'),
               gear_C=M('Gear (C) Down In Transit')):
        pass


class GearUpInTransit(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_deps(cls, available)

    def derive(self,
               gear_L=M('Gear (L) Up In Transit'),
               gear_N=M('Gear (N) Up In Transit'),
               gear_R=M('Gear (R) Up In Transit'),
               gear_C=M('Gear (C) Up In Transit')):
        pass


class GearPosition(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        merge_position = any_of(('Gear (L) Position', 'Gear (N) Position',
                                 'Gear (R) Position', 'Gear (C) Position'),
                                available)
        return merge_position

    def derive(self,
               gl=M('Gear (L) Position'),
               gn=M('Gear (N) Position'),
               gr=M('Gear (R) Position'),
               gc=M('Gear (C) Position')):
        pass
