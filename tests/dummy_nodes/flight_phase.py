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
    def can_operate(cls, available, ac_type=A('Aircraft Type'), seg_type=A('Segment Type')):
        if seg_type and seg_type.value in ('GROUND_ONLY', 'NO_MOVEMENT'):
            return False
        else:
            return 'Altitude AAL For Flight Phases' in available

    def derive(self,
               alt_aal=P('Altitude AAL For Flight Phases'),
               fast=S('Fast')):
        pass


class GoAroundAndClimbout(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, seg_type=A('Segment Type'), ac_type=A('Aircraft Type')):
        if ac_type == helicopter:
            return False
        correct_seg_type = seg_type and seg_type.value not in ('GROUND_ONLY', 'NO_MOVEMENT')
        return 'Altitude AAL For Flight Phases' in available and correct_seg_type

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               level_flights=S('Level Flight')):
        pass


class Holding(FlightPhaseNode):

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               head=P('Heading Continuous'),
               alt_max=KPV('Altitude Max'),
               lat=P('Latitude Smoothed'), lon=P('Longitude Smoothed')):
        pass


class EngHotelMode(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, family=A('Family'), ac_type=A('Aircraft Type')):
        return ac_type == aeroplane and all_deps(cls, available) and family.value in ('ATR-42', 'ATR-72')

    def derive(self, eng2_np=P('Eng (2) Np'),
               eng1_n1=P('Eng (1) N1'),
               eng2_n1=P('Eng (2) N1'),
               groundeds=S('Grounded'),
               prop_brake=M('Propeller Brake')):
        pass


class ApproachAndLanding(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'), seg_type=A('Segment Type')):
        if seg_type and seg_type.value in ('GROUND_ONLY', 'NO_MOVEMENT', 'START_ONLY'):
            return False
        elif ac_type == helicopter:
            return all_of(('Approach', 'Landing'), available)
        else:
            return 'Altitude AAL For Flight Phases' in available

    def derive(self,
               ac_type=A('Aircraft Type'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               level_flights=S('Level Flight'),
               apps=S('Approach'),
               landings=S('Landing')):
        pass


class Approach(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, seg_type=A('Segment Type'), ac_type=A('Aircraft Type')):
        if seg_type and seg_type.value in ('GROUND_ONLY', 'NO_MOVEMENT', 'START_ONLY'):
            return False
        elif ac_type == helicopter:
            return all_of(('Altitude AGL', 'Altitude STD'), available)
        else:
            return 'Altitude AAL For Flight Phases' in available

    def derive(self,
               ac_type=A('Aircraft Type'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               level_flights=S('Level Flight'),
               landings=S('Landing'),
               alt_agl=P('Altitude AGL'),
               alt_std=P('Altitude STD')):
        pass


class BouncedLanding(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type == aeroplane and \
               all_of(('Altitude AAL For Flight Phases', 'Airborne'), available)

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               airs=S('Airborne'), gog=P('Gear On Ground')):
        pass


class ClimbCruiseDescent(FlightPhaseNode):

    def derive(self, alt_std=P('Altitude STD Smoothed'),
               airs=S('Airborne')):
        pass


class Climb(FlightPhaseNode):

    def derive(self,
               toc=KTI('Top Of Climb'),
               eot=KTI('Climb Start')):
        pass


class Climbing(FlightPhaseNode):

    def derive(self, vert_spd=P('Vertical Speed For Flight Phases'),
               airs=S('Airborne')):
        pass


class Cruise(FlightPhaseNode):

    def derive(self,
               ccds=S('Climb Cruise Descent'),
               tocs=KTI('Top Of Climb'),
               tods=KTI('Top Of Descent'),
               air_spd=P('Airspeed')):
        pass


class InitialCruise(FlightPhaseNode):

    def derive(self, cruises=S('Cruise')):
        pass


class Descending(FlightPhaseNode):

    def derive(self, vert_spd=P('Vertical Speed For Flight Phases'),
               airs=S('Airborne')):
        pass


class Descent(FlightPhaseNode):

    def derive(self,
               tod_set=KTI('Top Of Descent'),
               bod_set=KTI('Bottom Of Descent')):
        pass


class DescentToFlare(FlightPhaseNode):

    def derive(self,
            descents=S('Descent'),
            alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class DescentLowClimb(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, seg_type=A('Segment Type'), ac_type=A('Aircraft Type')):
        if ac_type == helicopter:
            return False
        correct_seg_type = seg_type and seg_type.value not in ('GROUND_ONLY', 'NO_MOVEMENT')
        return 'Altitude AAL For Flight Phases' in available and correct_seg_type

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               level_flights=S('Level Flight')):
        pass


class Fast(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'),
                    seg_type=A('Segment Type')):
        if ac_type == helicopter:
            return 'Nr' in available
        else:
            return seg_type and seg_type.value == 'START_AND_STOP' and 'Airspeed' in available

    def derive(self, airspeed=P('Airspeed'), rotor_speed=P('Nr'),
               ac_type=A('Aircraft Type')):
        pass


class FinalApproach(FlightPhaseNode):

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               airs=S('Airborne')):
        pass


class GearExtending(FlightPhaseNode):

    def derive(self, down_in_transit=M('Gear Down In Transit'), airs=S('Airborne')):
        pass


class GearExtended(FlightPhaseNode):

    def derive(self, gear_down=M('Gear Down')):
        pass


class GearRetracting(FlightPhaseNode):

    def derive(self, up_in_transit=M('Gear Up In Transit'), airs=S('Airborne')):
        pass


class GearRetracted(FlightPhaseNode):

    def derive(self, gear_up=M('Gear Up')):
        pass


class IANFinalApproachCourseEstablished(FlightPhaseNode):
    name = 'IAN Final Approach Established'

    def derive(self,
               ian_final=P('IAN Final Approach Course'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               apps=S('Approach Information'),
               ils_freq=P('ILS Frequency'),
               app_src_capt=M('Displayed App Source (Capt)'),
               app_src_fo=M('Displayed App Source (FO)')):
        pass


class IANGlidepathEstablished(FlightPhaseNode):
    name = 'IAN Glidepath Established'

    def derive(self,
               ian_glidepath=P('IAN Glidepath'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               apps=App('Approach Information'),
               app_src_capt=P('Displayed App Source (Capt)'),
               app_src_fo=P('Displayed App Source (FO)')):
        pass


class ILSLocalizerEstablished(FlightPhaseNode):
    name = 'ILS Localizer Established'

    def derive(self, apps=App('Approach Information')):
        pass


class ILSGlideslopeEstablished(FlightPhaseNode):
    name = "ILS Glideslope Established"

    def derive(self, apps=App('Approach Information')):
        pass


class InitialApproach(FlightPhaseNode):

    def derive(self, alt_AAL=P('Altitude AAL For Flight Phases'),
               app_lands=S('Approach')):
        pass


class InitialClimb(FlightPhaseNode):

    def derive(self,
               takeoffs=S('Takeoff'),
               climb_starts=KTI('Climb Start'),
               tocs=KTI('Top Of Climb'),
               alt=P('Altitude STD'),
               ac_type=A('Aircraft Type')):
        pass


class LevelFlight(FlightPhaseNode):

    def derive(self,
               airs=S('Airborne'),
               vrt_spd=P('Vertical Speed For Flight Phases'),
               alt_aal=P('Altitude AAL')):
        pass


class StraightAndLevel(FlightPhaseNode):

    def derive(self,
               levels=S('Level Flight'),
               hdg=P('Heading')):
        pass


class Grounded(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type == helicopter:
            return all_of(('Airborne', 'Airspeed'), available)
        else:
            return 'HDF Duration' in available

    def derive(self,
               airspeed=P('Airspeed'),
               air=S('Airborne'),
               ac_type=A('Aircraft Type'),
               hdf_duration=A('HDF Duration')):
        pass


class Taxiing(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, seg_type=A('Segment Type')):
        default = all_of(('Mobile', 'Takeoff', 'Landing', 'Airborne'), available)
        ground_only = seg_type and seg_type.value == 'GROUND_ONLY' and \
            'Mobile' in available
        return default or ground_only

    def derive(self, mobiles=S('Mobile'), gspd=P('Groundspeed'),
               toffs=S('Takeoff'), lands=S('Landing'),
               rtos=S('Rejected Takeoff'),
               airs=S('Airborne')):
        pass


class Mobile(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available):
        return 'Heading Rate' in available

    def derive(self,
               rot=P('Heading Rate'),
               gspd=P('Groundspeed'),
               airs=S('Airborne'),
               fast=S('Fast'),
               ):
        pass


class Stationary(FlightPhaseNode):

    def derive(self,
               gspd=P('Groundspeed')):
        pass


class Landing(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'), seg_type=A('Segment Type')):
        if seg_type and seg_type.value in ('GROUND_ONLY', 'NO_MOVEMENT'):
            return False
        elif ac_type == helicopter:
            return all_of(('Altitude AGL', 'Collective', 'Airborne'), available)
        else:
            return 'Altitude AAL For Flight Phases' in available

    def derive(self,
               ac_type=A('Aircraft Type'),
               head=P('Heading Continuous'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fast=S('Fast'),
               mobile=S('Mobile'),
               alt_agl=P('Altitude AGL'),
               coll=P('Collective'),
               airs=S('Airborne')):
        pass


class LandingRoll(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return 'Landing' in available and any_of(('Airspeed True', 'Groundspeed'), available) \
               and ac_type == aeroplane

    def derive(self, pitch=P('Pitch'), gspd=P('Groundspeed'),
               aspd=P('Airspeed True'), lands=S('Landing')):
        pass


class TakeoffRunwayHeading(FlightPhaseNode):

    def derive(self,
               hdg=P('Heading'),
               groundeds=S('Grounded'),
               toffs=S('Takeoff Roll') ):
        pass


class RejectedTakeoff(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, seg_type=A('Segment Type')):
        req =  all_of(('Acceleration Longitudinal Offset Removed',
                       'Eng (*) All Running',
                       'Grounded',
                       'Segment Type'
                       ), available)
        if seg_type and seg_type.value == 'START_AND_STOP':
            return req and 'Takeoff Runway Heading' in available
        elif seg_type and seg_type.value == 'GROUND_ONLY':
            return req
        else:
            return False

    def derive(self,
               accel_lon=P('Acceleration Longitudinal Offset Removed'),
               eng_running=M('Eng (*) All Running'),
               groundeds=S('Grounded'),
               eng_n1=P('Eng (*) N1 Max'),
               toff_acc=KTI('Takeoff Acceleration Start'),
               toff_rwy_hdg=S('Takeoff Runway Heading'),
               seg_type=A('Segment Type'),
               toga=M('Takeoff And Go Around')):
        pass


class Takeoff(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'), seg_type=A('Segment Type')):
        if seg_type and seg_type.value in ('GROUND_ONLY', 'NO_MOVEMENT', 'STOP_ONLY'):
            return False
        else:
            return all_of(('Heading Continuous', 'Altitude AAL For Flight Phases', 'Fast', 'Airborne'), available)

    def derive(self,
               head=P('Heading Continuous'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fast=S('Fast'),
               airs=S('Airborne'),
               ):
        pass


class TakeoffRoll(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Takeoff', 'Takeoff Acceleration Start'), available)

    def derive(self, toffs=S('Takeoff'),
               acc_starts=KTI('Takeoff Acceleration Start'),
               pitch=P('Pitch')):
        pass


class TakeoffRollOrRejectedTakeoff(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               trolls=S('Takeoff Roll'),
               rtoffs=S('Rejected Takeoff'),
               helo_toffs=S('Transition Hover To Flight')):
        pass


class TakeoffRotation(FlightPhaseNode):

    def derive(self, lifts=S('Liftoff')):
        pass


class TakeoffRotationWow(FlightPhaseNode):
    name = 'Takeoff Rotation WOW'

    def derive(self, toff_rots=S('Takeoff Rotation')):
        pass


class Takeoff5MinRating(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, eng_type=A('Engine Propulsion'), ac_type=A('Aircraft Type')):
        if eng_type and eng_type.value == 'PROP':
            return all_of(('Takeoff Acceleration Start', 'Liftoff', 'Eng (*) Np Avg', 'Engine Propulsion', 'HDF Duration'), available)
        elif ac_type == helicopter:
            return all_of(('Liftoff', 'HDF Duration'), available)
        else:
            return all_of(('Takeoff Acceleration Start', 'HDF Duration'), available)

    def derive(self, toffs=KTI('Takeoff Acceleration Start'),
               lifts=KTI('Liftoff'),
               eng_np=P('Eng (*) Np Avg'),
               duration=A('HDF Duration'),
               eng_type=A('Engine Propulsion'),
               ac_type=A('Aircraft Type')):
        pass


class GoAround5MinRating(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, eng_type=A('Engine Propulsion')):
        if eng_type and eng_type.value == 'PROP':
            return all_of(('Go Around', 'Eng (*) Np Avg', 'HDF Duration', 'Engine Propulsion'), available)
        else:
            return all_of(('Go Around', 'HDF Duration'), available)

    def derive(self, gas=KTI('Go Around'),
               eng_np=P('Eng (*) Np Avg'),
               duration=A('HDF Duration'),
               eng_type=A('Engine Propulsion')):
        pass


class MaximumContinuousPower(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type == helicopter:
            return all_of(('Airborne', 'Takeoff 5 Min Rating'), available)
        else:
            return all_deps(cls, available)

    def derive(self,
               airborne=S('Airborne'),
               to_ratings=S('Takeoff 5 Min Rating'),
               ga_ratings=S('Go Around 5 Min Rating')):
        pass


class TaxiIn(FlightPhaseNode):

    def derive(self, gnds=S('Mobile'), lands=S('Landing'),
               last_eng_stops=KTI('Last Eng Stop After Touchdown')):
        pass


class TaxiOut(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Mobile', 'Takeoff'), available)

    def derive(self, gnds=S('Mobile'), toffs=S('Takeoff'),
               first_eng_starts=KTI('First Eng Start Before Liftoff')):
        pass


class TCASOperational(FlightPhaseNode):
    name = 'TCAS Operational'

    @classmethod
    def can_operate(cls, available):
        return 'Altitude AAL' in available

    def derive(self, alt_aal=P('Altitude AAL'),
               tcas_cc=M('TCAS Combined Control'),
               tcas_status=P('TCAS Status'),
               tcas_valid=P('TCAS Valid'),
               tcas_fail=P('TCAS Failure')):
        pass


class TCASTrafficAdvisory(FlightPhaseNode):
    name = 'TCAS Traffic Advisory'

    @classmethod
    def can_operate(cls, available):
        return any_one_of(('TCAS TA', 'TCAS All Threat Traffic', 'TCAS Traffic Alert', 'TCAS TA (1)'), available) \
            and 'TCAS Operational' in available

    def derive(self, tcas_ops=S('TCAS Operational'),
               tcas_ta1=M('TCAS TA'),
               tcas_ta2=M('TCAS All Threat Traffic'),
               tcas_ta3=M('TCAS Traffic Alert'),
               tcas_ta4=M('TCAS TA (1)'),
               tcas_ras=S('TCAS Resolution Advisory'),
               ):
        pass


class TCASResolutionAdvisory(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('TCAS Combined Control', 'TCAS Operational'), available) or \
               all_of(('TCAS RA', 'TCAS Operational'), available)
    name = 'TCAS Resolution Advisory'

    def derive(self, tcas_cc=M('TCAS Combined Control'),
               tcas_ops=S('TCAS Operational'),
               tcas_ra=M('TCAS RA')):
        pass


class TurningInAir(FlightPhaseNode):

    def derive(self, rate_of_turn=P('Heading Rate'),
               airborne=S('Airborne'),
               ac_type=A('Aircraft Type')):
        pass


class TurningOnGround(FlightPhaseNode):

    def derive(self, rate_of_turn=P('Heading Rate'), taxi=S('Taxiing')):
        pass


class TwoDegPitchTo35Ft(FlightPhaseNode):
    name = '2 Deg Pitch To 35 Ft'

    def derive(self, takeoff_rolls=S('Takeoff Roll'), takeoffs=S('Takeoff')):
        pass


class ShuttlingApproach(FlightPhaseNode):

    def derive(self, approaches=App('Approach Information')):
        pass


class AirborneRadarApproach(FlightPhaseNode):

    def derive(self, approaches=App('Approach Information')):
        pass


class BaroDifference(FlightPhaseNode):

    @classmethod
    def can_operate(cls, available, manufacturer=A('Manufacturer')):
        baro_setting_sel = True
        if manufacturer and manufacturer.value == 'Airbus':
            baro_setting_sel = any((
                any_of(('Baro Setting Selection', 'Baro Correction (ISIS)'), available),
                all_of(('Baro Setting Selection (Capt)', 'Baro Setting Selection (FO)'), available)
            ))
        two_baro =  all_of(('Baro Correction (Capt)', 'Baro Correction (FO)'), available)
        return two_baro and baro_setting_sel

    def derive(self, baro_cpt=P('Baro Correction (Capt)'),
               baro_fo=P('Baro Correction (FO)'),
               baro_sel=M('Baro Setting Selection'),
               baro_sel_cpt=M('Baro Setting Selection (Capt)'),
               baro_sel_fo=M('Baro Setting Selection (FO)'),
               baro_cor_isis=P('Baro Correction (ISIS)'),
               fasts=S('Fast')):
        pass
