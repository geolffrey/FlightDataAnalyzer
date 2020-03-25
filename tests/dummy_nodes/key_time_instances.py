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


class BottomOfDescent(KeyTimeInstanceNode):

    def derive(self, alt_std=P('Altitude STD Smoothed'),
               ccd=S('Climb Cruise Descent')):
        pass


class AltitudePeak(KeyTimeInstanceNode):

    def derive(self, alt_aal=P('Altitude AAL')):
        pass


class APEngagedSelection(KeyTimeInstanceNode):
    name = 'AP Engaged Selection'

    def derive(self, ap=M('AP Engaged'), phase=S('Fast')):
        pass


class APDisengagedSelection(KeyTimeInstanceNode):
    name = 'AP Disengaged Selection'

    def derive(self, ap=M('AP Engaged'), phase=S('Fast')):
        pass


class ATEngagedSelection(KeyTimeInstanceNode):
    name = 'AT Engaged Selection'

    def derive(self, at=M('AT Engaged'), phase=S('Airborne')):
        pass


class ATDisengagedSelection(KeyTimeInstanceNode):
    name = 'AT Disengaged Selection'

    def derive(self, at=P('AT Engaged'), phase=S('Airborne')):
        pass


class Transmit(KeyTimeInstanceNode):

    def derive(self, transmitting=M('Transmitting')):
        pass


class ClimbStart(KeyTimeInstanceNode):

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'), liftoffs=KTI('Liftoff'),
               tocs=KTI('Top Of Climb')):
        pass


class ClimbAccelerationStart(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available, eng_type=A('Engine Propulsion')):
        spd_sel = 'Airspeed Selected' in available
        spd = all_of(('Airspeed', 'Flap Lever Set'), available)
        jet = (eng_type and eng_type.value == 'JET' and
               'Throttle Levers' in available)
        prop = (eng_type and eng_type.value == 'PROP' and
                'Eng (*) Np Max' in available)
        alt = all_of(('Engine Propulsion', 'Altitude AAL For Flight Phases'), available)
        return all_of(('Initial Climb', 'Altitude When Climbing'), available) and \
               (spd_sel or spd or jet or prop or alt) and \
               not (eng_type and eng_type.value == 'ROTOR')

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               initial_climbs=S('Initial Climb'),
               alt_climbing=KTI('Altitude When Climbing'),
               spd_sel=P('Airspeed Selected'),
               spd_sel_fmc=P('Airspeed Selected (FMC)'),
               eng_type=A('Engine Propulsion'),
               eng_np=P('Eng (*) Np Max'),
               throttle=P('Throttle Levers'),
               spd=P('Airspeed'),
               flap=KTI('Flap Lever Set')):
        pass


class ClimbThrustDerateDeselected(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available, ac_family=A('Family')):
        if ac_family and ac_family.value == 'B787':
            return True
        return False

    def derive(self, climb_derate_1=P('AT Climb 1 Derate'),
               climb_derate_2=P('AT Climb 2 Derate'),):
        pass


class APUStart(KeyTimeInstanceNode):
    name = 'APU Start'

    def derive(self,
               apu=P('APU Running')):
        pass


class APUStop(KeyTimeInstanceNode):
    name = 'APU Stop'

    def derive(self,
               apu=P('APU Running')):
        pass


class LastAPUStartBeforeLiftoff(KeyTimeInstanceNode):
    name = 'Last APU Start Before Liftoff'

    def derive(self, apu_starts=KTI('APU Start'), liftoffs=KTI('Liftoff')):
        pass


class EngStart(KeyTimeInstanceNode):
    NAME_VALUES = NAME_VALUES_ENGINE

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng_1_n1=P('Eng (1) N1'),
               eng_2_n1=P('Eng (2) N1'),
               eng_3_n1=P('Eng (3) N1'),
               eng_4_n1=P('Eng (4) N1'),
               eng_1_n2=P('Eng (1) N2'),
               eng_2_n2=P('Eng (2) N2'),
               eng_3_n2=P('Eng (3) N2'),
               eng_4_n2=P('Eng (4) N2'),
               eng_1_n3=P('Eng (1) N3'),
               eng_2_n3=P('Eng (2) N3'),
               eng_3_n3=P('Eng (3) N3'),
               eng_4_n3=P('Eng (4) N3'),
               eng_1_ng=P('Eng (1) Ng'),
               eng_2_ng=P('Eng (2) Ng'),
               eng_3_ng=P('Eng (3) Ng'),
               eng_4_ng=P('Eng (4) Ng'),
               ac_type=A('Aircraft Type')):
        pass


class FirstEngStartBeforeLiftoff(KeyTimeInstanceNode):

    def derive(self, eng_starts=KTI('Eng Start'), eng_count=A('Engine Count'),
               liftoffs=KTI('Liftoff')):
        pass


class LastEngStartBeforeLiftoff(KeyTimeInstanceNode):

    def derive(self, eng_starts=KTI('Eng Start'), eng_count=A('Engine Count'),
               liftoffs=KTI('Liftoff')):
        pass


class EngStop(KeyTimeInstanceNode):
    NAME_VALUES = NAME_VALUES_ENGINE

    @classmethod
    def can_operate(cls, available):
        return 'Eng Start' in available and (
            any_of(('Eng (%d) N1' % n for n in range(1, 5)), available) or
            any_of(('Eng (%d) N2' % n for n in range(1, 5)), available)
        )

    def derive(self,
               eng_1_n1=P('Eng (1) N1'),
               eng_2_n1=P('Eng (2) N1'),
               eng_3_n1=P('Eng (3) N1'),
               eng_4_n1=P('Eng (4) N1'),
               eng_1_n2=P('Eng (1) N2'),
               eng_2_n2=P('Eng (2) N2'),
               eng_3_n2=P('Eng (3) N2'),
               eng_4_n2=P('Eng (4) N2'),
               eng_1_n3=P('Eng (1) N3'),
               eng_2_n3=P('Eng (2) N3'),
               eng_3_n3=P('Eng (3) N3'),
               eng_4_n3=P('Eng (4) N3'),
               eng_1_ng=P('Eng (1) Ng'),
               eng_2_ng=P('Eng (2) Ng'),
               eng_3_ng=P('Eng (3) Ng'),
               eng_4_ng=P('Eng (4) Ng'),
               eng_start=KTI('Eng Start'),
               ac_type=A('Aircraft Type')):
        pass


class LastEngStopAfterTouchdown(KeyTimeInstanceNode):

    def derive(self, eng_stops=KTI('Eng Stop'), eng_count=A('Engine Count'),
               touchdowns=KTI('Touchdown'), duration=A('HDF Duration')):
        pass


class EnterHold(KeyTimeInstanceNode):

    def derive(self, holds=S('Holding')):
        pass


class ExitHold(KeyTimeInstanceNode):

    def derive(self, holds=S('Holding')):
        pass


class EngFireExtinguisher(KeyTimeInstanceNode):

    def derive(self, e1f=P('Eng (1) Fire Extinguisher'),
               e2f=P('Eng (2) Fire Extinguisher'),
               airborne=S('Airborne')):
        pass


class GoAround(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available):
        return ('Descent Low Climb' in available and
                'Altitude AAL For Flight Phases' in available)

    def derive(self, dlcs=S('Descent Low Climb'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_rad=P('Altitude Radio')):
        pass


class TopOfClimb(KeyTimeInstanceNode):

    def derive(self, alt_std=P('Altitude STD Smoothed'),
               ccd=S('Climb Cruise Descent')):
        pass


class TopOfDescent(KeyTimeInstanceNode):

    def derive(self, alt_std=P('Altitude STD Smoothed'),
               ccd=S('Climb Cruise Descent')):
        pass


class FlapLeverSet(KeyTimeInstanceNode):
    NAME_VALUES = NAME_VALUES_LEVER

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available)

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)')):
        pass


class FirstFlapExtensionWhileAirborne(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available):
        return 'Airborne' in available and any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
        ), available)

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class FlapExtensionWhileAirborne(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available):
        return 'Airborne' in available and any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
        ), available)

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class FlapLoadReliefSet(KeyTimeInstanceNode):

    def derive(self, flr=M('Flap Load Relief')):
        pass


class FlapAlternateArmedSet(KeyTimeInstanceNode):

    def derive(self, faa=M('Flap Alternate Armed')):
        pass


class SlatAlternateArmedSet(KeyTimeInstanceNode):

    def derive(self, saa=M('Slat Alternate Armed')):
        pass


class FlapRetractionWhileAirborne(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available):
        return 'Airborne' in available and any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
        ), available)

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class FlapRetractionDuringGoAround(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available):
        return 'Go Around And Climbout' in available and any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
        ), available)

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               go_arounds=S('Go Around And Climbout')):
        pass


class GearDownSelection(KeyTimeInstanceNode):

    def derive(self,
               gear_dn_sel=M('Gear Down Selected'),
               airborne=S('Airborne')):
        pass


class GearUpSelection(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type != helicopter:
            return all_deps(cls, available)
        else:
            return all_of(('Gear Up Selected', 'Airborne'), available)

    def derive(self,
               gear_up_sel=M('Gear Up Selected'),
               airborne=S('Airborne'),
               go_arounds=S('Go Around And Climbout')):
        pass


class GearUpSelectionDuringGoAround(KeyTimeInstanceNode):

    def derive(self,
               gear_up_sel=M('Gear Up Selected'),
               go_arounds=S('Go Around And Climbout')):
        pass


class TAWSGlideslopeCancelPressed(KeyTimeInstanceNode):
    name = 'TAWS Glideslope Cancel Pressed'

    def derive(self, tgc=P('TAWS Glideslope Cancel'), airborne=S('Airborne')):
        pass


class TAWSMinimumsTriggered(KeyTimeInstanceNode):
    name = 'TAWS Minimums Triggered'

    def derive(self, tmin=P('TAWS Minimums'), airborne=S('Airborne')):
        pass


class TAWSTerrainOverridePressed(KeyTimeInstanceNode):
    name = 'TAWS Terrain Override Pressed'

    def derive(self, tmin=P('TAWS Terrain Override'), airborne=S('Airborne')):
        pass


class TakeoffTurnOntoRunway(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type and ac_type.value == 'helicopter':
            return False
        else:
            return all_deps(cls, available)

    def derive(self, head=P('Heading Continuous'),
               toffs=S('Takeoff'),
               fast=S('Fast')):
        pass


class TakeoffAccelerationStart(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type and ac_type.value == 'helicopter':
            return False
        else:
            if 'Acceleration Longitudinal' in available:
                return all_of(('Airspeed', 'Takeoff', 'Acceleration Longitudinal Offset Removed'), available)
            else:
                return all_of(('Airspeed', 'Takeoff'), available)

    def derive(self, speed=P('Airspeed'), takeoffs=S('Takeoff'),
               accel=P('Acceleration Longitudinal Offset Removed'),
               accel_raw=P('Acceleration Longitudinal')):
        pass


class TakeoffStart(KeyTimeInstanceNode):

    def derive(self,
               acc_start=KTI('Takeoff Acceleration Start'),
               throttle=P('Throttle Levers')):
        pass


class TakeoffPeakAcceleration(KeyTimeInstanceNode):

    def derive(self, toffs=S('Takeoff'),
               accel=P('Acceleration Longitudinal')):
        pass


class Liftoff(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available, seg_type=A('Segment Type')):
        if seg_type and seg_type.value in ('GROUND_ONLY', 'NO_MOVEMENT', 'MID_FLIGHT', 'STOP_ONLY'):
            return False
        return 'Airborne' in available

    def derive(self,
               vert_spd=P('Vertical Speed Inertial'),
               acc_norm=P('Acceleration Normal Offset Removed'),
               vert_spd_baro=P('Vertical Speed'),
               alt_rad=P('Altitude Radio Offset Removed'),
               gog=M('Gear On Ground'),
               airs=S('Airborne'),
               frame=A('Frame'),
               ac_type=A('Aircraft Type')):
        pass


class LowestAltitudeDuringApproach(KeyTimeInstanceNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               alt_rad=P('Altitude Radio'),
               approaches=S('Approach And Landing')):
        pass


class InitialClimbStart(KeyTimeInstanceNode):

    def derive(self, toffs=S('Takeoff')):
        pass


class LandingStart(KeyTimeInstanceNode):

    def derive(self, landings=S('Landing')):
        pass


class TouchAndGo(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Altitude AAL', 'Go Around And Climbout'), available)

    def derive(self, alt_aal=P('Altitude AAL'), go_around_and_climbouts=S('Go Around And Climbout'),
               gog=P('Gear On Ground')):
        pass


class Touchdown(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'), seg_type=A('Segment Type')):
        if 'Acceleration Longitudinal' in available and \
           'Acceleration Longitudinal Offset Removed' not in available:
            return False
        if ac_type and ac_type.value == 'helicopter':
            return 'Airborne' in available
        elif seg_type and seg_type.value in ('GROUND_ONLY', 'NO_MOVEMENT', 'MID_FLIGHT', 'START_ONLY'):
            return False
        else:
            return all_of(('Altitude AAL', 'Landing'), available)

    def derive(self, acc_norm=P('Acceleration Normal'),
               acc_long=P('Acceleration Longitudinal Offset Removed'),
               alt=P('Altitude AAL'),
               alt_rad=P('Altitude Radio'),
               gog=M('Gear On Ground'),
               lands=S('Landing'),
               flap=P('Flap'),
               manufacturer=A('Manufacturer'),
               family=A('Family'),
               airs=S('Airborne'),
               ac_type=A('Aircraft Type'),
               accel=P('Acceleration Longitudinal')):
        pass


class OffshoreTouchdown(KeyTimeInstanceNode):

    def derive(self, touchdowns=KTI('Touchdown'),
               offshore=M('Offshore')):
        pass


class OnshoreTouchdown(KeyTimeInstanceNode):

    def derive(self, touchdowns=KTI('Touchdown'),
               offshore=M('Offshore')):
        pass


class LandingDecelerationEnd(KeyTimeInstanceNode):

    def derive(self, speed=P('Airspeed'), landings=S('Landing')):
        pass


class LandingTurnOffRunway(KeyTimeInstanceNode):

    def derive(self, apps=App('Approach Information')):
        pass


class AltitudeWhenClimbing(KeyTimeInstanceNode):
    NAME_VALUES = NAME_VALUES_CLIMB

    def derive(self,
               takeoff=S('Takeoff'),
               initial_climb=S('Initial Climb'),
               climb=S('Climb'),
               alt_aal=P('Altitude AAL'),
               alt_std=P('Altitude STD Smoothed')):
        pass


class AltitudeWhenDescending(KeyTimeInstanceNode):
    NAME_VALUES = NAME_VALUES_DESCENT

    def derive(self, descending=S('Descent'),
               alt_aal=P('Altitude AAL'),
               alt_std=P('Altitude STD Smoothed')):
        pass


class AltitudeBeforeLevelFlightWhenClimbing(KeyTimeInstanceNode):
    NAME_VALUES = {'altitude': [1000, 2000]}

    def derive(self,
               aal=P('Altitude STD Smoothed'),
               level_flight=S('Level Flight'),
               climbing=S('Climb')):
        pass


class AltitudeBeforeLevelFlightWhenDescending(KeyTimeInstanceNode):
    NAME_VALUES = {'altitude': [1000, 2000]}

    def derive(self,
               aal=P('Altitude STD Smoothed'),
               level_flight=S('Level Flight'),
               descending=S('Descending')):
        pass


class MinsToTouchdown(KeyTimeInstanceNode):
    NAME_VALUES = {'time': [5, 4, 3, 2, 1]}

    def derive(self, touchdowns=KTI('Touchdown'),
               liftoffs=KTI('Liftoff')):
        pass


class SecsToTouchdown(KeyTimeInstanceNode):
    NAME_VALUES = {'time': [90, 30, 20]}

    def derive(self, touchdowns=KTI('Touchdown'),
               liftoffs=KTI('Liftoff')):
        pass


class DistanceToTouchdown(KeyTimeInstanceNode):
    NAME_VALUES = {'distance': [0.8, 1.0, 1.5, 2.0]}

    def derive(self, dtl=P('Distance To Landing'),
               touchdowns=KTI('Touchdown')):
        pass


class Autoland(KeyTimeInstanceNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('AP Channels Engaged', 'Touchdown'), available)

    def derive(self, ap=M('AP Channels Engaged'), touchdowns=KTI('Touchdown'),
               family=A('Family')):
        pass


class LocalizerEstablishedStart(KeyTimeInstanceNode):

    def derive(self, ilss=S('ILS Localizer Established')):
        pass


class LocalizerEstablishedEnd(KeyTimeInstanceNode):

    def derive(self, ilss=S('ILS Localizer Established')):
        pass


class GlideslopeEstablishedStart(KeyTimeInstanceNode):

    def derive(self, ilss=S('ILS Glideslope Established')):
        pass


class GlideslopeEstablishedEnd(KeyTimeInstanceNode):

    def derive(self, ilss=S('ILS Glideslope Established')):
        pass


class IANFinalApproachEstablishedStart(KeyTimeInstanceNode):
    name = 'IAN Final Approach Established Start'

    def derive(self, ilss=S('IAN Final Approach Established')):
        pass


class IANFinalApproachEstablishedEnd(KeyTimeInstanceNode):
    name = 'IAN Final Approach Established End'

    def derive(self, ilss=S('IAN Final Approach Established')):
        pass


class IANGlidepathEstablishedStart(KeyTimeInstanceNode):
    name = 'IAN Glidepath Established Start'

    def derive(self, ilss=S('IAN Glidepath Established')):
        pass


class IANGlidepathEstablishedEnd(KeyTimeInstanceNode):
    name = 'IAN Glidepath Established End'

    def derive(self, ilss=S('IAN Glidepath Established')):
        pass


class RejectedTakeoffStart(KeyTimeInstanceNode):

    def derive(self, rejs=S('Rejected Takeoff')):
        pass


class MovementStart(KeyTimeInstanceNode):

    def derive(self, stationary=S('Stationary')):
        pass


class MovementStop(KeyTimeInstanceNode):

    def derive(self, stationary=S('Stationary')):
        pass


class OffBlocks(KeyTimeInstanceNode):

    def derive(self, mobile=S('Mobile')):
        pass


class OnBlocks(KeyTimeInstanceNode):

    def derive(self, mobile=S('Mobile'), hdg=P('Heading')):
        pass


class FirstEngFuelFlowStart(KeyTimeInstanceNode):

    def derive(self, ff=S('Eng (*) Fuel Flow')):
        pass


class LastEngFuelFlowStop(KeyTimeInstanceNode):

    def derive(self, ff=S('Eng (*) Fuel Flow')):
        pass

class DistanceFromLocationMixin(object):
    pass


class DistanceFromTakeoffAirport(KeyTimeInstanceNode, DistanceFromLocationMixin):
    NAME_VALUES = NAME_VALUES_DISTANCE

    def derive(self,
               lon=P('Longitude Smoothed'),
               lat=P('Latitude Smoothed'),
               airs=S('Airborne'),
               apt=A('FDR Takeoff Airport')):
        pass


class DistanceFromLandingAirport(KeyTimeInstanceNode, DistanceFromLocationMixin):
    NAME_VALUES = NAME_VALUES_DISTANCE

    def derive(self,
               lon=P('Longitude Smoothed'),
               lat=P('Latitude Smoothed'),
               airs=S('Airborne'),
               apt=A('FDR Landing Airport')):
        pass


class DistanceFromThreshold(KeyTimeInstanceNode, DistanceFromLocationMixin):
    NAME_VALUES = NAME_VALUES_RANGES

    def derive(self,
               lon=P('Longitude Smoothed'),
               lat=P('Latitude Smoothed'),
               airs=S('Airborne'),
               rwy=A('FDR Landing Runway')):
        pass
