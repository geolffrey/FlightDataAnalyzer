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


class ApproachRange(DerivedParameterNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               lat=P('Latitude Smoothed'),
               lon=P('Longitude Smoothed'),
               tdwns=KTI('Touchdown')):
        pass


class AltitudeADH(DerivedParameterNode):
    name = 'Altitude ADH'

    def derive(self, rad=P('Altitude Radio'),
               hdot=P('Vertical Speed'),
               ):
        pass


class AltitudeAGL(DerivedParameterNode):
    name = 'Altitude AGL'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type == helicopter:
            return all_of(('Altitude Radio', 'Altitude STD Smoothed', 'Gear On Ground'), available) or \
                   ('Altitude Radio' not in available and 'Altitude AAL' in available)
        else:
            return False

    def derive(self, alt_rad=P('Altitude Radio'),
               alt_aal=P('Altitude AAL'),
               alt_baro=P('Altitude STD Smoothed'),
               gog=M('Gear On Ground')):
        pass


class AltitudeAGLForFlightPhases(DerivedParameterNode):
    name = 'Altitude AGL For Flight Phases'

    def derive(self, alt_agl=P('Altitude AGL')):
        pass


class AltitudeDensity(DerivedParameterNode):

    def derive(self, alt_std=P('Altitude STD'), sat=P('SAT'),
               isa_temp=P('SAT International Standard Atmosphere')):
        pass


class Collective(DerivedParameterNode):

    def derive(self,
               capt=P('Collective (1)'),
               fo=P('Collective (2)')):
        pass


class CyclicForeAft(DerivedParameterNode):
    name = 'Cyclic Fore-Aft'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type == helicopter and any_of(cls.get_dependency_names(), available)

    def derive(self,
               capt=P('Cyclic Fore-Aft (1)'),
               fo=P('Cyclic Fore-Aft (2)')):
        pass


class CyclicLateral(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type == helicopter and any_of(cls.get_dependency_names(), available)

    def derive(self,
               capt=P('Cyclic Lateral (1)'),
               fo=P('Cyclic Lateral (2)')):
        pass


class CyclicAngle(DerivedParameterNode):

    def derive(self,
               cyclic_pitch=P('Cyclic Fore-Aft'),
               cyclic_roll=P('Cyclic Lateral')):
        pass


class MGBOilTemp(DerivedParameterNode):
    name = 'MGB Oil Temp'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return any_of(('MGB Oil Temp (1)', 'MGB Oil Temp (2)'), available) \
               and ac_type == helicopter

    def derive(self, t1=P('MGB Oil Temp (1)'), t2=P('MGB Oil Temp (2)')):
        pass


class MGBOilPress(DerivedParameterNode):
    name = 'MGB Oil Press'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return any_of(('MGB Oil Press (1)', 'MGB Oil Press (2)'), available) \
               and ac_type == helicopter

    def derive(self, p1=P('MGB Oil Press (1)'), p2=P('MGB Oil Press (2)')):
        pass


class Nr(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type == helicopter and any_of(cls.get_dependency_names(), available)

    def derive(self, p1=P('Nr (1)'), p2=P('Nr (2)')):
        pass


class TailRotorPedal(DerivedParameterNode):

    def derive(self,
               capt=P('Tail Rotor Pedal (1)'),
               fo=P('Tail Rotor Pedal (2)')):
        pass
