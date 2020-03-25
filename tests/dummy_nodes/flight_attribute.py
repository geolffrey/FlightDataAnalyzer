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

class DeterminePilot(object):
    pass

class InvalidFlightType(Exception):
    pass


class AnalysisDatetime(FlightAttributeNode):
    name = 'FDR Analysis Datetime'

    def derive(self, start_datetime=A('Start Datetime')):
        pass


class DestinationAirport(FlightAttributeNode):
    name = 'FDR Destination Airport'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, dest=P('Destination'),
               afr_dest=A('AFR Destination Airport')):
        pass


class Duration(FlightAttributeNode):
    name = 'FDR Duration'

    def derive(self, takeoff_dt=A('FDR Takeoff Datetime'),
               landing_dt=A('FDR Landing Datetime')):
        pass


class FlightID(FlightAttributeNode):
    name = 'FDR Flight ID'

    def derive(self, flight_id=A('AFR Flight ID')):
        pass


class FlightNumber(FlightAttributeNode):
    name = 'FDR Flight Number'

    def derive(self,
               num=P('Flight Number'),
               mobiles=S('Mobile')):
        pass


class LandingAirport(FlightAttributeNode):
    name = 'FDR Landing Airport'

    @classmethod
    def can_operate(cls, available):
        '''
        We can determine a landing airport in one of two ways:
        1. Find the nearest airport to the coordinates at landing.
        2. Use the airport data provided in the achieved flight record.
        '''
        return any_of(('Approach Information', 'AFR Landing Airport'), available)

    def derive(self,
               approaches=KPV('Approach Information'),
               land_afr_apt=App('AFR Landing Airport')):
        pass


class LandingRunway(FlightAttributeNode):
    name = 'FDR Landing Runway'

    @classmethod
    def can_operate(cls, available):
        return any_of(('Approach Information', 'AFR Landing Runway'), available)

    def derive(self,
               approaches=App('Approach Information'),
               land_afr_rwy=A('AFR Landing Runway'),):
        pass


class OffBlocksDatetime(FlightAttributeNode):
    name = 'FDR Off Blocks Datetime'

    def derive(self, turning=S('Turning On Ground'),
               start_datetime=A('Start Datetime')):
        pass


class OnBlocksDatetime(FlightAttributeNode):
    name = 'FDR On Blocks Datetime'

    def derive(self, turning=S('Turning On Ground'),
               start_datetime=A('Start Datetime')):
        pass


class TakeoffAirport(FlightAttributeNode):
    name = 'FDR Takeoff Airport'

    @classmethod
    def can_operate(cls, available):
        '''
        We can determine a takeoff airport in one of three ways:
        1. Find the nearest airport to the coordinates at takeoff.
        2. Use the airport data provided in the achieved flight record.
        3. If segmetn does not takeoff eg RTO use coordinates off blocks
        '''
        complete_flight = all((
            'Latitude At Liftoff' in available,
            'Longitude At Liftoff' in available,
        ))
        afr = 'AFR Takeoff Airport' in available
        other_segments = all((
            'Latitude Off Blocks' in available,
            'Longitude Off Blocks' in available,
        ))
        return complete_flight or afr or other_segments

    def derive(self,
               toff_lat=KPV('Latitude At Liftoff'),
               toff_lon=KPV('Longitude At Liftoff'),
               toff_afr_apt=A('AFR Takeoff Airport'),
               off_block_lat=KPV('Latitude Off Blocks'),
               off_block_lon=KPV('Longitude Off Blocks'),):
        pass


class TakeoffDatetime(FlightAttributeNode):
    name = 'FDR Takeoff Datetime'

    @classmethod
    def can_operate(cls, available):
        return 'Start Datetime' in available

    def derive(self, liftoff=KTI('Liftoff'), rto=S('Rejected Takeoff'),
               off_blocks=KTI('Off Blocks'), start_dt=A('Start Datetime')):
        pass


class TakeoffFuel(FlightAttributeNode):
    name = 'FDR Takeoff Fuel'

    @classmethod
    def can_operate(cls, available):
        return 'AFR Takeoff Fuel' in available or \
               'Fuel Qty At Liftoff' in available

    def derive(self, afr_takeoff_fuel=A('AFR Takeoff Fuel'),
               liftoff_fuel_qty=KPV('Fuel Qty At Liftoff')):
        pass


class TakeoffGrossWeight(FlightAttributeNode):
    name = 'FDR Takeoff Gross Weight'

    def derive(self, liftoff_gross_weight=KPV('Gross Weight At Liftoff')):
        pass


class TakeoffPilot(FlightAttributeNode, DeterminePilot):
    name = 'FDR Takeoff Pilot'

    @classmethod
    def can_operate(cls, available):
        pilot_flying = all_of((
            'Pilot Flying',
            'Takeoff',
        ), available)
        controls = all_of((
            'Pitch (Capt)',
            'Pitch (FO)',
            'Roll (Capt)',
            'Roll (FO)',
            'Takeoff',
        ), available)
        forces = all_of((
            'Control Column Force (Capt)',
            'Control Column Force (FO)',
            'Takeoff',
        ), available)
        autopilot = all_of((
            'AP (1) Engaged',
            'AP (2) Engaged',
            'Liftoff',
        ), available)
        return 'AFR Takeoff Pilot' in available or pilot_flying or controls or forces or autopilot

    def derive(self,
               pilot_flying=M('Pilot Flying'),
               pitch_capt=P('Pitch (Capt)'),
               pitch_fo=P('Pitch (FO)'),
               roll_capt=P('Roll (Capt)'),
               roll_fo=P('Roll (FO)'),
               cc_capt=P('Control Column Force (Capt)'),
               cc_fo=P('Control Column Force (FO)'),
               ap1_eng=M('AP (1) Engaged'),
               ap2_eng=M('AP (2) Engaged'),
               takeoffs=S('Takeoff'),
               liftoffs=KTI('Liftoff'),
               rejected_toffs=S('Rejected Takeoff'),
               afr_takeoff_pilot=A('AFR Takeoff Pilot')):
        pass


class TakeoffRunway(FlightAttributeNode):
    name = 'FDR Takeoff Runway'

    @classmethod
    def can_operate(cls, available):
        '''
        We can determine a takeoff runway in a number of ways:
        1. Imprecisely using airport and heading during takeoff.
        2. Precisely using airport, heading and coordinates at takeoff.
        3. Use the runway data provided in the achieved flight record.
        '''
        minimum = all((
            'FDR Takeoff Airport' in available,
            'Heading During Takeoff' in available,
        ))
        fallback = 'AFR Takeoff Runway' in available
        return minimum or fallback

    def derive(self,
               toff_fdr_apt=A('FDR Takeoff Airport'),
               toff_afr_rwy=A('AFR Takeoff Runway'),
               toff_hdg=KPV('Heading During Takeoff'),
               toff_lat=KPV('Latitude At Liftoff'),
               toff_lon=KPV('Longitude At Liftoff'),
               accel_start_lat=KPV('Latitude At Takeoff Acceleration Start'),
               accel_start_lon=KPV('Longitude At Takeoff Acceleration Start'),
               precision=A('Precise Positioning')):
        pass


class FlightType(FlightAttributeNode):
    name = 'FDR Flight Type'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, afr_type=A('AFR Type'), fast=S('Fast'), mobile=S('Mobile'),
               liftoffs=KTI('Liftoff'), touchdowns=KTI('Touchdown'),
               touch_and_gos=S('Touch And Go'), rejected_to=S('Rejected Takeoff'),
               eng_start=KTI('Eng Start'), seg_type=A('Segment Type')):
        pass


class LandingDatetime(FlightAttributeNode):
    name = 'FDR Landing Datetime'

    def derive(self, start_datetime=A('Start Datetime'),
               touchdown=KTI('Touchdown')):
        pass


class LandingFuel(FlightAttributeNode):
    name = 'FDR Landing Fuel'

    @classmethod
    def can_operate(cls, available):
        return 'AFR Landing Fuel' in available or \
               'Fuel Qty At Touchdown' in available

    def derive(self, afr_landing_fuel=A('AFR Landing Fuel'),
               touchdown_fuel_qty=KPV('Fuel Qty At Touchdown')):
        pass


class LandingGrossWeight(FlightAttributeNode):
    name = 'FDR Landing Gross Weight'

    def derive(self, touchdown_gross_weight=KPV('Gross Weight At Touchdown')):
        pass


class LandingPilot(FlightAttributeNode, DeterminePilot):
    name = 'FDR Landing Pilot'

    @classmethod
    def can_operate(cls, available):
        pilot_flying = all_of((
            'Pilot Flying',
            'Landing',
        ), available)
        controls = all_of((
            'Pitch (Capt)',
            'Pitch (FO)',
            'Roll (Capt)',
            'Roll (FO)',
            'Landing',
        ), available)
        forces = all_of((
            'Control Column Force (Capt)',
            'Control Column Force (FO)',
            'Landing',
        ), available)
        autopilot = all_of((
            'AP (1) Engaged',
            'AP (2) Engaged',
            'Touchdown',
        ), available)
        return 'AFR Landing Pilot' in available or pilot_flying or controls or forces or autopilot

    def derive(self,
               pilot_flying=M('Pilot Flying'),
               pitch_capt=P('Pitch (Capt)'),
               pitch_fo=P('Pitch (FO)'),
               roll_capt=P('Roll (Capt)'),
               roll_fo=P('Roll (FO)'),
               cc_capt=P('Control Column Force (Capt)'),
               cc_fo=P('Control Column Force (FO)'),
               ap1_eng=M('AP (1) Engaged'),
               ap2_eng=M('AP (2) Engaged'),
               landings=S('Landing'),
               touchdowns=KTI('Touchdown'),
               afr_landing_pilot=A('AFR Landing Pilot')):
        pass


class Version(FlightAttributeNode):
    name = 'FDR Version'

    def derive(self, start_datetime=A('Start Datetime')):
        pass


class Eng1ESN(FlightAttributeNode):
    name = 'Eng (1) Serial Number'

    def derive(self, num=P('Eng (1) ESN')):
        pass


class Eng2ESN(FlightAttributeNode):
    name = 'Eng (2) Serial Number'

    def derive(self, num=P('Eng (2) ESN')):
        pass


class Eng3ESN(FlightAttributeNode):
    name = 'Eng (3) Serial Number'

    def derive(self, num=P('Eng (3) ESN')):
        pass


class Eng4ESN(FlightAttributeNode):
    name = 'Eng (4) Serial Number'

    def derive(self, num=P('Eng (4) ESN')):
        pass
