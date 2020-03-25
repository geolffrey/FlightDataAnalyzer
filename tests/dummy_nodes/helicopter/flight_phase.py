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


class Airborne(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, seg_type=A('Segment Type')):
        if seg_type and seg_type.value in ('GROUND_ONLY', 'NO_MOVEMENT'):
            return False
        return all_of(('Gear On Ground',), available)

    def derive(self,
               alt_rad=P('Altitude Radio'),
               alt_agl=P('Altitude AGL'),
               gog=M('Gear On Ground'),
               rtr=S('Rotors Turning')):
        pass


class Autorotation(FlightPhaseNode):

    def derive(self, max_n2=P('Eng (*) N2 Max'),
               nr=P('Nr'), descs=S('Descending')):
        pass


class Hover(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type == helicopter and \
               all_of(('Altitude AGL', 'Airborne', 'Groundspeed'), available)

    def derive(self, alt_agl=P('Altitude AGL'),
               airs=S('Airborne'),
               gspd=P('Groundspeed'),
               trans_hfs=S('Transition Hover To Flight'),
               trans_fhs=S('Transition Flight To Hover')):
        pass


class HoverTaxi(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type == helicopter and \
               all_of(('Altitude AGL', 'Airborne', 'Hover'), available)

    def derive(self, alt_agl=P('Altitude AGL'),
               airs=S('Airborne'),
               hovers=S('Hover'),
               trans_hfs=S('Transition Hover To Flight'),
               trans_fhs=S('Transition Flight To Hover')):
        pass


class NoseDownAttitudeAdoption(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        return family and family.value == 'H175' and all_of(('Pitch', 'Initial Climb'), available)

    def derive(self, pitch=P('Pitch'), climbs=S('Initial Climb')):
        pass


class RotorsTurning(FlightPhaseNode):

    def derive(self, rotors=M('Rotors Running')):
        pass


class Takeoff(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, seg_type=A('Segment Type')):
        if seg_type and seg_type.value in ('GROUND_ONLY', 'NO_MOVEMENT', 'STOP_ONLY'):
            return False
        else:
            return all_of(('Altitude AGL', 'Liftoff'), available)

    def derive(self,
               alt_agl=P('Altitude AGL'),
               lifts=S('Liftoff')):
        pass


class TransitionHoverToFlight(FlightPhaseNode):

    def derive(self, alt_agl=P('Altitude AGL'),
               ias=P('Airspeed'),
               airs=S('Airborne'),
               pitch_rate=P('Pitch Rate')):
        pass


class TransitionFlightToHover(FlightPhaseNode):

    def derive(self, alt_agl=P('Altitude AGL'),
               ias=P('Airspeed'),
               airs=S('Airborne'),
               pitch_rate=P('Pitch Rate')):
        pass


class OnDeck(FlightPhaseNode):

    def derive(self, gnds=S('Grounded'),
               pitch=P('Pitch'), roll=P('Roll')):
        pass
