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


class Airspeed500To100FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent')):
        pass


class Airspeed500To100FtMin(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent'),
               ac_type=A('Aircraft Type')):
        pass


class Airspeed100To20FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent'),
               ac_type=A('Aircraft Type')):
        pass


class Airspeed100To20FtMin(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent'),
               ac_type=A('Aircraft Type')):
        pass


class Airspeed20FtToTouchdownMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               touchdowns=KTI('Touchdown')):
        pass


class Airspeed2NMToOffshoreTouchdown(KeyPointValueNode):
    name = 'Airspeed 2 NM To Touchdown'

    def derive(self, airspeed=P('Airspeed'), dtts=P('Distance To Touchdown'),
               touchdown=KTI('Offshore Touchdown')):
        pass


class AirspeedAbove101PercentRotorSpeed(KeyPointValueNode):
    name = 'Airspeed Above 101 Percent Rotor Speed'

    def derive(self,
               airspeed=P('Airspeed'),
               airborne=S('Airborne'),
               nr=P('Nr'),
               ):
        pass


class AirspeedAbove500FtMin(KeyPointValueNode):

    def derive(self, air_spd= P('Airspeed'), alt_agl=P('Altitude AGL For Flight Phases'),
               approaches=App('Approach Information')):
        pass


class AirspeedAbove500FtMinOffshoreSpecialProcedure(KeyPointValueNode):

    def derive(self, air_spd= P('Airspeed'), alt_agl=P('Altitude AGL For Flight Phases'),
               approaches=App('Approach Information')):
        pass


class AirspeedAt200FtDuringOnshoreApproach(KeyPointValueNode):

    def derive(self, air_spd=P('Airspeed'), alt_agl=P('Altitude AGL For Flight Phases'),
               approaches=App('Approach Information'), offshore=M('Offshore')):
        pass


class AirspeedAtAPGoAroundEngaged(KeyPointValueNode):
    name = 'Airspeed At AP Go Around Engaged'

    def derive(self, air_spd=P('Airspeed'), airs=S('Airborne'),
               ap_mode=M('AP Pitch Mode (1)')):
        pass


class AirspeedWhileAPHeadingEngagedMin(KeyPointValueNode):
    name = 'Airspeed While AP Heading Engaged Min'

    def derive(self, air_spd=P('Airspeed'), airs=S('Airborne'),
               ap_mode=M('AP Roll-Yaw Mode (1)')):
        pass


class AirspeedWhileAPVerticalSpeedEngagedMin(KeyPointValueNode):
    name = 'Airspeed While AP Vertical Speed Engaged Min'

    def derive(self, air_spd=P('Airspeed'), airs=S('Airborne'),
               ap_mode=M('AP Collective Mode (1)')):
        pass


class AirspeedDuringAutorotationMax(KeyPointValueNode):

    def derive(self, airspeed=P('Airspeed'), phase=S('Autorotation')):
        pass


class AirspeedDuringAutorotationMin(KeyPointValueNode):

    def derive(self, airspeed=P('Airspeed'), phase=S('Autorotation')):
        pass


class AltitudeDensityMax(KeyPointValueNode):

    def derive(self, alt_density=P('Altitude Density'), airborne=S('Airborne')):
        pass


class AltitudeRadioDuringAutorotationMin(KeyPointValueNode):

    def derive(self, alt_rad=P('Altitude Radio'), autorotation=S('Autorotation')):
        pass


class AltitudeDuringCruiseMin(KeyPointValueNode):

    def derive(self, alt_agl=P('Altitude AGL'), cruise=S('Cruise')):
        pass


class CollectiveFrom10To60PercentDuration(KeyPointValueNode):
    name = 'Collective From 10 To 60% Duration'

    def derive(self, collective=P('Collective'), rtr=S('Rotors Turning')):
        pass


class TailRotorPedalWhileTaxiingABSMax(KeyPointValueNode):
    name = 'Tail Rotor Pedal While Taxiing ABS Max'

    def derive(self, pedal=P('Tail Rotor Pedal'), taxiing=S('Taxiing')):
        pass


class TailRotorPedalWhileTaxiingMax(KeyPointValueNode):

    def derive(self, pedal=P('Tail Rotor Pedal'), taxiing=S('Taxiing')):
        pass


class TailRotorPedalWhileTaxiingMin(KeyPointValueNode):

    def derive(self, pedal=P('Tail Rotor Pedal'), taxiing=S('Taxiing')):
        pass


class TailRotorPedalOnGroundFor5SecMax(KeyPointValueNode):

    def derive(self,
               collective=P('Collective'),
               nr=P('Nr'),
               grounded=S('Grounded'),
               stationary=S('Stationary'),
               pedal=P('Tail Rotor Pedal'),):
        pass


class CyclicDuringTaxiMax(KeyPointValueNode):

    def derive(self, cyclic=P('Cyclic Angle'), taxi=S('Taxiing'), rtr=S('Rotors Turning')):
        pass


class CyclicLateralDuringTaxiMax(KeyPointValueNode):

    def derive(self, cyclic=P('Cyclic Lateral'), taxi=S('Taxiing'), rtr=S('Rotors Turning')):
        pass


class CyclicAftDuringTaxiMax(KeyPointValueNode):

    def derive(self, cyclic=P('Cyclic Fore-Aft'), taxi=S('Taxiing'), rtr=S('Rotors Turning')):
        pass


class CyclicForeDuringTaxiMax(KeyPointValueNode):

    def derive(self, cyclic=P('Cyclic Fore-Aft'), taxi=S('Taxiing'), rtr=S('Rotors Turning')):
        pass


class EngTorqueExceeding100Percent(KeyPointValueNode):

    def derive(self, avg_torque = P('Eng (*) Torque Avg')):
        pass


class EngTorqueExceeding110Percent(KeyPointValueNode):

    def derive(self, avg_torque = P('Eng (*) Torque Avg')):
        pass


class EngN2DuringMaximumContinuousPowerMin(KeyPointValueNode):
    name = 'Eng N2 During Maximum Continuous Power Min'

    def derive(self,
               eng_n2_min=P('Eng (*) N2 Min'),
               mcp=S('Maximum Continuous Power')):
        pass


class EngTorqueWithOneEngineInoperativeMax(KeyPointValueNode):

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               airborne=S('Airborne'),
               one_eng=M('One Engine Inoperative')):
        pass


class EngTorqueAbove90KtsMax(KeyPointValueNode):
    name = 'Eng Torque Above 90 Kts Max'

    def derive(self, eng=P('Eng (*) Torque Max'), air_spd=P('Airspeed')):
        pass


class EngTorqueAbove100KtsMax(KeyPointValueNode):
    name = 'Eng Torque Above 100 Kts Max'

    def derive(self, eng=P('Eng (*) Torque Max'), air_spd=P('Airspeed')):
        pass


class MGBOilTempMax(KeyPointValueNode):
    name = 'MGB Oil Temp Max'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        aircraft = ac_type == helicopter
        gearbox = any_of(('MGB Oil Temp', 'MGB (Fwd) Oil Temp',
                          'MGB (Aft) Oil Temp'), available)
        airborne = 'Airborne' in available
        return aircraft and gearbox and airborne

    def derive(self, mgb=P('MGB Oil Temp'), mgb_fwd=P('MGB (Fwd) Oil Temp'),
               mgb_aft=P('MGB (Aft) Oil Temp'), airborne=S('Airborne')):
        pass


class MGBOilPressMax(KeyPointValueNode):
    name = 'MGB Oil Press Max'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        aircraft = ac_type == helicopter
        gearbox = any_of(('MGB Oil Press', 'MGB (Fwd) Oil Press',
                          'MGB (Aft) Oil Press'), available)
        airborne = 'Airborne' in available
        return aircraft and gearbox and airborne

    def derive(self, mgb=P('MGB Oil Press'), mgb_fwd=P('MGB (Fwd) Oil Press'),
               mgb_aft=P('MGB (Aft) Oil Press'), airborne=S('Airborne')):
        pass


class MGBOilPressMin(KeyPointValueNode):
    name = 'MGB Oil Press Min'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        aircraft = ac_type == helicopter
        gearbox = any_of(('MGB Oil Press', 'MGB (Fwd) Oil Press',
                          'MGB (Aft) Oil Press'), available)
        airborne = 'Airborne' in available
        return aircraft and gearbox and airborne

    def derive(self, mgb=P('MGB Oil Press'), mgb_fwd=P('MGB (Fwd) Oil Press'),
               mgb_aft=P('MGB (Aft) Oil Press'), airborne=S('Airborne')):
        pass


class MGBOilPressLowDuration(KeyPointValueNode):
    name = 'MGB Oil Press Low Duration'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        aircraft = ac_type == helicopter
        gearbox = any_of(('MGB Oil Press Low', 'MGB Oil Press Low (1)',
                          'MGB Oil Press Low (2)'), available)
        airborne = 'Airborne' in available
        return aircraft and gearbox and airborne

    def derive(self, mgb=M('MGB Oil Press Low'),
               mgb1=M('MGB Oil Press Low (1)'),
               mgb2=M('MGB Oil Press Low (2)'),
               airborne=S('Airborne')):
        pass


class CGBOilTempMax(KeyPointValueNode):
    name = 'CGB Oil Temp Max'

    def derive(self, cgb=P('CGB Oil Temp'), airborne=S('Airborne')):
        pass


class CGBOilPressMax(KeyPointValueNode):
    name = 'CGB Oil Press Max'

    def derive(self, cgb=P('CGB Oil Press'), airborne=S('Airborne')):
        pass


class CGBOilPressMin(KeyPointValueNode):
    name = 'CGB Oil Press Min'

    def derive(self, cgb=P('CGB Oil Press'), airborne=S('Airborne')):
        pass


class IGBOilTempMax(KeyPointValueNode):
    name = 'IGB Oil Temp Max'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        aircraft = ac_type == helicopter
        gearbox = 'IGB Oil Temp'in available
        airborne = 'Airborne' in available
        return aircraft and gearbox and airborne

    def derive(self, igb=P('IGB Oil Temp'), airborne=S('Airborne')):
        pass


class TGBOilTempMax(KeyPointValueNode):
    name = 'TGB Oil Temp Max'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        aircraft = ac_type == helicopter
        gearbox = 'TGB Oil Temp'in available
        airborne = 'Airborne' in available
        return aircraft and gearbox and airborne

    def derive(self, tgb=P('TGB Oil Temp'), airborne=S('Airborne')):
        pass


class HeadingVariation1_5NMTo1_0NMFromOffshoreTouchdownMaxStandardApproach(KeyPointValueNode):
    name = 'Heading Variation 1.5 NM To 1.0 NM From Offshore Touchdown Max Standard Approach'

    def derive(self, heading=P('Heading Continuous'),
               dtts=KTI('Distance To Touchdown'),
               offshore_twn=KTI('Offshore Touchdown'),
               approaches=App('Approach Information')):
        pass


class HeadingVariation1_5NMTo1_0NMFromOffshoreTouchdownMaxSpecialProcedure(KeyPointValueNode):
    name = 'Heading Variation 1.5 NM To 1.0 NM From Offshore Touchdown Max Special Procedure'

    def derive(self, heading=P('Heading Continuous'),
               dtts=KTI('Distance To Touchdown'),
               offshore_twn=KTI('Offshore Touchdown'),
               approaches=App('Approach Information')):
        pass


class TrackVariation100To50Ft(KeyPointValueNode):
    name = 'Track Variation 100 To 50 Ft'

    def derive(self, track=P('Track'),
               alt_agl=P('Altitude AGL')):
        pass


class HeadingDuringLanding(KeyPointValueNode):

    def derive(self,
               hdg=P('Heading Continuous'),
               land_helos=S('Transition Flight To Hover')):
        pass


class Groundspeed20FtToTouchdownMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Groundspeed'),
               alt_agl=P('Altitude AGL'),
               touchdowns=KTI('Touchdown')):
        pass


class Groundspeed20SecToOffshoreTouchdownMax(KeyPointValueNode):

    def derive(self, groundspeed=P('Groundspeed'),
               touchdown=KTI('Offshore Touchdown'),
               secs_tdwn=KTI('Secs To Touchdown')):
        pass


class Groundspeed0_8NMToOffshoreTouchdownSpecialProcedure(KeyPointValueNode):
    name = 'Groundspeed 0.8 NM To Offshore Touchdown Special Procedure'

    def derive(self, groundspeed=P('Groundspeed'),
               dtts=KTI('Distance To Touchdown'), touchdown=KTI('Offshore Touchdown'),
               approaches=App('Approach Information')):
        pass


class Groundspeed0_8NMToOffshoreTouchdownStandardApproach(KeyPointValueNode):
    name = 'Groundspeed 0.8 NM To Offshore Touchdown Standard Approach'

    def derive(self, groundspeed=P('Groundspeed'),
               dtts=KTI('Distance To Touchdown'), touchdown=KTI('Offshore Touchdown'),
               approaches=App('Approach Information')):
        pass


class GroundspeedBelow15FtFor20SecMax(KeyPointValueNode):

    def derive(self, gnd_spd=P('Groundspeed'), alt_aal=P('Altitude AAL For Flight Phases'), airborne=S('Airborne')):
        pass


class GroundspeedWhileAirborneWithASEOff(KeyPointValueNode):
    name = 'Groundspeed While Airborne With ASE Off'

    def derive(self, gnd_spd=P('Groundspeed'), ase=M('ASE Engaged'), airborne=S('Airborne')):
        pass


class GroundspeedWhileHoverTaxiingMax(KeyPointValueNode):
    name = 'Groundspeed While Hover Taxiing Max'

    def derive(self, gnd_spd=P('Groundspeed'), hover_taxi=S('Hover Taxi')):
        pass


class GroundspeedWithZeroAirspeedFor5SecMax(KeyPointValueNode):

    def derive(self, wind_spd=P('Wind Speed'), wind_dir=P('Wind Direction'),
               gnd_spd=P('Groundspeed'), heading=P('Heading'),
               airborne=S('Airborne')):
        pass


class GroundspeedBelow100FtMax(KeyPointValueNode):

    def derive(self, gnd_spd=P('Groundspeed'), alt_agl=P('Altitude AGL For Flight Phases'),
               airborne=S('Airborne')):
        pass


class PitchBelow1000FtMax(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), alt=P('Altitude AGL')):
        pass


class PitchBelow1000FtMin(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), alt=P('Altitude AGL')):
        pass


class PitchBelow5FtMax(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), alt_agl=P('Altitude AGL'),
               airborne=S('Airborne')):
        pass


class Pitch5To10FtMax(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), alt_agl=P('Altitude AGL'),
               airborne=S('Airborne')):
        pass


class Pitch10To5FtMax(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), alt_agl=P('Altitude AGL'),
               airborne=S('Airborne')):
        pass


class Pitch500To100FtMax(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent'),
               ac_type=A('Aircraft Type')):
        pass


class Pitch500To100FtMin(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent'),
               ac_type=A('Aircraft Type')):
        pass


class Pitch100To20FtMax(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent'),
               ac_type=A('Aircraft Type')):
        pass


class Pitch100To20FtMin(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent'),
               ac_type=A('Aircraft Type')):
        pass


class Pitch50FtToTouchdownMin(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_agl=P('Altitude AGL'),
               touchdowns=KTI('Touchdown')):
        pass


class PitchOnGroundMax(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), coll=P('Collective'),
               grounded=S('Grounded'), on_deck=S('On Deck')):
        pass


class PitchOnDeckMax(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), coll=P('Collective'), on_deck=S('On Deck')):
        pass


class PitchOnGroundMin(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), coll=P('Collective'), grounded=S('Grounded'), on_deck=S('On Deck')):
        pass


class PitchOnDeckMin(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), coll=P('Collective'), on_deck=S('On Deck')):
        pass


class RateOfDescent100To20FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed Inertial'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descent')):
        pass


class RateOfDescent500To100FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed Inertial'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descent')):
        pass


class RateOfDescent20FtToTouchdownMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed Inertial'),
               touchdowns=KTI('Touchdown'),
               alt_agl=P('Altitude AGL')):
        pass


class RateOfDescentBelow500FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed Inertial'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descending')):
        pass


class RateOfDescentBelow30KtsWithPowerOnMax(KeyPointValueNode):

    def derive(self, vrt_spd=P('Vertical Speed Inertial'), air_spd=P('Airspeed'), descending=S('Descending'),
               power=P('Eng (*) Torque Avg')):
        pass


class VerticalSpeedAtAltitude(KeyPointValueNode):
    NAME_VALUES = {'altitude': [500, 300]}

    def derive(self, vert_spd=P('Vertical Speed'), alt_agl=P('Altitude AGL'),
               approaches=S('Approach')):
        pass


class Roll100To20FtMax(KeyPointValueNode):

    def derive(self, roll=P('Roll'), alt_agl=P('Altitude AGL For Flight Phases'), descending=S('Descent')):
        pass


class RollAbove300FtMax(KeyPointValueNode):

    def derive(self, roll=P('Roll'), alt_agl=P('Altitude AGL For Flight Phases')):
        pass


class RollBelow300FtMax(KeyPointValueNode):

    def derive(self, roll=P('Roll'), alt_agl=P('Altitude AGL For Flight Phases'),
               airborne=S('Airborne')):
        pass


class RollWithAFCSDisengagedMax(KeyPointValueNode):
    name = 'Roll With AFCS Disengaged Max'

    def derive(self, roll=P('Roll'), afcs1=M('AFCS (1) Engaged'),
               afcs2=M('AFCS (2) Engaged')):
        pass


class RollAbove500FtMax(KeyPointValueNode):

    def derive(self, roll=P('Roll'), alt_agl=P('Altitude AGL For Flight Phases')):
        pass


class RollBelow500FtMax(KeyPointValueNode):

    def derive(self, roll=P('Roll'), alt_agl=P('Altitude AGL For Flight Phases')):
        pass


class RollOnGroundMax(KeyPointValueNode):

    def derive(self, roll=P('Roll'), coll=P('Collective'), grounded=S('Grounded'), on_deck=S('On Deck')):
        pass


class RollOnDeckMax(KeyPointValueNode):

    def derive(self, roll=P('Roll'), coll=P('Collective'), on_deck=S('On Deck')):
        pass


class RollRateMax(KeyPointValueNode):

    def derive(self, rr=P('Roll Rate'), airs=S('Airborne')):
        pass


class RotorSpeedDuringAutorotationAbove108KtsMin(KeyPointValueNode):

    def derive(self, nr=P('Nr'), air_spd=P('Airspeed'), autorotation=S('Autorotation')):
        pass


class RotorSpeedDuringAutorotationBelow108KtsMin(KeyPointValueNode):

    def derive(self, nr=P('Nr'), air_spd=P('Airspeed'), autorotation=S('Autorotation')):
        pass


class RotorSpeedDuringAutorotationMax(KeyPointValueNode):

    def derive(self, nr=P('Nr'), autorotation=S('Autorotation')):
        pass


class RotorSpeedDuringAutorotationMin(KeyPointValueNode):

    def derive(self, nr=P('Nr'), autorotation=S('Autorotation')):
        pass


class RotorSpeedWhileAirborneMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type == helicopter and all_of(('Nr', 'Airborne'), available)

    def derive(self, nr=P('Nr'), airborne=S('Airborne'), autorotation=S('Autorotation')):
        pass


class RotorSpeedWhileAirborneMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type == helicopter and all_of(('Nr', 'Airborne'), available)

    def derive(self, nr=P('Nr'), airborne=S('Airborne'), autorotation=S('Autorotation')):
        pass


class RotorSpeedWithRotorBrakeAppliedMax(KeyPointValueNode):

    def derive(self, nr=P('Nr'), rotor_brake=P('Rotor Brake Engaged')):
        pass


class RotorsRunningDuration(KeyPointValueNode):

    def derive(self, rotors=M('Rotors Running')):
        pass


class RotorSpeedDuringMaximumContinuousPowerMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type == helicopter and all_of(('Nr', 'Maximum Continuous Power'), available)

    def derive(self, nr=P('Nr'), mcp=S('Maximum Continuous Power'), autorotation=S('Autorotation')):
        pass


class RotorSpeed36To49Duration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'),
                    family=A('Family')):
        is_s92 = ac_type == helicopter and family and family.value == 'S92'
        return is_s92 and all_deps(cls, available)

    def derive(self, nr=P('Nr')):
        pass


class RotorSpeed56To67Duration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'),
                    family=A('Family')):
        is_s92 = ac_type == helicopter and family and family.value == 'S92'
        return is_s92 and all_deps(cls, available)

    def derive(self, nr=P('Nr')):
        pass


class RotorSpeedAt6PercentCollectiveDuringEngStart(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'),
                    family=A('Family')):
        is_s92 = ac_type == helicopter and family and family.value == 'S92'
        return is_s92 and all_deps(cls, available)

    def derive(self, nr=P('Nr'), collective=P('Collective'),
               firsts=KTI('First Eng Fuel Flow Start')):
        pass


class WindSpeedInCriticalAzimuth(KeyPointValueNode):

    def derive(self, wind_spd=P('Wind Speed'), wind_dir=P('Wind Direction'),
               tas=P('Airspeed True'), heading=P('Heading'),
               airborne=S('Airborne')):
        pass


class SATMin(KeyPointValueNode):
    name = 'SAT Min'

    def derive(self,
               sat=P('SAT'),
               rotors_turning=S('Rotors Turning')):
        pass


class SATRateOfChangeMax(KeyPointValueNode):
    name = 'SAT Rate Of Change Max'

    def derive(self, sat=P('SAT'), airborne=S('Airborne')):
        pass


class CruiseGuideIndicatorMax(KeyPointValueNode):

    def derive(self, cgi=P('Cruise Guide'), airborne=S('Airborne')):
        pass


class TrainingModeDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        if ('Training Mode' in available) and \
           not(any_of(('Eng (1) Training Mode', 'Eng (2) Training Mode'), available)):
            return True
        elif all_of(('Eng (1) Training Mode', 'Eng (2) Training Mode'), available) and \
            ('Training Mode' not in available) :
            return True
        else:
            return False

    def derive(self, trg=P('Training Mode'),
               trg1=P('Eng (1) Training Mode'),
               trg2=P('Eng (2) Training Mode'),
               ):
        pass


class HoverHeightDuringOnshoreTakeoffMax(KeyPointValueNode):

    def derive(self, rad_alt=P('Altitude Radio'), offshore=M('Offshore'), hover=S('Hover'), toff=S('Takeoff')):
        pass


class HoverHeightDuringOffshoreTakeoffMax(KeyPointValueNode):

    def derive(self, rad_alt=P('Altitude Radio'), offshore=M('Offshore'), hover=S('Hover'), toff=S('Takeoff')):
        pass


class AltitudeRadioMinBeforeNoseDownAttitudeAdoptionOffshore(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        return family and family.value == 'H175' and all_of(('Altitude Radio', 'Offshore', 'Liftoff', 'Hover',
                                                             'Nose Down Attitude Adoption',
                                                             'Altitude AAL For Flight Phases'), available)

    def derive(self, offshores=M('Offshore'), liftoffs=KTI('Liftoff'),
               hovers=S('Hover'), nose_downs=S('Nose Down Attitude Adoption'),
               rad_alt=P('Altitude Radio'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AltitudeRadioAtNoseDownAttitudeInitiation(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        return family and family.value == 'H175' and all_of(('Altitude Radio', 'Nose Down Attitude Adoption'), available)

    def derive(self, rad_alt=P('Altitude Radio'), nose_downs=S('Nose Down Attitude Adoption')):
        pass


class PitchNoseDownAttitudeAdoptionDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        return family and family.value == 'H175' and 'Nose Down Attitude Adoption' in available

    def derive(self, nose_downs=S('Nose Down Attitude Adoption')):
        pass


class PitchMinimumDuringNoseDownAttitudeAdoption(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        return family and family.value == 'H175' and all_of(('Pitch', 'Nose Down Attitude Adoption'), available)

    def derive(self, pitch=P('Pitch'), nose_downs=S('Nose Down Attitude Adoption')):
        pass
