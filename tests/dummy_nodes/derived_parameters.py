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


class AccelerationLateralOffsetRemoved(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return 'Acceleration Lateral' in available

    def derive(self,
               acc=P('Acceleration Lateral'),
               offset=KPV('Acceleration Lateral Offset')):
        pass


class AccelerationLateralSmoothed(DerivedParameterNode):

    def derive(self, acc=P('Acceleration Lateral Offset Removed')):
        pass


class AccelerationLongitudinalOffsetRemoved(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, seg_type=A('Segment Type')):
        if seg_type and seg_type.value == 'GROUND_ONLY':
            return 'Acceleration Longitudinal' in available
        return all_of(('Acceleration Longitudinal',
                       'Acceleration Longitudinal Offset'), available)

    def derive(self,
               acc=P('Acceleration Longitudinal'),
               offset=KPV('Acceleration Longitudinal Offset')):
        pass


class AccelerationNormalOffsetRemoved(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return 'Acceleration Normal' in available

    def derive(self,
               acc=P('Acceleration Normal'),
               offset=KPV('Acceleration Normal Offset')):
        pass


class AccelerationVertical(DerivedParameterNode):

    def derive(self, acc_norm=P('Acceleration Normal Offset Removed'),
               acc_lat=P('Acceleration Lateral Offset Removed'),
               acc_long=P('Acceleration Longitudinal'),
               pitch=P('Pitch'), roll=P('Roll')):
        pass


class AccelerationForwards(DerivedParameterNode):

    def derive(self, acc_norm=P('Acceleration Normal Offset Removed'),
               acc_long=P('Acceleration Longitudinal'),
               pitch=P('Pitch')):
        pass


class AccelerationAcrossTrack(DerivedParameterNode):

    def derive(self, acc_fwd=P('Acceleration Forwards'),
               acc_side=P('Acceleration Sideways'),
               drift=P('Drift')):
        pass


class AccelerationAlongTrack(DerivedParameterNode):

    def derive(self, acc_fwd=P('Acceleration Forwards'),
               acc_side=P('Acceleration Sideways'),
               drift=P('Drift')):
        pass


class AccelerationSideways(DerivedParameterNode):

    def derive(self, acc_norm=P('Acceleration Normal Offset Removed'),
               acc_lat=P('Acceleration Lateral Offset Removed'),
               acc_long=P('Acceleration Longitudinal'),
               pitch=P('Pitch'), roll=P('Roll')):
        pass


class AirspeedTrue(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return 'Airspeed' in available and 'Altitude STD Smoothed' in available

    def derive(self, cas_p=P('Airspeed'), alt_std_p=P('Altitude STD Smoothed'),
               sat_p=P('SAT'), toffs=S('Takeoff'), lands=S('Landing'),
               rtos=S('Rejected Takeoff'),
               gspd=P('Groundspeed'), acc_fwd=P('Acceleration Forwards')):
        pass


class AltitudeAAL(DerivedParameterNode):
    name = 'Altitude AAL'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = all_of(('Fast', 'Altitude STD Smoothed'), available)
        if ac_type == helicopter:
            if not 'Altitude Radio Offset Removed' in available:
                return required and ('Gear On Ground' in available)
        return required

    def derive(self, alt_rad=P('Altitude Radio Offset Removed'),
               alt_std=P('Altitude STD Smoothed'),
               speedies=S('Fast'),
               pitch=P('Pitch'),
               gog=P('Gear On Ground'),
               ac_type=A('Aircraft Type')):
        pass


class AltitudeAALForFlightPhases(DerivedParameterNode):
    name = 'Altitude AAL For Flight Phases'

    def derive(self, alt_aal=P('Altitude AAL')):
        pass


class AltitudeRadio(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        alt_rads = [n for n in cls.get_dependency_names() if n.startswith('Altitude Radio')]
        return ('Fast' in available) and any_of(alt_rads, available)

    def derive(self,
               source_A=P('Altitude Radio (A)'),
               source_B=P('Altitude Radio (B)'),
               source_C=P('Altitude Radio (C)'),
               source_L=P('Altitude Radio (L)'),
               source_R=P('Altitude Radio (R)'),
               source_efis=P('Altitude Radio (EFIS)'),
               source_efis_L=P('Altitude Radio (EFIS) (L)'),
               source_efis_R=P('Altitude Radio (EFIS) (R)'),
               alt_std=P('Altitude STD'),
               pitch=P('Pitch'),
               fast=S('Fast'),
               family=A('Family')):
        pass


class AltitudeRadioOffsetRemoved(DerivedParameterNode):

    def derive(self, alt_rad=P('Altitude Radio'), fasts=S('Fast')):
        pass


class AltitudeSTDSmoothed(DerivedParameterNode):
    name = 'Altitude STD Smoothed'

    @classmethod
    def can_operate(cls, available):
        return ('Frame' in available and
                (('Altitude STD' in available) or
                 all_of(('Altitude STD (Capt)', 'Altitude STD (FO)'), available)))

    def derive(self, fine=P('Altitude STD (Fine)'),
               alt=P('Altitude STD'),
               alt_capt=P('Altitude STD (Capt)'),
               alt_fo=P('Altitude STD (FO)'),
               frame=A('Frame')):
        pass


class BaroCorrection(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        baro_corr = all_of(('Baro Correction (Capt)', 'Baro Correction (FO)'), available)
        alt_baro_first = all_of(('Altitude STD', 'Altitude Baro (1)'), available)
        alt_baro_solo = all_of(('Altitude STD', 'Altitude Baro'), available)
        return baro_corr or alt_baro_first or alt_baro_solo

    def derive(self,
               baro_cpt=P('Baro Correction (Capt)'),
               baro_fo=P('Baro Correction (FO)'),
               alt_baro=P('Altitude Baro (1)'),
               alt_baro_solo=P('Altitude Baro'),
               alt_std=P('Altitude STD')):
        pass


class AltitudeQNH(DerivedParameterNode):
    name = 'Altitude QNH'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Baro Correction', 'Altitude STD'), available)

    def derive(self,
               alt_std=P('Altitude STD'),
               baro=P('Baro Correction'),
               baro_sel=M('Baro Setting Selection'),
               baro_sel_cpt=M('Baro Setting Selection (Capt)'),
               baro_sel_fo=M('Baro Setting Selection (FO)'),
               baro_cor_isis=P('Baro Correction (ISIS)')):
        pass


class AltitudeQNHCapt(DerivedParameterNode):
    name = 'Altitude QNH (Capt)'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Baro Correction (Capt)', 'Altitude STD'), available)

    def derive(self,
               alt_std=P('Altitude STD'),
               baro=P('Baro Correction (Capt)'),
               baro_sel_capt=M('Baro Setting Selection (Capt)'),
               baro_sel=M('Baro Setting Selection'),
               baro_cor_isis=P('Baro Correction (ISIS)')):
        pass


class AltitudeQNHFO(DerivedParameterNode):
    name = 'Altitude QNH (FO)'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Baro Correction (FO)', 'Altitude STD'), available)

    def derive(self,
               alt_std=P('Altitude STD'),
               baro=P('Baro Correction (FO)'),
               baro_sel_fo=M('Baro Setting Selection (FO)'),
               baro_sel=M('Baro Setting Selection'),
               baro_cor_isis=P('Baro Correction (ISIS)')):
        pass


class AltitudeVisualizationWithGroundOffset(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return 'Altitude AAL' in available

    def derive(self,
               alt_aal=P('Altitude AAL'),
               alt_std=P('Altitude STD Smoothed'),
               l_apt=A('FDR Landing Runway'),
               t_apt=A('FDR Takeoff Runway'),
               climbs=S('Climb'),
               descents=S('Descent'),
               tocs=KTI('Top Of Climb'),
               apps=App('Approach Information')):
        pass


class AltitudeVisualizationWithoutGroundOffset(DerivedParameterNode):
    name = 'Altitude Visualization Without Ground Offset'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return 'Altitude STD Smoothed' in available \
               and (('Altitude AGL' in available and ac_type == helicopter) \
               or ('Altitude AAL' in available and ac_type != helicopter))

    def derive(self,
               alt_agl=P('Altitude AGL'),
               alt_aal=P('Altitude AAL'),
               alt_std=P('Altitude STD Smoothed'),
               cruises=S('Cruise')):
        pass


class AltitudeTail(DerivedParameterNode):

    def derive(self, alt_rad=P('Altitude Radio'), pitch=P('Pitch'),
               toffs=S('Takeoff'), gas=S('Go Around And Climbout'),
               lands=S('Landing'),
               ground_to_tail=A('Ground To Lowest Point Of Tail'),
               dist_gear_to_tail=A('Main Gear To Lowest Point Of Tail')):
        pass


class CabinAltitude(DerivedParameterNode):

    def derive(self, cp=P('Cabin Press')):
        pass


class ClimbForFlightPhases(DerivedParameterNode):

    def derive(self, alt_std=P('Altitude STD Smoothed'), airs=S('Fast')):
        pass


class DescendForFlightPhases(DerivedParameterNode):

    def derive(self, alt_std=P('Altitude STD Smoothed'), airs=S('Fast')):
        pass


class AOA(DerivedParameterNode):
    name = 'AOA'

    @classmethod
    def can_operate(cls, available):
        return any_of(('AOA (L)', 'AOA (R)'), available)

    def derive(self, aoa_l=P('AOA (L)'), aoa_r=P('AOA (R)'),
               model=A('Model')):
        pass


class ControlColumn(DerivedParameterNode):

    def derive(self,
               posn_capt=P('Control Column (Capt)'),
               posn_fo=P('Control Column (FO)')):
        pass


class ControlColumnCapt(DerivedParameterNode):
    name = 'Control Column (Capt)'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               pot=P('Control Column (Capt) Potentiometer'),
               synchro=P('Control Column (Capt) Synchro')):
        pass


class ControlColumnFO(DerivedParameterNode):
    name = 'Control Column (FO)'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               pot=P('Control Column (FO) Potentiometer'),
               synchro=P('Control Column (FO) Synchro')):
        pass


class ControlColumnForce(DerivedParameterNode):

    def derive(self,
               force_capt=P('Control Column Force (Capt)'),
               force_fo=P('Control Column Force (FO)')):
        pass


class ControlColumnForceAtControlWheelCapt(DerivedParameterNode):
    name = 'Control Column Force At Control Wheel (Capt)'

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        is_atr = family and family.value in ('ATR-72')
        return all_of(('Control Column Force (Capt)', 'Control Column (Capt)'), available) and is_atr

    def derive(self, cc_force=P('Control Column Force (Capt)'),
                     cc_angle=P('Control Column (Capt)'),):
        pass


class ControlColumnForceAtControlWheelFO(DerivedParameterNode):
    name = 'Control Column Force At Control Wheel (FO)'

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        is_atr = family and family.value in ('ATR-72')
        return all_of(('Control Column Force (FO)', 'Control Column (FO)'), available) and is_atr

    def derive(self, cc_force=P('Control Column Force (FO)'),
                     cc_angle=P('Control Column (FO)'),):
        pass


class ControlWheel(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of((
            'Control Wheel (Capt)',
            'Control Wheel (FO)',
        ), available) or any_of((
            'Control Wheel Synchro',
            'Control Wheel Potentiometer',
        ), available)

    def derive(self,
               posn_capt=P('Control Wheel (Capt)'),
               posn_fo=P('Control Wheel (FO)'),
               synchro=P('Control Wheel Synchro'),
               pot=P('Control Wheel Potentiometer')):
        pass


class ControlWheelForce(DerivedParameterNode):

    def derive(self,
               force_capt=P('Control Wheel Force (Capt)'),
               force_fo=P('Control Wheel Force (FO)')):
        pass


class SidestickAngleCapt(DerivedParameterNode):
    name = 'Sidestick Angle (Capt)'

    def derive(self,
               pitch_capt=M('Sidestick Pitch (Capt)'),
               roll_capt=M('Sidestick Roll (Capt)')):
        pass


class SidestickAngleFO(DerivedParameterNode):
    name = 'Sidestick Angle (FO)'

    def derive(self,
               pitch_fo=M('Sidestick Pitch (FO)'),
               roll_fo=M('Sidestick Roll (FO)')):
        pass


class DistanceToLanding(DerivedParameterNode):

    def derive(self, dist=P('Distance Travelled'), tdwns=KTI('Touchdown')):
        pass


class DistanceFlown(DerivedParameterNode):

    def derive(self, tas=P('Airspeed True'), airs=S('Airborne')):
        pass


class DistanceTravelled(DerivedParameterNode):

    def derive(self, gspd=P('Groundspeed')):
        pass


class Drift(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Drift (1)', 'Drift (2)'), available) \
            or all_of(('Heading Continuous', 'Track'), available)

    def derive(self,
               drift_1=P('Drift (1)'),
               drift_2=P('Drift (2)'),
               track=P('Track'),
               heading=P('Heading Continuous')):
        pass


class BrakePressure(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of((
            'Brake (L) Press',
            'Brake (R) Press',
        ), available) or all_of((
            'Brake (L) Inboard Press',
            'Brake (L) Outboard Press',
            'Brake (R) Inboard Press',
            'Brake (R) Outboard Press',
        ), available)

    def derive(self,
               brake_L=P('Brake (L) Press'),
               brake_R=P('Brake (R) Press'),
               brake_L_ib=P('Brake (L) Inboard Press'),
               brake_L_ob=P('Brake (L) Outboard Press'),
               brake_R_ib=P('Brake (R) Inboard Press'),
               brake_R_ob=P('Brake (R) Outboard Press')):
        pass


class Brake_C_Temp(DerivedParameterNode):
    name = 'Brake (C) Temp'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               brake1=P('Brake (C) (1) Temp'),
               brake2=P('Brake (C) (2) Temp'),
               brake3=P('Brake (C) (3) Temp'),
               brake4=P('Brake (C) (4) Temp'),
               brake5=P('Brake (C) (5) Temp'),
               brake6=P('Brake (C) (6) Temp'),
               brake7=P('Brake (C) (7) Temp'),
               brake8=P('Brake (C) (8) Temp')):
        pass


class Brake_L_Temp(DerivedParameterNode):
    name = 'Brake (L) Temp'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               brake1=P('Brake (L) (1) Temp'),
               brake2=P('Brake (L) (2) Temp'),
               brake3=P('Brake (L) (3) Temp'),
               brake4=P('Brake (L) (4) Temp'),
               brake5=P('Brake (L) (5) Temp'),
               brake6=P('Brake (L) (6) Temp')):
        pass


class Brake_R_Temp(DerivedParameterNode):
    name = 'Brake (R) Temp'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               brake1=P('Brake (R) (1) Temp'),
               brake2=P('Brake (R) (2) Temp'),
               brake3=P('Brake (R) (3) Temp'),
               brake4=P('Brake (R) (4) Temp'),
               brake5=P('Brake (R) (5) Temp'),
               brake6=P('Brake (R) (6) Temp')):
        pass


class Brake_TempAvg(DerivedParameterNode):
    name = 'Brake (*) Temp Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               brake1=P('Brake (1) Temp'),
               brake2=P('Brake (2) Temp'),
               brake3=P('Brake (3) Temp'),
               brake4=P('Brake (4) Temp'),
               brake5=P('Brake (5) Temp'),
               brake6=P('Brake (6) Temp'),
               brake7=P('Brake (7) Temp'),
               brake8=P('Brake (8) Temp'),
               brake9=P('Brake (9) Temp'),
               brake10=P('Brake (10) Temp'),
               brake11=P('Brake (11) Temp'),
               brake12=P('Brake (12) Temp'),
               brakeC=P('Brake (C) Temp'),
               brakeL=P('Brake (L) Temp'),
               brakeR=P('Brake (R) Temp')):
        pass


class Brake_TempMax(DerivedParameterNode):
    name = 'Brake (*) Temp Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               brake1=P('Brake (1) Temp'),
               brake2=P('Brake (2) Temp'),
               brake3=P('Brake (3) Temp'),
               brake4=P('Brake (4) Temp'),
               brake5=P('Brake (5) Temp'),
               brake6=P('Brake (6) Temp'),
               brake7=P('Brake (7) Temp'),
               brake8=P('Brake (8) Temp'),
               brake9=P('Brake (9) Temp'),
               brake10=P('Brake (10) Temp'),
               brake11=P('Brake (11) Temp'),
               brake12=P('Brake (12) Temp'),
               brakeC=P('Brake (C) Temp'),
               brakeL=P('Brake (L) Temp'),
               brakeR=P('Brake (R) Temp')):
        pass


class Brake_TempMin(DerivedParameterNode):
    name = 'Brake (*) Temp Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               brake1=P('Brake (1) Temp'),
               brake2=P('Brake (2) Temp'),
               brake3=P('Brake (3) Temp'),
               brake4=P('Brake (4) Temp'),
               brake5=P('Brake (5) Temp'),
               brake6=P('Brake (6) Temp'),
               brake7=P('Brake (7) Temp'),
               brake8=P('Brake (8) Temp'),
               brake9=P('Brake (9) Temp'),
               brake10=P('Brake (10) Temp'),
               brake11=P('Brake (11) Temp'),
               brake12=P('Brake (12) Temp'),
               brakeC=P('Brake (C) Temp'),
               brakeL=P('Brake (L) Temp'),
               brakeR=P('Brake (R) Temp')):
        pass


class Eng_EPRAvg(DerivedParameterNode):
    name = 'Eng (*) EPR Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) EPR'),
               eng2=P('Eng (2) EPR'),
               eng3=P('Eng (3) EPR'),
               eng4=P('Eng (4) EPR')):
        pass


class Eng_EPRMax(DerivedParameterNode):
    name = 'Eng (*) EPR Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) EPR'),
               eng2=P('Eng (2) EPR'),
               eng3=P('Eng (3) EPR'),
               eng4=P('Eng (4) EPR')):
        pass


class Eng_EPRMin(DerivedParameterNode):
    name = 'Eng (*) EPR Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) EPR'),
               eng2=P('Eng (2) EPR'),
               eng3=P('Eng (3) EPR'),
               eng4=P('Eng (4) EPR')):
        pass


class Eng_EPRMinFor5Sec(DerivedParameterNode):
    name = 'Eng (*) EPR Min For 5 Sec'

    def derive(self, eng_epr_min=P('Eng (*) EPR Min')):
        pass


class Eng_EPRAvgFor10Sec(DerivedParameterNode):
    name = 'Eng (*) EPR Avg For 10 Sec'

    def derive(self, eng_epr_avg=P('Eng (*) EPR Avg')):
        pass


class EngTPRLimitDifference(DerivedParameterNode):
    name = 'Eng TPR Limit Difference'

    def derive(self,
               eng_tpr_max=P('Eng (*) TPR Max'),
               eng_tpr_limit=P('Eng TPR Limit Max')):
        pass


class Eng_TPRMax(DerivedParameterNode):
    name = 'Eng (*) TPR Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) TPR'),
               eng2=P('Eng (2) TPR'),
               eng3=P('Eng (3) TPR'),
               eng4=P('Eng (4) TPR')):
        pass


class Eng_TPRMin(DerivedParameterNode):
    name = 'Eng (*) TPR Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) TPR'),
               eng2=P('Eng (2) TPR'),
               eng3=P('Eng (3) TPR'),
               eng4=P('Eng (4) TPR')):
        pass


class Eng_FuelFlow(DerivedParameterNode):
    name = 'Eng (*) Fuel Flow'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Fuel Flow'),
               eng2=P('Eng (2) Fuel Flow'),
               eng3=P('Eng (3) Fuel Flow'),
               eng4=P('Eng (4) Fuel Flow')):
        pass


class Eng_FuelFlowMin(DerivedParameterNode):
    name = 'Eng (*) Fuel Flow Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Fuel Flow'),
               eng2=P('Eng (2) Fuel Flow'),
               eng3=P('Eng (3) Fuel Flow'),
               eng4=P('Eng (4) Fuel Flow')):
        pass


class Eng_FuelFlowMax(DerivedParameterNode):
    name = 'Eng (*) Fuel Flow Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Fuel Flow'),
               eng2=P('Eng (2) Fuel Flow'),
               eng3=P('Eng (3) Fuel Flow'),
               eng4=P('Eng (4) Fuel Flow')):
        pass


class Eng_1_FuelBurn(DerivedParameterNode):
    name = 'Eng (1) Fuel Burn'

    def derive(self, ff=P('Eng (1) Fuel Flow')):
        pass


class Eng_2_FuelBurn(DerivedParameterNode):
    name = 'Eng (2) Fuel Burn'

    def derive(self, ff=P('Eng (2) Fuel Flow')):
        pass


class Eng_3_FuelBurn(DerivedParameterNode):
    name = 'Eng (3) Fuel Burn'

    def derive(self, ff=P('Eng (3) Fuel Flow')):
        pass


class Eng_4_FuelBurn(DerivedParameterNode):
    name = 'Eng (4) Fuel Burn'

    def derive(self, ff=P('Eng (4) Fuel Flow')):
        pass


class Eng_FuelBurn(DerivedParameterNode):
    name = 'Eng (*) Fuel Burn'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Fuel Burn'),
               eng2=P('Eng (2) Fuel Burn'),
               eng3=P('Eng (3) Fuel Burn'),
               eng4=P('Eng (4) Fuel Burn')):
        pass


class Eng_GasTempAvg(DerivedParameterNode):
    name = 'Eng (*) Gas Temp Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Gas Temp'),
               eng2=P('Eng (2) Gas Temp'),
               eng3=P('Eng (3) Gas Temp'),
               eng4=P('Eng (4) Gas Temp')):
        pass


class Eng_GasTempMax(DerivedParameterNode):
    name = 'Eng (*) Gas Temp Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Gas Temp'),
               eng2=P('Eng (2) Gas Temp'),
               eng3=P('Eng (3) Gas Temp'),
               eng4=P('Eng (4) Gas Temp')):
        pass


class Eng_GasTempMin(DerivedParameterNode):
    name = 'Eng (*) Gas Temp Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Gas Temp'),
               eng2=P('Eng (2) Gas Temp'),
               eng3=P('Eng (3) Gas Temp'),
               eng4=P('Eng (4) Gas Temp')):
        pass


class Eng_N1Avg(DerivedParameterNode):
    name = 'Eng (*) N1 Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) N1'),
               eng2=P('Eng (2) N1'),
               eng3=P('Eng (3) N1'),
               eng4=P('Eng (4) N1')):
        pass


class Eng_N1AvgFor10Sec(DerivedParameterNode):
    name = 'Eng (*) N1 Avg For 10 Sec'

    def derive(self, eng_n1_avg=P('Eng (*) N1 Avg')):
        pass


class Eng_N1Max(DerivedParameterNode):
    name = 'Eng (*) N1 Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) N1'),
               eng2=P('Eng (2) N1'),
               eng3=P('Eng (3) N1'),
               eng4=P('Eng (4) N1')):
        pass


class Eng_N1Min(DerivedParameterNode):
    name = 'Eng (*) N1 Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) N1'),
               eng2=P('Eng (2) N1'),
               eng3=P('Eng (3) N1'),
               eng4=P('Eng (4) N1')):
        pass


class Eng_N1Split(DerivedParameterNode):
    name = 'Eng (*) N1 Split'

    @classmethod
    def can_operate(cls, available):
        return all_of(cls.get_dependency_names(), available)

    def derive(self,
               n1max=P('Eng (*) N1 Max'),
               n1min=P('Eng (*) N1 Min')):
        pass


class Eng_N1MinFor5Sec(DerivedParameterNode):
    name = 'Eng (*) N1 Min For 5 Sec'

    def derive(self, eng_n1_min=P('Eng (*) N1 Min')):
        pass


class Eng_N2Avg(DerivedParameterNode):
    name = 'Eng (*) N2 Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) N2'),
               eng2=P('Eng (2) N2'),
               eng3=P('Eng (3) N2'),
               eng4=P('Eng (4) N2')):
        pass


class Eng_N2Max(DerivedParameterNode):
    name = 'Eng (*) N2 Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) N2'),
               eng2=P('Eng (2) N2'),
               eng3=P('Eng (3) N2'),
               eng4=P('Eng (4) N2')):
        pass


class Eng_N2Min(DerivedParameterNode):
    name = 'Eng (*) N2 Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) N2'),
               eng2=P('Eng (2) N2'),
               eng3=P('Eng (3) N2'),
               eng4=P('Eng (4) N2')):
        pass


class Eng_N3Avg(DerivedParameterNode):
    name = 'Eng (*) N3 Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) N3'),
               eng2=P('Eng (2) N3'),
               eng3=P('Eng (3) N3'),
               eng4=P('Eng (4) N3')):
        pass


class Eng_N3Max(DerivedParameterNode):
    name = 'Eng (*) N3 Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) N3'),
               eng2=P('Eng (2) N3'),
               eng3=P('Eng (3) N3'),
               eng4=P('Eng (4) N3')):
        pass


class Eng_N3Min(DerivedParameterNode):
    name = 'Eng (*) N3 Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) N3'),
               eng2=P('Eng (2) N3'),
               eng3=P('Eng (3) N3'),
               eng4=P('Eng (4) N3')):
        pass


class Eng_NpAvg(DerivedParameterNode):
    name = 'Eng (*) Np Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Np'),
               eng2=P('Eng (2) Np'),
               eng3=P('Eng (3) Np'),
               eng4=P('Eng (4) Np')):
        pass


class Eng_NpMax(DerivedParameterNode):
    name = 'Eng (*) Np Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Np'),
               eng2=P('Eng (2) Np'),
               eng3=P('Eng (3) Np'),
               eng4=P('Eng (4) Np')):
        pass


class Eng_NpMin(DerivedParameterNode):
    name = 'Eng (*) Np Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Np'),
               eng2=P('Eng (2) Np'),
               eng3=P('Eng (3) Np'),
               eng4=P('Eng (4) Np')):
        pass


class Eng_OilPressAvg(DerivedParameterNode):
    name = 'Eng (*) Oil Press Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Oil Press'),
               eng2=P('Eng (2) Oil Press'),
               eng3=P('Eng (3) Oil Press'),
               eng4=P('Eng (4) Oil Press')):
        pass


class Eng_OilPressMax(DerivedParameterNode):
    name = 'Eng (*) Oil Press Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Oil Press'),
               eng2=P('Eng (2) Oil Press'),
               eng3=P('Eng (3) Oil Press'),
               eng4=P('Eng (4) Oil Press')):
        pass


class Eng_OilPressMin(DerivedParameterNode):
    name = 'Eng (*) Oil Press Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Oil Press'),
               eng2=P('Eng (2) Oil Press'),
               eng3=P('Eng (3) Oil Press'),
               eng4=P('Eng (4) Oil Press')):
        pass


class Eng_OilQtyAvg(DerivedParameterNode):
    name = 'Eng (*) Oil Qty Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Oil Qty'),
               eng2=P('Eng (2) Oil Qty'),
               eng3=P('Eng (3) Oil Qty'),
               eng4=P('Eng (4) Oil Qty')):
        pass


class Eng_OilQtyMax(DerivedParameterNode):
    name = 'Eng (*) Oil Qty Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Oil Qty'),
               eng2=P('Eng (2) Oil Qty'),
               eng3=P('Eng (3) Oil Qty'),
               eng4=P('Eng (4) Oil Qty')):
        pass


class Eng_OilQtyMin(DerivedParameterNode):
    name = 'Eng (*) Oil Qty Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Oil Qty'),
               eng2=P('Eng (2) Oil Qty'),
               eng3=P('Eng (3) Oil Qty'),
               eng4=P('Eng (4) Oil Qty')):
        pass


class Eng_OilTempAvg(DerivedParameterNode):
    name = 'Eng (*) Oil Temp Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Oil Temp'),
               eng2=P('Eng (2) Oil Temp'),
               eng3=P('Eng (3) Oil Temp'),
               eng4=P('Eng (4) Oil Temp')):
        pass


class Eng_OilTempMax(DerivedParameterNode):
    name = 'Eng (*) Oil Temp Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Oil Temp'),
               eng2=P('Eng (2) Oil Temp'),
               eng3=P('Eng (3) Oil Temp'),
               eng4=P('Eng (4) Oil Temp')):
        pass


class Eng_OilTempMin(DerivedParameterNode):
    name = 'Eng (*) Oil Temp Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Oil Temp'),
               eng2=P('Eng (2) Oil Temp'),
               eng3=P('Eng (3) Oil Temp'),
               eng4=P('Eng (4) Oil Temp')):
        pass


class Eng_TorqueAvg(DerivedParameterNode):
    name = 'Eng (*) Torque Avg'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Torque'),
               eng2=P('Eng (2) Torque'),
               eng3=P('Eng (3) Torque'),
               eng4=P('Eng (4) Torque')):
        pass


class Eng_TorqueMax(DerivedParameterNode):
    name = 'Eng (*) Torque Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Torque'),
               eng2=P('Eng (2) Torque'),
               eng3=P('Eng (3) Torque'),
               eng4=P('Eng (4) Torque')):
        pass


class Eng_TorqueMin(DerivedParameterNode):
    name = 'Eng (*) Torque Min'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Torque'),
               eng2=P('Eng (2) Torque'),
               eng3=P('Eng (3) Torque'),
               eng4=P('Eng (4) Torque')):
        pass


class TorqueAsymmetry(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, eng_type=A('Engine Propulsion'), ac_type=A('Aircraft Type')):
        turbo_prop = eng_type and eng_type.value == 'PROP'
        required = ['Eng (*) Torque Max', 'Eng (*) Torque Min']
        return (ac_type == helicopter or turbo_prop) and all_of(required, available)

    def derive(self, torq_max=P('Eng (*) Torque Max'), torq_min=P('Eng (*) Torque Min')):
        pass


class Eng_VibN1Max(DerivedParameterNode):
    name = 'Eng (*) Vib N1 Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Vib N1'),
               eng2=P('Eng (2) Vib N1'),
               eng3=P('Eng (3) Vib N1'),
               eng4=P('Eng (4) Vib N1'),
               fan1=P('Eng (1) Vib N1 Fan'),
               fan2=P('Eng (2) Vib N1 Fan'),
               fan3=P('Eng (3) Vib N1 Fan'),
               fan4=P('Eng (4) Vib N1 Fan'),
               lpt1=P('Eng (1) Vib N1 Turbine'),
               lpt2=P('Eng (2) Vib N1 Turbine'),
               lpt3=P('Eng (3) Vib N1 Turbine'),
               lpt4=P('Eng (4) Vib N1 Turbine'),
               comp1=P('Eng (1) Vib N1 Compressor'),
               comp2=P('Eng (2) Vib N1 Compressor'),
               gear1=P('Eng (1) Vib N1 Gearbox'),
               gear2=P('Eng (2) Vib N1 Gearbox')):
        pass


class Eng_VibN2Max(DerivedParameterNode):
    name = 'Eng (*) Vib N2 Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Vib N2'),
               eng2=P('Eng (2) Vib N2'),
               eng3=P('Eng (3) Vib N2'),
               eng4=P('Eng (4) Vib N2'),
               hpc1=P('Eng (1) Vib N2 Compressor'),
               hpc2=P('Eng (2) Vib N2 Compressor'),
               hpt1=P('Eng (1) Vib N2 Turbine'),
               hpt2=P('Eng (2) Vib N2 Turbine'),
               hpt3=P('Eng (3) Vib N2 Turbine'),
               hpt4=P('Eng (4) Vib N2 Turbine')):
        pass


class Eng_VibN3Max(DerivedParameterNode):
    name = 'Eng (*) Vib N3 Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Vib N3'),
               eng2=P('Eng (2) Vib N3'),
               eng3=P('Eng (3) Vib N3'),
               eng4=P('Eng (4) Vib N3'),
               hpt1=P('Eng (1) Vib N3 Turbine'),
               hpt2=P('Eng (2) Vib N3 Turbine'),
               hpt3=P('Eng (3) Vib N3 Turbine'),
               hpt4=P('Eng (4) Vib N3 Turbine')):
        pass


class Eng_VibBroadbandMax(DerivedParameterNode):
    name = 'Eng (*) Vib Broadband Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Vib Broadband'),
               eng2=P('Eng (2) Vib Broadband'),
               eng3=P('Eng (3) Vib Broadband'),
               eng4=P('Eng (4) Vib Broadband'),
               lpt1=P('Eng (1) Vib Broadband Turbine'),
               lpt2=P('Eng (2) Vib Broadband Turbine'),
               comp1=P('Eng (1) Vib Broadband Compressor'),
               comp2=P('Eng (2) Vib Broadband Compressor'),
               gear1=P('Eng (1) Vib Broadband Gearbox'),
               gear2=P('Eng (2) Vib Broadband Gearbox'),
               eng1_accel_a=P('Eng (1) Vib Broadband Accel A'),
               eng2_accel_a=P('Eng (2) Vib Broadband Accel A'),
               eng3_accel_a=P('Eng (3) Vib Broadband Accel A'),
               eng4_accel_a=P('Eng (4) Vib Broadband Accel A'),
               eng1_accel_b=P('Eng (1) Vib Broadband Accel B'),
               eng2_accel_b=P('Eng (2) Vib Broadband Accel B'),
               eng3_accel_b=P('Eng (3) Vib Broadband Accel B'),
               eng4_accel_b=P('Eng (4) Vib Broadband Accel B')):
        pass


class Eng_VibNpMax(DerivedParameterNode):
    name = 'Eng (*) Vib Np Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Vib Np'),
               eng2=P('Eng (2) Vib Np'),
               fan1=P('Eng (1) Vib Np Fan'),
               fan2=P('Eng (2) Vib Np Fan'),
               lpt1=P('Eng (1) Vib Np Turbine'),
               lpt2=P('Eng (2) Vib Np Turbine'),
               comp1=P('Eng (1) Vib Np Compressor'),
               comp2=P('Eng (2) Vib Np Compressor'),
               gear1=P('Eng (1) Vib Np Gearbox'),
               gear2=P('Eng (2) Vib Np Gearbox')):
        pass


class Eng_VibAMax(DerivedParameterNode):
    name = 'Eng (*) Vib A Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Vib (A)'),
               eng2=P('Eng (2) Vib (A)'),
               eng3=P('Eng (3) Vib (A)'),
               eng4=P('Eng (4) Vib (A)')):
        pass


class Eng_VibBMax(DerivedParameterNode):
    name = 'Eng (*) Vib B Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Vib (B)'),
               eng2=P('Eng (2) Vib (B)'),
               eng3=P('Eng (3) Vib (B)'),
               eng4=P('Eng (4) Vib (B)')):
        pass


class Eng_VibCMax(DerivedParameterNode):
    name = 'Eng (*) Vib C Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Vib (C)'),
               eng2=P('Eng (2) Vib (C)'),
               eng3=P('Eng (3) Vib (C)'),
               eng4=P('Eng (4) Vib (C)')):
        pass


class FuelQty(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        fuel_l_and_r = ('Fuel Qty (L)', 'Fuel Qty (R)')
        if any_of(fuel_l_and_r, available):
            return all_of(fuel_l_and_r, available)
        else:
            return any_of(
                [d for d in cls.get_dependency_names() if d != 'Airborne'],
                available
            )

    def derive(self,
               fuel_qty_l=P('Fuel Qty (L)'),
               fuel_qty_c=P('Fuel Qty (C)'),
               fuel_qty_r=P('Fuel Qty (R)'),
               fuel_qty_trim=P('Fuel Qty (Trim)'),
               fuel_qty_aux=P('Fuel Qty (Aux)'),
               fuel_qty_tail=P('Fuel Qty (Tail)'),
               fuel_qty_stab=P('Fuel Qty (Stab)'),
               airbornes=S('Airborne')):
        pass


class FuelQtyC(DerivedParameterNode):
    name = 'Fuel Qty (C)'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, fuel_qty_c_1=P('Fuel Qty (C) (1)'),
               fuel_qty_c_2=P('Fuel Qty (C) (2)'),
               fuel_qty_c_3=P('Fuel Qty (C) (3)'),
               fuel_qty_c_4=P('Fuel Qty (C) (4)')):
        pass


class FuelQtyL(DerivedParameterNode):
    name = 'Fuel Qty (L)'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, fuel_qty_l_1=P('Fuel Qty (L) (1)'),
               fuel_qty_l_2=P('Fuel Qty (L) (2)'),
               fuel_qty_l_3=P('Fuel Qty (L) (3)'),
               fuel_qty_l_4=P('Fuel Qty (L) (4)'),
               fuel_qty_l_5=P('Fuel Qty (L) (5)')):
        pass


class FuelQtyR(DerivedParameterNode):
    name = 'Fuel Qty (R)'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, fuel_qty_r_1=P('Fuel Qty (R) (1)'),
               fuel_qty_r_2=P('Fuel Qty (R) (2)'),
               fuel_qty_r_3=P('Fuel Qty (R) (3)'),
               fuel_qty_r_4=P('Fuel Qty (R) (4)'),
               fuel_qty_r_5=P('Fuel Qty (R) (5)')):
        pass


class FuelQtyAux(DerivedParameterNode):
    name = 'Fuel Qty (Aux)'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               fuel_qty_1=P('Fuel Qty (Aux) (1)'),
               fuel_qty_2=P('Fuel Qty (Aux) (2)')):
        pass


class GrossWeight(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return (all_of(('AFR Landing Gross Weight', 'HDF Duration'), available) or
                all_of(('AFR Takeoff Gross Weight', 'HDF Duration', 'AFR Takeoff Fuel', 'AFR Landing Fuel'), available) or
                all_of(('Zero Fuel Weight', 'Fuel Qty'), available))

    def derive(self, zfw=P('Zero Fuel Weight'), fq=P('Fuel Qty'),
               hdf_duration=A('HDF Duration'),
               afr_land_wgt=A('AFR Landing Gross Weight'),
               afr_takeoff_wgt=A('AFR Takeoff Gross Weight'),
               afr_land_fuel=A('AFR Landing Fuel'),
               afr_takeoff_fuel=A('AFR Takeoff Fuel'),
               touchdowns=KTI('Touchdown'),
               liftoffs=KTI('Liftoff')):
        pass


class ZeroFuelWeight(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return ('HDF Duration' in available and
                ('Dry Operating Weight' in available or
                 all_of(('Fuel Qty', 'Gross Weight'), available)))

    def derive(self, fuel_qty=P('Fuel Qty'), gross_wgt=P('Gross Weight'),
               dry_operating_wgt=A('Dry Operating Weight'),
               payload=A('Payload'), duration=A('HDF Duration')):
        pass


class GrossWeightSmoothed(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return 'Gross Weight' in available

    def derive(self,
               ff=P('Eng (*) Fuel Flow'),
               gw=P('Gross Weight'),
               climbs=S('Climbing'),
               descends=S('Descending'),
               airs=S('Airborne')):
        pass


class Groundspeed(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'),
                    precise=A('Precise Positioning')):
        gspd_sources = any_of(('Groundspeed (1)', 'Groundspeed (2)'),
                              available)
        lat_lon = all_of(('Latitude Prepared', 'Longitude Prepared'),
                         available)
        return gspd_sources or (lat_lon and ac_type == helicopter
                                and precise.value)

    def derive(self,
               source_A=P('Groundspeed (1)'),
               source_B=P('Groundspeed (2)'),
               lat=P('Latitude Prepared'),
               lon=P('Longitude Prepared'),
               ac_type=A('Aircraft Type')):
        pass


class GroundspeedSigned(DerivedParameterNode):

    def derive(self,
               gspd=P('Groundspeed'),
               power=P('Eng (*) Any Running'),
               ac_type=A('Aircraft Type'),
               precise=A('Precise Positioning'),
               taxis=S('Taxiing'),
               lat=P('Latitude Prepared'),
               lon=P('Longitude Prepared'),
               ):
        pass


class FlapAngle(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Flap Angle (L)', 'Flap Angle (R)',
            'Flap Angle (C)', 'Flap Angle (MCP)',
            'Flap Angle (L) Inboard', 'Flap Angle (R) Inboard',
        ), available)

    def derive(self,
               flap_A=P('Flap Angle (L)'),
               flap_B=P('Flap Angle (R)'),
               flap_C=P('Flap Angle (C)'),
               flap_D=P('Flap Angle (MCP)'),
               flap_A_inboard=P('Flap Angle (L) Inboard'),
               flap_B_inboard=P('Flap Angle (R) Inboard')):
        pass


class FlapSynchroAsymmetry(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Flap Angle (L) Synchro', 'Flap Angle (R) Synchro',), available)

    def derive(self, synchro_l=P('Flap Angle (L) Synchro'), synchro_r=P('Flap Angle (R) Synchro'),):
        pass


class SlatAngle(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family')):
        if any_of(('Slat Angle (L)', 'Slat Angle (R)'), available):
            return True
        elif 'Slat Angle Recorded' in available:
            return True
        else:
            if not all_of(('Slat Fully Extended', 'Model', 'Series', 'Family'), available):
                return False
            try:
                at.get_slat_map(model.value, series.value, family.value)
            except KeyError:
                cls.debug("No slat mapping available for '%s', '%s', '%s'.",
                          model.value, series.value, family.value)
                return False
            return True

    def derive(self, slat_l=P('Slat Angle (L)'), slat_r=P('Slat Angle (R)'),
               slat_full=M('Slat Fully Extended'), slat_part=M('Slat Part Extended'),
               slat_retracted=M('Slat Retracted'), slat_angle_rec=P('Slat Angle Recorded'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass

class _SlopeMixin(object):
    pass


class SlopeToLanding(DerivedParameterNode, _SlopeMixin):

    def derive(self, alt_aal=P('Altitude AAL'),
               dist=P('Distance To Landing'),
               alt_std=P('Altitude STD'),
               sat=P('SAT'),
               apps=S('Approach')):
        pass


class SlopeAngleToLanding(DerivedParameterNode):

    def derive(self, slope_to_ldg=P('Slope To Landing')):
        pass


class SlopeToAimingPoint(DerivedParameterNode, _SlopeMixin):

    def derive(self, alt_aal=P('Altitude AAL'),
               dist=P('Aiming Point Range'),
               alt_std=P('Altitude STD'),
               sat=P('SAT'),
               apps=S('Approach')):
        pass


class SlopeAngleToAimingPoint(DerivedParameterNode):

    def derive(self, slope_to_ldg=P('Slope To Aiming Point')):
        pass


class ApproachFlightPathAngle(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Altitude AAL', 'SAT', 'Approach And Landing'),
                      available) and \
               any_of(('Aiming Point Range', 'Distance To Landing'), available)

    def derive(self, alt_aal=P('Altitude AAL'),
               dist_aim=P('Aiming Point Range'),
               dist_land=P('Distance To Landing'),
               sat=P('SAT'),
               apps=S('Approach And Landing')):
        pass


class HeadingContinuous(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return ('Heading' in available or
                all_of(('Heading (Capt)', 'Heading (FO)'), available))

    def derive(self, head_mag=P('Heading'),
               head_capt=P('Heading (Capt)'),
               head_fo=P('Heading (FO)'),
               frame = A('Frame')):
        pass


class HeadingTrueContinuous(DerivedParameterNode):

    def derive(self, hdg=P('Heading True')):
        pass


class Heading(DerivedParameterNode):

    def derive(self, head_true=P('Heading True Continuous'),
               mag_var=P('Magnetic Variation')):
        pass


class HeadingTrue(DerivedParameterNode):

    def derive(self, head=P('Heading Continuous'),
               rwy_var=P('Magnetic Variation From Runway')):
        pass


class ILSFrequency(DerivedParameterNode):
    name = 'ILS Frequency'

    @classmethod
    def can_operate(cls, available):
        return ('ILS (1) Frequency' in available and
                'ILS (2) Frequency' in available) or \
               ('ILS-VOR (1) Frequency' in available)

    def derive(self, f1=P('ILS (1) Frequency'), f2=P('ILS (2) Frequency'),
               f1v=P('ILS-VOR (1) Frequency'), f2v=P('ILS-VOR (2) Frequency')):
        pass


class ILSLocalizer(DerivedParameterNode):
    name = 'ILS Localizer'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               src_A=P('ILS (1) Localizer'),
               src_B=P('ILS (2) Localizer'),
               src_C=P('ILS (3) Localizer'),
               src_D=P('ILS (4) Localizer'),
               src_E=P('ILS (L) Localizer'),
               src_F=P('ILS (R) Localizer'),
               src_G=P('ILS (C) Localizer'),
               src_J=P('ILS (EFIS) Localizer'),
               ias=P('Airspeed'),
               ):
        pass


class ILSLateralDistance(DerivedParameterNode):
    name = 'ILS Lateral Distance'

    def derive(self, loc=P('ILS Localizer'), app_rng=P('Approach Range'),
               approaches=App('Approach Information')):
        pass


class ILSGlideslope(DerivedParameterNode):
    name = 'ILS Glideslope'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               src_A=P('ILS (1) Glideslope'),
               src_B=P('ILS (2) Glideslope'),
               src_C=P('ILS (3) Glideslope'),
               src_D=P('ILS (4) Glideslope'),
               src_E=P('ILS (L) Glideslope'),
               src_F=P('ILS (R) Glideslope'),
               src_G=P('ILS (C) Glideslope'),
               src_J=P('ILS (EFIS) Glideslope')):
        pass


class AimingPointRange(DerivedParameterNode):

    def derive(self, app_rng=P('Approach Range'),
               approaches=App('Approach Information'),
               ):
        pass

class CoordinatesSmoothed(object):
    pass


class LatitudeSmoothed(DerivedParameterNode, CoordinatesSmoothed):

    @classmethod
    def can_operate(cls, available, precise=A('Precise Positioning'), ac_type=A('Aircraft Type')):
        if ac_type == helicopter:
            return 'Longitude Prepared' in available
        required = [
            'Latitude Prepared',
            'Longitude Prepared',
            'Airspeed True',
            'Approach Information',
            'Precise Positioning',
            'FDR Takeoff Runway',
            'Mobile']
        if bool(getattr(precise, 'value', False)) is False:
            required.append('Approach Range')
        return all_of(required, available) \
               and any_of(('Heading True Continuous',
                           'Heading Continuous'), available)

    def derive(self,
               lon=P('Longitude Prepared'),
               lat=P('Latitude Prepared'),
               hdg_mag=P('Heading Continuous'),
               ils_loc=P('ILS Localizer'),
               app_range=P('Approach Range'),
               hdg_true=P('Heading True Continuous'),
               gspd_u = P('Groundspeed'),
               gspd_s = P('Groundspeed Signed'),
               tas=P('Airspeed True'),
               precise=A('Precise Positioning'),
               toff=S('Takeoff Roll Or Rejected Takeoff'),
               toff_rwy = A('FDR Takeoff Runway'),
               tdwns = S('Touchdown'),
               approaches = App('Approach Information'),
               mobile=S('Mobile'),
               ac_type = A('Aircraft Type'),
               ):
        pass


class LongitudeSmoothed(DerivedParameterNode, CoordinatesSmoothed):

    @classmethod
    def can_operate(cls, available, precise=A('Precise Positioning'), ac_type=A('Aircraft Type')):
        if ac_type == helicopter:
            return 'Longitude Prepared' in available
        required = [
            'Latitude Prepared',
            'Longitude Prepared',
            'Airspeed True',
            'Approach Information',
            'Precise Positioning',
            'FDR Takeoff Runway',
            'Mobile']
        if bool(getattr(precise, 'value', False)) is False:
            required.append('Approach Range')
        return all_of(required, available) \
               and any_of(('Heading True Continuous',
                           'Heading Continuous'), available)

    def derive(self,
               lon = P('Longitude Prepared'),
               lat = P('Latitude Prepared'),
               hdg_mag=P('Heading Continuous'),
               ils_loc = P('ILS Localizer'),
               app_range = P('Approach Range'),
               hdg_true = P('Heading True Continuous'),
               gspd_u = P('Groundspeed'),
               gspd_s = P('Groundspeed Signed'),
               tas = P('Airspeed True'),
               precise =A('Precise Positioning'),
               toff = S('Takeoff Roll Or Rejected Takeoff'),
               toff_rwy = A('FDR Takeoff Runway'),
               tdwns = S('Touchdown'),
               approaches = App('Approach Information'),
               mobile=S('Mobile'),
               ac_type = A('Aircraft Type'),
               ):
        pass


class Mach(DerivedParameterNode):

    def derive(self, cas=P('Airspeed'), alt=P('Altitude STD Smoothed')):
        pass


class MagneticVariation(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        lat = any_of(('Latitude', 'Latitude (Coarse)'), available)
        lon = any_of(('Longitude', 'Longitude (Coarse)'), available)
        return lat and lon and all_of(('Altitude AAL', 'Start Datetime'),
                                      available)

    def derive(self, lat=P('Latitude'), lat_coarse=P('Latitude (Coarse)'),
               lon=P('Longitude'), lon_coarse=P('Longitude (Coarse)'),
               alt_aal=P('Altitude AAL'), start_datetime=A('Start Datetime')):
        pass


class MagneticVariationFromRunway(DerivedParameterNode):

    def derive(self,
               mag=P('Magnetic Variation'),
               head_toff = KPV('Heading During Takeoff'),
               head_land = KPV('Heading During Landing'),
               toff_rwy = A('FDR Takeoff Runway'),
               land_rwy = A('FDR Landing Runway')):
        pass


class VerticalSpeedInertial(DerivedParameterNode):

    def derive(self,
               az = P('Acceleration Vertical'),
               alt_std = P('Altitude STD Smoothed'),
               alt_rad = P('Altitude Radio Offset Removed'),
               fast = S('Fast'),
               ac_type=A('Aircraft Type')):
        pass


class VerticalSpeed(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return 'Altitude STD Smoothed' in available

    def derive(self, alt_std=P('Altitude STD Smoothed'), frame=A('Frame')):
        pass


class VerticalSpeedForFlightPhases(DerivedParameterNode):

    def derive(self, alt_std = P('Altitude STD Smoothed')):
        pass


class Relief(DerivedParameterNode):

    def derive(self, alt_aal = P('Altitude AAL'),
               alt_rad = P('Altitude Radio')):
        pass

class CoordinatesStraighten(object):
    pass


class LongitudePrepared(DerivedParameterNode, CoordinatesStraighten):
    name = 'Longitude Prepared'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Airspeed True',
                       'Latitude At Liftoff',
                       'Longitude At Liftoff',
                       'Latitude At Touchdown',
                       'Longitude At Touchdown'), available) and \
                any_of(('Heading', 'Heading True'), available)

    def derive(self,
               hdg_mag=P('Heading'),
               hdg_true=P('Heading True'),
               tas=P('Airspeed True'),
               gspd=P('Groundspeed'),
               alt_aal=P('Altitude AAL'),
               lat_lift=KPV('Latitude At Liftoff'),
               lon_lift=KPV('Longitude At Liftoff'),
               lat_land=KPV('Latitude At Touchdown'),
               lon_land=KPV('Longitude At Touchdown')):
        pass


class LatitudePrepared(DerivedParameterNode, CoordinatesStraighten):
    name = 'Latitude Prepared'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Airspeed True',
                       'Latitude At Liftoff',
                       'Longitude At Liftoff',
                       'Latitude At Touchdown',
                       'Longitude At Touchdown'), available) and \
               any_of(('Heading', 'Heading True'), available)

    def derive(self,
               hdg_mag=P('Heading'),
               hdg_true=P('Heading True'),
               tas=P('Airspeed True'),
               gspd=P('Groundspeed'),
               alt_aal=P('Altitude AAL'),
               lat_lift=KPV('Latitude At Liftoff'),
               lon_lift=KPV('Longitude At Liftoff'),
               lat_land=KPV('Latitude At Touchdown'),
               lon_land=KPV('Longitude At Touchdown')):
        pass


class HeadingRate(DerivedParameterNode):

    def derive(self, head=P('Heading Continuous')):
        pass


class Pitch(DerivedParameterNode):

    def derive(self, p1=P('Pitch (1)'), p2=P('Pitch (2)')):
        pass


class PitchRate(DerivedParameterNode):

    def derive(self,
               pitch=P('Pitch'),
               frame=A('Frame')):
        pass


class Roll(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of((
            'Altitude AAL',
            'Heading Continuous',
        ), available) or \
               all_of((
                   'Roll (1)',
                   'Roll (2)',
        ), available)

    def derive(self,
               r1=P('Roll (1)'),
               r2=P('Roll (2)'),
               hdg=P('Heading Continuous'),
               alt_aal=P('Altitude AAL')):
        pass


class RollSmoothed(DerivedParameterNode):

    def derive(self,
               source_A=P('Roll'),
               source_B=P('Roll (1)'),
               source_C=P('Roll (2)'),
               ):
        pass


class PitchSmoothed(DerivedParameterNode):

    def derive(self,
               source_A=P('Pitch'),
               source_B=P('Pitch (1)'),
               source_C=P('Pitch (2)'),
               ):
        pass


class RollRate(DerivedParameterNode):

    def derive(self, roll=P('Roll')):
        pass


class RollRateForTouchdown(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    family=A('Family'),):
        family_name = family.value if family else None
        return family_name in ('ERJ-170/175',) and (
            'Roll' in available)

    def derive(self,
               roll=P('Roll'),):
        pass


class RollRateAtTouchdownLimit(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    family=A('Family'),):
        family_name = family.value if family else None
        return family_name in ('ERJ-170/175',) and (
               'Gross Weight Smoothed' in available)

    def derive(self,
               gw=P('Gross Weight Smoothed'),):
        pass


class AccelerationNormalLowLimitForLandingWeight(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    family=A('Family'),):
        family_name = family.value if family else None
        return family_name in ('ERJ-170/175',) and ('Gross Weight Smoothed' in available)

    def derive(self,
               gw=P('Gross Weight Smoothed')):
        pass


class AccelerationNormalHighLimitForLandingWeight(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    family=A('Family'),):
        family_name = family.value if family else None
        return family_name in ('ERJ-170/175',) and ('Gross Weight Smoothed' in available)

    def derive(self,
               gw=P('Gross Weight Smoothed')):
        pass


class AccelerationNormalHighLimitWithFlapsDown(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    family=A('Family'),):
        family_name = family.value if family else None
        return family_name in ('B737 MAX',) and \
               any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) and \
               all_of(('Gross Weight Smoothed', 'Maximum Takeoff Weight',
                       'Maximum Landing Weight'), available)

    def derive(self,
               flap_lever=P('Flap Lever'),
               flap_synth=P('Flap Lever (Synthetic)'),
               gw=P('Gross Weight Smoothed'),
               mtow=A('Maximum Takeoff Weight'),
               mlw=A('Maximum Landing Weight')):
        pass


class Rudder(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Rudder (Upper)',
            'Rudder (Middle)',
            'Rudder (Lower)',
        ), available)

    def derive(self,
               src_A=P('Rudder (Upper)'),
               src_B=P('Rudder (Middle)'),
               src_C=P('Rudder (Lower)'),
               ):
        pass


class RudderPedalCapt(DerivedParameterNode):
    name = 'Rudder Pedal (Capt)'

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Rudder Pedal (Capt) (1)',
            'Rudder Pedal (Capt) (2)',
        ), available)

    def derive(self, rudder_pedal_capt_1=P('Rudder Pedal (Capt) (1)'),
               rudder_pedal_capt_2=P('Rudder Pedal (Capt) (2)')):
        pass


class RudderPedalFO(DerivedParameterNode):
    name = 'Rudder Pedal (FO)'

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Rudder Pedal (FO) (1)',
            'Rudder Pedal (FO) (2)',
        ), available)

    def derive(self, rudder_pedal_fo_1=P('Rudder Pedal (FO) (1)'),
               rudder_pedal_fo_2=P('Rudder Pedal (FO) (2)')):
        pass


class RudderPedal(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Rudder Pedal (Capt)',
            'Rudder Pedal (FO)',
            'Rudder Pedal Potentiometer',
            'Rudder Pedal Synchro',
        ), available)

    def derive(self, rudder_pedal_capt=P('Rudder Pedal (Capt)'),
               rudder_pedal_fo=P('Rudder Pedal (FO)'),
               pot=P('Rudder Pedal Potentiometer'),
               synchro=P('Rudder Pedal Synchro')):
        pass


class RudderPedalForce(DerivedParameterNode):

    def derive(self,
               fcl=P('Rudder Pedal Force (Capt) (L)'),
               fcr=P('Rudder Pedal Force (Capt) (R)'),
               ffl=P('Rudder Pedal Force (FO) (L)'),
               ffr=P('Rudder Pedal Force (FO) (R)')):
        pass


class ThrottleLevers(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Eng (1) Throttle Lever',
            'Eng (2) Throttle Lever',
        ), available)

    def derive(self,
               tla1=P('Eng (1) Throttle Lever'),
               tla2=P('Eng (2) Throttle Lever')):
        pass


class ThrustAsymmetry(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Eng (*) EPR Max', 'Eng (*) EPR Min'), available) or\
               all_of(('Eng (*) N1 Max', 'Eng (*) N1 Min'), available)

    def derive(self, epr_max=P('Eng (*) EPR Max'), epr_min=P('Eng (*) EPR Min'),
               n1_max=P('Eng (*) N1 Max'), n1_min=P('Eng (*) N1 Min')):
        pass


class Turbulence(DerivedParameterNode):

    def derive(self, acc=P('Acceleration Vertical')):
        pass


class WindDirectionContinuous(DerivedParameterNode):

    def derive(self, wind_head=P('Wind Direction'),):
        pass


class WindDirectionTrueContinuous(DerivedParameterNode):

    def derive(self, wind_dir_cont=P('Wind Direction Continuous'),):
        pass


class WindDirectionMagneticContinuous(DerivedParameterNode):

    def derive(self, wind_head=P('Wind Direction Magnetic')):
        pass


class Headwind(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        wind_based = all_of((
            'Wind Speed',
            'Wind Direction',
            'Heading True',
            'Altitude AAL',
        ), available)
        aspd_based = all_of((
            'Airspeed True',
            'Groundspeed'
        ), available)
        return wind_based or aspd_based

    def derive(self, aspd=P('Airspeed True'),
               windspeed=P('Wind Speed'),
               wind_dir=P('Wind Direction'),
               head=P('Heading True'),
               alt_aal=P('Altitude AAL'),
               gspd=P('Groundspeed')):
        pass


class Tailwind(DerivedParameterNode):

    def derive(self, hwd=P('Headwind')):
        pass


class SAT(DerivedParameterNode):
    name = 'SAT'

    @classmethod
    def can_operate(cls, available):
        return any_of (('SAT (1)', 'SAT (2)', 'SAT (3)'), available) or all_of(('TAT', 'Mach'), available)

    def derive(self,
               sat1=P('SAT (1)'),
               sat2=P('SAT (2)'),
               sat3=P('SAT (3)'),
               tat=P('TAT'),
               mach=P('Mach')):
        pass


class SAT_ISA(DerivedParameterNode):
    name = 'SAT International Standard Atmosphere'

    def derive(self, alt=P('Altitude STD Smoothed')):
        pass


class TAT(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return (('TAT (1)' in available and 'TAT (2)' in available) or \
                ('SAT' in available and 'Mach' in available))
    name = 'TAT'

    def derive(self,
               source_1=P('TAT (1)'),
               source_2=P('TAT (2)'),
               sat=P('SAT'), mach=P('Mach')):
        pass


class WindAcrossLandingRunway(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Wind Speed', 'Wind Direction Continuous', 'FDR Landing Runway'), available) \
               or \
               all_of(('Wind Speed', 'Wind Direction Magnetic Continuous', 'Heading During Landing'), available)

    def derive(self, windspeed=P('Wind Speed'),
               wind_dir_true=P('Wind Direction Continuous'),
               wind_dir_mag=P('Wind Direction Magnetic Continuous'),
               land_rwy=A('FDR Landing Runway'),
               land_hdg=KPV('Heading During Landing')):
        pass


class Aileron(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Aileron (L)', 'Aileron (R)'), available)

    def derive(self, al=P('Aileron (L)'), ar=P('Aileron (R)')):
        pass


class AileronLeft(DerivedParameterNode):
    name = 'Aileron (L)'

    @classmethod
    def can_operate(cls, available):
        return any_of(('Aileron (L) Potentiometer',
                       'Aileron (L) Synchro',
                       'Aileron (L) Inboard',
                       'Aileron (L) Outboard'), available)

    def derive(self, pot=P('Aileron (L) Potentiometer'),
               synchro=P('Aileron (L) Synchro'),
               ali=P('Aileron (L) Inboard'),
               alo=P('Aileron (L) Outboard')):
        pass


class AileronRight(DerivedParameterNode):
    name = 'Aileron (R)'

    @classmethod
    def can_operate(cls, available):
        return any_of(('Aileron (R) Potentiometer',
                       'Aileron (R) Synchro',
                       'Aileron (R) Inboard',
                       'Aileron (R) Outboard'), available)

    def derive(self, pot=P('Aileron (R) Potentiometer'),
               synchro=P('Aileron (R) Synchro'),
               ari=P('Aileron (R) Inboard'),
               aro=P('Aileron (R) Outboard')):
        pass


class AileronTrim(DerivedParameterNode):
    name = 'Aileron Trim'

    def derive(self,
               atl=P('Aileron Trim (L)'),
               atr=P('Aileron Trim (R)')):
        pass


class Elevator(DerivedParameterNode):

    @classmethod
    def can_operate(cls,available):
        return any_of(('Elevator (L)', 'Elevator (R)'), available)

    def derive(self,
               el=P('Elevator (L)'),
               er=P('Elevator (R)')):
        pass


class ElevatorLeft(DerivedParameterNode):
    name = 'Elevator (L)'

    @classmethod
    def can_operate(cls, available):
        return any_of(('Elevator (L) Potentiometer',
                       'Elevator (L) Synchro',
                       'Elevator (L) Inboard',
                       'Elevator (L) Outboard'), available)

    def derive(self, pot=P('Elevator (L) Potentiometer'),
               synchro=P('Elevator (L) Synchro'),
               inboard=P('Elevator (L) Inboard'),
               outboard=P('Elevator (L) Outboard')):
        pass


class ElevatorRight(DerivedParameterNode):
    name = 'Elevator (R)'

    @classmethod
    def can_operate(cls, available):
        return any_of(('Elevator (R) Potentiometer',
                       'Elevator (R) Synchro',
                       'Elevator (R) Inboard',
                       'Elevator (R) Outboard'), available)

    def derive(self, pot=P('Elevator (R) Potentiometer'),
               synchro=P('Elevator (R) Synchro'),
               inboard=P('Elevator (R) Inboard'),
               outboard=P('Elevator (R) Outboard')):
        pass


class Speedbrake(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        '''
        Note: The frame name cannot be accessed within this method to determine
              which parameters are required.
        For B737-NG aircraft, D226A101-2 RevH states:
            NOTE 25D Spoiler Position No. 3 and 10
            (737-3, -3A, -3B, -3C, -7)
            For airplanes that do not have the Short Field Performance option
        This suggests that the synchro sourced L&R 3 positions have a scaling
        that changes with short field option.
        CL-600 has 3 operational combinations;
         * CRJ100/200/Challenger 850 Flight Spoiler is L&R 3
         * CRJ700/900 Flight Spoilers are L&R 3 and 4
         * Challenger 605 Flight Spoiler is L&R 2
        '''
        family_name = family.value if family else None
        return family_name and (
            family_name in {'CL-600', 'G-V', 'G-IV'} and (
                'Spoiler (L) (2)' in available and
                'Spoiler (R) (2)' in available
            ) or
            family_name == 'G-VI' and (
                'Spoiler (L) (1)' in available and
                'Spoiler (R) (1)' in available
            ) or
            family_name in {'A300', 'A318', 'A319', 'A320', 'A321', 'A330', 'A340', 'A380'} and (
                ('Spoiler (L) (3)' in available and
                    'Spoiler (R) (3)' in available) or
                ('Spoiler (L) (2)' in available and
                    'Spoiler (R) (2)' in available)
            ) or
            family_name == 'A350' and (
                'Spoiler (L) (4)' in available and
                'Spoiler (R) (4)' in available
            ) or
            family_name == 'B737 Classic' and (
                'Spoiler (L) (4)' in available and
                'Spoiler (R) (4)' in available
            ) or
            family_name in {'B737 NG', 'B737 MAX'} and (
                ('Spoiler (L) (3)' in available and
                    'Spoiler (R) (3)' in available) or
                ('Spoiler (L) (4)' in available and
                    'Spoiler (R) (4)' in available)
            ) or
            family_name == 'Global' and (
                'Spoiler (L) (5)' in available and
                'Spoiler (R) (5)' in available
            ) or
            family_name == 'B787' and (
                'Spoiler (L) (7)' in available and
                'Spoiler (R) (7)' in available
            ) or
            family_name in {'Citation', 'Citation VLJ', 'Learjet', 'Phenom 300', 'Pilatus-PC'} and all_of((
                'Spoiler (L)',
                'Spoiler (R)'),
                available
            ) or
            family_name in {'CRJ 900', 'CL-600', 'G-IV'} and all_of((
                'Spoiler (L) (3)',
                'Spoiler (L) (4)',
                'Spoiler (R) (3)',
                'Spoiler (R) (4)'),
                available
            ) or
            family_name == 'CL-600' and all_of((
                'Spoiler (L) (3)',
                'Spoiler (R) (3)',),
                available
            ) or
            family_name == 'MD-11' and all_of((
                'Spoiler (L) (3)',
                'Spoiler (L) (5)',
                'Spoiler (R) (3)',
                'Spoiler (R) (5)'),
                available
            ) or
            family_name in {'ERJ-170/175', 'ERJ-190/195'} and all_of((
                'Spoiler (L) (3)',
                'Spoiler (L) (4)',
                'Spoiler (L) (5)',
                'Spoiler (R) (3)',
                'Spoiler (R) (4)',
                'Spoiler (R) (5)'),
                available
            ) or
            family_name == 'B777' and all_of((
                'Spoiler (L) (6)',
                'Spoiler (L) (7)',
                'Spoiler (R) (6)',
                'Spoiler (R) (7)'),
                available
            )
        )

    def derive(self,
               spoiler_l=P('Spoiler (L)'),
               spoiler_l1=P('Spoiler (L) (1)'),
               spoiler_l2=P('Spoiler (L) (2)'),
               spoiler_l3=P('Spoiler (L) (3)'),
               spoiler_l4=P('Spoiler (L) (4)'),
               spoiler_l5=P('Spoiler (L) (5)'),
               spoiler_l6=P('Spoiler (L) (6)'),
               spoiler_l7=P('Spoiler (L) (7)'),
               spoiler_r=P('Spoiler (R)'),
               spoiler_r1=P('Spoiler (R) (1)'),
               spoiler_r2=P('Spoiler (R) (2)'),
               spoiler_r3=P('Spoiler (R) (3)'),
               spoiler_r4=P('Spoiler (R) (4)'),
               spoiler_r5=P('Spoiler (R) (5)'),
               spoiler_r6=P('Spoiler (R) (6)'),
               spoiler_r7=P('Spoiler (R) (7)'),
               family=A('Family'),
               ):
        pass


class SpeedbrakeHandle(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Speedbrake Handle (L)',
            'Speedbrake Handle (R)',
            'Speedbrake Handle (C)',
            'Speedbrake Handle (1)',
            'Speedbrake Handle (2)',
            'Speedbrake Handle (3)',
            'Speedbrake Handle (4)',
        ), available)

    def derive(self,
               sbh_l=P('Speedbrake Handle (L)'),
               sbh_r=P('Speedbrake Handle (R)'),
               sbh_c=P('Speedbrake Handle (C)'),
               sbh_1=P('Speedbrake Handle (1)'),
               sbh_2=P('Speedbrake Handle (2)'),
               sbh_3=P('Speedbrake Handle (3)'),
               sbh_4=P('Speedbrake Handle (4)')):
        pass


class Stabilizer(DerivedParameterNode):

    def derive(self,
               src_1=P('Stabilizer (1)'),
               src_2=P('Stabilizer (2)'),
               src_3=P('Stabilizer (3)'),
               frame = A('Frame'),
               ):
        pass


class ApproachRange(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Airspeed True',
                       'Altitude AAL',
                       'Approach Information'), available) and \
               any_of(('Heading True',
                       'Track True',
                       'Track',
                       'Heading'), available)

    def derive(self, gspd=P('Groundspeed'),
               glide=P('ILS Glideslope'),
               trk_mag=P('Track'),
               trk_true=P('Track True'),
               hdg_mag=P('Heading'),
               hdg_true=P('Heading True'),
               tas=P('Airspeed True'),
               alt_aal=P('Altitude AAL'),
               approaches=App('Approach Information'),
               ):
        pass


class VOR1Frequency(DerivedParameterNode):
    name = 'VOR (1) Frequency'

    def derive(self, f=P('ILS-VOR (1) Frequency')):
        pass


class VOR2Frequency(DerivedParameterNode):
    name = 'VOR (2) Frequency'

    def derive(self, f=P('ILS-VOR (2) Frequency')):
        pass


class WindSpeed(DerivedParameterNode):

    def derive(self, wind_1=P('Wind Speed (1)'), wind_2=P('Wind Speed (2)')):
        pass


class WindDirection(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return (('Wind Direction (1)' in available or
                 'Wind Direction (2)' in available))

    def derive(self, wind_1=P('Wind Direction (1)'),
               wind_2=P('Wind Direction (2)')):
        pass


class WindDirectionTrue(DerivedParameterNode):

    def derive(self, wind_dir=P('Wind Direction'),):
        pass


class WindDirectionMagnetic(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return 'Wind Direction' in available and \
               any_of(('Magnetic Variation From Runway', 'Magnetic Variation'),
                      available)

    def derive(self, wind=P('Wind Direction'),
               rwy_var=P('Magnetic Variation From Runway'),
               mag_var=P('Magnetic Variation')):
        pass


class WheelSpeedLeft(DerivedParameterNode):
    name = 'Wheel Speed (L)'

    @classmethod
    def can_operate(cls, available):
        return 'Wheel Speed (L) (1)' in available

    def derive(self, ws_1=P('Wheel Speed (L) (1)'), ws_2=P('Wheel Speed (L) (2)'),
               ws_3=P('Wheel Speed (L) (3)'), ws_4=P('Wheel Speed (L) (4)')):
        pass


class WheelSpeedRight(DerivedParameterNode):
    name = 'Wheel Speed (R)'

    @classmethod
    def can_operate(cls, available):
        return 'Wheel Speed (R) (1)' in available

    def derive(self, ws_1=P('Wheel Speed (R) (1)'), ws_2=P('Wheel Speed (R) (2)'),
               ws_3=P('Wheel Speed (R) (3)'), ws_4=P('Wheel Speed (R) (4)')):
        pass


class AirspeedSelectedForApproaches(DerivedParameterNode):

    def derive(self, aspd=P('Airspeed Selected'), fast=S('Fast')):
        pass


class AirspeedSelected(DerivedParameterNode):
    name = 'Airspeed Selected'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, as_l=P('Airspeed Selected (L)'),
               as_r=P('Airspeed Selected (R)'),
               as_mcp=P('Airspeed Selected (MCP)'),
               as_1=P('Airspeed Selected (1)'),
               as_2=P('Airspeed Selected (2)'),
               as_3=P('Airspeed Selected (3)'),
               as_4=P('Airspeed Selected (4)')):
        pass


class WheelSpeed(DerivedParameterNode):

    def derive(self, ws_l=P('Wheel Speed (L)'), ws_r=P('Wheel Speed (R)')):
        pass


class Track(DerivedParameterNode):

    def derive(self, heading=P('Heading'), drift=P('Drift')):
        pass


class TrackTrue(DerivedParameterNode):

    def derive(self, heading=P('Heading True'), drift=P('Drift')):
        pass


class TrackContinuous(DerivedParameterNode):

    def derive(self, heading=P('Heading Continuous'), drift=P('Drift')):
        pass


class TrackTrueContinuous(DerivedParameterNode):

    def derive(self, heading=P('Heading True Continuous'), drift=P('Drift')):
        pass


class TrackDeviationFromRunway(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Approach Information', 'FDR Takeoff Runway'), available) \
               and any_of(('Track Continuous', 'Track True Continuous'), available)

    def derive(self, track_true=P('Track True Continuous'),
               track_mag=P('Track Continuous'),
               takeoff=S('Takeoff Roll Or Rejected Takeoff'),
               to_rwy=A('FDR Takeoff Runway'),
               apps=App('Approach Information')):
        pass


class V2Lookup(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family'),
                    engine_series=A('Engine Series'), engine_type=A('Engine Type')):
        core = all_of((
            'Airspeed',
            'Liftoff',
            'Climb Start',
            'Model',
            'Series',
            'Family',
            'Engine Type',
            'Engine Series',
        ), available)
        flap = any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
        ), available)
        attrs = (model, series, family, engine_type, engine_series)
        return core and flap and lookup_table(cls, 'v2', *attrs)

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airspeed=P('Airspeed'),
               weight_liftoffs=KPV('Gross Weight At Liftoff'),
               liftoffs=KTI('Liftoff'),
               climb_starts=KTI('Climb Start'),
               model=A('Model'),
               series=A('Series'),
               family=A('Family'),
               engine_type=A('Engine Type'),
               engine_series=A('Engine Series')):
        pass


class Vref(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, afr_vref=A('AFR Vref')):
        afr = all_of((
            'Airspeed',
            'AFR Vref',
            'Approach And Landing',
        ), available) and afr_vref and afr_vref.value >= AIRSPEED_THRESHOLD
        embraer = all_of((
            'Airspeed',
            'V1-Vref',
            'Approach And Landing',
        ), available)
        return afr or embraer

    def derive(self,
               airspeed=P('Airspeed'),
               v1_vref=P('V1-Vref'),
               afr_vref=A('AFR Vref'),
               approaches=S('Approach And Landing')):
        pass


class VrefLookup(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family'),
                    engine_type=A('Engine Type'), engine_series=A('Engine Series')):
        core = all_of((
            'Airspeed',
            'Approach And Landing',
            'Model',
            'Series',
            'Family',
            'Engine Type',
            'Engine Series',
        ), available)
        flap = any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
        ), available)
        weight = any_of((
            'Gross Weight Smoothed',
            'Touchdown',
        ), available)
        attrs = (model, series, family, engine_type, engine_series)
        return core and flap and weight and lookup_table(cls, 'vref', *attrs)

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               air_spd=P('Airspeed'),
               gw=P('Gross Weight Smoothed'),
               approaches=S('Approach And Landing'),
               touchdowns=KTI('Touchdown'),
               model=A('Model'),
               series=A('Series'),
               family=A('Family'),
               engine_type=A('Engine Type'),
               engine_series=A('Engine Series')):
        pass


class Vapp(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, afr_vapp=A('AFR Vapp')):
        afr = all_of((
            'Airspeed',
            'AFR Vapp',
            'Approach And Landing',
        ), available) and afr_vapp and afr_vapp.value >= AIRSPEED_THRESHOLD
        embraer = all_of((
            'Airspeed',
            'VR-Vapp',
            'Approach And Landing',
        ), available)
        return afr or embraer

    def derive(self,
               airspeed=P('Airspeed'),
               vr_vapp=A('VR-Vapp'),
               afr_vapp=A('AFR Vapp'),
               approaches=S('Approach And Landing')):
        pass


class VappLookup(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family'),
                    engine_type=A('Engine Type'), engine_series=A('Engine Series')):
        core = all_of((
            'Airspeed',
            'Approach And Landing',
            'Model',
            'Series',
            'Family',
            'Engine Type',
            'Engine Series',
        ), available)
        flap = any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
        ), available)
        weight = any_of((
            'Gross Weight Smoothed',
            'Touchdown',
        ), available)
        attrs = (model, series, family, engine_type, engine_series)
        return core and flap and weight and lookup_table(cls, 'vapp', *attrs)

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               air_spd=P('Airspeed'),
               gw=P('Gross Weight Smoothed'),
               approaches=S('Approach And Landing'),
               touchdowns=KTI('Touchdown'),
               model=A('Model'),
               series=A('Series'),
               family=A('Family'),
               engine_type=A('Engine Type'),
               engine_series=A('Engine Series')):
        pass


class VLSLookup(DerivedParameterNode):
    name = 'VLS Lookup'

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family'),
                    engine_type=A('Engine Type'), engine_series=A('Engine Series')):
        if family and not family.value in ('A319', 'A320', 'A321', 'A330', 'A340'):
            return False
        core = all_of((
            'Airspeed',
            'Approach And Landing',
            'Model',
            'Series',
            'Family',
            'Engine Type',
            'Engine Series',
            'Gross Weight Smoothed',
            'Airborne',
        ), available)
        flap = any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
        ), available)
        attrs = (model, series, family, engine_type, engine_series)
        return core and flap and lookup_table(cls, 'vls', *attrs)

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               air_spd=P('Airspeed'),
               gw=P('Gross Weight Smoothed'),
               approaches=S('Approach And Landing'),
               model=A('Model'),
               series=A('Series'),
               family=A('Family'),
               engine_type=A('Engine Type'),
               engine_series=A('Engine Series'),
               center_of_gravity=P('Center Of Gravity'),
               alt_std=P('Altitude STD Smoothed'),
               airborne=S('Airborne')):
        pass


class VMOLookup(DerivedParameterNode):
    name = 'VMO Lookup'

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family'),
                    engine_type=A('Engine Type'), engine_series=A('Engine Series')):
        core = all_of((
            'Altitude STD Smoothed',
            'Model',
            'Series',
            'Family',
            'Engine Type',
            'Engine Series',
        ), available)
        attrs = (model, series, family, engine_type, engine_series)
        return core and lookup_table(cls, 'vmo', *attrs)

    def derive(self,
               alt_std=P('Altitude STD Smoothed'),
               model=A('Model'),
               series=A('Series'),
               family=A('Family'),
               engine_type=A('Engine Type'),
               engine_series=A('Engine Series')):
        pass


class MMOLookup(DerivedParameterNode):
    name = 'MMO Lookup'

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family'),
                    engine_type=A('Engine Type'), engine_series=A('Engine Series')):
        core = all_of((
            'Altitude STD Smoothed',
            'Model',
            'Series',
            'Family',
            'Engine Type',
            'Engine Series',
        ), available)
        attrs = (model, series, family, engine_type, engine_series)
        return core and lookup_table(cls, 'mmo', *attrs)

    def derive(self,
               alt_std=P('Altitude STD Smoothed'),
               model=A('Model'),
               series=A('Series'),
               family=A('Family'),
               engine_type=A('Engine Type'),
               engine_series=A('Engine Series')):
        pass


class MinimumAirspeed(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        core = all_of(('Airborne', 'Airspeed'), available)
        a = any_of((
            'FC Min Operating Speed',
            'Min Operating Speed',
            'VLS',
            'VLS Lookup',
        ), available)
        b = any_of((
            'Minimum Clean Lookup',
        ), available)
        f = any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available)
        return core and (a or (b and f))

    def derive(self,
               airspeed=P('Airspeed'),
               mos_fc=P('FC Min Operating Speed'),
               mos=P('Min Operating Speed'),
               vls=P('VLS'),
               vls_lookup=P('VLS Lookup'),
               min_clean=P('Minimum Clean Lookup'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class MinimumCleanLookup(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        return family and family.value in ('B757', 'B767') and \
               all_of(cls.get_dependency_names(), available)

    def derive(self,
               air_spd=P('Airspeed'),
               gw=P('Gross Weight Smoothed'),
               airborne=S('Airborne'),
               model=A('Model'),
               series=A('Series'),
               family=A('Family'),
               engine_type=A('Engine Type'),
               engine_series=A('Engine Series'),
               alt_std=P('Altitude STD Smoothed'),
               crz=S('Cruise'),):
        pass


class FlapManoeuvreSpeed(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available, manufacturer=A('Manufacturer'),
                    model=A('Model'), series=A('Series'), family=A('Family'),
                    engine_type=A('Engine Type'), engine_series=A('Engine Series')):
        if not manufacturer or not manufacturer.value == 'Boeing':
            return False
        try:
            at.get_fms_map(model.value, series.value, family.value)
        except KeyError:
            cls.warning("No flap manoeuvre speed tables available for '%s', "
                        "'%s', '%s'.", model.value, series.value, family.value)
            return False
        core = all_of((
            'Airspeed', 'Altitude STD Smoothed',
            'Gross Weight Smoothed', 'Model', 'Series', 'Family',
            'Engine Type', 'Engine Series',
        ), available)
        flap = any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
        ), available)
        attrs = (model, series, family, engine_type, engine_series)
        return core and flap and lookup_table(cls, 'vref', *attrs)

    def derive(self,
               airspeed=P('Airspeed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               gw=P('Gross Weight Smoothed'),
               vref_25=P('Vref (25)'),
               vref_30=P('Vref (30)'),
               alt_std=P('Altitude STD Smoothed'),
               model=A('Model'),
               series=A('Series'),
               family=A('Family'),
               engine_type=A('Engine Type'),
               engine_series=A('Engine Series')):
        pass


class AirspeedMinusAirspeedSelectedFor3Sec(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Airspeed', 'Airspeed Selected For Approaches'), available)

    def derive(self, aspd=P('Airspeed'), aspd_sel=P('Airspeed Selected For Approaches')):
        pass


class AirspeedMinusAirspeedSelectedFMS(DerivedParameterNode):
    name = 'Airspeed Minus Airspeed Selected (FMS)'

    def derive(self,
               airspeed=P('Airspeed'),
               fms=P('Airspeed Selected (FMS)'),
               approaches=S('Approach And Landing')):
        pass


class AirspeedMinusAirspeedSelectedFMSFor3Sec(DerivedParameterNode):
    name = 'Airspeed Minus Airspeed Selected (FMS) For 3 Sec'

    def derive(self, speed=P('Airspeed Minus Airspeed Selected (FMS)')):
        pass


class AirspeedMinusV2(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return (all_of(('Airspeed', 'Liftoff', 'Climb Start',
                        'Climb Acceleration Start', 'Grounded'), available) and
                any_of(('V2 At Liftoff', 'Airspeed Selected At Takeoff Acceleration Start',
                        'V2 Lookup At Liftoff'), available))

    def derive(self,
               airspeed=P('Airspeed'),
               v2_recorded=KPV('V2 At Liftoff'),
               airspeed_selected=KPV('Airspeed Selected At Takeoff Acceleration Start'),
               v2_lookup=KPV('V2 Lookup At Liftoff'),
               liftoffs=KTI('Liftoff'),
               climb_starts=KTI('Climb Start'),
               climb_accel_starts=KTI('Climb Acceleration Start'),
               grounded=S('Grounded')):
        pass


class AirspeedMinusV2For3Sec(DerivedParameterNode):

    def derive(self, speed=P('Airspeed Minus V2')):
        pass


class AirspeedMinusVref(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of((
            'Airspeed',
            'Approach And Landing',
        ), available) and any_of(('Vref', 'Vref Lookup'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               vref_recorded=P('Vref'),
               vref_lookup=P('Vref Lookup'),
               approaches=S('Approach And Landing')):
        pass


class AirspeedMinusVrefFor3Sec(DerivedParameterNode):

    def derive(self, speed=P('Airspeed Minus Vref')):
        pass


class AirspeedMinusVapp(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of((
            'Airspeed',
            'Approach And Landing',
        ), available) and any_of(('Vapp', 'Vapp Lookup'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               vapp_recorded=P('Vapp'),
               vapp_lookup=P('Vapp Lookup'),
               approaches=S('Approach And Landing')):
        pass


class AirspeedMinusVappFor3Sec(DerivedParameterNode):

    def derive(self, speed=P('Airspeed Minus Vapp')):
        pass


class AirspeedMinusVLS(DerivedParameterNode):
    name = 'Airspeed Minus VLS'

    @classmethod
    def can_operate(cls, available):
        return all_of((
            'Airspeed',
            'Approach And Landing',
        ), available) and any_of(('VLS', 'VLS Lookup'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               vls_recorded=P('VLS'),
               vls_lookup=P('VLS Lookup'),
               approaches=S('Approach And Landing')):
        pass


class AirspeedMinusVLSFor3Sec(DerivedParameterNode):
    name = 'Airspeed Minus VLS For 3 Sec'

    def derive(self, speed=P('Airspeed Minus VLS')):
        pass


class AirspeedMinusMinimumAirspeed(DerivedParameterNode):

    def derive(self,
               airspeed=P('Airspeed'),
               minimum_airspeed=P('Minimum Airspeed')):
        pass


class AirspeedMinusMinimumAirspeedFor3Sec(DerivedParameterNode):

    def derive(self, speed=P('Airspeed Minus Minimum Airspeed')):
        pass


class AirspeedMinusFlapManoeuvreSpeed(DerivedParameterNode):

    def derive(self,
               airspeed=P('Airspeed'),
               fms=P('Flap Manoeuvre Speed')):
        pass


class AirspeedMinusFlapManoeuvreSpeedFor3Sec(DerivedParameterNode):

    def derive(self,
               airspeed=P('Airspeed'),
               fms=P('Flap Manoeuvre Speed')):
        pass


class AirspeedRelative(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Airspeed Minus V2',
            'Airspeed Minus Vapp',
            'Airspeed Minus Vref',
        ), available)

    def derive(self,
               takeoff=P('Airspeed Minus V2'),
               vapp=P('Airspeed Minus Vapp'),
               vref=P('Airspeed Minus Vref')):
        pass


class AirspeedRelativeFor3Sec(DerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Airspeed Minus V2 For 3 Sec',
            'Airspeed Minus Vapp For 3 Sec',
            'Airspeed Minus Vref For 3 Sec',
        ), available)

    def derive(self,
               takeoff=P('Airspeed Minus V2 For 3 Sec'),
               vapp=P('Airspeed Minus Vapp For 3 Sec'),
               vref=P('Airspeed Minus Vref For 3 Sec')):
        pass


class KineticEnergy(DerivedParameterNode):

    def derive(self,airspeed=P('Airspeed True'),
               mass=P('Gross Weight Smoothed')):
        pass


class PotentialEnergy(DerivedParameterNode):

    def derive(self, altitude_aal=P('Altitude AAL'),
               gross_weight_smoothed=P('Gross Weight Smoothed')):
        pass


class AircraftEnergy(DerivedParameterNode):

    def derive(self, potential_energy=P('Potential Energy'),
               kinetic_energy=P('Kinetic Energy')):
        pass
