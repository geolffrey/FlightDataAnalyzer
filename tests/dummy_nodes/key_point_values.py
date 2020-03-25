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

class FlapOrConfigurationMaxOrMin(object):
    pass


class AccelerationLateralMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        '''
        This KPV has no inherent flight phase associated with it, but we can
        reasonably say that we are not interested in anything while the aircraft is
        stationary.
        '''
        return 'Acceleration Lateral Offset Removed' in available

    def derive(self,
               acc_lat=P('Acceleration Lateral Offset Removed'),
               gnd_spd=P('Groundspeed')):
        pass


class AccelerationLateralAtTouchdown(KeyPointValueNode):

    def derive(self,
               acc_lat=P('Acceleration Lateral Offset Removed'),
               touchdowns=KTI('Touchdown')):
        pass


class AccelerationLateralDuringTakeoffMax(KeyPointValueNode):

    def derive(self,
               acc_lat=P('Acceleration Lateral Offset Removed'),
               takeoff_rolls=S('Takeoff Roll')):
        pass


class AccelerationLateralDuringLandingMax(KeyPointValueNode):

    def derive(self,
               acc_lat=P('Acceleration Lateral Offset Removed'),
               landing_rolls=S('Landing Roll'),
               ldg_rwy=A('FDR Landing Runway')):
        pass


class AccelerationLateralWhileAirborneMax(KeyPointValueNode):

    def derive(self,
               acc_lat=P('Acceleration Lateral Offset Removed'),
               airborne=S('Airborne')):
        pass


class AccelerationLateralWhileTaxiingStraightMax(KeyPointValueNode):

    def derive(self,
               acc_lat=P('Acceleration Lateral Smoothed'),
               taxiing=S('Taxiing'),
               turns=S('Turning On Ground')):
        pass


class AccelerationLateralWhileTaxiingTurnMax(KeyPointValueNode):

    def derive(self,
               acc_lat=P('Acceleration Lateral Smoothed'),
               taxiing=S('Taxiing'),
               turns=S('Turning On Ground')):
        pass


class AccelerationLateralInTurnDuringTaxiInMax(KeyPointValueNode):

    def derive(self,
               acc_lat=P('Acceleration Lateral Smoothed'),
               taxiing=S('Taxi In'),
               turns=S('Turning On Ground')):
        pass


class AccelerationLateralInTurnDuringTaxiOutMax(KeyPointValueNode):

    def derive(self,
               acc_lat=P('Acceleration Lateral Smoothed'),
               taxiing=S('Taxi Out'),
               turns=S('Turning On Ground')):
        pass


class AccelerationLateralOffset(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Acceleration Lateral', 'Altitude AAL', 'Heading Rate'), available) or \
               all_of(('Acceleration Lateral', 'Taxiing', 'Turning On Ground'), available)

    def derive(self,
               acc_lat=P('Acceleration Lateral'),
               alt=P('Altitude AAL'),
               hdg_rate=P('Heading Rate'),
               taxiing=S('Taxiing'),
               turns=S('Turning On Ground'),):
        pass


class AccelerationLateralFor5SecMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, frame=A('Frame')):
        if frame and frame.value.startswith('787'):
            return False
        else:
            return all_deps(cls, available)

    def derive(self, accel_lat=P('Acceleration Lateral Offset Removed')):
        pass


class AccelerationLongitudinalOffset(KeyPointValueNode):

    def derive(self,
               acc_lon=P('Acceleration Longitudinal'),
               mobiles=S('Mobile'),
               fasts=S('Fast')):
        pass


class AccelerationLongitudinalDuringTakeoffMax(KeyPointValueNode):

    def derive(self,
               acc_lon=P('Acceleration Longitudinal Offset Removed'),
               takeoff=S('Takeoff')):
        pass


class AccelerationLongitudinalDuringLandingMin(KeyPointValueNode):

    def derive(self,
               acc_lon=P('Acceleration Longitudinal Offset Removed'),
               landing=S('Landing')):
        pass


class AccelerationLongitudinalWhileAirborneMax(KeyPointValueNode):

    def derive(self,
               acc_long=P('Acceleration Longitudinal Offset Removed'),
               airborne=S('Airborne')):
        pass


class AccelerationNormalMax(KeyPointValueNode):

    def derive(self,
               acc_norm=P('Acceleration Normal Offset Removed'),
               mobile=S('Mobile')):
        pass


class AccelerationNormal20FtTo5FtMax(KeyPointValueNode):

    def derive(self,
               acc_norm=P('Acceleration Normal Offset Removed'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AccelerationNormalWithFlapUpWhileAirborneMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) and \
            all_of(('Acceleration Normal Offset Removed', 'Airborne'), available)

    def derive(self,
               acc_norm=P('Acceleration Normal Offset Removed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class AccelerationNormalWithFlapUpWhileAirborneMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) and \
            all_of(('Acceleration Normal Offset Removed', 'Airborne'), available)

    def derive(self,
               acc_norm=P('Acceleration Normal Offset Removed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class AccelerationNormalWithFlapDownWhileAirborneMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) and \
            all_of(('Acceleration Normal Offset Removed', 'Airborne'), available)

    def derive(self,
               acc_norm=P('Acceleration Normal Offset Removed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class AccelerationNormalWithFlapDownWhileAirborneMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) and \
            all_of(('Acceleration Normal Offset Removed', 'Airborne'), available)

    def derive(self,
               acc_norm=P('Acceleration Normal Offset Removed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class AccelerationNormalAboveLimitWithFlapDownWhileAirborne(KeyPointValueNode):

    def derive(self,
               acc_norm=P('Acceleration Normal Offset Removed'),
               acc_limit=P('Acceleration Normal High Limit With Flaps Down'),
               airborne=S('Airborne')):
        pass


class AccelerationNormalAtLiftoff(KeyPointValueNode):

    def derive(self,
               acc_norm=P('Acceleration Normal Offset Removed'),
               liftoffs=KTI('Liftoff')):
        pass


class AccelerationNormalAtTouchdown(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Acceleration Normal Offset Removed', 'Touchdown',
                       'Landing'), available)

    def derive(self,
               acc_norm=P('Acceleration Normal Offset Removed'),
               touchdowns=KTI('Touchdown'),
               ldgs=S('Landing'),
               ldg_rolls=S('Landing Roll'),
               touch_and_gos=KTI('Touch And Go')):
        pass


class AccelerationNormalAboveWeightLowLimitAtTouchdown(KeyPointValueNode):

    def derive(self,
               acc_norm_tdwns = KPV('Acceleration Normal At Touchdown'),
               acc_limit = P('Acceleration Normal Low Limit For Landing Weight'),
               ):
        pass


class AccelerationNormalAboveWeightHighLimitAtTouchdown(KeyPointValueNode):

    def derive(self,
               acc_norm_tdwns = KPV('Acceleration Normal At Touchdown'),
               acc_limit = P('Acceleration Normal High Limit For Landing Weight'),
               ):
        pass


class LoadFactorThresholdAtTouchdown(KeyPointValueNode):

    @staticmethod
    def get_landing_weight(s, m, modif):
        return True
                    

    @classmethod
    def can_operate(cls, available, model=A('Model'), series=A('Series'),
                    mods=A('Modifications')):
        if None in (model, series, mods):
            return False
        ac_weight = cls.get_landing_weight(series.value, model.value,
                                           mods.value)
        return ac_weight and all_deps(cls, available)

    def derive(self,
               land_vert_acc=KPV('Acceleration Normal At Touchdown'),
               roll=P('Roll'),
               tdwns=KTI('Touchdown'),
               gw_kpv=KPV('Gross Weight At Touchdown'),
               gw = P('Gross Weight'),
               model=A('Model'),
               series=A('Series'),
               mods=A('Modifications'),
               touch_and_go=KTI('Touch And Go')):
        pass


class AccelerationNormalMinusLoadFactorThresholdAtTouchdown(KeyPointValueNode):

    @staticmethod
    def get_landing_weight(s, m, modif):
        return True
                    

    @classmethod
    def can_operate(cls, available, model=A('Model'), series=A('Series'),
                    mods=A('Modifications')):
        return all_deps(cls, available)

    def derive(self,
               land_vert_acc=KPV('Acceleration Normal At Touchdown'),
               load_factors=KPV('Load Factor Threshold At Touchdown')):
        pass


class AccelerationNormalLiftoffTo35FtMax(KeyPointValueNode):

    def derive(self,
               acc_norm=P('Acceleration Normal Offset Removed'),
               liftoffs=S('Liftoff'),
               takeoffs=S('Takeoff')):
        pass


class AccelerationNormalOffset(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Acceleration Normal', 'Taxiing'), available)

    def derive(self,
               acc_norm=P('Acceleration Normal'),
               taxiing = S('Taxiing')):
        pass


class AccelerationNormalWhileAirborneMax(KeyPointValueNode):

    def derive(self, accel_norm=P('Acceleration Normal Offset Removed'),
               airborne=S('Airborne')):
        pass


class AccelerationNormalWhileAirborneMin(KeyPointValueNode):

    def derive(self, accel_norm=P('Acceleration Normal Offset Removed'),
               airborne=S('Airborne')):
        pass


class AirspeedMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               airborne=S('Airborne')):
        pass


class AirspeedAt8000FtDescending(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_std_desc=S('Altitude When Descending')):
        pass


class AirspeedDuringCruiseMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever (Synthetic)', 'Flap Lever'), available) and \
               all_of(('Airspeed', 'Cruise'), available)

    def derive(self,
               air_spd=P('Airspeed'),
               cruises=S('Cruise'),
               flap_synth=M('Flap Lever (Synthetic)'),
               flap_lever=M('Flap Lever')):
        pass


class AirspeedDuringCruiseMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever (Synthetic)', 'Flap Lever'), available) and \
               all_of(('Airspeed', 'Cruise'), available)

    def derive(self,
               air_spd=P('Airspeed'),
               cruises=S('Cruise'),
               flap_synth=M('Flap Lever (Synthetic)'),
               flap_lever=M('Flap Lever')):
        pass


class AirspeedGustsDuringFinalApproach(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               gnd_spd=P('Groundspeed'),
               alt_rad=P('Altitude Radio'),
               airborne=S('Airborne')):
        pass


class AirspeedBelowAirspeedSelectedDurationMax(KeyPointValueNode):

    def derive(self, spd=P('Airspeed'),
               spd_sel=P('Airspeed Selected'),
               airs=S('Airborne')):
        pass


class AirspeedAtLiftoff(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               liftoffs=KTI('Liftoff')):
        pass


class AirspeedAt35FtDuringTakeoff(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               takeoffs=S('Takeoff')):
        pass


class Airspeed35To1000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               initial_climb=S('Initial Climb')):
        pass


class Airspeed35To1000FtMin(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               initial_climb=S('Initial Climb')):
        pass


class Airspeed1000To5000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               climbs=S('Climb')):
        pass


class Airspeed5000To8000FtMax(KeyPointValueNode):

    def derive(self, air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_std=P('Altitude STD Smoothed'),
               climbs=S('Climb')):
        pass


class Airspeed5000To10000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_std=P('Altitude STD Smoothed'),
               climbs=S('Climb')):
        pass


class Airspeed1000To8000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_std=P('Altitude STD Smoothed'),
               climbs=S('Climb')):
        pass


class Airspeed1000To8000FtMaxQNH(KeyPointValueNode):
    name = 'Airspeed 1000 To 8000 Ft Max QNH'

    def derive(self,
               air_spd=P('Airspeed'),
               alt_qnh=P('Altitude QNH'),
               climbs=S('Climb')):
        pass


class Airspeed8000To10000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_std=P('Altitude STD Smoothed'),
               climb=S('Climb')):
        pass


class Airspeed8000To10000FtMaxQNH(KeyPointValueNode):
    name = 'Airspeed 8000 To 10000 Ft Max QNH'

    def derive(self,
               air_spd=P('Airspeed'),
               alt_qnh=P('Altitude QNH'),
               climbs=S('Climb'),
               levels=S('Level Flight')):
        pass


class Airspeed3000FtToTopOfClimbMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               tocs=KTI('Top Of Climb')):
        pass


class Airspeed3000FtToTopOfClimbMin(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               tocs=KTI('Top Of Climb')):
        pass


class Airspeed10000To5000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_std=P('Altitude STD Smoothed'),
               descends=S('Descent')):
        pass


class Airspeed10000To8000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_std=P('Altitude STD Smoothed'),
               descent=S('Descent')):
        pass


class Airspeed10000To8000FtMaxQNH(KeyPointValueNode):
    name = 'Airspeed 10000 To 8000 Ft Max QNH'

    def derive(self,
               air_spd=P('Airspeed'),
               alt_qnh=P('Altitude QNH'),
               descents=S('Descent'),
               levels=S('Level Flight')):
        pass


class Airspeed8000To5000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_std=P('Altitude STD Smoothed'),
               descends=S('Descent')):
        pass


class Airspeed8000To5000FtMaxQNH(KeyPointValueNode):
    name = 'Airspeed 8000 To 5000 Ft Max QNH'

    def derive(self,
               air_spd=P('Airspeed'),
               alt_qnh=P('Altitude QNH'),
               descents=S('Descent')):
        pass


class Airspeed5000To3000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               descent=S('Descent')):
        pass


class Airspeed5000To3000FtMaxQNH(KeyPointValueNode):
    name = 'Airspeed 5000 To 3000 Ft Max QNH'

    def derive(self,
               air_spd=P('Airspeed'),
               alt_qnh=P('Altitude QNH'),
               descents=S('Descent')):
        pass


class Airspeed3000To1000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class Airspeed3000To1000FtMaxQNH(KeyPointValueNode):
    name = 'Airspeed 3000 To 1000 Ft Max QNH'

    def derive(self,
               air_spd=P('Airspeed'),
               alt_qnh=P('Altitude QNH'),
               descents=S('Descent')):
        pass


class Airspeed1000To500FtMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Airspeed']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.extend(['Altitude AAL For Flight Phases', 'Final Approach'])
        return all_of(required, available)

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               final_app=S('Final Approach'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descending'),
               ac_type=A('Aircraft Type')):
        pass


class Airspeed1000To500FtMin(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               final_app=S('Final Approach')):
        pass


class Airspeed500To20FtMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Airspeed']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descent'])
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent'),
               ac_type=A('Aircraft Type')):
        pass


class Airspeed500To20FtMin(KeyPointValueNode):

    def derive(self, air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class Airspeed500To50FtMedian(KeyPointValueNode):

    def derive(self, air_spd=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class Airspeed500To50FtMedianMinusAirspeedSelected(KeyPointValueNode):

    def derive(self, spd_selected=P('Airspeed Selected'),
               spds_500_to_50=KPV('Airspeed 500 To 50 Ft Median')):
        pass


class AirspeedAtTouchdown(KeyPointValueNode):

    def derive(self, air_spd=P('Airspeed'), touchdowns=KTI('Touchdown')):
        pass


class AirspeedMinsToTouchdown(KeyPointValueNode):
    NAME_VALUES = MinsToTouchdown.NAME_VALUES

    def derive(self,
               air_spd=P('Airspeed'),
               mtt_kti=KTI('Mins To Touchdown')):
        pass


class AirspeedNMToThreshold(KeyPointValueNode):
    NAME_VALUES = DistanceFromThreshold.NAME_VALUES

    def derive(self,
               air_spd=P('Airspeed'),
               dtt_kti=KTI('Distance From Threshold')):
        pass


class AirspeedAtAPUpperModesEngaged(KeyPointValueNode):
    name = 'Airspeed At AP Upper Modes Engaged'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'),
                    family=A('Family')):
        is_s92 = ac_type == helicopter and family and family.value == 'S92'
        return is_s92 and all_deps(cls, available)

    def derive(self,
               air_spd=P('Airspeed'),
               ap_1_hdg=M('AP (1) Heading Selected Mode Engaged'),
               ap_2_hdg=M('AP (2) Heading Selected Mode Engaged'),
               ap_1_alt=M('AP (1) Altitude Preselect Mode Engaged'),
               ap_2_alt=M('AP (2) Altitude Preselect Mode Engaged'),
               ap_1_vrt=M('AP (1) Vertical Speed Mode Engaged'),
               ap_2_vrt=M('AP (2) Vertical Speed Mode Engaged'),
               ap_1_air=M('AP (1) Airspeed Mode Engaged'),
               ap_2_air=M('AP (2) Airspeed Mode Engaged'),
               climb=S('Initial Climb')):
        pass


class AirspeedTrueAtTouchdown(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed True'),
               touchdowns=KTI('Touchdown')):
        pass


class AirspeedReferenceVariationMax(KeyPointValueNode):

    def derive(self,
               spd_ref_rec=P('Airspeed Reference'),
               spd_ref_tbl=P('Airspeed Reference Lookup'),
               apps=S('Approach And Landing')):
        pass


class V2VariationMax(KeyPointValueNode):

    def derive(self,
               v2_rec=P('V2'),
               v2_tbl=P('V2 Lookup')):
        pass


class V2AtLiftoff(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, afr_v2=A('AFR V2'),
                    manufacturer=A('Manufacturer')):
        '''
        Some other aircraft types record multiple parameters in the same location
        within data frames. We need to select only the data that we are interested
        in, i.e. the V2 values.
        Reference was made to the following documentation to assist with the
        development of this algorithm:
        - A320 Flight Profile Specification
        - A321 Flight Profile Specification
        '''
        afr = all_of((
            'AFR V2',
            'Liftoff',
        ), available) and afr_v2 and afr_v2.value >= AIRSPEED_THRESHOLD
        airbus = all_of((
            'Airspeed Selected',
            'Liftoff',
            'Manufacturer',
        ), available) and manufacturer and manufacturer.value == 'Airbus'
        embraer = all_of((
            'V2-Vac',
            'Liftoff',
        ), available)
        v2 = all_of((
            'V2',
            'Liftoff',
        ), available)
        return v2 or afr or airbus or embraer

    def derive(self,
               v2=P('V2'),
               v2_vac=A('V2-Vac'),
               spd_sel=P('Airspeed Selected'),
               afr_v2=A('AFR V2'),
               liftoffs=KTI('Liftoff'),
               manufacturer=A('Manufacturer')):
        pass


class V2LookupAtLiftoff(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family'),
                    engine_series=A('Engine Series'), engine_type=A('Engine Type')):
        core = all_of((
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
               weight_liftoffs=KPV('Gross Weight At Liftoff'),
               liftoffs=KTI('Liftoff'),
               climb_starts=KTI('Climb Start'),
               model=A('Model'),
               series=A('Series'),
               family=A('Family'),
               engine_type=A('Engine Type'),
               engine_series=A('Engine Series')):
        pass


class AirspeedSelectedAtLiftoff(KeyPointValueNode):

    def derive(self,
               spd_sel=P('Airspeed Selected'),
               liftoffs=KTI('Liftoff'),
               accel_starts=KTI('Takeoff Acceleration Start'),
               climb_starts=KTI('Climb Start')):
        pass


class AirspeedSelectedAtTakeoffAccelerationStart(KeyPointValueNode):

    def derive(self,
               spd_sel=P('Airspeed Selected'),
               accel_starts=KTI('Takeoff Acceleration Start'),
               liftoffs=KTI('Liftoff')):
        pass


class AirspeedMinusV2AtLiftoff(KeyPointValueNode):
    name = 'Airspeed Minus V2 At Liftoff'

    def derive(self,
               spd_v2=P('Airspeed Minus V2'),
               liftoffs=KTI('Liftoff')):
        pass


class AirspeedMinusV2At35FtDuringTakeoff(KeyPointValueNode):
    name = 'Airspeed Minus V2 At 35 Ft During Takeoff'

    def derive(self,
               spd_v2=P('Airspeed Minus V2'),
               takeoffs=S('Takeoff')):
        pass


class AirspeedMinusV235ToClimbAccelerationStartMin(KeyPointValueNode):
    name = 'Airspeed Minus V2 35 To Climb Acceleration Start Min'

    def derive(self,
               spd_v2=P('Airspeed Minus V2'),
               climbs=S('Initial Climb'),
               climb_accel_start=KTI('Climb Acceleration Start')):
        pass


class AirspeedMinusV235ToClimbAccelerationStartMax(KeyPointValueNode):
    name = 'Airspeed Minus V2 35 To Climb Acceleration Start Max'

    def derive(self,
               spd_v2=P('Airspeed Minus V2'),
               climbs=S('Initial Climb'),
               climb_accel_start=KTI('Climb Acceleration Start')):
        pass


class AirspeedMinusV2For3Sec35ToClimbAccelerationStartMin(KeyPointValueNode):
    name = 'Airspeed Minus V2 For 3 Sec 35 To Climb Acceleration Start Min'

    def derive(self,
               spd_v2=P('Airspeed Minus V2 For 3 Sec'),
               climbs=S('Initial Climb'),
               climb_accel_start=KTI('Climb Acceleration Start')):
        pass


class AirspeedMinusV2For3Sec35ToClimbAccelerationStartMax(KeyPointValueNode):
    name = 'Airspeed Minus V2 For 3 Sec 35 To Climb Acceleration Start Max'

    def derive(self,
               spd_v2=P('Airspeed Minus V2 For 3 Sec'),
               climbs=S('Initial Climb'),
               climb_accel_start=KTI('Climb Acceleration Start')):
        pass


class AirspeedMinusV235To1000FtMax(KeyPointValueNode):
    name = 'Airspeed Minus V2 35 To 1000 Ft Max'

    def derive(self,
               spd_v2=P('Airspeed Minus V2'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AirspeedMinusV235To1000FtMin(KeyPointValueNode):
    name = 'Airspeed Minus V2 35 To 1000 Ft Min'

    def derive(self,
               spd_v2=P('Airspeed Minus V2'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AirspeedMinusV2For3Sec35To1000FtMax(KeyPointValueNode):
    name = 'Airspeed Minus V2 For 3 Sec 35 To 1000 Ft Max'

    def derive(self,
               spd_v2=P('Airspeed Minus V2 For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedMinusV2For3Sec35To1000FtMin(KeyPointValueNode):
    name = 'Airspeed Minus V2 For 3 Sec 35 To 1000 Ft Min'

    def derive(self,
               spd_v2=P('Airspeed Minus V2 For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedMinusMinimumAirspeedAbove10000FtMin(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed Minus Minimum Airspeed'),
               alt_std=P('Altitude STD Smoothed')):
        pass


class AirspeedMinusMinimumAirspeed35To10000FtMin(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed Minus Minimum Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_std=P('Altitude STD Smoothed'),
               init_climbs=S('Initial Climb'),
               climbs=S('Climb')):
        pass


class AirspeedMinusMinimumAirspeed10000To50FtMin(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed Minus Minimum Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_std=P('Altitude STD Smoothed'),
               descents=S('Descent')):
        pass


class AirspeedMinusMinimumAirspeedDuringGoAroundMin(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed Minus Minimum Airspeed'),
               phases=S('Go Around And Climbout')):
        pass


class AirspeedMinusAirspeedSelectedFor3Sec500To20FtMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Altitude AAL For Flight Phases', 'HDF Duration'),
                      available) and \
               any_of(('Airspeed Minus Airspeed Selected For 3 Sec',
                       'Airspeed Minus Airspeed Selected (FMS) For 3 Sec'),
                      available)

    def derive(self,
               spd_sel=P('Airspeed Minus Airspeed Selected For 3 Sec'),
               spd_fms=P('Airspeed Minus Airspeed Selected (FMS) For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedMinusAirspeedSelectedFor3Sec500To20FtMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Altitude AAL For Flight Phases', 'HDF Duration'),
                      available) and \
               any_of(('Airspeed Minus Airspeed Selected For 3 Sec',
                       'Airspeed Minus Airspeed Selected (FMS) For 3 Sec'),
                      available)

    def derive(self,
               spd_sel=P('Airspeed Minus Airspeed Selected For 3 Sec'),
               spd_fms=P('Airspeed Minus Airspeed Selected (FMS) For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedMinusAirspeedSelectedFor3Sec1000To500FtMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Altitude AAL For Flight Phases', 'HDF Duration'),
                      available) and \
               any_of(('Airspeed Minus Airspeed Selected For 3 Sec',
                       'Airspeed Minus Airspeed Selected (FMS) For 3 Sec'),
                      available)

    def derive(self,
               spd_sel=P('Airspeed Minus Airspeed Selected For 3 Sec'),
               spd_fms=P('Airspeed Minus Airspeed Selected (FMS) For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedMinusAirspeedSelectedFor3Sec1000To500FtMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Altitude AAL For Flight Phases', 'HDF Duration'),
                      available) and \
               any_of(('Airspeed Minus Airspeed Selected For 3 Sec',
                       'Airspeed Minus Airspeed Selected (FMS) For 3 Sec'),
                      available)

    def derive(self,
               spd_sel=P('Airspeed Minus Airspeed Selected For 3 Sec'),
               spd_fms=P('Airspeed Minus Airspeed Selected (FMS) For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedRelativeAtTouchdown(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative'),
               touchdowns=KTI('Touchdown')):
        pass


class AirspeedRelative1000To500FtMax(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AirspeedRelative1000To500FtMin(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AirspeedRelative500To20FtMax(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AirspeedRelative500To20FtMin(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AirspeedRelative20FtToTouchdownMax(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               touchdowns=KTI('Touchdown')):
        pass


class AirspeedRelative20FtToTouchdownMin(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               touchdowns=KTI('Touchdown')):
        pass


class AirspeedRelativeFor3Sec1000To500FtMax(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedRelativeFor3Sec1000To500FtMin(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedRelativeFor3Sec500To20FtMax(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedRelativeFor3Sec500To20FtMin(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedRelativeFor3Sec20FtToTouchdownMax(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               touchdowns=KTI('Touchdown'),
               duration=A('HDF Duration')):
        pass


class AirspeedRelativeFor3Sec20FtToTouchdownMin(KeyPointValueNode):

    def derive(self,
               spd_rel=P('Airspeed Relative For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               touchdowns=KTI('Touchdown'),
               duration=A('HDF Duration')):
        pass


class AirspeedMinusVLSAtTouchdown(KeyPointValueNode):
    name = 'Airspeed Minus VLS At Touchdown'

    def derive(self,
               spd_rel=P('Airspeed Minus VLS'),
               touchdowns=KTI('Touchdown')):
        pass


class AirspeedMinusVLS1000To500FtMax(KeyPointValueNode):
    name = 'Airspeed Minus VLS 1000 To 500 Ft Max'

    def derive(self,
               spd_rel=P('Airspeed Minus VLS'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AirspeedMinusVLS1000To500FtMin(KeyPointValueNode):
    name = 'Airspeed Minus VLS 1000 To 500 Ft Min'

    def derive(self,
               spd_rel=P('Airspeed Minus VLS'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AirspeedMinusVLS500To20FtMax(KeyPointValueNode):
    name = 'Airspeed Minus VLS 500 To 20 Ft Max'

    def derive(self,
               spd_rel=P('Airspeed Minus VLS'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AirspeedMinusVLS500To20FtMin(KeyPointValueNode):
    name = 'Airspeed Minus VLS 500 To 20 Ft Min'

    def derive(self,
               spd_rel=P('Airspeed Minus VLS'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AirspeedMinusVLSFor3Sec1000To500FtMax(KeyPointValueNode):
    name = 'Airspeed Minus VLS For 3 Sec 1000 To 500 Ft Max'

    def derive(self,
               spd_rel=P('Airspeed Minus VLS For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedMinusVLSFor3Sec1000To500FtMin(KeyPointValueNode):
    name = 'Airspeed Minus VLS For 3 Sec 1000 To 500 Ft Min'

    def derive(self,
               spd_rel=P('Airspeed Minus VLS For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedMinusVLSFor3Sec500To20FtMax(KeyPointValueNode):
    name = 'Airspeed Minus VLS For 3 Sec 500 To 20 Ft Max'

    def derive(self,
               spd_rel=P('Airspeed Minus VLS For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedMinusVLSFor3Sec500To20FtMin(KeyPointValueNode):
    name = 'Airspeed Minus VLS For 3 Sec 500 To 20 Ft Min'

    def derive(self,
               spd_rel=P('Airspeed Minus VLS For 3 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class AirspeedWithFlapMax(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_LEVER.copy()

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
            'Flap Including Transition',
            'Flap Excluding Transition',
        ), available) and all_of(('Airspeed', 'Fast'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               flap_inc_trans=M('Flap Including Transition'),
               flap_exc_trans=M('Flap Excluding Transition'),
               scope=S('Fast'),
               #
               #
               ):
        pass


class AirspeedWithFlapMin(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_LEVER

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Airspeed', 'Airborne'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               scope=S('Airborne')):
        pass


class AirspeedWithFlapAndSlatExtendedMax(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = {
        'parameter': [
            'Flap Including Transition',
            'Flap Excluding Transition',
        ],
        'flap': ['0'],
    }

    @classmethod
    def can_operate(cls, available):
        exc = all_of((
            'Flap Excluding Transition',
            'Slat Excluding Transition',
        ), available)
        inc = all_of((
            'Flap Including Transition',
            'Slat Including Transition',
        ), available)
        return (exc or inc) and all_of(('Airspeed', 'Fast'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               flap_exc_trsn=M('Flap Excluding Transition'),
               flap_inc_trsn=M('Flap Including Transition'),
               slat_exc_trsn=M('Slat Excluding Transition'),
               slat_inc_trsn=M('Slat Including Transition'),
               fast=S('Fast')):
        pass


class AirspeedWithFlapIncludingTransition20AndSlatFullyExtendedMax(KeyPointValueNode, FlapOrConfigurationMaxOrMin):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        slat_only_transition = family and family.value in ('B777',
                                                           'B787')
        inc = all_of((
            'Flap Including Transition',
            'Slat Including Transition',
            'Airspeed',
            'Fast'
        ), available)
        return slat_only_transition and inc

    def derive(self,
               airspeed=P('Airspeed'),
               flap=M('Flap Including Transition'),
               slat=M('Slat Including Transition'),
               fast=S('Fast'),
               family=A('Family'),
               series=A('Series')):
        pass


class AirspeedWithFlapDuringClimbMax(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_LEVER.copy()

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
            'Flap Including Transition',
            'Flap Excluding Transition',
        ), available) and all_of(('Airspeed', 'Climb'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               flap_inc_trans=M('Flap Including Transition'),
               flap_exc_trans=M('Flap Excluding Transition'),
               scope=S('Climb')):
        pass


class AirspeedWithFlapDuringClimbMin(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_LEVER

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Airspeed', 'Climb'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               scope=S('Climb')):
        pass


class AirspeedWithFlapDuringDescentMax(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_LEVER.copy()

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
            'Flap Including Transition',
            'Flap Excluding Transition',
        ), available) and all_of(('Airspeed', 'Descent'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               flap_inc_trans=M('Flap Including Transition'),
               flap_exc_trans=M('Flap Excluding Transition'),
               scope=S('Descent')):
        pass


class AirspeedWithFlapDuringDescentMin(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_LEVER

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Airspeed', 'Descent To Flare'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               scope=S('Descent To Flare')):
        pass


class AirspeedMinusFlapManoeuvreSpeedWithFlapDuringDescentMin(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_LEVER

    @classmethod
    def can_operate(cls, available):
        core = all_of((
            'Airspeed Minus Flap Manoeuvre Speed',
            'Descent To Flare',
        ), available)
        flap = any_of((
            'Flap Lever',
            'Flap Lever (Synthetic)',
        ), available)
        return core and flap

    def derive(self,
               airspeed=P('Airspeed Minus Flap Manoeuvre Speed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               scope=S('Descent To Flare')):
        pass


class AirspeedAtFirstFlapExtensionWhileAirborne(KeyPointValueNode):

    def derive(self,
               airspeed=P('Airspeed'),
               ff_ext=KTI('First Flap Extension While Airborne')):
        pass


class AirspeedSelectedFMCMinusFlapManoeuvreSpeed1000to5000FtMin(KeyPointValueNode):
    name = 'Airspeed Selected (FMC) Minus Flap Manoeuvre Speed 1000 to 5000 Ft Min'

    def derive(self,
               spd_sel=P('Airspeed Selected (FMC)'),
               flap_spd=P('Flap Manoeuvre Speed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               climbs=S('Climb')):
        pass


class AirspeedWithGearDownMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               gear=M('Gear Down'),
               airs=S('Airborne')):
        pass


class AirspeedWhileGearRetractingMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               gear_ret=S('Gear Retracting')):
        pass


class AirspeedWhileGearExtendingMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               gear_ext=S('Gear Extending')):
        pass


class AirspeedAtGearUpSelection(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               gear_up_sel=KTI('Gear Up Selection')):
        pass


class AirspeedAtGearDownSelection(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               gear_dn_sel=KTI('Gear Down Selection')):
        pass


class MainGearOnGroundToNoseGearOnGroundDuration(KeyPointValueNode):

    def derive(self, gog=P('Gear On Ground'), gogn=P('Gear (N) On Ground'),
               landings=S('Landing')):
        pass


class AirspeedWithConfigurationMax(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_CONF.copy()

    def derive(self,
               airspeed=P('Airspeed'),
               conf=M('Configuration'),
               scope=S('Fast')):
        pass


class AirspeedWithConfiguration1FExcludingTransitionMax(KeyPointValueNode):

    def derive(self,
               airspeed=P('Airspeed'),
               conf=M('Configuration Excluding Transition'),):
        pass


class AirspeedRelativeWithConfigurationDuringDescentMin(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_CONF.copy()

    def derive(self,
               airspeed=P('Airspeed Relative'),
               conf=M('Configuration'),
               scope=S('Descent To Flare')):
        pass


class AirspeedWithSpeedbrakeDeployedMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               spdbrk=P('Speedbrake')):
        pass


class AirspeedWithThrustReversersDeployedMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Airspeed True', 'Thrust Reversers', 'Landing'),
                      available) and \
            any_of(('Eng (*) EPR Max', 'Eng (*) N1 Max'), available)

    def derive(self,
               air_spd=P('Airspeed True'),
               tr=M('Thrust Reversers'),
               eng_epr=P('Eng (*) EPR Max'),
               eng_n1=P('Eng (*) N1 Max'),
               landings=S('Landing')):
        pass


class AirspeedAtThrustReversersSelection(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               tr=M('Thrust Reversers'),
               landings=S('Landing')):
        pass


class GroundspeedWithThrustReversersDeployedAnyPowerMin(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed'),
               tr=M('Thrust Reversers'),):
        pass


class AirspeedVacatingRunway(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed True'),
               off_rwy=KTI('Landing Turn Off Runway')):
        pass


class AirspeedDuringRejectedTakeoffMax(KeyPointValueNode):

    def derive(self, air_spd=P('Airspeed'), rtos=S('Rejected Takeoff')):
        pass


class AirspeedBelow10000FtDuringDescentMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_std=P('Altitude STD Smoothed'),
               alt_qnh=P('Altitude QNH'),
               ldg_apt=A('FDR Landing Airport'),
               descent=S('Descent')):
        pass


class AirspeedTopOfDescentTo10000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_std=P('Altitude STD Smoothed'),
               alt_qnh=P('Altitude QNH'),
               ldg_apt=A('FDR Landing Airport'),
               descent=S('Descent')):
        pass


class AirspeedTopOfDescentTo4000FtMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_std=P('Altitude STD Smoothed'),
               alt_qnh=P('Altitude QNH'),
               ldg_apt=A('FDR Landing Airport'),
               descent=S('Descent')):
        pass


class AirspeedTopOfDescentTo4000FtMin(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               alt_std=P('Altitude STD Smoothed'),
               alt_qnh=P('Altitude QNH'),
               ldg_apt=A('FDR Landing Airport'),
               descent=S('Descent')):
        pass


class AirspeedDuringLevelFlightMax(KeyPointValueNode):

    def derive(self,
               air_spd=P('Airspeed'),
               lvl_flt=S('Level Flight')):
        pass


class AirspeedBetweenFL200AndFL300Max(KeyPointValueNode):
    name = 'Airspeed Between FL200 And FL300 Max'

    def derive(self, air_spd= P('Airspeed'), alt=P('Altitude STD Smoothed')):
        pass


class AirspeedBetweenFL200AndFL300Min(KeyPointValueNode):
    name = 'Airspeed Between FL200 and FL300 Min'

    def derive(self, air_spd= P('Airspeed'), alt=P('Altitude STD Smoothed')):
        pass


class AirspeedAboveFL300Max(KeyPointValueNode):
    name = 'Airspeed Above FL300 Max'

    def derive(self, air_spd= P('Airspeed'), alt=P('Altitude STD Smoothed')):
        pass


class AirspeedAboveFL300Min(KeyPointValueNode):
    name = 'Airspeed Above FL300 Min'

    def derive(self, air_spd= P('Airspeed'), alt=P('Altitude STD Smoothed')):
        pass


class AirspeedAboveStickShakerSpeedMin(KeyPointValueNode):

    def derive(self, ias=P('Airspeed'),
                     stick_shaker_speed=P('Stick Shaker Speed'),
                     airborne=S('Airborne'),):
        pass


class AlphaFloorDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return 'Airborne' in available and any_of(('Alpha Floor', 'FMA AT Information'), available)

    def derive(self,
               alpha_floor=M('Alpha Floor'),
               autothrottle_info=M('FMA AT Information'),
               airs=S('Airborne')):
        pass


class AOADuringGoAroundMax(KeyPointValueNode):
    name = 'AOA During Go Around Max'

    def derive(self,
               aoa=P('AOA'),
               go_arounds=S('Go Around And Climbout')):
        pass


class AOAWithFlapMax(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_LEVER
    name = 'AOA With Flap Max'

    @classmethod
    def can_operate(cls, available):
        '''
        FDS developed this KPV to support the UK CAA Significant Seven programme.
        "Loss of Control. Pitch/Angle of Attack vs stall angles"
        This is an adaptation of the airspeed algorithm, used to determine peak
        AOA vs flap. It may not be possible to obtain stalling angle of attack
        figures to set event thresholds, but a threshold based on in-service data
        may suffice.
        '''
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('AOA', 'Airborne'), available)

    def derive(self,
               aoa=P('AOA'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               scope=S('Airborne')):
        pass


class AOAWithFlapDuringClimbMax(KeyPointValueNode):
    name = 'AOA With Flap During Climb Max'

    @classmethod
    def can_operate(cls, available):
        return (all_of(('AOA', 'Climbing'), available) and
                any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available))

    def derive(self,
               aoa=P('AOA'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               climbs=S('Climbing')):
        pass


class AOAWithFlapDuringDescentMax(KeyPointValueNode):
    name = 'AOA With Flap During Descent Max'

    @classmethod
    def can_operate(cls, available):
        return (all_of(('AOA', 'Descending'), available) and
                any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available))

    def derive(self,
               aoa=P('AOA'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               descends=S('Descending')):
        pass


class AOAAbnormalOperationDuration(KeyPointValueNode):
    name = 'AOA Abnormal Operation Duration'

    def derive(self, aoa_state=M('AOA Abnormal Operation'),
               airborne=S('Airborne'),):
        pass


class AOABelowStickShakerAOAMin(KeyPointValueNode):
    name = 'AOA Below Stick Shaker AOA Min'

    def derive(self, aoa_stick_shaker=P('Stick Shaker AOA'),
               aoa_l=P('AOA (L)'),
               aoa_r=P('AOA (R)'),
               airborne=S('Airborne'),):
        pass


class SensorDifference5SecMaxMixin(object):

    @classmethod
    def can_operate(cls, available):
        sensors = [param for param in cls.get_dependency_names() if param != 'Airborne']
        return ('Airborne' in available and
                any_of(sensors, available))


class AOADifference5SecMax(SensorDifference5SecMaxMixin, KeyPointValueNode):
    name = 'AOA Difference 5 Sec Max'

    def derive(self,
               aoa_l=P('AOA (L)'),
               aoa_r=P('AOA (R)'),
               aoa_1=P('AOA (1)'),
               aoa_2=P('AOA (2)'),
               airs=S('Airborne'),):
        pass


class AirspeedDifference5SecMax(SensorDifference5SecMaxMixin, KeyPointValueNode):
    name = 'Airspeed Difference 5 Sec Max'

    def derive(self,
               ias=P('Airspeed'),
               ias_1=P('Airspeed (1)'),
               ias_2=P('Airspeed (2)'),
               ias_3=P('Airspeed (3)'),
               ias_4=P('Airspeed (4)'),
               airs=S('Airborne'),):
        pass


class AltitudeSTDDifference5SecMax(SensorDifference5SecMaxMixin, KeyPointValueNode):
    name = 'Altitude STD Difference 5 Sec Max'

    def derive(self,
               alt=P('Altitude STD'),
               alt_1=P('Altitude STD (1)'),
               alt_2=P('Altitude STD (2)'),
               alt_3=P('Altitude STD (3)'),
               alt_4=P('Altitude STD (4)'),
               airs=S('Airborne'),):
        pass


class PitchDifference5SecMax(SensorDifference5SecMaxMixin, KeyPointValueNode):
    name = 'Pitch Difference 5 Sec Max'

    def derive(self,
               pitch_1=P('Pitch (1)'),
               pitch_2=P('Pitch (2)'),
               pitch_3=P('Pitch (3)'),
               pitch_4=P('Pitch (4)'),
               pitch_5=P('Pitch (5)'),
               pitch_6=P('Pitch (6)'),
               pitch_7=P('Pitch (7)'),
               pitch_8=P('Pitch (8)'),
               airs=S('Airborne'),):
        pass


class RollDifference5SecMax(SensorDifference5SecMaxMixin, KeyPointValueNode):
    name = 'Roll Difference 5 Sec Max'

    def derive(self,
               roll_1=P('Roll (1)'),
               roll_2=P('Roll (2)'),
               roll_3=P('Roll (3)'),
               roll_4=P('Roll (4)'),
               roll_5=P('Roll (5)'),
               roll_6=P('Roll (6)'),
               roll_7=P('Roll (7)'),
               roll_8=P('Roll (8)'),
               roll_9=P('Roll (9)'),
               airs=S('Airborne'),):
        pass


class HeadingDifference5SecMax(SensorDifference5SecMaxMixin, KeyPointValueNode):
    name = 'Heading Difference 5 Sec Max'

    def derive(self,
               hdg=P('Heading'),
               hdg_1=P('Heading (1)'),
               hdg_2=P('Heading (2)'),
               hdg_3=P('Heading (3)'),
               airs=S('Airborne'),):
        pass


class AOAFlapsUpAPOffMax(KeyPointValueNode):
    name = 'AOA Flaps Up AP Off Max'

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        is_max = 'B737 MAX' in family.value if family else None
        return is_max and all_deps(cls, available)

    def derive(self,
               aoa_l=P('AOA (L)'),
               aoa_r=P('AOA (R)'),
               flap=P('Flap Including Transition'),
               cmd=M('AP Engaged'),
               airborne=S('Airborne'),):
        pass


class AOAStickShakerMinusAOAFlapsUpAPOffMin(KeyPointValueNode):
    name = 'AOA Stick Shaker Minus AOA Flaps Up AP Off Min'

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        is_max = 'B737 MAX' in family.value if family else None
        return is_max and all_deps(cls, available)

    def derive(self, aoa_stick_shaker=P('Stick Shaker AOA'),
               aoa_l=P('AOA (L)'),
               aoa_r=P('AOA (R)'),
               airborne=S('Airborne'),
               flap=P('Flap Including Transition'),
               cmd=M('AP Engaged'),):
        pass


class TrimDownWhileControlColumnUpDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        is_max = 'B737 MAX' in family.value if family else None
        return is_max and all_deps(cls, available)

    def derive(self, cc=P('Control Column'),
               pitch_trim=P('AP Trim Down'),
               airborne=S('Airborne'),):
        pass


class ThrustReversersDeployedDuration(KeyPointValueNode):

    def derive(self, tr=M('Thrust Reversers'), landings=S('Landing')):
        pass


class ThrustReversersDeployedDuringFlightDuration(KeyPointValueNode):

    def derive(self, tr=M('Thrust Reversers'), airs=S('Airborne')):
        pass


class ThrustReversersCancelToEngStopDuration(KeyPointValueNode):

    def derive(self, tr=M('Thrust Reversers'),
               eng_starts=KTI('Eng Start'),
               eng_stops=KTI('Eng Stop')):
        pass


class TouchdownToThrustReversersDeployedDuration(KeyPointValueNode):

    def derive(self,
               tr=M('Thrust Reversers'),
               landings=S('Landing'),
               touchdowns=KTI('Touchdown')):
        pass


class TouchdownToSpoilersDeployedDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Speedbrake Selected', 'Landing', 'Touchdown'), available)

    def derive(self, brake=M('Speedbrake Selected'),
               lands=S('Landing'), tdwns=KTI('Touchdown')):
        pass


class SpoilersDeployedDurationDuringLanding(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Speedbrake Selected', 'Landing'), available)

    def derive(self, brake=M('Speedbrake Selected'), landings=S('Landing')):
        pass


class TrackDeviationFromRunway1000To500Ft(KeyPointValueNode):

    def derive(self,
               track_dev=P('Track Deviation From Runway'),
               alt_aal=P('Altitude AAL')):
        pass


class TrackDeviationFromRunway500To300Ft(KeyPointValueNode):

    def derive(self,
               track_dev=P('Track Deviation From Runway'),
               alt_aal=P('Altitude AAL')):
        pass


class TrackDeviationFromRunway300FtToTouchdown(KeyPointValueNode):

    def derive(self,
               track_dev=P('Track Deviation From Runway'),
               alt_aal=P('Altitude AAL')):
        pass


class TOGASelectedDuringFlightDuration(KeyPointValueNode):
    name = 'TOGA Selected During Flight Not Go Around Duration'

    def derive(self,
               toga=M('Takeoff And Go Around'),
               go_arounds=S('Go Around And Climbout'),
               airborne=S('Airborne')):
        pass


class TOGASelectedDuringGoAroundDuration(KeyPointValueNode):
    name = 'TOGA Selected During Go Around Duration'

    def derive(self, toga=M('Takeoff And Go Around'),
               go_arounds=S('Go Around And Climbout')):
        pass


class LiftoffToClimbPitchDuration(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), lifts=KTI('Liftoff')):
        pass


class BrakeTempDuringTaxiInMax(KeyPointValueNode):

    def derive(self, brakes=P('Brake (*) Temp Max'), taxiin=S('Taxi In')):
        pass


class BrakeTempAfterTouchdownDelta(KeyPointValueNode):

    def derive(self, brakes=P('Brake (*) Temp Avg'), touchdowns=S('Touchdown')):
        pass


class BrakeTempBeforeTakeoffMax(KeyPointValueNode):

    def derive(self, brakes=P('Brake (*) Temp Max'), taxiout=S('Taxi Out'),
               liftoff=KTI('Liftoff')):
        pass


class BrakePressureInTakeoffRollMax(KeyPointValueNode):

    def derive(self, bp=P('Brake Pressure'),
               rolls=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class DelayedBrakingAfterTouchdown(KeyPointValueNode):

    def derive(self,
               lands=S('Landing'),
               gs=P('Groundspeed'),
               tdwns=KTI('Touchdown')):
        pass


class DecelerationAfterTouchdownAvg(KeyPointValueNode):

    def derive(self,
               lands=S('Landing'),
               gs=P('Groundspeed'),
               tdwns=KTI('Touchdown')):
        pass


class AutobrakeRejectedTakeoffNotSetDuringTakeoff(KeyPointValueNode):

    def derive(self,
               ab_rto=M('Autobrake Selected RTO'),
               takeoff=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class AltitudeMax(KeyPointValueNode):

    def derive(self,
               alt_std=P('Altitude STD Smoothed'),
               airborne=S('Airborne')):
        pass


class AltitudeDuringGoAroundMin(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               go_arounds=S('Go Around And Climbout')):
        pass


class HeightAtGoAround(KeyPointValueNode):

    def derive(self,
               alt_rad=P('Altitude Radio'),
               go_arounds=KTI('Go Around')):
        pass


class AltitudeOvershootAtSuspectedLevelBust(KeyPointValueNode):

    def derive(self, alt_std=P('Altitude STD Smoothed'), alt_aal=P('Altitude AAL')):
        pass


class CabinAltitudeWarningDuration(KeyPointValueNode):

    def derive(self,
               cab_warn=M('Cabin Altitude Warning'),
               airborne=S('Airborne')):
        pass


class AltitudeDuringCabinAltitudeWarningMax(KeyPointValueNode):

    def derive(self,
               cab_warn=M('Cabin Altitude Warning'),
               airborne=S('Airborne'),
               alt=P('Altitude STD Smoothed')):
        pass


class CabinAltitudeMax(KeyPointValueNode):

    def derive(self,
               cab_alt=P('Cabin Altitude'),
               airborne=S('Airborne')):
        pass


class AltitudeSTDMax(KeyPointValueNode):
    name = 'Altitude STD Max'

    def derive(self, alt_std=P('Altitude STD')):
        pass


class AltitudeInCruiseAverage(KeyPointValueNode):

    def derive(self, alt_std=P('Altitude STD'), cruises=S('Cruise')):
        pass


class AltitudeWithFlapMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        '''
        The exceedance being detected here is the altitude reached with flaps not
        stowed, hence any flap value greater than zero is applicable and we're not
        really interested (for the purpose of identifying the event) what flap
        setting was reached.
        '''
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Altitude STD Smoothed', 'Airborne'), available)

    def derive(self,
               alt_std=P('Altitude STD Smoothed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class AltitudeAtFlapExtension(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               flaps=KTI('Flap Extension While Airborne')):
        pass


class AltitudeAtFirstFlapExtensionAfterLiftoff(KeyPointValueNode):

    def derive(self, flap_exts=KPV('Altitude At Flap Extension')):
        pass


class AltitudeAtFlapExtensionWithGearDownSelected(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_LEVER

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Altitude AAL', 'Gear Down Selected', 'Airborne'), available)

    def derive(self,
               alt_aal=P('Altitude AAL'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               gear_ext=M('Gear Down Selected'),
               airborne=S('Airborne')):
        pass


class AirspeedAtFlapExtension(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_LEVER

    def derive(self, flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               air_spd=P('Airspeed'),
               airborne=S('Airborne')):
        pass


class AirspeedAtFlapExtensionWithGearDownSelected(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_LEVER

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Airspeed', 'Gear Down Selected', 'Airborne'), available)

    def derive(self,
               air_spd=P('Airspeed'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               gear_ext=M('Gear Down Selected'),
               airborne=S('Airborne')):
        pass


class AltitudeAALCleanConfigurationMin(KeyPointValueNode):
    name = 'Altitude AAL Clean Configuration Min'

    def derive(self,
               alt_rad=P('Altitude AAL'),
               flap=M('Flap'),
               gear_retr=S('Gear Retracted')):
        pass


class AltitudeAtFirstFlapChangeAfterLiftoff(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Flap At Liftoff', 'Altitude AAL', 'Airborne'), available)

    def derive(self,
               alt_aal=P('Altitude AAL'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               flap_liftoff=KPV('Flap At Liftoff'),
               airborne=S('Airborne')):
        pass


class AltitudeAtLastFlapChangeBeforeBottomOfDescent(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(
                ('Altitude AAL', 'Bottom Of Descent','Approach And Landing'),
                available)

    def derive(self,
               alt_aal=P('Altitude AAL'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               bottoms=KTI('Bottom Of Descent'),
               apps=S('Approach And Landing'),
               far=P('Flap Automatic Retraction')):
        pass


class AltitudeAtLastFlapSelectionBeforeTouchdown(KeyPointValueNode):
    NAME_VALUES = {'flap': [15, 30, 35]}

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Altitude AAL', 'Touchdown'), available)

    def derive(self, alt_aal=P('Altitude AAL'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               tdwns=KTI('Touchdown')):
        pass


class AltitudeAtFirstFlapRetractionDuringGoAround(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               flap_rets=KTI('Flap Retraction During Go Around'),
               go_arounds=S('Go Around And Climbout')):
        pass


class AltitudeAtFirstFlapRetraction(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               flap_rets=KTI('Flap Retraction While Airborne')):
        pass


class AltitudeAtLastFlapRetraction(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               flap_rets=KTI('Flap Retraction While Airborne')):
        pass


class AltitudeAtClimbThrustDerateDeselectedDuringClimbBelow33000Ft(KeyPointValueNode):

    def derive(self, alt_aal=P('Altitude AAL'),
               derate_deselecteds=KTI('Climb Thrust Derate Deselected'),
               climbs=S('Climbing')):
        pass


class AltitudeAtClimbThrustDerateSelection(KeyPointValueNode):

    def derive(self, alt_aal=P('Altitude AAL'),
               tmc=M('Takeoff Mode (TMC) Operation'),
               airborne=S('Airborne'),):
        pass


class AltitudeAtLastGearDownSelection(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               gear_dn_sel=KTI('Gear Down Selection')):
        pass


class AltitudeAtGearDownSelectionWithFlapDown(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        '''
        Inclusion of the "...WithFlap" term is intended to exclude data points
        where only the gear is down (these are exceptional occasions where gear
        has been extended with flaps up to burn extra fuel).
        '''
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Altitude AAL', 'Gear Down Selection'), available)

    def derive(self,
               alt_aal=P('Altitude AAL'),
               gear_downs=KTI('Gear Down Selection'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)')):
        pass


class AltitudeAtFirstGearUpSelection(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               gear_up_sel=KTI('Gear Up Selection')):
        pass


class AltitudeAtGearUpSelectionDuringGoAround(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               go_arounds=S('Go Around And Climbout'),
               gear_up_sel=KTI('Gear Up Selection During Go Around')):
        pass


class AltitudeWithGearDownMax(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               gear=M('Gear Down'),
               airs=S('Airborne')):
        pass


class AltitudeSTDWithGearDownMax(KeyPointValueNode):
    name = 'Altitude STD With Gear Down Max'

    def derive(self,
               alt_std=P('Altitude STD Smoothed'),
               gear=M('Gear Down'),
               airs=S('Airborne')):
        pass


class AltitudeAtGearDownSelectionWithFlapUp(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Altitude AAL', 'Gear Down Selection'), available)

    def derive(self,
               alt_aal=P('Altitude AAL'),
               gear_downs=KTI('Gear Down Selection'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)')):
        pass


class AltitudeWithGearUpBeforeBottomOfDescentMin(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               gear_downs=KTI('Gear Down Selection'),
               bottom_descents=KTI('Bottom Of Descent')):
        pass


class AltitudeAtAPEngagedSelection(KeyPointValueNode):
    name = 'Altitude At AP Engaged Selection'

    def derive(self,
               alt_aal=P('Altitude AAL'),
               ap_eng=KTI('AP Engaged Selection')):
        pass


class AltitudeAtAPDisengagedSelection(KeyPointValueNode):
    name = 'Altitude At AP Disengaged Selection'

    def derive(self,
               alt_aal=P('Altitude AAL'),
               ap_dis=KTI('AP Disengaged Selection')):
        pass


class AltitudeAtATEngagedSelection(KeyPointValueNode):
    name = 'Altitude At AT Engaged Selection'

    def derive(self,
               alt_aal=P('Altitude AAL'),
               at_eng=KTI('AT Engaged Selection')):
        pass


class AltitudeAtATDisengagedSelection(KeyPointValueNode):
    name = 'Altitude At AT Disengaged Selection'

    def derive(self,
               alt_aal=P('Altitude AAL'),
               at_dis=KTI('AT Disengaged Selection')):
        pass


class AltitudeAtFirstAPEngagedAfterLiftoff(KeyPointValueNode):
    name = 'Altitude At First AP Engaged After Liftoff'

    def derive(self,
               ap=KTI('AP Engaged'),
               alt_aal=P('Altitude AAL'),
               airborne=S('Airborne')):
        pass


class ATEngagedAPDisengagedOutsideClimbDuration(KeyPointValueNode):
    name = 'AT Engaged AP Disengaged Outside Climb Duration'

    @classmethod
    def can_operate(cls, available, ac_family=A('Family')):
        '''
        Autothrottle Use
        ================
        Autothrottle use is recommended during takeoff and climb in either automatic or
        manual flight. During all other phases of flight, autothrottle use is recommended
        only when the autopilot is engaged in CMD.
        FCTM B737NG - AFDS guidelines 1.35
        Uses custom 300fpm climb criteria
        '''
        if ac_family and ac_family.value in ('B737 NG', 'B747', 'B757', 'B767'):
            return all_deps(cls, available)
        else:
            return False

    def derive(self,
               at_engaged=M('AT Engaged'),
               ap_engaged=M('AP Engaged'),
               vert_spd=P('Vertical Speed For Flight Phases'),
               airborne=S('Airborne'),
               takeoff=S('Takeoff')):
        pass


class AltitudeAtMachMax(KeyPointValueNode):

    def derive(self,
               alt_std=P('Altitude STD Smoothed'),
               max_mach=KPV('Mach Max')):
        pass


class HeightAtDistancesFromThreshold(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_RANGES

    def derive(self, alt = P('Altitude AAL'),
               dist_ktis = KTI('Distance From Threshold')):
        pass


class HeightAtOffsetILSTurn(KeyPointValueNode):
    name = 'Height At Offset ILS Turn'

    def derive(self, alt= P('Altitude AAL'),
               apps=App('Approach Information')):
        pass


class HeightAtRunwayChange(KeyPointValueNode):
    name = 'Height At Runway Change'

    def derive(self, alt= P('Altitude AAL'),
               apps=App('Approach Information')):
        pass


class HeightSelectedOnApproachMin(KeyPointValueNode):

    def derive(self, alt_mcp=P('Altitude Selected (MCP)'),
               apps=App('Approach Information')):
        pass


class QNHDifferenceDuringApproach(KeyPointValueNode):
    name = 'QNH Difference During Approach'

    def derive(self, alt_qnh=P('Altitude QNH'),
               alt_aal=P('Altitude AAL'),
               apps=App('Approach Information')):
        pass


class QNHDifferenceDuringTakeoff(KeyPointValueNode):
    name = 'QNH Difference During Takeoff'

    def derive(self, alt_qnh=P('Altitude QNH'),
               alt_aal=P('Altitude AAL'),
               takeoffs=S('Takeoff'),
               to_runway=A('FDR Takeoff Runway')):
        pass


class BaroCorrectionMinus1013Above20000FtDuringLevelFlightMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Altitude STD', 'Level Flight'), available)

    def derive(self, baro=P('Baro Correction'),
               alt_std=P('Altitude STD'),
               level=S('Level Flight'),
               baro_sel=M('Baro Setting Selection'),
               baro_sel_cpt=M('Baro Setting Selection (Capt)'),
               baro_sel_fo=M('Baro Setting Selection (FO)'),
               baro_cor_isis=P('Baro Correction (ISIS)'),
               manufacturer=A('Manufacturer')):
        pass


class BaroDifferenceDuration(KeyPointValueNode):

    def derive(self, baro_diff=S('Baro Difference')):
        pass


class AltitudeFirstStableDuringLastApproach(KeyPointValueNode):

    def derive(self, stable=M('Stable Approach'), alt=P('Altitude AAL')):
        pass


class AltitudeFirstStableDuringApproachBeforeGoAround(KeyPointValueNode):

    def derive(self, stable=M('Stable Approach'), alt=P('Altitude AAL')):
        pass


class AltitudeLastUnstableDuringLastApproach(KeyPointValueNode):

    def derive(self, stable=M('Stable Approach'), alt=P('Altitude AAL')):
        pass


class AltitudeLastUnstableDuringLastApproachExcludingEngThrust(KeyPointValueNode):

    def derive(self, stable=M('Stable Approach Excluding Eng Thrust'),
               alt=P('Altitude AAL')):
        pass


class AltitudeLastUnstableDuringApproachBeforeGoAround(KeyPointValueNode):

    def derive(self, stable=M('Stable Approach'), alt=P('Altitude AAL')):
        pass


class LastUnstableStateDuringLastApproach(KeyPointValueNode):

    def derive(self, stable=M('Stable Approach')):
        pass


class LastUnstableStateDuringApproachBeforeGoAround(KeyPointValueNode):

    def derive(self, stable=M('Stable Approach')):
        pass


class PercentApproachStable(KeyPointValueNode):
    NAME_VALUES = {
        'altitude': (1000, 500),
        'approach': ('During Last Approach', 'During Approach Before Go Around'),
    }

    def derive(self, stable=M('Stable Approach'), alt=P('Altitude AAL')):
        pass


class AltitudeAtLastAPDisengagedDuringApproach(KeyPointValueNode):
    name = 'Altitude At Last AP Disengaged During Approach'

    def derive(self,
               alt_aal=P('Altitude AAL'),
               ap_dis=KTI('AP Disengaged Selection'),
               apps=App('Approach Information')):
        pass


class APDisengagedDuringCruiseDuration(KeyPointValueNode):
    name = 'AP Disengaged During Cruise Duration'

    def derive(self, ap=M('AP Engaged'), cruise=S('Cruise')):
        pass


class ATDisengagedAPEngagedDuration(KeyPointValueNode):
    name = 'AT Disengaged AP Engaged Duration'

    @classmethod
    def can_operate(cls, available, ac_family=A('Family')):
        if ac_family and ac_family.value in ('B737 NG', 'B747', 'B757', 'B767'):
            return all_deps(cls, available)
        else:
            return False

    def derive(self,
               at_engaged=M('AT Engaged'),
               ap_engaged=M('AP Engaged'),
               airborne=S('Airborne'),):
        pass


class NumberOfAPChannelsEngagedAtTouchdown(KeyPointValueNode):
    name = 'Number of AP Channels Engaged At Touchdown'

    @classmethod
    def can_operate(cls, available):
        ap = any_of(['AP Engaged', 'AP Channels Engaged'], available)
        return ap and 'Touchdown' in available

    def derive(self,
               ap_engaged=P('AP Engaged'),
               ap_ch_count=P('AP Channels Engaged'),
               tdwn=KTI('Touchdown')):
        pass


class ControlColumnStiffness(KeyPointValueNode):

    def derive(self,
               force=P('Control Column Force'),
               disp=P('Control Column'),
               fast=S('Fast')):
        pass


class ControlColumnForceMax(KeyPointValueNode):

    def derive(self,
               force=P('Control Column Force'),
               fast=S('Airborne')):
        pass


class ControlWheelForceMax(KeyPointValueNode):

    def derive(self,
               force=P('Control Wheel Force'),
               fast=S('Airborne')):
        pass


class ElevatorPreflightCheck(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, model=A('Model'), series=A('Series'), family=A('Family')):
        if not (all_of(('Elevator', 'Takeoff Acceleration Start', 'Model', 'Series', 'Family'), available) and
                any_of(('First Eng Start Before Liftoff', 'Last APU Start Before Liftoff'), available)):
            return False
        try:
            at.get_elevator_range(model.value, series.value, family.value)
        except KeyError:
            cls.warning("No Elevator range available for '%s', '%s', '%s'.", model.value, series.value, family.value)
            return False
        return True

    def derive(self, disp=P('Elevator'),
               eng_firsts=KTI('First Eng Start Before Liftoff'),
               apu_lasts=KTI('Last APU Start Before Liftoff'),
               accels=KTI('Takeoff Acceleration Start'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class AileronPreflightCheck(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, model=A('Model'), series=A('Series'), family=A('Family')):
        if not (all_of(('Aileron', 'Takeoff Acceleration Start', 'Model', 'Series', 'Family'), available) and
                any_of(('First Eng Start Before Liftoff', 'Last APU Start Before Liftoff'), available)):
            return False
        try:
            at.get_aileron_range(model.value, series.value, family.value)
        except KeyError:
            cls.warning("No Aileron range available for '%s', '%s', '%s'.", model.value, series.value, family.value)
            return False
        return True

    def derive(self, disp=P('Aileron'),
               eng_firsts=KTI('First Eng Start Before Liftoff'),
               apu_lasts=KTI('Last APU Start Before Liftoff'),
               accels=KTI('Takeoff Acceleration Start'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class RudderPreflightCheck(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, model=A('Model'), series=A('Series'), family=A('Family')):
        if not (all_of(('Rudder', 'Takeoff Acceleration Start', 'Model', 'Series', 'Family'), available) and
                any_of(('First Eng Start Before Liftoff', 'Last APU Start Before Liftoff'), available)):
            return False
        try:
            at.get_rudder_range(model.value, series.value, family.value)
        except KeyError:
            cls.warning("No Rudder range available for '%s', '%s', '%s'.", model.value, series.value, family.value)
            return False
        return True

    def derive(self, disp=P('Rudder'),
               eng_firsts=KTI('First Eng Start Before Liftoff'),
               apu_lasts=KTI('Last APU Start Before Liftoff'),
               accels=KTI('Takeoff Acceleration Start'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class FlightControlPreflightCheck(KeyPointValueNode):

    def derive(self, elevator=KPV('Elevator Preflight Check'),
               aileron=KPV('Aileron Preflight Check'),
               rudder=KPV('Rudder Preflight Check')):
        pass


class GreatCircleDistance(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        toff = all_of(('Latitude Smoothed At Liftoff', 'Longitude Smoothed At Liftoff'), available) \
            or 'FDR Takeoff Airport' in available
        ldg = all_of(('Latitude Smoothed At Touchdown', 'Longitude Smoothed At Touchdown'), available) \
            or 'FDR Landing Airport' in available
        return toff and ldg and 'Touchdown' in available

    def derive(self,
               lat_lift=KPV('Latitude Smoothed At Liftoff'),
               lon_lift=KPV('Longitude Smoothed At Liftoff'),
               toff_airport=A('FDR Takeoff Airport'),
               lat_tdwn=KPV('Latitude Smoothed At Touchdown'),
               lon_tdwn=KPV('Longitude Smoothed At Touchdown'),
               ldg_airport=A('FDR Landing Airport'),
               tdwn=KTI('Touchdown')):
        pass


class DistanceTravelledDuringTurnback(KeyPointValueNode):

    def derive(self, gspd=P('Groundspeed'), toff_airport=A('FDR Takeoff Airport'),
               ldg_airport=A('FDR Landing Airport'),
               loffs=KTI('Liftoff'), tdowns=KTI('Touchdown')):
        pass


class DistanceTravelledFollowingDiversion(KeyPointValueNode):

    def derive(self, gspd=P('Groundspeed'), destination=P('Destination'),
               loff=KTI('Liftoff'), tdwn=KTI('Touchdown')):
        pass


class DistanceFromLiftoffToRunwayEnd(KeyPointValueNode):

    def derive(self,
               lat_lift=KPV('Latitude Smoothed At Liftoff'),
               lon_lift=KPV('Longitude Smoothed At Liftoff'),
               rwy=A('FDR Takeoff Runway')):
        pass


class DistanceFromRotationToRunwayEnd(KeyPointValueNode):

    def derive(self,
               lat=P('Latitude Smoothed'),
               lon=P('Longitude Smoothed'),
               rwy=A('FDR Takeoff Runway'),
               toff_rolls=S('Takeoff Roll')):
        pass


class DecelerationToAbortTakeoffAtRotation(KeyPointValueNode):

    def derive(self,
               lat=P('Latitude Smoothed'),
               lon=P('Longitude Smoothed'),
               gspd=P('Groundspeed'),
               aspd=P('Airspeed True'),
               rwy=A('FDR Takeoff Runway'),
               toff_rolls=S('Takeoff Roll')):
        pass


class DistancePastGlideslopeAntennaToTouchdown(KeyPointValueNode):

    def derive(self,
               lat_tdn=KPV('Latitude Smoothed At Touchdown'),
               lon_tdn=KPV('Longitude Smoothed At Touchdown'),
               tdwns=KTI('Touchdown'), rwy=A('FDR Landing Runway'),
               ils_ldgs=S('ILS Localizer Established')):
        pass


class DistanceFromRunwayStartToTouchdown(KeyPointValueNode):

    def derive(self, lat_tdn=KPV('Latitude Smoothed At Touchdown'),
               lon_tdn=KPV('Longitude Smoothed At Touchdown'),
               tdwns=KTI('Touchdown'),
               rwy=A('FDR Landing Runway')):
        pass


class DistanceFromTouchdownToRunwayEnd(KeyPointValueNode):

    def derive(self, lat_tdn=KPV('Latitude Smoothed At Touchdown'),
               lon_tdn=KPV('Longitude Smoothed At Touchdown'),
               tdwns=KTI('Touchdown'),
               rwy=A('FDR Landing Runway')):
        pass


class DecelerationFromTouchdownToStopOnRunway(KeyPointValueNode):

    def derive(self,
               gspd=P('Groundspeed'),
               tdwns=S('Touchdown'),
               landings=S('Landing'),
               lat_tdn=KPV('Latitude Smoothed At Touchdown'),
               lon_tdn=KPV('Longitude Smoothed At Touchdown'),
               rwy=A('FDR Landing Runway'),
               ils_gs_apps=S('ILS Glideslope Established'),
               ils_loc_apps=S('ILS Localizer Established'),
               precise=A('Precise Positioning')):
        pass


class DistanceFromRunwayCentrelineAtTouchdown(KeyPointValueNode):
    name = 'Distance From Runway Centreline At Touchdown'

    def derive(self,
               lat_dist=P('ILS Lateral Distance'),
               tdwns=KTI('Touchdown')):
        pass


class DistanceFromRunwayCentrelineFromTouchdownTo60KtMax(KeyPointValueNode):
    name = 'Distance From Runway Centreline From Touchdown To 60 Kt Max'

    def derive(self,
               lat_dist=P('ILS Lateral Distance'),
               lands=S('Landing'),
               gspd=P('Groundspeed'),
               tdwns=KTI('Touchdown')):
        pass


class RunwayHeadingTrue(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('FDR Takeoff Runway', 'Liftoff'), available) \
            or 'Approach Information' in available

    def derive(self,
               takeoff_runway=A('FDR Takeoff Runway'),
               liftoffs=KTI('Liftoff'),
               apps=App('Approach Information')):
        pass


class RunwayOverrunWithoutSlowingDuration(KeyPointValueNode):

    def derive(self,
               gspd=P('Groundspeed'),
               tdwns=S('Touchdown'),
               landings=S('Landing'),
               lat=P('Latitude Smoothed'),
               lon=P('Longitude Smoothed'),
               lat_tdn=KPV('Latitude Smoothed At Touchdown'),
               lon_tdn=KPV('Longitude Smoothed At Touchdown'),
               rwy=A('FDR Landing Runway'),
               ils_gs_apps=S('ILS Glideslope Established'),
               ils_loc_apps=S('ILS Localizer Established'),
               precise=A('Precise Positioning'),
               turnoff=KTI('Landing Turn Off Runway')):
        pass


class DistanceOnLandingFrom60KtToRunwayEnd(KeyPointValueNode):
    name = 'Distance On Landing From 60 Kt To Runway End'

    def derive(self,
               gspd=P('Groundspeed'),
               lat=P('Latitude Smoothed'),
               lon=P('Longitude Smoothed'),
               tdwns=KTI('Touchdown'),
               rwy=A('FDR Landing Runway')):
        pass


class HeadingDuringTakeoff(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type and ac_type.value == 'helicopter':
            return all_of(('Heading Continuous', 'Transition Hover To Flight', 'Aircraft Type'), available)
        else:
            return all_of(('Heading Continuous', 'Takeoff Roll Or Rejected Takeoff'), available)

    def derive(self,
               hdg=P('Heading Continuous'),
               takeoffs=S('Takeoff Roll Or Rejected Takeoff'),
               ac_type=A('Aircraft Type'),
               toff_helos=S('Transition Hover To Flight')):
        pass


class HeadingTrueDuringTakeoff(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type and ac_type.value == 'helicopter':
            return all_of(('Heading True Continuous', 'Transition Hover To Flight', 'Aircraft Type'), available)
        else:
            return all_of(('Heading True Continuous', 'Takeoff Roll Or Rejected Takeoff'), available)

    def derive(self,
               hdg_true=P('Heading True Continuous'),
               toff_aeros=S('Takeoff Roll Or Rejected Takeoff'),
               ac_type=A('Aircraft Type'),
               toff_helos=S('Transition Hover To Flight')):
        pass


class HeadingDuringLanding(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type and ac_type.value == 'helicopter':
            return all_of(('Heading Continuous', 'Transition Flight To Hover', 'Aircraft Type'), available)
        else:
            return all_of(('Heading Continuous', 'Landing Roll'), available)

    def derive(self,
               hdg=P('Heading Continuous'),
               land_aeros=S('Landing Roll'),
               ac_type=A('Aircraft Type'),
               land_helos=S('Transition Flight To Hover')):
        pass


class HeadingTrueDuringLanding(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type and ac_type.value == 'helicopter':
            return all_of(('Heading True Continuous', 'Transition Flight To Hover', 'Aircraft Type'), available)
        else:
            return all_of(('Heading True Continuous', 'Landing Roll'), available)

    def derive(self,
               hdg=P('Heading True Continuous'),
               land_aeros=S('Landing Roll'),
               ac_type=A('Aircraft Type'),
               land_helos=S('Transition Flight To Hover')):
        pass


class HeadingAtLowestAltitudeDuringApproach(KeyPointValueNode):

    def derive(self,
               hdg=P('Heading Continuous'),
               low_points=KTI('Lowest Altitude During Approach')):
        pass


class HeadingChange(KeyPointValueNode):

    def derive(self,
               hdg=P('Heading Continuous'),
               turns=S('Turning In Air')):
        pass


class ElevatorDuringLandingMin(KeyPointValueNode):

    def derive(self, elev=P('Elevator'), landing=S('Landing')):
        pass


class HeightLossLiftoffTo35Ft(KeyPointValueNode):

    def derive(self,
               vs=P('Vertical Speed Inertial'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class HeightLoss35To1000Ft(KeyPointValueNode):

    def derive(self,
               ht_loss=P('Descend For Flight Phases'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               init_climb=S('Initial Climb')):
        pass


class HeightLoss1000To2000Ft(KeyPointValueNode):

    def derive(self,
               ht_loss=P('Descend For Flight Phases'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               climbs=S('Climb')):
        pass


class ApproachFlightPathAngle1500To1000FtMax(KeyPointValueNode):

    def derive(self, angle=P('Approach Flight Path Angle'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class ApproachFlightPathAngle1500To1000FtMin(KeyPointValueNode):

    def derive(self, angle=P('Approach Flight Path Angle'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class ApproachFlightPathAngle1000To500FtMax(KeyPointValueNode):

    def derive(self, angle=P('Approach Flight Path Angle'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class ApproachFlightPathAngle1000To500FtMin(KeyPointValueNode):

    def derive(self, angle=P('Approach Flight Path Angle'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class ApproachFlightPathAngle500To200FtMax(KeyPointValueNode):

    def derive(self, angle=P('Approach Flight Path Angle'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class ApproachFlightPathAngle500To200FtMin(KeyPointValueNode):

    def derive(self, angle=P('Approach Flight Path Angle'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class ILSFrequencyDuringApproach(KeyPointValueNode):
    name = 'ILS Frequency During Approach'

    def derive(self, apps=A('Approach Information')):
        pass


class ILSGlideslopeDeviation1500To1000FtMax(KeyPointValueNode):
    name = 'ILS Glideslope Deviation 1500 To 1000 Ft Max'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['ILS Glideslope', 'ILS Glideslope Established']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               ils_glideslope=P('ILS Glideslope'),
               ils_ests=S('ILS Glideslope Established'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descending'),
               ac_type=A('Aircraft Type')):
        pass


class ILSGlideslopeDeviation1000To500FtMax(KeyPointValueNode):
    name = 'ILS Glideslope Deviation 1000 To 500 Ft Max'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['ILS Glideslope', 'ILS Glideslope Established']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               ils_glideslope=P('ILS Glideslope'),
               ils_ests=S('ILS Glideslope Established'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descending'),
               ac_type=A('Aircraft Type')):
        pass


class ILSGlideslopeDeviation500To200FtMax(KeyPointValueNode):
    name = 'ILS Glideslope Deviation 500 To 200 Ft Max'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['ILS Glideslope', 'ILS Glideslope Established']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               ils_glideslope=P('ILS Glideslope'),
               ils_ests=S('ILS Glideslope Established'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descending'),
               ac_type=A('Aircraft Type')):
        pass


class ILSGlideslopeNotEstablishedHighestAltitude1000To200Ft(KeyPointValueNode):
    name = 'ILS Glideslope Not Established Highest Altitude 1000 To 200Ft'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type and ac_type.value == 'helicopter':
            return all_of(('Altitude AGL','ILS Glideslope', 'ILS Localizer'), available)
        else:
            return all_of(('Altitude AAL For Flight Phases', 'ILS Glideslope', 'ILS Localizer'), available)

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               ac_type=A('Aircraft Type'),
               approach=S('Approach'),
               ils_gs=P('ILS Glideslope'),
               ils_loc=P('ILS Localizer')):
        pass


class ILSGlideslopeNotEstablishedHighestAltitude500To200Ft(KeyPointValueNode):
    name = 'ILS Glideslope Not Established Highest Altitude 500 To 200 Ft'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type and ac_type.value == 'helicopter':
            return all_of(('Altitude AGL','ILS Glideslope', 'ILS Localizer'), available)
        else:
            return all_of(('Altitude AAL For Flight Phases', 'ILS Glideslope', 'ILS Localizer'), available)

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               ac_type=A('Aircraft Type'),
               approach=S('Approach'),
               ils_gs=P('ILS Glideslope'),
               ils_loc=P('ILS Localizer')):
        pass


class ILSLocalizerNotEstablishedHighestAltitude1000To200Ft(KeyPointValueNode):
    name = 'ILS Localizer Not Established Highest Altitude 1000 To 200 Ft'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type and ac_type.value == 'helicopter':
            return all_of(('Altitude AGL','ILS Localizer'), available)
        else:
            return all_of(('Altitude AAL For Flight Phases', 'ILS Localizer'), available)

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               ac_type=A('Aircraft Type'),
               approach=S('Approach'),
               ils_loc=P('ILS Localizer')):
        pass


class ILSLocalizerNotEstablishedHighestAltitude500To200Ft(KeyPointValueNode):
    name = 'ILS Localizer Not Established Highest Altitude 500 To 200 Ft'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type and ac_type.value == 'helicopter':
            return all_of(('Altitude AGL','ILS Localizer'), available)
        else:
            return all_of(('Altitude AAL For Flight Phases', 'ILS Localizer'), available)

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               ac_type=A('Aircraft Type'),
               approach=S('Approach'),
               ils_loc=P('ILS Localizer'),
               ils_loc_ests=S('ILS Localizer Established')):
        pass


class ILSLocalizerDeviation1500To1000FtMax(KeyPointValueNode):
    name = 'ILS Localizer Deviation 1500 To 1000 Ft Max'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['ILS Localizer', 'ILS Localizer Established']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               ils_localizer=P('ILS Localizer'),
               ils_ests=S('ILS Localizer Established'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descending'),
               ac_type=A('Aircraft Type')):
        pass


class ILSGlideslope10SecBeforeEstablished(KeyPointValueNode):
    name = 'ILS Glideslope 10 Sec Before Established'

    def derive(self,
               ils_glideslope=P('ILS Glideslope'),
               ils_established=S('ILS Glideslope Established')):
        pass


class ILSLocalizerDeviation1000To500FtMax(KeyPointValueNode):
    name = 'ILS Localizer Deviation 1000 To 500 Ft Max'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['ILS Localizer', 'ILS Localizer Established']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               ils_localizer=P('ILS Localizer'),
               ils_ests=S('ILS Localizer Established'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descending'),
               ac_type=A('Aircraft Type')):
        pass


class ILSLocalizerDeviation500To200FtMax(KeyPointValueNode):
    name = 'ILS Localizer Deviation 500 To 200 Ft Max'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['ILS Localizer', 'ILS Localizer Established']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               ils_localizer=P('ILS Localizer'),
               ils_ests=S('ILS Localizer Established'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descending'),
               ac_type=A('Aircraft Type')):
        pass


class ILSLocalizerDeviationAtTouchdown(KeyPointValueNode):
    name = 'ILS Localizer Deviation At Touchdown'

    def derive(self,
               ils_localizer=P('ILS Localizer'),
               ils_ests=S('ILS Localizer Established'),
               tdwns=KTI('Touchdown')):
        pass


class IANGlidepathDeviationMax(KeyPointValueNode):
    NAME_VALUES = {
        'max_alt': (1500, 1000, 500),
        'min_alt': (1000, 500, 200),
    }
    name = 'IAN Glidepath Deviation'

    def derive(self,
               ian_glidepath=P('IAN Glidepath'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               ian_est=S('IAN Glidepath Established')):
        pass


class IANFinalApproachCourseDeviationMax(KeyPointValueNode):
    NAME_VALUES = {
        'max_alt': (1500, 1000, 500),
        'min_alt': (1000, 500, 200),
    }
    name = 'IAN Final Approach Course Deviation'

    def derive(self,
               ian_final=P('IAN Final Approach Course'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               ian_est=S('IAN Final Approach Course Established')):
        pass


class IsolationValveOpenAtLiftoff(KeyPointValueNode):

    def derive(self,
               isol=M('Isolation Valve Open'),
               liftoffs=KTI('Liftoff')):
        pass


class PackValvesOpenAtLiftoff(KeyPointValueNode):

    def derive(self,
               pack=M('Pack Valves Open'),
               liftoffs=KTI('Liftoff')):
        pass


class LatitudeAtTouchdown(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        '''
        The position of the landing is recorded in the form of KPVs as this is
        used in a number of places. From the touchdown moments, the raw latitude
        and longitude data is used to create the *AtTouchdown parameters, and these
        are in turn used to compute the landing attributes.
        Once the landing attributes (especially the runway details) are known,
        the positional data can be smoothed using ILS data or (if this is a
        non-precision approach) the known touchdown aiming point. With more
        accurate positional data the touchdown point can be computed more
        accurately.
        Note: Cannot use smoothed position as this causes circular dependency.
        '''
        return 'Touchdown' in available and any_of(('Latitude',
                                                    'Latitude (Coarse)',
                                                    'AFR Landing Runway',
                                                    'AFR Landing Airport'),
                                                   available)

    def derive(self,
               lat=P('Latitude'),
               tdwns=KTI('Touchdown'),
               land_afr_apt=A('AFR Landing Airport'),
               land_afr_rwy=A('AFR Landing Runway'),
               lat_c=P('Latitude (Coarse)'),
               ac_type=A('Aircraft Type'),
               land_helos=KTI('Enter Transition Flight To Hover')):
        pass


class LongitudeAtTouchdown(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return 'Touchdown' in available and any_of(('Longitude',
                                                    'Longitude (Coarse)',
                                                    'AFR Landing Runway',
                                                    'AFR Landing Airport'),
                                                   available)

    def derive(self,
               lon=P('Longitude'),
               tdwns=KTI('Touchdown'),
               land_afr_apt=A('AFR Landing Airport'),
               land_afr_rwy=A('AFR Landing Runway'),
               lon_c=P('Longitude (Coarse)'),
               ac_type=A('Aircraft Type'),
               land_helos=KTI('Exit Transition Flight To Hover')):
        pass


class LatitudeAtLiftoff(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = 'Exit Transition Hover To Flight' if ac_type and ac_type.value == 'helicopter' else 'Liftoff'
        return required in available and any_of(('Latitude',
                                                  'Latitude (Coarse)',
                                                  'AFR Takeoff Runway',
                                                  'AFR Takeoff Airport'),
                                                 available)

    def derive(self,
               lat=P('Latitude'),
               liftoffs=KTI('Liftoff'),
               toff_afr_apt=A('AFR Takeoff Airport'),
               toff_afr_rwy=A('AFR Takeoff Runway'),
               lat_c=P('Latitude (Coarse)'),
               ac_type=A('Aircraft Type'),
               toff_helos=KTI('Exit Transition Hover To Flight')):
        pass


class LongitudeAtLiftoff(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = 'Liftoff'
        if ac_type and ac_type.value == 'helicopter':
            required = 'Exit Transition Hover To Flight'
        return required in available and any_of(('Longitude',
                                                  'Longitude (Coarse)',
                                                  'AFR Takeoff Runway',
                                                  'AFR Takeoff Airport'),
                                                 available)

    def derive(self,
               lon=P('Longitude'),
               liftoffs=KTI('Liftoff'),
               toff_afr_apt=A('AFR Takeoff Airport'),
               toff_afr_rwy=A('AFR Takeoff Runway'),
               lon_c=P('Longitude (Coarse)'),
               ac_type=A('Aircraft Type'),
               toff_helos=KTI('Exit Transition Hover To Flight')):
        pass


class LatitudeOffBlocks(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return 'Off Blocks' in available and any_of(
            ('Latitude', 'Latitude (Coarse)'), available)

    def derive(self,
               lat=P('Latitude'),
               off_blocks=KTI('Off Blocks'),
               lat_c=P('Latitude (Coarse)')):
        pass


class LongitudeOffBlocks(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return 'Off Blocks' in available and any_of(
            ('Longitude', 'Longitude (Coarse)',), available)

    def derive(self,
               lon=P('Longitude'),
               off_blocks=KTI('Off Blocks'),
               lon_c=P('Longitude (Coarse)')):
        pass


class LatitudeAtTakeoffAccelerationStart(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return 'Takeoff Acceleration Start' in available and any_of(
            ('Latitude', 'Latitude (Coarse)'), available)

    def derive(self,
               lat=P('Latitude'),
               toff_accel=KTI('Takeoff Acceleration Start'),
               lat_c=P('Latitude (Coarse)')):
        pass


class LongitudeAtTakeoffAccelerationStart(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return 'Takeoff Acceleration Start' in available and any_of(
            ('Longitude', 'Longitude (Coarse)',), available)

    def derive(self,
               lon=P('Longitude'),
               toff_accel=KTI('Takeoff Acceleration Start'),
               lon_c=P('Longitude (Coarse)')):
        pass


class LatitudeSmoothedAtTouchdown(KeyPointValueNode):

    def derive(self, lat=P('Latitude Smoothed'), tdwns=KTI('Touchdown')):
        pass


class LongitudeSmoothedAtTouchdown(KeyPointValueNode):

    def derive(self, lon=P('Longitude Smoothed'), tdwns=KTI('Touchdown')):
        pass


class LatitudeSmoothedAtLiftoff(KeyPointValueNode):

    def derive(self, lat=P('Latitude Smoothed'), liftoffs=KTI('Liftoff')):
        pass


class LongitudeSmoothedAtLiftoff(KeyPointValueNode):

    def derive(self, lon=P('Longitude Smoothed'), liftoffs=KTI('Liftoff')):
        pass


class LatitudeAtLowestAltitudeDuringApproach(KeyPointValueNode):

    def derive(self,
               lat=P('Latitude Prepared'),
               low_points=KTI('Lowest Altitude During Approach')):
        pass


class LongitudeAtLowestAltitudeDuringApproach(KeyPointValueNode):

    def derive(self,
               lon=P('Longitude Prepared'),
               low_points=KTI('Lowest Altitude During Approach')):
        pass


class MachMax(KeyPointValueNode):

    def derive(self,
               mach=P('Mach'),
               airs=S('Airborne')):
        pass


class MachDuringCruiseAvg(KeyPointValueNode):

    def derive(self,
               mach=P('Mach'),
               cruises=S('Cruise')):
        pass


class MachBetweenFL200AndFL300Max(KeyPointValueNode):
    name = 'Mach Between FL200 And FL300 Max'

    def derive(self,
               mach=P('Mach'),
               alt=P('Altitude STD Smoothed')):
        pass


class MachBetweenFL200AndFL300Min(KeyPointValueNode):
    name = 'Mach Between FL200 And FL300 Min'

    def derive(self,
               mach=P('Mach'),
               alt=P('Altitude STD Smoothed')):
        pass


class MachAboveFL300Max(KeyPointValueNode):
    name = 'Mach Above FL300 Max'

    def derive(self,
               mach=P('Mach'),
               alt=P('Altitude STD Smoothed')):
        pass


class MachAboveFL300Min(KeyPointValueNode):
    name = 'Mach Above FL300 Min'

    def derive(self,
               mach=P('Mach'),
               alt=P('Altitude STD Smoothed')):
        pass


class MachWithFlapMax(KeyPointValueNode, FlapOrConfigurationMaxOrMin):
    NAME_VALUES = NAME_VALUES_LEVER

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Mach', 'Fast'), available)

    def derive(self,
               mach=P('Mach'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               scope=S('Fast')):
        pass


class MachWithGearDownMax(KeyPointValueNode):

    def derive(self,
               mach=P('Mach'),
               gear=M('Gear Down'),
               airs=S('Airborne')):
        pass


class MachWhileGearRetractingMax(KeyPointValueNode):

    def derive(self,
               mach=P('Mach'),
               gear_ret=S('Gear Retracting')):
        pass


class MachWhileGearExtendingMax(KeyPointValueNode):

    def derive(self,
               mach=P('Mach'),
               gear_ext=S('Gear Extending')):
        pass


class MagneticVariationAtTakeoffTurnOntoRunway(KeyPointValueNode):

    def derive(self,
               mag_var=P('Magnetic Variation'),
               takeoff_turn_on_rwy=KTI('Takeoff Turn Onto Runway')):
        pass


class MagneticVariationAtLandingTurnOffRunway(KeyPointValueNode):

    def derive(self,
               mag_var=P('Magnetic Variation'),
               landing_turn_off_rwy=KTI('Landing Turn Off Runway')):
        pass


class EngGasTempOverThresholdDuration(KeyPointValueNode):
    NAME_VALUES = {'period': ['Takeoff Power', 'MCP', 'Go Around Power']}

    @classmethod
    def can_operate(cls, available, eng_series=A('Engine Series'), eng_type=A('Engine Type'), mods=A('Modifications')):
        try:
            at.get_engine_map(eng_series.value, eng_type.value, mods.value)
        except AttributeError:
            return False
        except KeyError:
            cls.warning("No engine thresholds available for '%s', '%s', '%s'.",
                        eng_series.value, eng_type.value, mods.value)
            return False
        except AttributeError:
            return False
        return any_of((
            'Eng (1) Gas Temp',
            'Eng (2) Gas Temp',
            'Eng (3) Gas Temp',
            'Eng (4) Gas Temp'
        ), available) and any_of((
            'Takeoff 5 Min Rating',
            'Maximum Continuous Power',
            'Go Around 5 Min Rating',
        ), available)

    def derive(self,
               eng1=M('Eng (1) Gas Temp'),
               eng2=M('Eng (2) Gas Temp'),
               eng3=M('Eng (3) Gas Temp'),
               eng4=M('Eng (4) Gas Temp'),
               takeoff=S('Takeoff 5 Min Rating'),
               mcp=S('Maximum Continuous Power'),
               go_around=S('Go Around 5 Min Rating'),
               eng_series=A('Engine Series'),
               eng_type=A('Engine Type'),
               mods=A('Modifications')):
        pass


class EngN1OverThresholdDuration(KeyPointValueNode):
    NAME_VALUES = {'period': ['Takeoff Power', 'MCP', 'Go Around Power']}

    @classmethod
    def can_operate(cls, available, eng_series=A('Engine Series'), eng_type=A('Engine Type'), mods=A('Modifications')):
        try:
            at.get_engine_map(eng_series.value, eng_type.value, mods.value)
        except AttributeError:
            return False
        except KeyError:
            cls.warning("No engine thresholds available for '%s', '%s', '%s'.",
                        eng_series.value, eng_type.value, mods.value)
            return False
        return any_of((
            'Eng (1) N1',
            'Eng (2) N1',
            'Eng (3) N1',
            'Eng (4) N1'
        ), available) and any_of((
            'Takeoff 5 Min Rating',
            'Maximum Continuous Power',
            'Go Around 5 Min Rating',
        ), available)

    def derive(self,
               eng1=M('Eng (1) N1'),
               eng2=M('Eng (2) N1'),
               eng3=M('Eng (3) N1'),
               eng4=M('Eng (4) N1'),
               takeoff=S('Takeoff 5 Min Rating'),
               mcp=S('Maximum Continuous Power'),
               go_around=S('Go Around 5 Min Rating'),
               eng_series=A('Engine Series'),
               eng_type=A('Engine Type'),
               mods=A('Modifications')):
        pass


class EngN2OverThresholdDuration(KeyPointValueNode):
    NAME_VALUES = {'period': ['Takeoff Power', 'MCP', 'Go Around Power']}

    @classmethod
    def can_operate(cls, available, eng_series=A('Engine Series'), eng_type=A('Engine Type'), mods=A('Modifications')):
        try:
            at.get_engine_map(eng_series.value, eng_type.value, mods.value)
        except AttributeError:
            return False
        except KeyError:
            cls.warning("No engine thresholds available for '%s', '%s', '%s'.",
                        eng_series.value, eng_type.value, mods.value)
            return False
        return any_of((
            'Eng (1) N2',
            'Eng (2) N2',
            'Eng (3) N2',
            'Eng (4) N2'
        ), available) and any_of((
            'Takeoff 5 Min Rating',
            'Maximum Continuous Power',
            'Go Around 5 Min Rating',
        ), available)

    def derive(self,
               eng1=M('Eng (1) N2'),
               eng2=M('Eng (2) N2'),
               eng3=M('Eng (3) N2'),
               eng4=M('Eng (4) N2'),
               takeoff=S('Takeoff 5 Min Rating'),
               mcp=S('Maximum Continuous Power'),
               go_around=S('Go Around 5 Min Rating'),
               eng_series=A('Engine Series'),
               eng_type=A('Engine Type'),
               mods=A('Modifications')):
        pass


class EngNpOverThresholdDuration(KeyPointValueNode):
    NAME_VALUES = {'period': ['Takeoff Power', 'MCP', 'Go Around Power']}

    @classmethod
    def can_operate(cls, available, eng_series=A('Engine Series'), eng_type=A('Engine Type'), mods=A('Modifications')):
        try:
            at.get_engine_map(eng_series.value, eng_type.value, mods.value)
        except AttributeError:
            return False
        except KeyError:
            cls.warning("No engine thresholds available for '%s', '%s', '%s'.",
                        eng_series.value, eng_type.value, mods.value)
            return False
        return any_of((
            'Eng (1) Np',
            'Eng (2) Np',
            'Eng (3) Np',
            'Eng (4) Np'
        ), available) and any_of((
            'Takeoff 5 Min Rating',
            'Maximum Continuous Power',
            'Go Around 5 Min Rating',
        ), available)

    def derive(self,
               eng1=M('Eng (1) Np'),
               eng2=M('Eng (2) Np'),
               eng3=M('Eng (3) Np'),
               eng4=M('Eng (4) Np'),
               takeoff=S('Takeoff 5 Min Rating'),
               mcp=S('Maximum Continuous Power'),
               go_around=S('Go Around 5 Min Rating'),
               eng_series=A('Engine Series'),
               eng_type=A('Engine Type'),
               mods=A('Modifications')):
        pass


class EngTorqueOverThresholdDuration(KeyPointValueNode):
    NAME_VALUES = {'period': ['Takeoff Power', 'MCP', 'Go Around Power']}

    @classmethod
    def can_operate(cls, available, eng_series=A('Engine Series'), eng_type=A('Engine Type'),
                    mods=A('Modifications'), ac_type=A('Aircraft Type')):
        try:
            at.get_engine_map(eng_series.value, eng_type.value, mods.value)
        except KeyError:
            cls.warning("No engine thresholds available for '%s', '%s', '%s'.",
                        eng_series.value, eng_type.value, mods.value)
            return False
        except AttributeError:
            return False
        base = any_of((
            'Eng (1) Torque',
            'Eng (2) Torque',
            'Eng (3) Torque',
            'Eng (4) Torque'
        ), available) and any_of((
            'Takeoff 5 Min Rating',
            'Maximum Continuous Power',
            'Go Around 5 Min Rating',
        ), available)
        heli_additions = False if ac_type == helicopter and 'All Engines Operative' not in available else True
        return base and heli_additions

    def derive(self,
               eng1=P('Eng (1) Torque'),
               eng2=P('Eng (2) Torque'),
               eng3=P('Eng (3) Torque'),
               eng4=P('Eng (4) Torque'),
               takeoff=S('Takeoff 5 Min Rating'),
               mcp=S('Maximum Continuous Power'),
               go_around=S('Go Around 5 Min Rating'),
               eng_series=A('Engine Series'),
               eng_type=A('Engine Type'),
               mods=A('Modifications'),
               all_eng=M('All Engines Operative')):
        pass


class EngTorqueLimitExceedanceWithOneEngineInoperativeDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, eng_series=A('Engine Series'), eng_type=A('Engine Type'),
                    mods=A('Modifications'), ac_type=A('Aircraft Type')):
        if ac_type != helicopter:
            return False
        try:
            at.get_engine_map(eng_series.value, eng_type.value, mods.value, restriction='single')
        except KeyError:
            cls.warning("No engine thresholds available for '%s', '%s', '%s'.",
                        eng_series.value, eng_type.value, mods.value)
            return False
        return any_of((
            'Eng (1) Torque',
            'Eng (2) Torque',
            'Eng (3) Torque',
            'Eng (4) Torque'
        ), available) and 'One Engine Inoperative' in available

    def derive(self,
               eng1=M('Eng (1) Torque'),
               eng2=M('Eng (2) Torque'),
               eng3=M('Eng (3) Torque'),
               eng4=M('Eng (4) Torque'),
               one_eng=M('One Engine Inoperative'),
               eng_series=A('Engine Series'),
               eng_type=A('Engine Type'),
               mods=A('Modifications')):
        pass


class EngBleedValvesAtLiftoff(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of((
            'Eng Bleed Open',
            'Liftoff',
        ), available)

    def derive(self,
               bleed=M('Eng Bleed Open'),
               liftoffs=KTI('Liftoff')):
        pass


class EngEPRDuringApproachMax(KeyPointValueNode):
    name = 'Eng EPR During Approach Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               approaches=S('Approach')):
        pass


class EngEPRDuringApproachMin(KeyPointValueNode):
    name = 'Eng EPR During Approach Min'

    def derive(self,
               eng_epr_min=P('Eng (*) EPR Min'),
               approaches=S('Approach')):
        pass


class EngEPRDuringTaxiMax(KeyPointValueNode):
    name = 'Eng EPR During Taxi Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               taxiing=S('Taxiing')):
        pass


class EngEPRDuringTaxiOutMax(KeyPointValueNode):
    name = 'Eng EPR During Taxi Out Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               taxiing=S('Taxi Out')):
        pass


class EngEPRDuringTaxiInMax(KeyPointValueNode):
    name = 'Eng EPR During Taxi In Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               taxiing=S('Taxi In')):
        pass


class EngEPRDuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng EPR During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngEPRFor5SecDuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng EPR For 5 Sec During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngTPRDuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng TPR During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_tpr_limit=P('Eng TPR Limit Difference'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngTPRFor5SecDuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng TPR For 5 Sec During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_tpr_limit=P('Eng TPR Limit Difference'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngEPRDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng EPR During Go Around 5 Min Rating Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngEPRFor5SecDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng EPR For 5 Sec During Go Around 5 Min Rating Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngTPRDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng TPR During Go Around 5 Min Rating Max'

    def derive(self,
               eng_tpr_limit=P('Eng TPR Limit Difference'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngTPRFor5SecDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng TPR For 5 Sec During Go Around 5 Min Rating Max'

    def derive(self,
               eng_tpr_limit=P('Eng TPR Limit Difference'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngEPRDuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng EPR During Maximum Continuous Power Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               mcp=S('Maximum Continuous Power')):
        pass


class EngEPRFor5SecDuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng EPR For 5 Sec During Maximum Continuous Power Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               ratings=S('Maximum Continuous Power')):
        pass


class EngTPRDuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng TPR During Maximum Continuous Power Max'

    def derive(self,
               eng_tpr_max=P('Eng (*) TPR Max'),
               mcp=S('Maximum Continuous Power')):
        pass


class EngTPRFor5SecDuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng TPR For 5 Sec During Maximum Continuous Power Max'

    def derive(self,
               eng_tpr_max=P('Eng (*) TPR Max'),
               ratings=S('Maximum Continuous Power')):
        pass


class EngEPR500To50FtMax(KeyPointValueNode):
    name = 'Eng EPR 500 To 50 Ft Max'

    def derive(self,
               eng_epr_max=P('Eng (*) EPR Max'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class EngEPR500To50FtMin(KeyPointValueNode):
    name = 'Eng EPR 500 To 50 Ft Min'

    def derive(self,
               eng_epr_min=P('Eng (*) EPR Min'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class EngEPRFor5Sec500To50FtMin(KeyPointValueNode):
    name = 'Eng EPR For 5 Sec 500 To 50 Ft Min'

    def derive(self,
               eng_epr_min=P('Eng (*) EPR Min For 5 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class EngEPRFor5Sec1000To500FtMin(KeyPointValueNode):
    name = 'Eng EPR For 5 Sec 1000 To 500 Ft Min'

    def derive(self,
               eng_epr_min=P('Eng (*) EPR Min For 5 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class EngEPRAtTOGADuringTakeoffMax(KeyPointValueNode):
    name = 'Eng EPR At TOGA During Takeoff Max'

    def derive(self,
               toga=M('Takeoff And Go Around'),
               eng_epr_max=P('Eng (*) EPR Max'),
               takeoff=S('Takeoff')):
        pass


class EngTPRAtTOGADuringTakeoffMin(KeyPointValueNode):
    name = 'Eng TPR At TOGA During Takeoff Min'

    def derive(self,
               toga=M('Takeoff And Go Around'),
               eng_tpr_min=P('Eng (*) TPR Min'),
               takeoff=S('Takeoff')):
        pass


class EngEPRExceedEPRRedlineDuration(KeyPointValueNode):
    name = 'Eng EPR Exceeded EPR Redline Duration'

    def derive(self,
               eng_1_epr=P('Eng (1) EPR'),
               eng_1_epr_red=P('Eng (1) EPR Redline'),
               eng_2_epr=P('Eng (2) EPR'),
               eng_2_epr_red=P('Eng (2) EPR Redline'),
               eng_3_epr=P('Eng (3) EPR'),
               eng_3_epr_red=P('Eng (3) EPR Redline'),
               eng_4_epr=P('Eng (4) EPR'),
               eng_4_epr_red=P('Eng (4) EPR Redline')):
        pass


class EngEPRLowDuringTakeoff(KeyPointValueNode):
    name = 'Eng EPR Low During Takeoff'

    def derive(self,
               eng_epr_min=P('Eng (*) EPR Min'),
               takeoff=S('Takeoff'),
               ):
        pass


class EngFireWarningDuration(KeyPointValueNode):

    def derive(self, eng_fire=M('Eng (*) Fire'), airborne=S('Airborne')):
        pass


class APUOnDuringFlightDuration(KeyPointValueNode):
    name = 'APU On During Flight Duration'

    def derive(self,
               apu=P('APU On'),
               airborne=S('Airborne')):
        pass


class APUFireWarningDuration(KeyPointValueNode):
    name = 'APU Fire Warning Duration'

    @classmethod
    def can_operate(cls, available):
        return any_of(
            (
                "APU Fire",
                "Fire APU Single Bottle System",
                "Fire APU Dual Bottle System",
            ),
            available,
        )

    def derive(self, fire=M('APU Fire'),
               single_bottle=M('Fire APU Single Bottle System'),
               dual_bottle=M('Fire APU Dual Bottle System')):
        pass


class EngGasTempDuringTakeoff5MinRatingMax(KeyPointValueNode):

    def derive(self,
               eng_egt_max=P('Eng (*) Gas Temp Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngGasTempFor5SecDuringTakeoff5MinRatingMax(KeyPointValueNode):

    def derive(self,
               eng_egt_max=P('Eng (*) Gas Temp Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngGasTempDuringGoAround5MinRatingMax(KeyPointValueNode):

    def derive(self,
               eng_egt_max=P('Eng (*) Gas Temp Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngGasTempFor5SecDuringGoAround5MinRatingMax(KeyPointValueNode):

    def derive(self,
               eng_egt_max=P('Eng (*) Gas Temp Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngGasTempDuringMaximumContinuousPowerMax(KeyPointValueNode):

    def derive(self,
               eng_egt_max=P('Eng (*) Gas Temp Max'),
               mcp=S('Maximum Continuous Power')):
        pass


class EngGasTempFor5SecDuringMaximumContinuousPowerMax(KeyPointValueNode):

    def derive(self,
               eng_egt_max=P('Eng (*) Gas Temp Max'),
               ratings=S('Maximum Continuous Power')):
        pass


class EngGasTempDuringMaximumContinuousPowerForXMinMax(KeyPointValueNode):
    NAME_VALUES = {'duration': [10, 20, 3, 5],
                   'unit': ['Sec', 'Min']}

    @classmethod
    def can_operate(cls, available):
        return all_of(('Eng (*) Gas Temp Max', 'Takeoff 5 Min Rating', 'Airborne'),
                      available)

    def derive(self,
               eng_egt_max=P('Eng (*) Gas Temp Max'),
               to_ratings=S('Takeoff 5 Min Rating'),
               ga_ratings=S('Go Around 5 Min Rating'),
               airborne=S('Airborne')):
        pass


class EngGasTempMaxDuringTakeoffMaxMaintained(KeyPointValueNode):
    NAME_VALUES = {'durations': ['5 Sec', '10 Sec', '20 Sec', '5 Min']}

    @classmethod
    def can_operate(cls, available):
        return all_of(('Eng (*) Gas Temp Max', 'Takeoff 5 Min Rating'), available)

    def derive(self,
               eng_egt_max=P('Eng (*) Gas Temp Max'),
               takeoffs=S('Takeoff 5 Min Rating'),
               go_arounds=S('Go Around 5 Min Rating')):
        pass


class EngGasTempDuringEngStartMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        egt = any_of(['Eng (1) Gas Temp',
                      'Eng (2) Gas Temp',
                      'Eng (3) Gas Temp',
                      'Eng (4) Gas Temp'], available)
        n3 = any_of(('Eng (1) N3',
                     'Eng (2) N3',
                     'Eng (3) N3',
                     'Eng (4) N3'), available)
        n2 = any_of(('Eng (1) N2',
                     'Eng (2) N2',
                     'Eng (3) N2',
                     'Eng (4) N2'), available)
        n1 = any_of(('Eng (1) N1',
                     'Eng (2) N1',
                     'Eng (3) N1',
                     'Eng (4) N1'), available)
        if ac_type == helicopter:
            return egt and n1
        else:
            return egt and (n3 or n2)

    def derive(self,
               eng_1_egt=P('Eng (1) Gas Temp'),
               eng_2_egt=P('Eng (2) Gas Temp'),
               eng_3_egt=P('Eng (3) Gas Temp'),
               eng_4_egt=P('Eng (4) Gas Temp'),
               eng_1_n3=P('Eng (1) N3'),
               eng_2_n3=P('Eng (2) N3'),
               eng_3_n3=P('Eng (3) N3'),
               eng_4_n3=P('Eng (4) N3'),
               eng_1_n2=P('Eng (1) N2'),
               eng_2_n2=P('Eng (2) N2'),
               eng_3_n2=P('Eng (3) N2'),
               eng_4_n2=P('Eng (4) N2'),
               eng_1_n1=P('Eng (1) N1'),
               eng_2_n1=P('Eng (2) N1'),
               eng_3_n1=P('Eng (3) N1'),
               eng_4_n1=P('Eng (4) N1'),
               eng_starts=KTI('Eng Start'),
               ac_type=A('Aircraft Type')):
        pass


class EngGasTempDuringEngStartForXSecMax(KeyPointValueNode):
    NAME_VALUES = {'seconds': [5, 10, 20, 40]}

    def derive(self,
               eng_egt_max=P('Eng (*) Gas Temp Max'),
               eng_n2_min=P('Eng (*) N2 Min'),
               toff_turn_rwy=KTI('Takeoff Turn Onto Runway')):
        pass


class EngGasTempDuringFlightMin(KeyPointValueNode):

    def derive(self,
               eng_egt_min=P('Eng (*) Gas Temp Min'),
               airborne=S('Airborne')):
        pass


class EngGasTempExceededEngGasTempRedlineDuration(KeyPointValueNode):
    name = 'Eng Gas Temp Exceeded Eng Gas Temp Redline Duration'

    def derive(self,
               eng_1_egt=P('Eng (1) Gas Temp'),
               eng_1_egt_red=P('Eng (1) Gas Temp Redline'),
               eng_2_egt=P('Eng (2) Gas Temp'),
               eng_2_egt_red=P('Eng (2) Gas Temp Redline'),
               eng_3_egt=P('Eng (3) Gas Temp'),
               eng_3_egt_red=P('Eng (3) Gas Temp Redline'),
               eng_4_egt=P('Eng (4) Gas Temp'),
               eng_4_egt_red=P('Eng (4) Gas Temp Redline')):
        pass


class EngGasTempAboveNormalMaxLimitDuringTakeoff5MinRatingDuration(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_ENGINE

    @classmethod
    def can_operate(cls, available, eng_series=A('Engine Series')):
        gas_temps = any_of(('Eng (%d) Gas Temp' % n for n in range(1, 5)), available)
        engine_series = eng_series and eng_series.value == 'CFM56-3'
        return gas_temps and engine_series and 'Takeoff 5 Min Rating' in available

    def derive(self,
               eng1=P('Eng (1) Gas Temp'),
               eng2=P('Eng (2) Gas Temp'),
               eng3=P('Eng (3) Gas Temp'),
               eng4=P('Eng (4) Gas Temp'),
               takeoffs=S('Takeoff 5 Min Rating'),
               eng_series=A('Engine Series')):
        pass


class EngGasTempAboveNormalMaxLimitDuringMaximumContinuousPowerDuration(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_ENGINE

    @classmethod
    def can_operate(cls, available, eng_series=A('Engine Series')):
        gas_temps = any_of(('Eng (%d) Gas Temp' % n for n in range(1, 5)), available)
        engine_series = eng_series and eng_series.value == 'CFM56-3'
        return gas_temps and engine_series and ('Maximum Continous Power' in available)

    def derive(self,
               eng1=P('Eng (1) Gas Temp'),
               eng2=P('Eng (2) Gas Temp'),
               eng3=P('Eng (3) Gas Temp'),
               eng4=P('Eng (4) Gas Temp'),
               mcp=S('Maximum Continous Power')):
        pass


class EngN1DuringTaxiMax(KeyPointValueNode):
    name = 'Eng N1 During Taxi Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               taxi_out=S('Taxi Out'),
               taxi_in=S('Taxi In'),
               taxiing=S('Taxiing')):
        pass


class EngN1DuringTaxiOutMax(KeyPointValueNode):
    name = 'Eng N1 During Taxi Out Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               taxiing=S('Taxi Out')):
        pass


class EngN1DuringTaxiInMax(KeyPointValueNode):
    name = 'Eng N1 During Taxi In Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               taxiing=S('Taxi In')):
        pass


class EngN1DuringApproachMax(KeyPointValueNode):
    name = 'Eng N1 During Approach Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               approaches=S('Approach')):
        pass


class EngN1DuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng N1 During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngN1For5SecDuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng N1 For 5 Sec During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngN1DuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng N1 During Go Around 5 Min Rating Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngN1For5SecDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng N1 For 5 Sec During Go Around 5 Min Rating Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngN1DuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng N1 During Maximum Continuous Power Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               mcp=S('Maximum Continuous Power')):
        pass


class EngN1For5SecDuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng N1 For 5 Sec During Maximum Continuous Power Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               ratings=S('Maximum Continuous Power')):
        pass


class EngAPRDuration(KeyPointValueNode):
    name = 'Eng APR Duration'

    @classmethod
    def can_operate(cls, available):
        return 'Mobile' in available and \
               all_of(('FADEC (L) APR Active',
                       'FADEC (R) APR Active',), available) or \
               all_of(('Eng (1) ATTCS Armed',
                       'Eng (1) ATTCS Enabled',
                       'Eng (1) ATTCS Triggered',
                       'Eng (2) ATTCS Armed',
                       'Eng (2) ATTCS Enabled',
                       'Eng (2) ATTCS Triggered',), available)

    def derive(self,
               mobiles=S('Mobile'),
               eng1_apr=P('FADEC (L) APR Active'),
               eng2_apr=P('FADEC (R) APR Active'),
               eng1_attcs_arm=P('Eng (1) ATTCS Armed'),
               eng1_attcs_enabled=P('Eng (1) ATTCS Enabled'),
               eng1_attcs_trigger=P('Eng (1) ATTCS Triggered'),
               eng2_attcs_arm=P('Eng (2) ATTCS Armed'),
               eng2_attcs_enabled=P('Eng (2) ATTCS Enabled'),
               eng2_attcs_trigger=P('Eng (2) ATTCS Triggered'),):
        pass


class EngN1CyclesDuringFinalApproach(KeyPointValueNode):
    name = 'Eng N1 Cycles During Final Approach'

    def derive(self,
               eng_n1_avg=P('Eng (*) N1 Avg'),
               fin_apps=S('Final Approach')):
        pass


class EngN1500To50FtMax(KeyPointValueNode):
    name = 'Eng N1 500 To 50 Ft Max'

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class EngN1500To50FtMin(KeyPointValueNode):
    name = 'Eng N1 500 To 50 Ft Min'

    def derive(self,
               eng_n1_min=P('Eng (*) N1 Min'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class EngN1For5Sec500To50FtMin(KeyPointValueNode):
    name = 'Eng N1 For 5 Sec 500 To 50 Ft Min'

    @classmethod
    def can_operate(self, available):
        return all_of(('Eng (*) N1 Min', 'Altitude AAL For Flight Phases', 'HDF Duration'), available)

    def derive(self,
               eng_n1_min_param=P('Eng (*) N1 Min'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class EngN1For5Sec1000To500FtMin(KeyPointValueNode):
    name = 'Eng N1 For 5 Sec 1000 To 500 Ft Min'

    def derive(self,
               eng_n1_min=P('Eng (*) N1 Min For 5 Sec'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               duration=A('HDF Duration')):
        pass


class EngN1WithThrustReversersInTransitMax(KeyPointValueNode):
    name = 'Eng N1 With Thrust Reversers In Transit Max'

    def derive(self,
               eng_n1_avg=P('Eng (*) N1 Avg'),
               tr=M('Thrust Reversers'),
               landings=S('Landing')):
        pass


class EngN1WithThrustReversersDeployedMax(KeyPointValueNode):
    name = 'Eng N1 With Thrust Reversers Deployed Max'

    def derive(self,
               eng_n1_avg=P('Eng (*) N1 Avg'),
               tr=M('Thrust Reversers'),
               landings=S('Landing')):
        pass


class EngEngStartToN1At60PercentDuration(KeyPointValueNode):
    NAME_VALUES = {'number': [1, 2, 3, 4]}

    @classmethod
    def can_operate(cls, available):
        eng = any_of(('Eng (1) N1', 'Eng (2) N1', 'Eng (3) N1', 'Eng (4) N1'),
                     available)
        engstart = 'Eng Start' in available
        liftoff = 'Liftoff' in available
        return eng and engstart and liftoff

    def derive(self,
               eng1=P('Eng (1) N1'),
               eng2=P('Eng (2) N1'),
               eng3=P('Eng (3) N1'),
               eng4=P('Eng (4) N1'),
               engstarts=KTI('Eng Start'),
               liftoffs=KTI('Liftoff')):
        pass


class EngN1Below60PercentAfterTouchdownDuration(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_ENGINE

    @classmethod
    def can_operate(cls, available):
        return all((
            any_of(('Eng (%d) N1' % n for n in range(1, 5)), available),
            'Eng Stop' in available,
            'Touchdown' in available,
        ))

    def derive(self,
               engines_stop=KTI('Eng Stop'),
               eng1=P('Eng (1) N1'),
               eng2=P('Eng (2) N1'),
               eng3=P('Eng (3) N1'),
               eng4=P('Eng (4) N1'),
               tdwn=KTI('Touchdown')):
        pass


class EngN1AtTOGADuringTakeoff(KeyPointValueNode):
    name = 'Eng N1 At TOGA During Takeoff'

    def derive(self,
               toga=M('Takeoff And Go Around'),
               eng_n1=P('Eng (*) N1 Min'),
               takeoff=S('Takeoff')):
        pass


class EngN154to72PercentWithThrustReversersDeployedDurationMax(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_ENGINE

    @classmethod
    def can_operate(cls, available, eng_series=A('Engine Series')):
        engine_series = eng_series and eng_series.value == 'Tay 620'
        return all((
            any_of(('Eng (%d) N1' % n for n in cls.NAME_VALUES['number']), available),
            'Thrust Reversers' in available,
            engine_series,
        ))

    def derive(self, eng1_n1=P('Eng (1) N1'), eng2_n1=P('Eng (2) N1'),
               eng3_n1=P('Eng (3) N1'), eng4_n1=P('Eng (4) N1'),
               tr=M('Thrust Reversers'), eng_series=A('Engine Series')):
        pass


class EngNp82To90PercentDurationMax(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_ENGINE

    @classmethod
    def can_operate(cls, available, ac_series=A('Series'),
                       ):
        ac_concerned = ac_series and ac_series.value == 'Jetstream 41'
        return all_of(('Eng (1) Np', 'Eng (2) Np'), available) and ac_concerned

    def derive(self, eng1_np=P('Eng (1) Np'), eng2_np=P('Eng (2) Np')):
        pass


class EngN1ExceededN1RedlineDuration(KeyPointValueNode):
    name = 'Eng N1 Exceeded N1 Redline Duration'

    def derive(self,
               eng_1_n1=P('Eng (1) N1'),
               eng_1_n1_red=P('Eng (1) N1 Redline'),
               eng_2_n1=P('Eng (2) N1'),
               eng_2_n1_red=P('Eng (2) N1 Redline'),
               eng_3_n1=P('Eng (3) N1'),
               eng_3_n1_red=P('Eng (3) N1 Redline'),
               eng_4_n1=P('Eng (4) N1'),
               eng_4_n1_red=P('Eng (4) N1 Redline')):
        pass


class EngN2DuringTaxiMax(KeyPointValueNode):
    name = 'Eng N2 During Taxi Max'

    def derive(self,
               eng_n2_max=P('Eng (*) N2 Max'),
               taxiing=S('Taxiing')):
        pass


class EngN2DuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng N2 During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_n2_max=P('Eng (*) N2 Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngN2For5SecDuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng N2 For 5 Sec During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_n2_max=P('Eng (*) N2 Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngN2DuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng N2 During Go Around 5 Min Rating Max'

    def derive(self,
               eng_n2_max=P('Eng (*) N2 Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngN2For5SecDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng N2 For 5 Sec During Go Around 5 Min Rating Max'

    def derive(self,
               eng_n2_max=P('Eng (*) N2 Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngN2DuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng N2 During Maximum Continuous Power Max'

    def derive(self,
               eng_n2_max=P('Eng (*) N2 Max'),
               mcp=S('Maximum Continuous Power')):
        pass


class EngN2For5SecDuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng N2 For 5 Sec During Maximum Continuous Power Max'

    def derive(self,
               eng_n2_max=P('Eng (*) N2 Max'),
               ratings=S('Maximum Continuous Power')):
        pass


class EngN2CyclesDuringFinalApproach(KeyPointValueNode):
    name = 'Eng N2 Cycles During Final Approach'

    def derive(self,
               eng_n2_avg=P('Eng (*) N2 Avg'),
               fin_apps=S('Final Approach')):
        pass


class EngN2ExceededN2RedlineDuration(KeyPointValueNode):
    name = 'Eng N2 Exceeded N2 Redline Duration'

    def derive(self,
               eng_1_n2=P('Eng (1) N2'),
               eng_1_n2_red=P('Eng (1) N2 Redline'),
               eng_2_n2=P('Eng (2) N2'),
               eng_2_n2_red=P('Eng (2) N2 Redline'),
               eng_3_n2=P('Eng (3) N2'),
               eng_3_n2_red=P('Eng (3) N2 Redline'),
               eng_4_n2=P('Eng (4) N2'),
               eng_4_n2_red=P('Eng (4) N2 Redline')):
        pass


class EngN3DuringTaxiMax(KeyPointValueNode):
    name = 'Eng N3 During Taxi Max'

    def derive(self,
               eng_n3_max=P('Eng (*) N3 Max'),
               taxiing=S('Taxiing')):
        pass


class EngN3DuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng N3 During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_n3_max=P('Eng (*) N3 Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngN3For5SecDuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng N3 For 5 Sec During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_n3_max=P('Eng (*) N3 Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngN3DuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng N3 During Go Around 5 Min Rating Max'

    def derive(self,
               eng_n3_max=P('Eng (*) N3 Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngN3For5SecDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng N3 For 5 Sec During Go Around 5 Min Rating Max'

    def derive(self,
               eng_n3_max=P('Eng (*) N3 Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngN3DuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng N3 During Maximum Continuous Power Max'

    def derive(self,
               eng_n3_max=P('Eng (*) N3 Max'),
               mcp=S('Maximum Continuous Power')):
        pass


class EngN3For5SecDuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng N3 For 5 Sec During Maximum Continuous Power Max'

    def derive(self,
               eng_n3_max=P('Eng (*) N3 Max'),
               ratings=S('Maximum Continuous Power')):
        pass


class EngN3ExceededN3RedlineDuration(KeyPointValueNode):
    name = 'Eng N3 Exceeded N3 Redline Duration'

    def derive(self,
               eng_1_n3=P('Eng (1) N3'),
               eng_1_n3_red=P('Eng (1) N3 Redline'),
               eng_2_n3=P('Eng (2) N3'),
               eng_2_n3_red=P('Eng (2) N3 Redline'),
               eng_3_n3=P('Eng (3) N3'),
               eng_3_n3_red=P('Eng (3) N3 Redline'),
               eng_4_n3=P('Eng (4) N3'),
               eng_4_n3_red=P('Eng (4) N3 Redline')):
        pass


class EngNpDuringClimbMin(KeyPointValueNode):
    name = 'Eng Np During Climb Min'

    def derive(self,
               eng_np_min=P('Eng (*) Np Min'),
               climbs=S('Climbing')):
        pass


class EngNpDuringTaxiMax(KeyPointValueNode):
    name = 'Eng Np During Taxi Max'

    def derive(self,
               eng_np_max=P('Eng (*) Np Max'),
               taxiing=S('Taxiing')):
        pass


class EngNpDuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng Np During Takeoff 5 Min Rating Max'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Eng (*) Np Max', 'Takeoff 5 Min Rating'), available)

    def derive(self,
               eng_np_max=P('Eng (*) Np Max'),
               takeoffs=S('Takeoff 5 Min Rating'),
               go_arounds=S('Go Around 5 Min Rating')):
        pass


class EngNpFor5SecDuringTakeoff5MinRatingMax(KeyPointValueNode):
    name = 'Eng Np For 5 Sec During Takeoff 5 Min Rating Max'

    def derive(self,
               eng_np_max=P('Eng (*) Np Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngNpDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng Np During Go Around 5 Min Rating Max'

    def derive(self,
               eng_np_max=P('Eng (*) Np Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngNpFor5SecDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng Np For 5 Sec During Go Around 5 Min Rating Max'

    def derive(self,
               eng_np_max=P('Eng (*) Np Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngNpDuringMaximumContinuousPowerMax(KeyPointValueNode):
    name = 'Eng Np During Maximum Continuous Power Max'

    def derive(self,
               eng_np_max=P('Eng (*) Np Max'),
               mcp=S('Maximum Continuous Power')):
        pass


class EngNpForXSecDuringMaximumContinuousPowerMax(KeyPointValueNode):
    NAME_VALUES = {'seconds': [5, 20]}

    def derive(self,
               eng_np_max=P('Eng (*) Np Max'),
               ratings=S('Maximum Continuous Power')):
        pass


class ThrottleReductionToTouchdownDuration(KeyPointValueNode):

    def derive(self,
               tla=P('Throttle Levers'),
               landings=S('Landing'),
               touchdowns=KTI('Touchdown'),
               eng_n1=P('Eng (*) N1 Avg'),
               frame=A('Frame')):
        pass


class EngVibBroadbandMax(KeyPointValueNode):

    def derive(self, eng_vib_max=P('Eng (*) Vib Broadband Max'),
               any_running=M('Eng (*) Any Running')):
        pass


class EngOilPressMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return 'Eng (*) Oil Press Max' in available

    def derive(self, oil_press=P('Eng (*) Oil Press Max'),
               taxi_outs=S('Taxi Out'),
               eng_starts=KTI('First Eng Start Before Liftoff'),
               touchdowns=KTI('Touchdown')):
        pass


class EngOilPressFor60SecDuringCruiseMax(KeyPointValueNode):

    def derive(self, oil_press=P('Eng (*) Oil Press Max'),
               cruise=S('Cruise')):
        pass


class EngOilPressMin(KeyPointValueNode):

    def derive(self, oil_press=P('Eng (*) Oil Press Min'),
               airborne=S('Airborne')):
        pass


class EngOilPressWarningDuration(KeyPointValueNode):

    def derive(self,
               oil_press_warn=P('Eng (*) Oil Press Warning'),
               airborne=S('Airborne')):
        pass


class EngOilPressLowRedlineExceededDuration(KeyPointValueNode):

    def derive(self, press_low_1=M('Eng (1) Oil Press Low Redline Exceeded'),
               press_low_2=M('Eng (2) Oil Press Low Redline Exceeded')):
        pass


class EngOilQtyMax(KeyPointValueNode):

    def derive(self,
               oil_qty=P('Eng (*) Oil Qty Max'),
               airborne=S('Airborne')):
        pass


class EngOilQtyMin(KeyPointValueNode):

    def derive(self,
               oil_qty=P('Eng (*) Oil Qty Min'),
               airborne=S('Airborne')):
        pass


class EngOilQtyDuringTaxiInMax(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_ENGINE

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Eng (1) Oil Qty',
            'Eng (2) Oil Qty',
            'Eng (3) Oil Qty',
            'Eng (4) Oil Qty'
        ), available) and 'Taxi In' in available

    def derive(self,
               oil_qty1=P('Eng (1) Oil Qty'),
               oil_qty2=P('Eng (2) Oil Qty'),
               oil_qty3=P('Eng (3) Oil Qty'),
               oil_qty4=P('Eng (4) Oil Qty'),
               taxi_in=S('Taxi In')):
        pass


class EngOilQtyDuringTaxiOutMax(KeyPointValueNode):
    NAME_VALUES = NAME_VALUES_ENGINE

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Eng (1) Oil Qty',
            'Eng (2) Oil Qty',
            'Eng (3) Oil Qty',
            'Eng (4) Oil Qty'
        ), available) and 'Taxi Out' in available

    def derive(self,
               oil_qty1=P('Eng (1) Oil Qty'),
               oil_qty2=P('Eng (2) Oil Qty'),
               oil_qty3=P('Eng (3) Oil Qty'),
               oil_qty4=P('Eng (4) Oil Qty'),
               taxi_out=S('Taxi Out')):
        pass


class EngOilTempMax(KeyPointValueNode):

    def derive(self,
               oil_temp=P('Eng (*) Oil Temp Max'),
               airborne=S('Airborne')):
        pass


class EngOilTempForXMinMax(KeyPointValueNode):
    NAME_VALUES = {'minutes': [15, 20, 45]}
    name = 'Eng Oil Temp For X Min Max'

    def derive(self, oil_temp=P('Eng (*) Oil Temp Max')):
        pass


class EngTorqueDuringTaxiMax(KeyPointValueNode):

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               taxiing=S('Taxiing')):
        pass


class EngTorqueDuringTakeoff5MinRatingMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        heli = ac_type == helicopter and all_of(('Eng (*) Torque Max', 'Takeoff 5 Min Rating', 'All Engines Operative'), available)
        aero = ac_type == aeroplane and all_of(('Eng (*) Torque Max', 'Takeoff 5 Min Rating'), available)
        return heli or aero

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               ratings=S('Takeoff 5 Min Rating'),
               all_eng=M('All Engines Operative')):
        pass


class EngTorqueFor5SecDuringTakeoff5MinRatingMax(KeyPointValueNode):

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               ratings=S('Takeoff 5 Min Rating')):
        pass


class EngTorque65KtsTo35FtMin(KeyPointValueNode):

    def derive(self,
               eng_trq_min=P('Eng (*) Torque Min'),
               airspeed=P('Airspeed'),
               takeoffs=S('Takeoff')):
        pass


class EngTorqueDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng Torque During Go Around 5 Min Rating Max'

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngTorqueFor5SecDuringGoAround5MinRatingMax(KeyPointValueNode):
    name = 'Eng Torque For 5 Sec During Go Around 5 Min Rating Max'

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               ratings=S('Go Around 5 Min Rating')):
        pass


class EngTorqueDuringMaximumContinuousPowerMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        heli = ac_type == helicopter and all_of(('Eng (*) Torque Max', 'Maximum Continuous Power', 'All Engines Operative'), available)
        aero = ac_type == aeroplane and all_of(('Eng (*) Torque Max', 'Maximum Continuous Power'), available)
        return heli or aero

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               mcp=S('Maximum Continuous Power'),
               all_eng=M('All Engines Operative')):
        pass


class EngTorqueFor5SecDuringMaximumContinuousPowerMax(KeyPointValueNode):

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               ratings=S('Maximum Continuous Power')):
        pass


class EngTorque500To50FtMax(KeyPointValueNode):

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class EngTorque500To50FtMin(KeyPointValueNode):

    def derive(self,
               eng_trq_min=P('Eng (*) Torque Min'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class EngTorqueWhileDescendingMax(KeyPointValueNode):

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               descending=S('Descending')):
        pass


class EngTorque7FtToTouchdownMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, eng_type=A('Engine Propulsion')):
        turbo_prop = eng_type and eng_type.value == 'PROP'
        required_params = all_of(['Eng (*) Torque Max',
                                  'Altitude AAL For Flight Phases',
                                  'Touchdown'], available)
        return turbo_prop and required_params

    def derive(self,
               eng_trq_max=P('Eng (*) Torque Max'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               touchdowns=KTI('Touchdown')):
        pass


class EngTorqueWithin1SecOfTouchdownMax(KeyPointValueNode):

    def derive(self,
               tdwns=KTI('Touchdown'),
               torque=P('Eng (*) Torque Max'),):
        pass


class TorqueAsymmetryWhileAirborneMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Torque Asymmetry', 'Airborne'), available)

    def derive(self, torq_asym=P('Torque Asymmetry'), airborne=S('Airborne')):
        pass


class EngVibN1Max(KeyPointValueNode):
    name = 'Eng Vib N1 Max'

    def derive(self,
               eng_vib_n1=P('Eng (*) Vib N1 Max'),
               airborne=S('Airborne')):
        pass


class EngVibN2Max(KeyPointValueNode):
    name = 'Eng Vib N2 Max'

    def derive(self,
               eng_vib_n2=P('Eng (*) Vib N2 Max'),
               airborne=S('Airborne')):
        pass


class EngVibN3Max(KeyPointValueNode):
    name = 'Eng Vib N3 Max'

    def derive(self,
               eng_vib_n3=P('Eng (*) Vib N3 Max'),
               airborne=S('Airborne')):
        pass


class EngVibAMax(KeyPointValueNode):
    name = 'Eng Vib A Max'

    def derive(self,
               eng_vib_a=P('Eng (*) Vib A Max'),
               airborne=S('Airborne')):
        pass


class EngVibBMax(KeyPointValueNode):
    name = 'Eng Vib B Max'

    def derive(self,
               eng_vib_b=P('Eng (*) Vib B Max'),
               airborne=S('Airborne')):
        pass


class EngVibCMax(KeyPointValueNode):
    name = 'Eng Vib C Max'

    def derive(self,
               eng_vib_c=P('Eng (*) Vib C Max'),
               airborne=S('Airborne')):
        pass


class EngVibNpMax(KeyPointValueNode):
    name = 'Eng Vib Np Max'

    def derive(self,
               eng_vib_np=P('Eng (*) Vib Np Max'),
               airborne=S('Airborne')):
        pass


class EngChipDetectorWarningDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        chips = any_of(('Eng (1) Chip Detector',
                        'Eng (2) Chip Detector',
                        'Eng (1) Chip Detector (1)',
                        'Eng (2) Chip Detector (1)',
                        'Eng (1) Chip Detector (2)',
                        'Eng (2) Chip Detector (2)'), available)
        return chips and 'Eng (*) Any Running' in available

    def derive(self,
               eng_1_chip=M('Eng (1) Chip Detector'),
               eng_2_chip=M('Eng (2) Chip Detector'),
               eng_1_chip_1=M('Eng (1) Chip Detector (1)'),
               eng_2_chip_1=M('Eng (2) Chip Detector (1)'),
               eng_1_chip_2=M('Eng (1) Chip Detector (2)'),
               eng_2_chip_2=M('Eng (2) Chip Detector (2)'),
               any_run=M('Eng (*) Any Running')):
        pass


class GearboxChipDetectorWarningDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        chips = any_of(('EGB (1) Chip Detector',
                        'EGB (2) Chip Detector',
                        'MGB Chip Detector',
                        'MGB Front Chip Detector',
                        'MGB Sump Chip Detector',
                        'MGB Epicyclic Chip Detector',
                        'MGB (Fore) Chip Detector',
                        'MGB (Aft) Chip Detector',
                        'IGB Chip Detector',
                        'TGB Chip Detector',
                        'CGB Chip Detector',
                        'Rotor Shaft Chip Detector'), available)
        return chips and 'Eng (*) Any Running' in available

    def derive(self,
               eng_1_chip=M('EGB (1) Chip Detector'),
               eng_2_chip=M('EGB (2) Chip Detector'),
               mgb_chip=M('MGB Chip Detector'),
               mgb_front_chip=M('MGB Front Chip Detector'),
               mgb_sump_chip=M('MGB Sump Chip Detector'),
               mgb_epicyclic_chip=M('MGB Epicyclic Chip Detector'),
               mgb_fore_chip=M('MGB (Fore) Chip Detector'),
               mgb_aft_chip=M('MGB (Aft) Chip Detector'),
               igb_chip=M('IGB Chip Detector'),
               tgb_chip=M('TGB Chip Detector'),
               cgb_chip=M('CGB Chip Detector'),
               rotor_shaft_chip=M('Rotor Shaft Chip Detector'),
               any_run=M('Eng (*) Any Running')):
        pass


class EngShutdownDuringFlightDuration(KeyPointValueNode):

    def derive(self,
               eng_running=P('Eng (*) All Running'),
               airborne=S('Airborne')):
        pass


class EngRunningDuration(KeyPointValueNode):
    NAME_VALUES = {'engnum': [1, 2, 3, 4, '*']}

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, eng1=M('Eng (1) Running'), eng2=M('Eng (2) Running'),
               eng3=M('Eng (3) Running'), eng4=M('Eng (4) Running')):
        pass


class EngStartTimeMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'),
                    family=A('Family')):
        is_phenom = ac_type == aeroplane and family and family.value == 'Phenom 300'
        return is_phenom and all_deps(cls, available)

    def derive(self, eng1_n2=P('Eng (1) N2'), eng2_n2=P('Eng (2) N2'),
               station=S('Stationary'), taxi_out=S('Taxi Out')):
        pass


class SingleEngineDuringTaxiInDuration(KeyPointValueNode):

    def derive(self,
               all_run=M('Eng (*) All Running'),
               any_run=M('Eng (*) Any Running'),
               taxi=S('Taxi In')):
        pass


class SingleEngineDuringTaxiOutDuration(KeyPointValueNode):

    def derive(self,
               all_run=M('Eng (*) All Running'),
               any_run=M('Eng (*) Any Running'),
               taxi=S('Taxi Out')):
        pass


class EventMarkerPressed(KeyPointValueNode):

    def derive(self, event=P('Event Marker'), airs=S('Airborne')):
        pass


class HeightOfBouncedLanding(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               bounced_ldg=S('Bounced Landing')):
        pass


class HeadingVariationAbove80KtsAirspeedDuringTakeoff(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        heading = any_of(('Heading True Continuous', 'Heading Continuous'), available)
        return ac_type == A('Aircraft Type', 'aeroplane') and \
               heading and all_of(('Airspeed', 'Pitch Rate', 'Takeoff'), available)

    def derive(self,
               nosewheel=P('Gear (N) On Ground'),
               head_true=P('Heading True Continuous'),
               head_mag=P('Heading Continuous'),
               airspeed=P('Airspeed'),
               pitch_rate=P('Pitch Rate'),
               toffs=S('Takeoff')):
        pass


class HeadingDeviationFromRunwayAtTOGADuringTakeoff(KeyPointValueNode):
    name = 'Heading Deviation From Runway At TOGA During Takeoff'

    def derive(self,
               toga=M('Takeoff And Go Around'),
               head=P('Heading True Continuous'),
               takeoff=S('Takeoff'),
               rwy=A('FDR Takeoff Runway')):
        pass


class HeadingDeviationFromRunwayAt50FtDuringLanding(KeyPointValueNode):

    def derive(self,
               head=P('Heading True Continuous'),
               landings=S('Landing'),
               rwy=A('FDR Landing Runway')):
        pass


class HeadingDeviationFromRunwayDuringLandingRoll(KeyPointValueNode):

    def derive(self,
               head=P('Heading True Continuous'),
               land_rolls=S('Landing Roll'),
               rwy=A('FDR Landing Runway')):
        pass


class HeadingVariation300To50Ft(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Heading Continuous']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               head=P('Heading Continuous'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descending'),
               ac_type=A('Aircraft Type')):
        pass


class HeadingVariation500To50Ft(KeyPointValueNode):

    def derive(self,
               head=P('Heading Continuous'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class HeadingVariation800To50Ft(KeyPointValueNode):

    def derive(self,
               head=P('Heading Continuous'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class HeadingVariationAbove100KtsAirspeedDuringLanding(KeyPointValueNode):

    def derive(self,
               head=P('Heading Continuous'),
               airspeed=P('Airspeed'),
               alt=P('Altitude AAL For Flight Phases'),
               lands=S('Landing')):
        pass


class HeadingVariationTouchdownPlus4SecTo60KtsAirspeed(KeyPointValueNode):

    def derive(self,
               head=P('Heading Continuous'),
               airspeed=P('Airspeed True'),
               tdwns=KTI('Touchdown')):
        pass


class HeadingVacatingRunway(KeyPointValueNode):

    def derive(self,
               head=P('Heading Continuous'),
               off_rwys=KTI('Landing Turn Off Runway')):
        pass


class HeadingRateWhileAirborneMax(KeyPointValueNode):

    def derive(self, heading_rate=P('Heading Rate'), airborne=P('Airborne')):
        pass


class HeightMinsToTouchdown(KeyPointValueNode):
    NAME_VALUES = MinsToTouchdown.NAME_VALUES

    def derive(self,
               alt_aal=P('Altitude AAL'),
               mtt_kti=KTI('Mins To Touchdown')):
        pass


class GearExtensionDuration(KeyPointValueNode):

    def derive(self, gear_extending=P('Gear Down In Transit'),):
        pass


class GearRetractionDuration(KeyPointValueNode):

    def derive(self, gear_retracting=P('Gear Up In Transit'),):
        pass


class FlapAtFirstMovementAfterEngineStart(KeyPointValueNode):

    def derive(self, flap=P('Flap Including Transition'), gnd_spd=P('Groundspeed Signed'),
               eng_start=KTI('First Eng Start Before Liftoff'),
               liftoff=KTI('Liftoff')):
        pass


class FlapAtLiftoff(KeyPointValueNode):

    def derive(self, flap=M('Flap'), liftoffs=KTI('Liftoff')):
        pass


class FlapAtTouchdown(KeyPointValueNode):

    def derive(self, flap=M('Flap'), touchdowns=KTI('Touchdown')):
        pass


class FlapAtGearDownSelection(KeyPointValueNode):

    def derive(self, flap=M('Flap'), gear_dn_sel=KTI('Gear Down Selection')):
        pass


class FlapAtGearUpSelectionDuringGoAround(KeyPointValueNode):

    def derive(self, flap=M('Flap'),
               gear_up_sel=KTI('Gear Up Selection During Go Around')):
        pass


class FlapLeverAtGearDownSelection(KeyPointValueNode):

    @classmethod
    def can_operate(cls,
                    available,
                    family=A('Family')):
        embraer = family and family.value in ('ERJ-170/175', 'ERJ-190/195')
        return embraer and ('Flap Lever' in available)

    def derive(self,
               flap_lever=M('Flap Lever'),
               gear_dn_sel=KTI('Gear Down Selection')):
        pass


class FlapLeverAtGearUpSelectionDuringGoAround(KeyPointValueNode):

    @classmethod
    def can_operate(cls,
                    available,
                    family=A('Family')):
        embraer = family and family.value in ('ERJ-170/175', 'ERJ-190/195')
        return embraer and ('Flap Lever' in available)

    def derive(self,
               flap_lever=M('Flap Lever'),
               gear_up_sel=KTI('Gear Up Selection During Go Around')):
        pass


class FlapWithGearUpMax(KeyPointValueNode):

    def derive(self, flap=M('Flap'), gear=M('Gear Down')):
        pass


class FlapWithSpeedbrakeDeployedMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Flap Including Transition', 'Speedbrake Selected',
                      'Airborne', 'Landing'), available) or \
               all_of(('Flap Including Transition', 'Speedbrake Selected',
                      'Airborne', 'Landing', 'Landing Attitude Mode Delta CL'),
                      available)

    def derive(self,
               flap=M('Flap Including Transition'),
               spd_brk=M('Speedbrake Selected'),
               airborne=S('Airborne'),
               landings=S('Landing'),
               lam=P('Landing Attitude Mode Delta CL'),):
        pass


class FlapAt1000Ft(KeyPointValueNode):

    def derive(self, flap=M('Flap'), gates=KTI('Altitude When Descending')):
        pass


class FlapAt500Ft(KeyPointValueNode):

    def derive(self, flap=M('Flap'), gates=KTI('Altitude When Descending')):
        pass


class GearDownToLandingFlapConfigurationDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family'),
                    engine_type=A('Engine Type'), engine_series=A('Engine Series')):
        flap_lever = any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available)
        required = all_of(('Gear Down Selection', 'Approach And Landing'), available)
        attrs = (model, series, family, engine_type, engine_series)
        table = lookup_table(cls, 'vref', *attrs) or lookup_table(cls, 'vapp', *attrs)
        return flap_lever and required and table

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               gear_dn_sel=KTI('Gear Down Selection'),
               approaches=S('Approach And Landing'),
               model=A('Model'), series=A('Series'), family=A('Family'),
               engine_type=A('Engine Type'), engine_series=A('Engine Series')):
        pass


class FlapSynchroAsymmetryMax(KeyPointValueNode):

    def derive(self, synchro=P('Flap Synchro Asymmetry')):
        pass


class FlapBypassValveDuration(KeyPointValueNode):

    def derive(self, valve=P('Flap Bypass Valve Position'),):
        pass


class FlareDuration20FtToTouchdown(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL For Flight Phases'),
               tdowns=KTI('Touchdown'),
               lands=S('Landing'),
               ralt=P('Altitude Radio')):
        pass


class FlareDistance20FtToTouchdown(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL For Flight Phases'),
               tdowns=KTI('Touchdown'),
               lands=S('Landing'),
               gspd=P('Groundspeed')):
        pass


class FuelQtyAtLiftoff(KeyPointValueNode):

    def derive(self,
               fuel_qty=P('Fuel Qty'),
               liftoffs=KTI('Liftoff')):
        pass


class FuelQtyAtTouchdown(KeyPointValueNode):

    def derive(self,
               fuel_qty=P('Fuel Qty'),
               touchdowns=KTI('Touchdown')):
        pass


class FuelQtyWingDifferenceMax(KeyPointValueNode):

    def derive(self, left_wing=P('Fuel Qty (L)'), right_wing=P('Fuel Qty (R)'),
               airbornes=S('Airborne')):
        pass


class FuelQtyWingDifference787Max(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, frame=A('Frame')):
        if frame and frame.value.startswith('787'):
            return all_deps(cls, available)
        else:
            return False

    def derive(self, left_wing=P('Fuel Qty (L)'), right_wing=P('Fuel Qty (R)'),
               airbornes=S('Airborne')):
        pass


class FuelQtyLowWarningDuration(KeyPointValueNode):

    def derive(self, warning=M('Fuel Qty (*) Low'), airborne=S('Airborne')):
        pass


class FuelJettisonDuration(KeyPointValueNode):

    def derive(self,
               jet=P('Fuel Jettison Nozzle'),
               airborne=S('Airborne')):
        pass


class FuelCrossFeedValveStateAtLiftoff(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(['Fuel Cross Feed Valve Position',
                       'Fuel Cross Feed Valve'], available)

    def derive(self, fuel_valve=P('Fuel Cross Feed Valve Position'),
               fuel_valve_fallback=P('Fuel Cross Feed Valve'),
               liftoffs=KTI('Liftoff')):
        pass


class MainFuelQuantityOffBlockWithFuelInCenterTank(KeyPointValueNode):

    def derive(self,
               fuel_l=P('Fuel Qty (L)'),
               fuel_r=P('Fuel Qty (R)'),
               fuel_c=P('Fuel Qty (C)'),
               offblocks=KTI('Off Blocks')):
        pass


class GroundspeedWithGearOnGroundMax(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed Signed'),
               gear=M('Gear On Ground'),
               groundeds=S('Grounded')):
        pass


class GroundspeedWhileTaxiingStraightMax(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed Signed'),
               taxiing=S('Taxiing'),
               turns=S('Turning On Ground')):
        pass


class GroundspeedInStraightLineDuringTaxiInMax(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed Signed'),
               taxiing=S('Taxi In'),
               turns=S('Turning On Ground')):
        pass


class GroundspeedInStraightLineDuringTaxiOutMax(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed Signed'),
               taxiing=S('Taxi Out'),
               turns=S('Turning On Ground')):
        pass


class GroundspeedWhileTaxiingTurnMax(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed Signed'),
               taxiing=S('Taxiing'),
               turns=S('Turning On Ground')):
        pass


class GroundspeedInTurnDuringTaxiOutMax(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed Signed'),
               taxiing=S('Taxi Out'),
               turns=S('Turning On Ground')):
        pass


class GroundspeedInTurnDuringTaxiInMax(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed Signed'),
               taxiing=S('Taxi In'),
               turns=S('Turning On Ground')):
        pass


class GroundspeedDuringRejectedTakeoffMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return 'Rejected Takeoff' in available and any_of(
            ('Acceleration Longitudinal Offset Removed',
             'Groundspeed Signed'), available)

    def derive(self,
               accel=P('Acceleration Longitudinal Offset Removed'),
               gnd_spd=P('Groundspeed Signed'),
               rtos=S('Rejected Takeoff')):
        pass


class GroundspeedAtLiftoff(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed'),
               liftoffs=KTI('Liftoff')):
        pass


class GroundspeedAtTouchdown(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed'),
               touchdowns=KTI('Touchdown')):
        pass


class GroundspeedVacatingRunway(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed Signed'),
               off_rwy=KTI('Landing Turn Off Runway')):
        pass


class GroundspeedAtTOGA(KeyPointValueNode):
    name = 'Groundspeed At TOGA'

    def derive(self,
               toga=M('Takeoff And Go Around'),
               gnd_spd=P('Groundspeed'),
               takeoffs=S('Takeoff')):
        pass


class GroundspeedWithThrustReversersDeployedMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Groundspeed', 'Thrust Reversers', 'Landing'),
                      available) and \
            any_of(('Eng (*) EPR Max', 'Eng (*) N1 Max'), available)

    def derive(self,
               gnd_spd=P('Groundspeed'),
               tr=M('Thrust Reversers'),
               eng_epr=P('Eng (*) EPR Max'),
               eng_n1=P('Eng (*) N1 Max'),
               landings=S('Landing'),
               recorded_n1=P('Eng (1) N1')):
        pass


class GroundspeedStabilizerOutOfTrimDuringTakeoffMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, model=A('Model'), series=A('Series'), family=A('Family')):
        if not all_of(('Groundspeed', 'Stabilizer', 'Takeoff Roll Or Rejected Takeoff', 'Model', 'Series', 'Family'), available):
            return False
        try:
            at.get_stabilizer_limits(model.value, series.value, family.value)
        except KeyError:
            cls.warning("No stabilizer limits available for '%s', '%s', '%s'.",
                        model.value, series.value, family.value)
            return False
        return True

    def derive(self,
               gnd_spd=P('Groundspeed'),
               stab=P('Stabilizer'),
               takeoff_roll=S('Takeoff Roll Or Rejected Takeoff'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class GroundspeedSpeedbrakeHandleDuringTakeoffMax(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed'),
               spdbrk=P('Speedbrake Handle'),
               spdbrk_selected=M('Speedbrake Selected'),
               takeoff_roll=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class GroundspeedSpeedbrakeDuringTakeoffMax(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed'),
               spdbrk=P('Speedbrake'),
               takeoff_roll=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class GroundspeedFlapChangeDuringTakeoffMax(KeyPointValueNode):

    def derive(self,
               gnd_spd=P('Groundspeed'),
               flap=M('Flap'),
               takeoff_roll=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class AlternateLawDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Alternate Law',
            'Pitch Alternate Law',
            'Roll Alternate Law',
        ), available) and 'Airborne' in available

    def derive(self,
               alternate_law=M('Alternate Law'),
               pitch_alternate_law=M('Pitch Alternate Law'),
               roll_alternate_law=M('Roll Alternate Law'),
               airborne=S('Airborne')):
        pass


class DirectLawDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Direct Law',
            'Pitch Direct Law',
            'Roll Direct Law',
        ), available) and 'Airborne' in available

    def derive(self,
               direct_law=M('Direct Law'),
               pitch_direct_law=M('Pitch Direct Law'),
               roll_direct_law=M('Roll Direct Law'),
               airborne=S('Airborne')):
        pass


class PitchAfterFlapRetractionMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Pitch', 'Airborne'), available)

    def derive(self,
               pitch=P('Pitch'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class PitchAtLiftoff(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               liftoffs=KTI('Liftoff')):
        pass


class PitchAtTouchdown(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               touchdowns=KTI('Touchdown')):
        pass


class PitchAt35FtDuringClimb(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL'),
               climbs=S('Initial Climb')):
        pass


class PitchAbove1000FtMin(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), alt=P('Altitude AAL')):
        pass


class PitchAbove1000FtMax(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), alt=P('Altitude AAL')):
        pass


class PitchTakeoffMax(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               takeoffs=S('Takeoff')):
        pass


class Pitch35ToClimbAccelerationStartMin(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               climbs=S('Initial Climb'),
               climb_accel_start=KTI('Climb Acceleration Start')):
        pass


class Pitch35ToClimbAccelerationStartMax(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               climbs=S('Initial Climb'),
               climb_accel_start=KTI('Climb Acceleration Start')):
        pass


class Pitch35To400FtMax(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               climbs=S('Initial Climb')):
        pass


class Pitch35To400FtMin(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               climbs=S('Initial Climb')):
        pass


class Pitch400To1000FtMax(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               climbs=S('Initial Climb')):
        pass


class Pitch400To1000FtMin(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               climbs=S('Initial Climb')):
        pass


class Pitch1000To500FtMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Pitch']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL For Flight Phases', 'Descent'])
        else:
            required.extend(['Altitude AAL For Flight Phases', 'Final Approach'])
        return all_of(required, available)

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fin_app=S('Final Approach'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent'),
               ac_type=A('Aircraft Type')):
        pass


class Pitch1000To500FtMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Pitch']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descent'])
        else:
            required.extend(['Altitude AAL For Flight Phases', 'Final Approach'])
        return all_of(required, available)

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fin_app=S('Final Approach'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descent'),
               ac_type=A('Aircraft Type')):
        pass


class Pitch500To50FtMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Pitch']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.extend(['Altitude AAL For Flight Phases', 'Final Approach'])
        return all_of(required, available)

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fin_app=S('Final Approach'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descending'),
               ac_type=A('Aircraft Type')):
        pass


class Pitch500To50FtMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Pitch']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.extend(['Altitude AAL For Flight Phases', 'Final Approach'])
        return all_of(required, available)

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fin_app=S('Final Approach'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descending'),
               ac_type=A('Aircraft Type')):
        pass


class Pitch500To20FtMin(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class Pitch500To7FtMax(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class Pitch500To7FtMin(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class Pitch50FtToTouchdownMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Pitch', 'Touchdown']
        if ac_type and ac_type.value == 'helicopter':
            required.append('Altitude AGL')
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               pitch=P('Pitch'),
               touchdowns=KTI('Touchdown'),
               ac_type=A('Aircraft Type'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL')):
        pass


class Pitch20FtToTouchdownMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Pitch']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Touchdown'])
        else:
            required.extend(['Altitude AAL For Flight Phases', 'Touchdown'])
        return all_of(required, available)

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               touchdowns=KTI('Touchdown'),
               ac_type=A('Aircraft Type')):
        pass


class Pitch20FtToTouchdownMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Pitch']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Touchdown'])
        else:
            required.extend(['Altitude AAL For Flight Phases', 'Touchdown'])
        return all_of(required, available)

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL'),
               touchdowns=KTI('Touchdown'),
               ac_type=A('Aircraft Type')):
        pass


class Pitch7FtToTouchdownMin(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               touchdowns=KTI('Touchdown')):
        pass


class Pitch7FtToTouchdownMax(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               touchdowns=KTI('Touchdown')):
        pass


class PitchCyclesDuringFinalApproach(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               fin_apps=S('Final Approach')):
        pass


class PitchDuringGoAroundMax(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               go_arounds=S('Go Around And Climbout')):
        pass


class PitchWhileAirborneMax(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), airborne=S('Airborne')):
        pass


class PitchWhileAirborneMin(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), airborne=S('Airborne')):
        pass


class PitchTouchdownTo60KtsAirspeedMax(KeyPointValueNode):

    def derive(self,
               pitch=P('Pitch'),
               airspeed=P('Airspeed'),
               touchdowns=KTI('Touchdown')):
        pass


class PitchBetweenFL200AndFL300Max(KeyPointValueNode):
    name = 'Pitch Between FL200 And FL300 Max'

    def derive(self, pitch=P('Pitch'), alt=P('Altitude STD Smoothed')):
        pass


class PitchBetweenFL200AndFL300Min(KeyPointValueNode):
    name = 'Pitch Between FL200 And FL300 Min'

    def derive(self, pitch=P('Pitch'), alt=P('Altitude STD Smoothed')):
        pass


class PitchAboveFL300Max(KeyPointValueNode):
    name = 'Pitch Above FL300 Max'

    def derive(self, pitch=P('Pitch'), alt=P('Altitude STD Smoothed')):
        pass


class PitchAboveFL300Min(KeyPointValueNode):
    name = 'Pitch Above FL300 Min'

    def derive(self, pitch=P('Pitch'), alt=P('Altitude STD Smoothed')):
        pass


class PitchRateWhileAirborneMax(KeyPointValueNode):

    def derive(self, pitch_rate=P('Pitch Rate'), airborne=S('Airborne')):
        pass


class PitchRate35To1000FtMax(KeyPointValueNode):

    def derive(self,
               pitch_rate=P('Pitch Rate'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class PitchRate35ToClimbAccelerationStartMax(KeyPointValueNode):

    def derive(self,
               pitch_rate=P('Pitch Rate'),
               climbs=S('Initial Climb'),
               climb_accel_start=KTI('Climb Acceleration Start')):
        pass


class PitchRate20FtToTouchdownMax(KeyPointValueNode):

    def derive(self,
               pitch_rate=P('Pitch Rate'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               touchdowns=KTI('Touchdown')):
        pass


class PitchRate20FtToTouchdownMin(KeyPointValueNode):

    def derive(self,
               pitch_rate=P('Pitch Rate'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               touchdowns=KTI('Touchdown')):
        pass


class PitchRate2DegPitchTo35FtMax(KeyPointValueNode):

    def derive(self,
               pitch_rate=P('Pitch Rate'),
               two_deg_pitch_to_35ft=S('2 Deg Pitch To 35 Ft')):
        pass


class PitchRate2DegPitchTo35FtMin(KeyPointValueNode):

    def derive(self,
               pitch_rate=P('Pitch Rate'),
               two_deg_pitch_to_35ft=S('2 Deg Pitch To 35 Ft')):
        pass


class PitchRateTouchdownTo60KtsAirspeedMax(KeyPointValueNode):

    def derive(self, pitchrate=P('Pitch Rate'), airspeed=P('Airspeed'),
               touchdowns=KTI('Touchdown')):
        pass


class RateOfClimbMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               climbing=S('Climbing')):
        pass


class RateOfClimb35ToClimbAccelerationStartMin(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               climbs=S('Initial Climb'),
               climb_accel_start=KTI('Climb Acceleration Start')):
        pass


class RateOfClimb35To1000FtMin(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               climbs=S('Initial Climb')):
        pass


class RateOfClimbBelow10000FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               alt_aal=P('Altitude STD Smoothed'),
               airborne=S('Airborne')):
        pass


class RateOfClimbDuringGoAroundMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               go_arounds=S('Go Around And Climbout')):
        pass


class RateOfClimbAtHeightBeforeLevelFlight(KeyPointValueNode):
    NAME_VALUES = {'altitude': [2000, 1000]}

    def derive(self, vert_spd=P('Vertical Speed'),
               heights=KTI('Altitude Before Level Flight When Climbing')):
        pass


class RateOfClimbAtHeightBeforeAltitudeSelected(KeyPointValueNode):
    NAME_VALUES = {'altitude': [2000, 1000]}

    @classmethod
    def can_operate(cls, available, manufacturer=A('Manufacturer')):
        if manufacturer and manufacturer.value == 'Airbus':
            baro_setting_sel = any((
                any_of(('Baro Setting Selection', 'Baro Correction (ISIS)'), available),
                all_of(('Baro Setting Selection (Capt)', 'Baro Setting Selection (FO)'), available)
            ))
            if not baro_setting_sel:
                return False
        return all_of(
            ('Altitude QNH', 'Altitude Selected', 'Airborne', 'Vertical Speed'),
            available
        )

    def derive(self,
               alt=P('Altitude QNH'),
               alt_sel=P('Altitude Selected'),
               vert_spd=P('Vertical Speed'),
               airborne=S('Airborne'),
               bar_sel=P('Baro Setting Selection'),
               bar_sel_cpt=P('Baro Setting Selection (Capt)'),
               bar_sel_fo=P('Baro Setting Selection (FO)'),
               bar_cor_isis=P('Baro Correction (ISIS)')):
        pass


class RateOfDescentMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               descending=S('Descending')):
        pass


class RateOfDescentTopOfDescentTo10000FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               alt_aal=P('Altitude STD Smoothed'),
               descents=S('Descent')):
        pass


class RateOfDescentBelow10000FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               alt_std=P('Altitude STD Smoothed'),
               descents=S('Descent')):
        pass


class RateOfDescent10000To5000FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               alt_std=P('Altitude STD Smoothed'),
               descent=S('Descent')):
        pass


class RateOfDescent5000To3000FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               descent=S('Descent')):
        pass


class RateOfDescentAbove3000FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               descents=S('Descent')):
        pass


class RateOfDescent3000To2000FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class RateOfDescent2000To1000FtMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class RateOfDescent1000To500FtMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Vertical Speed']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descent'])
        else:
            required.extend(['Altitude AAL For Flight Phases', 'Final Approach'])
        return all_of(required, available)

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               ac_type=A('Aircraft Type'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fin_app=S('Final Approach'),
               alt_agl=P('Altitude AGL'),
               descending=S('Descent')):
        pass


class RateOfDescent500To50FtMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Vertical Speed']
        if ac_type and ac_type.value == 'helicopter':
            required.extend(['Altitude AGL', 'Descending'])
        else:
            required.extend(['Altitude AAL For Flight Phases', 'Final Approach'])
        return all_of(required, available)

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               ac_type=A('Aircraft Type'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fin_app=S('Final Approach'),
               alt_agl=P('Altitude AGL For Flight Phases'),
               descending=S('Descending')):
        pass


class RateOfDescent50FtToTouchdownMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Vertical Speed Inertial', 'Touchdown']
        if ac_type and ac_type.value == 'helicopter':
            required.append('Altitude AGL')
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               vrt_spd=P('Vertical Speed Inertial'),
               touchdowns=KTI('Touchdown'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL')):
        pass


class RateOfDescentAtTouchdown(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed Inertial'),
               tdns=KTI('Touchdown')):
        pass


class RateOfDescentDuringGoAroundMax(KeyPointValueNode):

    def derive(self,
               vrt_spd=P('Vertical Speed'),
               go_arounds=S('Go Around And Climbout')):
        pass


class RateOfDescentBelow80KtsMax(KeyPointValueNode):

    def derive(self, vrt_spd=P('Vertical Speed'), air_spd=P('Airspeed'), descending=S('Descending')):
        pass


class RateOfDescentAtHeightBeforeLevelFlight(KeyPointValueNode):
    NAME_VALUES = {'altitude': [2000, 1000]}

    def derive(self, vert_spd=P('Vertical Speed'),
               heights=KTI('Altitude Before Level Flight When Descending')):
        pass


class RateOfDescentAtHeightBeforeAltitudeSelected(KeyPointValueNode):
    NAME_VALUES = {'altitude': [2000, 1000]}

    @classmethod
    def can_operate(cls, available, manufacturer=A('Manufacturer')):
        if manufacturer and manufacturer.value == 'Airbus':
            baro_setting_sel = any((
                any_of(('Baro Setting Selection', 'Baro Correction (ISIS)'), available),
                all_of(('Baro Setting Selection (Capt)', 'Baro Setting Selection (FO)'), available)
            ))
            if not baro_setting_sel:
                return False
        return all_of(
            (
                'Altitude QNH', 'Altitude Selected', 'Airborne',
                'Approach And Landing', 'Vertical Speed'
            ),
            available
        )

    def derive(self,
               alt=P('Altitude QNH'),
               alt_sel=P('Altitude Selected'),
               vert_spd=P('Vertical Speed'),
               airborne=S('Airborne'),
               apps=S('Approach And Landing'),
               bar_sel=P('Baro Setting Selection'),
               bar_sel_cpt=P('Baro Setting Selection (Capt)'),
               bar_sel_fo=P('Baro Setting Selection (FO)'),
               bar_cor_isis=P('Baro Correction (ISIS)')):
        pass


class RollLiftoffTo20FtMax(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               airs=S('Airborne')):
        pass


class Roll20To400FtMax(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class Roll400To1000FtMax(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class RollAbove1000FtMax(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class Roll1000To300FtMax(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fin_app=S('Final Approach')):
        pass


class Roll1000To500FtMax(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fin_app=S('Final Approach')):
        pass


class Roll300To20FtMax(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class Roll20FtToTouchdownMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        required = ['Roll', 'Touchdown']
        if ac_type and ac_type.value == 'helicopter':
            required.append('Altitude AGL')
        else:
            required.append('Altitude AAL For Flight Phases')
        return all_of(required, available)

    def derive(self,
               roll=P('Roll'),
               touchdowns=KTI('Touchdown'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               alt_agl=P('Altitude AGL')):
        pass


class Roll500FtToTouchdownMax(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               touchdowns=KTI('Touchdown')):
        pass


class RollCyclesExceeding5DegDuringFinalApproach(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               fin_apps=S('Final Approach')):
        pass


class RollCyclesExceeding15DegDuringFinalApproach(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               fin_apps=S('Final Approach')):
        pass


class RollCyclesExceeding5DegDuringInitialClimb(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               initial_climbs=S('Initial Climb')):
        pass


class RollCyclesExceeding15DegDuringInitialClimb(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               initial_climbs=S('Initial Climb')):
        pass


class RollCyclesNotDuringFinalApproach(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               airborne=S('Airborne'),
               fin_apps=S('Final Approach'),
               landings=S('Landing')):
        pass


class RollAtLowAltitude(KeyPointValueNode):

    def derive(self,
               roll=P('Roll'),
               alt_rad=P('Altitude Radio')):
        pass


class RollLeftBelow6000FtAltitudeDensityBelow60Kts(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'), family=A('Family')):
        is_puma = ac_type == helicopter and family and family.value == 'Puma'
        return is_puma and all_deps(cls, available)

    def derive(self, roll=P('Roll'), alt=P('Altitude Density'), airspeed=P('Airspeed'), airborne=S('Airborne')):
        pass


class RollLeftBelow8000FtAltitudeDensityAbove60Kts(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'), family=A('Family')):
        is_puma = ac_type == helicopter and family and family.value == 'Puma'
        return is_puma and all_deps(cls, available)

    def derive(self, roll=P('Roll'), alt=P('Altitude Density'), airspeed=P('Airspeed'), airborne=S('Airborne')):
        pass


class RollLeftAbove6000FtAltitudeDensityBelow60Kts(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'), family=A('Family')):
        is_puma = ac_type == helicopter and family and family.value == 'Puma'
        return is_puma and all_deps(cls, available)

    def derive(self, roll=P('Roll'), alt=P('Altitude Density'), airspeed=P('Airspeed'), airborne=S('Airborne')):
        pass


class RollLeftAbove8000FtAltitudeDensityAbove60Kts(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'), family=A('Family')):
        is_puma = ac_type == helicopter and family and family.value == 'Puma'
        return is_puma and all_deps(cls, available)

    def derive(self, roll=P('Roll'), alt=P('Altitude Density'), airspeed=P('Airspeed'), airborne=S('Airborne')):
        pass


class RollBetweenFL200AndFL300Max(KeyPointValueNode):
    name = 'Roll Between FL200 and FL300 Max'

    def derive(self,
               roll=P('Roll'),
               alt=P('Altitude STD Smoothed')):
        pass


class RollAboveFL300Max(KeyPointValueNode):
    name = 'Roll Above FL300 Max'

    def derive(self,
               roll=P('Roll'),
               alt=P('Altitude STD Smoothed')):
        pass


class RollRateMaxAboveLimitAtTouchdown(KeyPointValueNode):

    def derive(self,
               roll_rate=P('Roll Rate For Touchdown'),
               limit=P('Roll Rate At Touchdown Limit'),
               touchdowns=KTI('Touchdown'),
               touch_and_go=KTI('Touch And Go'),
               bounces=S('Bounced Landing'),):
        pass


class RudderDuringTakeoffMax(KeyPointValueNode):

    def derive(self,
               rudder=P('Rudder'),
               to_rolls=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class RudderCyclesAbove50Ft(KeyPointValueNode):

    def derive(self,
               rudder=P('Rudder'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class RudderReversalAbove50Ft(KeyPointValueNode):

    def derive(self,
               rudder=P('Rudder'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class RudderPedalForceMax(KeyPointValueNode):

    def derive(self,
               force=P('Rudder Pedal Force'),
               fast=S('Fast')):
        pass


class RudderPedalMax(KeyPointValueNode):

    def derive(self, pedal=P('Rudder Pedal')):
        pass


class RudderPedalMin(KeyPointValueNode):

    def derive(self, pedal=P('Rudder Pedal')):
        pass


class SpeedbrakeDeployed1000To20FtDuration(KeyPointValueNode):

    def derive(self,
               spd_brk=M('Speedbrake Selected'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class AltitudeWithSpeedbrakeDeployedDuringFinalApproachMin(KeyPointValueNode):

    def derive(self, alt_aal=P('Altitude AAL'),
               spd_brk=M('Speedbrake Selected'),
               fin_app=S('Final Approach')):
        pass


class SpeedbrakeDeployedWithFlapDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and all_of(('Speedbrake Selected', 'Airborne'), available)

    def derive(self,
               spd_brk=M('Speedbrake Selected'),
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               airborne=S('Airborne')):
        pass


class SpeedbrakeDeployedWithPowerOnDuration(KeyPointValueNode):

    def derive(self,
               spd_brk=M('Speedbrake Selected'),
               power=P('Eng (*) N1 Avg'),
               alt_aal=S('Altitude AAL For Flight Phases'),
               model=A('Model')):
        pass


class SpeedbrakeDeployedDuringGoAroundDuration(KeyPointValueNode):

    def derive(self,
               spd_brk=M('Speedbrake Selected'),
               go_arounds=S('Go Around And Climbout')):
        pass


class StallWarningDuration(KeyPointValueNode):

    def derive(self, stall_warning=M('Stall Warning'), airs=S('Airborne')):
        pass


class StickPusherActivatedDuration(KeyPointValueNode):

    def derive(self, stick_pusher=M('Stick Pusher'), airs=S('Airborne')):
        pass


class StickShakerActivatedDuration(KeyPointValueNode):

    def derive(self, stick_shaker=M('Stick Shaker'), airs=S('Airborne')):
        pass


class OverspeedDuration(KeyPointValueNode):

    def derive(self, overspeed=M('Overspeed Warning'), airs=S('Airborne')):
        pass


class StallFaultCautionDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        stall_fault = any_of(('Stall (L) Fault Caution',
                              'Stall (R) Fault Caution'), available)
        airborne = 'Airborne' in available
        return stall_fault and airborne

    def derive(self, stall_l=M('Stall (L) Fault Caution'),
               stall_r=M('Stall (L) Fault Caution'), airborne=S('Airborne')):
        pass


class CruiseSpeedLowDuration(KeyPointValueNode):

    def derive(self, spd=M('Cruise Speed Low'), airborne=S('Airborne')):
        pass


class DegradedPerformanceCautionDuration(KeyPointValueNode):

    def derive(self, caution=M('Degraded Performance Caution'),
               airborne=S('Airborne')):
        pass


class AirspeedIncreaseAlertDuration(KeyPointValueNode):

    def derive(self, alert=M('Airspeed Increase Alert'),
               airborne=S('Airborne')):
        pass


class AirspeedBelowMinimumAirspeedFlapCleanMin(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        core = all_of(['Airspeed', 'Airborne', 'Flap Including Transition'], available)
        min_spd = any_of(['Minimum Airspeed', 'Flap Manoeuvre Speed',],
                         available)
        return core and min_spd

    def derive(self,
               air_spd=P('Airspeed'),
               min_spd=P('Minimum Airspeed'),
               flap = M('Flap Including Transition'),
               f_m_spd = P('Flap Manoeuvre Speed'),
               airborne = S('Airborne')):
        pass


class TailClearanceDuringTakeoffMin(KeyPointValueNode):

    def derive(self,
               alt_tail=P('Altitude Tail'),
               takeoffs=S('Takeoff')):
        pass


class TailClearanceDuringLandingMin(KeyPointValueNode):

    def derive(self,
               alt_tail=P('Altitude Tail'),
               landings=S('Landing')):
        pass


class TailClearanceDuringGoAroundMin(KeyPointValueNode):

    def derive(self,
               alt_tail=P('Altitude Tail'),
               go_arounds=S('Go Around And Climbout')):
        pass


class TailClearanceDuringApproachMin(KeyPointValueNode):

    def derive(self,
               alt_aal=P('Altitude AAL'),
               alt_tail=P('Altitude Tail'),
               dtl=P('Distance To Landing')):
        pass


class TerrainClearanceAbove3000FtMin(KeyPointValueNode):

    def derive(self,
               alt_rad=P('Altitude Radio'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class TailwindLiftoffTo100FtMax(KeyPointValueNode):

    def derive(self,
                tailwind=P('Tailwind'),
                alt_aal=P('Altitude AAL For Flight Phases'),
                ):
        pass


class Tailwind100FtToTouchdownMax(KeyPointValueNode):

    def derive(self,
               tailwind=P('Tailwind'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               landing=S('Approach And Landing'),
               ):
        pass


class TailwindDuringTakeoffMax(KeyPointValueNode):

    def derive(self,
               tailwind=P('Tailwind'),
               airspeed=P('Airspeed True'),
               toffs=S('Takeoff'),
               toff_rotations=S('Takeoff Rotation'),
               ):
        pass


class MasterWarningDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type == helicopter:
            sections = 'Airborne' in available
        else:
            sections = all_of(['Takeoff', 'Airborne', 'Landing'], available)
        return all_of(['Master Warning', 'Aircraft Type'], available) and sections

    def derive(self,
               warning=M('Master Warning'),
               ac_type=A('Aircraft Type'),
               tkoffs=S('Takeoff'),
               airborne=S('Airborne'),
               landings=S('Landing'),
               ):
        pass


class MasterWarningDuringTakeoffDuration(KeyPointValueNode):

    def derive(self,
               warning=M('Master Warning'),
               takeoff_rolls=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class MasterCautionDuringTakeoffDuration(KeyPointValueNode):

    def derive(self,
               caution=M('Master Caution'),
               takeoff_rolls=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class TaxiInDuration(KeyPointValueNode):

    def derive(self,
               taxi_ins=S('Taxi In')):
        pass


class TaxiOutDuration(KeyPointValueNode):

    def derive(self,
               taxi_outs=S('Taxi Out')):
        pass


class TAWSAlertDuration(KeyPointValueNode):
    name = 'TAWS Alert Duration'

    def derive(self, taws_alert=M('TAWS Alert'),
               airborne=S('Airborne')):
        pass


class TAWSWarningDuration(KeyPointValueNode):
    name = 'TAWS Warning Duration'

    def derive(self, taws_warning=M('TAWS Warning'),
               airborne=S('Airborne')):
        pass


class TAWSGeneralWarningDuration(KeyPointValueNode):
    name = 'TAWS General Warning Duration'

    def derive(self, taws_general=M('TAWS General'),
               airborne=S('Airborne')):
        pass


class TAWSSinkRateWarningDuration(KeyPointValueNode):
    name = 'TAWS Sink Rate Warning Duration'

    def derive(self, taws_sink_rate=M('TAWS Sink Rate'),
               airborne=S('Airborne')):
        pass


class TAWSTooLowFlapWarningDuration(KeyPointValueNode):
    name = 'TAWS Too Low Flap Warning Duration'

    def derive(self, taws_too_low_flap=M('TAWS Too Low Flap'),
               airborne=S('Airborne')):
        pass


class TAWSTerrainWarningDuration(KeyPointValueNode):
    name = 'TAWS Terrain Warning Duration'

    @classmethod
    def can_operate(cls, available):
        return ('Airborne' in available and
                any_of(('TAWS Terrain', 'TAWS Terrain Warning'), available))

    def derive(self, taws_terrain=M('TAWS Terrain'),
               taws_terrain_warning=M('TAWS Terrain Warning'),
               airborne=S('Airborne')):
        pass


class TAWSTerrainPullUpWarningDuration(KeyPointValueNode):
    name = 'TAWS Terrain Pull Up Warning Duration'

    def derive(self, taws_terrain_pull_up=M('TAWS Terrain Pull Up'),
               airborne=S('Airborne')):
        pass


class TAWSTerrainClearanceFloorAlertDuration(KeyPointValueNode):
    name = 'TAWS Terrain Clearance Floor Alert Duration'

    @classmethod
    def can_operate(cls, available):
        return 'Airborne' in available and any_of(
            ['TAWS Terrain Clearance Floor Alert',
             'TAWS Terrain Clearance Floor Alert (2)'], available)

    def derive(self,
               taws_terrain_clearance_floor_alert=
               M('TAWS Terrain Clearance Floor Alert'),
               taws_terrain_clearance_floor_alert_2=
               M('TAWS Terrain Clearance Floor Alert (2)'),
               airborne=S('Airborne')):
        pass


class TAWSGlideslopeWarning1500To1000FtDuration(KeyPointValueNode):
    name = 'TAWS Glideslope Warning 1500 To 1000 Ft Duration'

    @classmethod
    def can_operate(cls, available):
        return 'Altitude AAL For Flight Phases' in available and\
               any_of(['TAWS Glideslope', 'TAWS Glideslope Alert'], available)

    def derive(self,
               taws_glideslope=M('TAWS Glideslope'),
               taws_alert=M('TAWS Glideslope Alert'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class TAWSGlideslopeWarning1000To500FtDuration(KeyPointValueNode):
    name = 'TAWS Glideslope Warning 1000 To 500 Ft Duration'

    @classmethod
    def can_operate(cls, available):
        return 'Altitude AAL For Flight Phases' in available and\
               any_of(['TAWS Glideslope', 'TAWS Glideslope Alert'], available)

    def derive(self,
               taws_glideslope=M('TAWS Glideslope'),
               taws_alert=M('TAWS Glideslope Alert'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class TAWSGlideslopeWarning500To200FtDuration(KeyPointValueNode):
    name = 'TAWS Glideslope Warning 500 To 200 Ft Duration'

    @classmethod
    def can_operate(cls, available):
        return 'Altitude AAL For Flight Phases' in available and\
               any_of(['TAWS Glideslope', 'TAWS Glideslope Alert'], available)

    def derive(self,
               taws_glideslope=M('TAWS Glideslope'),
               taws_alert=M('TAWS Glideslope Alert'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        pass


class TAWSTooLowTerrainWarningDuration(KeyPointValueNode):
    name = 'TAWS Too Low Terrain Warning Duration'

    def derive(self, taws_too_low_terrain=M('TAWS Too Low Terrain'),
               airborne=S('Airborne')):
        pass


class TAWSTooLowGearWarningDuration(KeyPointValueNode):
    name = 'TAWS Too Low Gear Warning Duration'

    def derive(self, taws_too_low_gear=M('TAWS Too Low Gear'),
               airborne=S('Airborne')):
        pass


class TAWSPullUpWarningDuration(KeyPointValueNode):
    name = 'TAWS Pull Up Warning Duration'

    def derive(self, taws_pull_up=M('TAWS Pull Up'), airborne=S('Airborne')):
        pass


class TAWSDontSinkWarningDuration(KeyPointValueNode):
    name = 'TAWS Dont Sink Warning Duration'

    def derive(self, taws_dont_sink=M('TAWS Dont Sink'),
               airborne=S('Airborne')):
        pass


class TAWSCautionObstacleDuration(KeyPointValueNode):
    name = 'TAWS Caution Obstacle Duration'

    def derive(self, taws_caution_obstacle=M('TAWS Caution Obstacle'),
               airborne=S('Airborne')):
        pass


class TAWSCautionTerrainDuration(KeyPointValueNode):
    name = 'TAWS Caution Terrain Duration'

    def derive(self, taws_caution_terrain=M('TAWS Caution Terrain'),
               airborne=S('Airborne')):
        pass


class TAWSTerrainCautionDuration(KeyPointValueNode):
    name = 'TAWS Terrain Caution Duration'

    def derive(self, taws_terrain_caution=M('TAWS Terrain Caution'),
               airborne=S('Airborne')):
        pass


class TAWSFailureDuration(KeyPointValueNode):
    name = 'TAWS Failure Duration'

    def derive(self, taws_failure=M('TAWS Failure'),
               airborne=S('Airborne')):
        pass


class TAWSObstacleWarningDuration(KeyPointValueNode):
    name = 'TAWS Obstacle Warning Duration'

    def derive(self, taws_obstacle_warning=M('TAWS Obstacle Warning'),
               airborne=S('Airborne')):
        pass


class TAWSPredictiveWindshearDuration(KeyPointValueNode):
    name = 'TAWS Predictive Windshear Duration'

    def derive(self, taws_pw=M('TAWS Predictive Windshear'),
               airborne=S('Airborne')):
        pass


class TAWSTerrainAheadDuration(KeyPointValueNode):
    name = 'TAWS Terrain Ahead Duration'

    def derive(self, taws_terrain_ahead=M('TAWS Terrain Ahead'),
               airborne=S('Airborne')):
        pass


class TAWSTerrainAheadPullUpDuration(KeyPointValueNode):
    name = 'TAWS Terrain Ahead Pull Up Duration'

    def derive(self, taws_terrain_ahead_pu=M('TAWS Terrain Ahead Pull Up'),
               airborne=S('Airborne')):
        pass


class TAWSWindshearWarningBelow1500FtDuration(KeyPointValueNode):
    name = 'TAWS Windshear Warning Below 1500 Ft Duration'

    def derive(self, taws_windshear=M('TAWS Windshear Warning'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fasts=S('Fast')):
        pass


class TAWSWindshearCautionBelow1500FtDuration(KeyPointValueNode):
    name = 'TAWS Windshear Caution Below 1500 Ft Duration'

    def derive(self, taws_windshear=M('TAWS Windshear Caution'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fasts=S('Fast')):
        pass


class TAWSWindshearSirenBelow1500FtDuration(KeyPointValueNode):
    name = 'TAWS Windshear Siren Below 1500 Ft Duration'

    def derive(self, taws_windshear=M('TAWS Windshear Siren'),
               alt_aal=P('Altitude AAL For Flight Phases'),
               fasts=S('Fast')):
        pass


class TAWSUnspecifiedDuration(KeyPointValueNode):
    name = 'TAWS Unspecified Duration'

    def derive(self, taws_unspecified=M('TAWS Unspecified'),
               airborne=S('Airborne')):
        pass


class TCASTAWarningDuration(KeyPointValueNode):
    name = 'TCAS TA Warning Duration'

    def derive(self, tcas_tas=S('TCAS Traffic Advisory'),
               tcas_ras=S('TCAS Resolution Advisory')):
        pass


class TCASTAAcceleration(KeyPointValueNode):
    name = 'TCAS TA Acceleration'

    def derive(self, acc=P('Acceleration Vertical'),
               tcas_tas=S('TCAS Traffic Advisory'),
               tcas_warns=KPV('TCAS TA Warning Duration')):
        pass


class TCASTAChangeOfVerticalSpeed(KeyPointValueNode):
    name = 'TCAS TA Change Of Vertical Speed'

    def derive(self, vs=P('Vertical Speed'),
               tcas_tas=S('TCAS Traffic Advisory')):
        pass


class TCASRAWarningDuration(KeyPointValueNode):
    name = 'TCAS RA Warning Duration'

    def derive(self, tcas_ras=S('TCAS Resolution Advisory')):
        pass


class TCASRAWarningBelowFL100InClimbDuration(KeyPointValueNode):
    name = 'TCAS RA Warning Below FL100 In Climb Duration'

    def derive(self, alt_std=P('Altitude STD Smoothed'),
               tcas_ras=S('TCAS Resolution Advisory')):
        pass


class TCASRAWarningAboveFL100Duration(KeyPointValueNode):
    name = 'TCAS RA Warning Above FL100 Duration'

    def derive(self, alt_std=P('Altitude STD Smoothed'),
               tcas_ras=S('TCAS Resolution Advisory')):
        pass


class TCASRAWarningBelowFL100InDescentDuration(KeyPointValueNode):
    name = 'TCAS RA Warning Below FL100 In Descent Duration'

    def derive(self, alt_std=P('Altitude STD Smoothed'),
               tcas_ras=S('TCAS Resolution Advisory')):
        pass


class TCASRADirection(KeyPointValueNode):
    name = 'TCAS RA Direction'

    @classmethod
    def can_operate(cls, available):
        return 'TCAS Resolution Advisory' in available and (
            'TCAS Combined Control' in available or
            any_of(('TCAS Advisory Rate To Maintain',
                    'TCAS Altitude Rate To Maintain',
                    'TCAS Advisory Rate'), available))

    def derive(self, tcas_ras=S('TCAS Resolution Advisory'),
               tcas_cc=M('TCAS Combined Control'),
               ## rate_1=P('TCAS Altitude Rate Advisory'),
               rate_1=P('TCAS Advisory Rate To Maintain'),
               rate_2=P('TCAS Altitude Rate To Maintain'),
               rate_3=P('TCAS Advisory Rate')):
        pass


class TCASRAReactionDelay(KeyPointValueNode):
    name = 'TCAS RA Reaction Delay'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Acceleration Vertical', 'TCAS Resolution Advisory'), available)

    def derive(self, acc=P('Acceleration Vertical'),
               tcas_ras=S('TCAS Resolution Advisory'),
               tcas_tas=S('TCAS Traffic Advisory')):
        pass


class TCASRAAcceleration(KeyPointValueNode):
    name = 'TCAS RA Acceleration'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Acceleration Vertical',
                       'TCAS Resolution Advisory',
                       'TCAS RA Direction'), available)

    def derive(self, acc=P('Acceleration Vertical'),
               tcas_tas=S('TCAS Traffic Advisory'),
               tcas_ras=S('TCAS Resolution Advisory'),
               tcas_dirs=KPV('TCAS RA Direction')):
        pass


class TCASRAChangeOfVerticalSpeed(KeyPointValueNode):
    name = 'TCAS RA Change Of Vertical Speed'

    def derive(self, vs=P('Vertical Speed'),
               tcas_ras=S('TCAS Resolution Advisory')):
        pass


class TCASRAAPDisengaged(KeyPointValueNode):
    name = 'TCAS RA AP Disengaged'

    @classmethod
    def can_operate(cls, available):
        return all_of(('AP Disengaged Selection', 'TCAS Resolution Advisory'), available)

    def derive(self, ap_offs=KTI('AP Disengaged Selection'),
               tcas_ras=S('TCAS Resolution Advisory'),
               tcas_tas=S('TCAS Traffic Advisory')):
        pass


class TCASRAToAPDisengagedDelay(KeyPointValueNode):
    name = 'TCAS RA To AP Disengaged Delay'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Acceleration Vertical', 'AP Disengaged Selection', 'TCAS Resolution Advisory'), available)

    def derive(self, acc=P('Acceleration Vertical'),
               ap_offs=KTI('AP Disengaged Selection'),
               tcas_ras=S('TCAS Resolution Advisory'),
               tcas_tas=S('TCAS Traffic Advisory')):
        pass


class TCASRAErroneousAcceleration(KeyPointValueNode):
    name = 'TCAS RA Erroneous Acceleration'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Acceleration Vertical',
                       'TCAS Resolution Advisory',
                       'TCAS RA Direction'), available)

    def derive(self, acc=P('Acceleration Vertical'),
               tcas_tas=S('TCAS Traffic Advisory'),
               tcas_ras=S('TCAS Resolution Advisory'),
               tcas_ra_accs=KPV('TCAS RA Acceleration'),
               tcas_dirs=KPV('TCAS RA Direction')):
        pass


class TCASRASubsequentAcceleration(KeyPointValueNode):
    name = 'TCAS RA Subsequent Acceleration'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Acceleration Vertical', 'TCAS Resolution Advisory', 'TCAS Combined Control'), available)

    def derive(self, acc=P('Acceleration Vertical'),
               tcas_ras=S('TCAS Resolution Advisory'),
               tcas_cc=M('TCAS Combined Control'),
               ## rate_1=P('TCAS Altitude Rate Advisory'),
               rate_1=P('TCAS Advance Rate To Maintain'),
               rate_2=P('TCAS Advisory Rate To Maintain'),
               rate_3=P('TCAS Altitude Rate To Maintain'),
               rate_4=P('TCAS Advisory Rate')):
        pass


class TCASRASubsequentReactionDelay(KeyPointValueNode):
    name = 'TCAS RA Subsequent Reaction Delay'

    @classmethod
    def can_operate(cls, available):
        return all_of(('Acceleration Vertical', 'TCAS Resolution Advisory', 'TCAS Combined Control'), available)

    def derive(self, acc=P('Acceleration Vertical'),
               tcas_ras=S('TCAS Resolution Advisory'),
               tcas_cc=M('TCAS Combined Control'),
               ## rate_1=P('TCAS Altitude Rate Advisory'),
               rate_1=P('TCAS Advance Rate To Maintain'),
               rate_2=P('TCAS Advisory Rate To Maintain'),
               rate_3=P('TCAS Altitude Rate To Maintain'),
               rate_4=P('TCAS Advisory Rate')):
        pass


class TCASFailureRatio(KeyPointValueNode):
    name = 'TCAS Failure Ratio'

    def derive(self, tcas_ops=S('TCAS Operational'),
               airs=S('Airborne')):
        pass


class TCASRAAltitudeSTD(KeyPointValueNode):
    name = 'TCAS RA Altitude STD'

    def derive(self, alt=P('Altitude STD'),
               tcas_ras=S('TCAS Resolution Advisory')):
        pass


class TCASRAAltitudeAAL(KeyPointValueNode):
    name = 'TCAS RA Altitude AAL'

    def derive(self, alt=P('Altitude AAL'),
               tcas_ras=S('TCAS Resolution Advisory')):
        pass


class TCASRAHeading(KeyPointValueNode):
    name = 'TCAS RA Heading'

    def derive(self, hdg=P('Heading'),
               tcas_ras=S('TCAS Resolution Advisory')):
        pass


class TCASTAAltitudeSTD(KeyPointValueNode):
    name = 'TCAS TA Altitude STD'

    def derive(self, alt=P('Altitude STD'),
               ta_warns=KPV('TCAS TA Warning Duration')):
        pass


class TCASTAAltitudeAAL(KeyPointValueNode):
    name = 'TCAS TA Altitude AAL'

    def derive(self, alt=P('Altitude AAL'),
               ta_warns=KPV('TCAS TA Warning Duration')):
        pass


class TCASTAHeading(KeyPointValueNode):
    name = 'TCAS TA Heading'

    def derive(self, hdg=P('Heading'),
               ta_warns=KPV('TCAS TA Warning Duration')):
        pass


class TakeoffConfigurationWarningDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, manufacturer=A('Manufacturer')):
        if manufacturer and manufacturer.value == 'Airbus':
            return False
        return all_of(['Takeoff Configuration Warning', 'Mobile'], available)

    def derive(self, takeoff_warn=M('Takeoff Configuration Warning'),
               mobile=S('Mobile'),
               airborne=S('Airborne')):
        pass


class TakeoffConfigurationFlapWarningDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Takeoff Configuration Flap Warning', 'Mobile'), available)

    def derive(self, takeoff_warn=M('Takeoff Configuration Flap Warning'),
               mobile=S('Mobile'),
               airborne=S('Airborne')):
        pass


class TakeoffConfigurationParkingBrakeWarningDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Takeoff Configuration Parking Brake Warning', 'Mobile'), available)

    def derive(self,
               takeoff_warn=M('Takeoff Configuration Parking Brake Warning'),
               mobile=S('Mobile'),
               airborne=S('Airborne')):
        pass


class TakeoffConfigurationSpoilerWarningDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Takeoff Configuration Spoiler Warning', 'Mobile'), available)

    def derive(self,
               takeoff_warn=M('Takeoff Configuration Spoiler Warning'),
               mobile=S('Mobile'),
               airborne=S('Airborne')):
        pass


class TakeoffConfigurationStabilizerWarningDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Takeoff Configuration Stabilizer Warning', 'Mobile'), available)

    def derive(self,
               takeoff_warn=M('Takeoff Configuration Stabilizer Warning'),
               mobile=S('Mobile'),
               airborne=S('Airborne')):
        pass


class LandingConfigurationGearWarningDuration(KeyPointValueNode):

    def derive(self,
               landing_cfg_warn=M('Landing Configuration Gear Warning'),
               airs=S('Airborne')):
        pass


class LandingConfigurationSpeedbrakeCautionDuration(KeyPointValueNode):

    def derive(self,
               landing_cfg_caution=M(
                   'Landing Configuration Speedbrake Caution'),
               airs=S('Airborne')):
        pass


class SmokeWarningDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return 'Smoke Warning' in available

    def derive(self, smoke_warning=M('Smoke Warning')):
        pass


class CargoSmokeOrFireWarningDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Cargo (*) Smoke Or Fire', 'Airborne'), available)

    def derive(self, c_smoke_fire=M('Cargo (*) Smoke Or Fire'), airborne=S('Airborne')):
        pass


class ThrottleCyclesDuringFinalApproach(KeyPointValueNode):

    def derive(self, levers=P('Throttle Levers'),
               fin_apps=S('Final Approach')):
        pass


class ThrottleLeverAtLiftoff(KeyPointValueNode):

    def derive(self, levers=P('Throttle Levers'), liftoffs=KTI('Liftoff')):
        pass


class ThrottleLeverVariationAbove80KtsToTakeoff(KeyPointValueNode):

    def derive(self, levers=P('Throttle Levers'), speed=P('Airspeed'),
               takeoffs=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class ThrustAsymmetryDuringTakeoffMax(KeyPointValueNode):

    def derive(self, ta=P('Thrust Asymmetry'),
               takeoff_rolls=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class ThrustAsymmetryDuringFlightMax(KeyPointValueNode):

    def derive(self, ta=P('Thrust Asymmetry'),
               airborne=S('Airborne')):
        pass


class ThrustAsymmetryDuringGoAroundMax(KeyPointValueNode):

    def derive(self, ta=P('Thrust Asymmetry'),
               go_arounds=S('Go Around And Climbout')):
        pass


class ThrustAsymmetryDuringApproachMax(KeyPointValueNode):

    def derive(self, ta=P('Thrust Asymmetry'),
               approaches=S('Approach')):
        pass


class ThrustAsymmetryWithThrustReversersDeployedMax(KeyPointValueNode):

    def derive(self, ta=P('Thrust Asymmetry'), tr=M('Thrust Reversers'),
               mobile=S('Mobile')):
        pass


class ThrustAsymmetryDuringApproachDuration(KeyPointValueNode):

    def derive(self, ta=P('Thrust Asymmetry'), approaches=S('Approach')):
        pass


class ThrustAsymmetryWithThrustReversersDeployedDuration(KeyPointValueNode):

    def derive(self,
               ta=P('Thrust Asymmetry'),
               tr=M('Thrust Reversers'),
               mobile=S('Mobile')):
        pass


class ThrustRatingCLB1Duration(KeyPointValueNode):
    name = 'Thrust Rating CLB1 Duration'

    def derive(self,
               thrust_rating=M('Thrust Rating Mode'),
               airs=S('Airborne')):
        pass


class TouchdownToElevatorDownDuration(KeyPointValueNode):

    def derive(self,
               airspeed=P('Airspeed'),
               elevator=P('Elevator'),
               tdwns=KTI('Touchdown'),
               lands=S('Landing')):
        pass


class TouchdownTo60KtsDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Airspeed', 'Touchdown'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               groundspeed=P('Groundspeed'),
               tdwns=KTI('Touchdown')):
        pass


class TouchdownToPitch2DegreesAbovePitchAt60KtsDuration(KeyPointValueNode):

    def derive(self, pitch=P('Pitch'), airspeed=P('Airspeed'),
               tdwns=KTI('Touchdown')):
        pass


class TurbulenceDuringApproachMax(KeyPointValueNode):

    def derive(self,
               turbulence=P('Turbulence'),
               approaches=S('Approach')):
        pass


class TurbulenceDuringCruiseMax(KeyPointValueNode):

    def derive(self,
               turbulence=P('Turbulence'),
               cruises=S('Cruise')):
        pass


class TurbulenceDuringFlightMax(KeyPointValueNode):

    def derive(self,
               turbulence=P('Turbulence'),
               airborne=S('Airborne'),
               apps=S('Approach')):
        pass


class WindSpeedAtAltitudeDuringDescent(KeyPointValueNode):
    NAME_VALUES = {'altitude': [2000, 1500, 1000, 500, 100, 50]}

    def derive(self,
               alt_aal=P('Altitude AAL For Flight Phases'),
               wind_spd=P('Wind Speed')):
        pass


class WindDirectionAtAltitudeDuringDescent(KeyPointValueNode):
    NAME_VALUES = {'altitude': [2000, 1500, 1000, 500, 100, 50]}

    def derive(self,
               alt_aal=P('Altitude AAL For Flight Phases'),
               wind_dir=P('Wind Direction Continuous')):
        pass


class WindAcrossLandingRunwayAt50Ft(KeyPointValueNode):

    def derive(self,
               walr=P('Wind Across Landing Runway'),
               landings=S('Landing')):
        pass


class TailwindAtAltitudeDuringDescent(KeyPointValueNode):
    NAME_VALUES = {'altitude': [2000, 1500, 1000, 500, 100, 50]}

    def derive(self,
               alt_aal=P('Altitude AAL For Flight Phases'),
               tailwind=P('Tailwind')):
        pass


class GrossWeightAtLiftoff(KeyPointValueNode):

    def derive(self, gw=P('Gross Weight Smoothed'), liftoffs=KTI('Liftoff')):
        pass


class GrossWeightAtTouchdown(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Gross Weight Smoothed', 'Touchdown'), available)

    def derive(self, gw=P('Gross Weight Smoothed'),
               touchdowns=KTI('Touchdown'),
               touch_and_go=KTI('Touch And Go')):
        pass


class GrossWeightConditionalAtTouchdown(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, manufacturer=A('Manufacturer')):
        required_params = ('Gross Weight At Touchdown',
                           'Acceleration Normal At Touchdown',
                           'Rate Of Descent At Touchdown')
        return all_of(required_params, available) \
            and manufacturer and manufacturer.value == 'Airbus'

    def derive(self, gw_kpv=KPV('Gross Weight At Touchdown'),
               acc_norm_kpv=KPV('Acceleration Normal At Touchdown'),
               rod_kpv=KPV('Rate Of Descent At Touchdown')):
        pass


class GrossWeightDelta60SecondsInFlightMax(KeyPointValueNode):

    def derive(self, gross_weight=P('Gross Weight'), airborne=S('Airborne')):
        pass


class DualInputWarningDuration(KeyPointValueNode):

    def derive(self,
               dual=M('Dual Input Warning'),
               takeoff_rolls=S('Takeoff Roll'),
               landing_rolls=S('Landing Roll')):
        pass


class DualInputAbove200FtDuration(KeyPointValueNode):

    def derive(self,
               dual=M('Dual Input'),
               alt_aal=P('Altitude AAL')):
        pass


class DualInputBelow200FtDuration(KeyPointValueNode):

    def derive(self,
               dual=M('Dual Input'),
               alt_aal=P('Altitude AAL'),
               takeoff_rolls=S('Takeoff Roll'),
               landing_rolls=S('Landing Roll')):
        pass


class DualInputByCaptDuration(KeyPointValueNode):

    def derive(self,
               dual=M('Dual Input'),
               pilot=M('Pilot Flying'),
               takeoff_rolls=S('Takeoff Roll'),
               landing_rolls=S('Landing Roll')):
        pass


class DualInputByFODuration(KeyPointValueNode):
    name = 'Dual Input By FO Duration'

    def derive(self,
               dual=M('Dual Input'),
               pilot=M('Pilot Flying'),
               takeoff_rolls=S('Takeoff Roll'),
               landing_rolls=S('Landing Roll')):
        pass


class DualInputByCaptMax(KeyPointValueNode):

    def derive(self,
               stick_capt=P('Sidestick Angle (Capt)'),
               dual=M('Dual Input'),
               pilot=M('Pilot Flying'),
               takeoff_rolls=S('Takeoff Roll'),
               landing_rolls=S('Landing Roll')):
        pass


class DualInputByFOMax(KeyPointValueNode):
    name = 'Dual Input By FO Max'

    def derive(self,
               stick_fo=P('Sidestick Angle (FO)'),
               dual=M('Dual Input'),
               pilot=M('Pilot Flying'),
               takeoff_rolls=S('Takeoff Roll'),
               landing_rolls=S('Landing Roll')):
        pass


class ControlColumnDualInputOppositeDirectionForceMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        is_atr = family and family.value in ('ATR-72')
        return all_of(('Control Column Force At Control Wheel (Capt)', 'Control Column Force At Control Wheel (FO)'), available) and is_atr

    def derive(self,
               force_capt=P('Control Column Force At Control Wheel (Capt)'),
               force_fo=P('Control Column Force At Control Wheel (FO)'),
               taxiing=S('Taxiing'),
               turns=S('Turning On Ground'), ):
        pass


class PitchDisconnectDuration(KeyPointValueNode):

    def derive(self, pitch_disconnect=M('Pitch Disconnect'),):
        pass


class HoldingDuration(KeyPointValueNode):

    def derive(self, holds=S('Holding')):
        pass


class TwoDegPitchTo35FtDuration(KeyPointValueNode):
    name = '2 Deg Pitch To 35 Ft Duration'

    def derive(self, two_deg_pitch_to_35ft=S('2 Deg Pitch To 35 Ft')):
        pass


class LastFlapChangeToTakeoffRollEndDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Flap Lever', 'Flap Lever (Synthetic)'), available) \
            and 'Takeoff Roll Or Rejected Takeoff' in available

    def derive(self,
               flap_lever=M('Flap Lever'),
               flap_synth=M('Flap Lever (Synthetic)'),
               rolls=S('Takeoff Roll Or Rejected Takeoff')):
        pass


class AirspeedMinusVMOMax(KeyPointValueNode):
    name = 'Airspeed Minus VMO Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(('VMO', 'VMO Lookup'), available) \
            and all_of(('Airborne', 'Airspeed'), available)

    def derive(self,
               airspeed=P('Airspeed'),
               vmo_record=P('VMO'),
               vmo_lookup=P('VMO Lookup'),
               airborne=S('Airborne')):
        pass


class MachMinusMMOMax(KeyPointValueNode):
    name = 'Mach Minus MMO Max'

    @classmethod
    def can_operate(cls, available):
        return any_of(('MMO', 'MMO Lookup'), available) \
            and all_of(('Airborne', 'Mach'), available)

    def derive(self,
               mach=P('Mach'),
               mmo_record=P('MMO'),
               mmo_lookup=P('MMO Lookup'),
               airborne=S('Airborne')):
        pass


class KineticEnergyAtRunwayTurnoff(KeyPointValueNode):

    def derive(self, turn_off=KTI('Landing Turn Off Runway'),
               kinetic_energy=P('Kinetic Energy')):
        pass


class AircraftEnergyWhenDescending(KeyPointValueNode):
    NAME_VALUES = {'height': AltitudeWhenDescending.names()}

    def derive(self, aircraft_energy=P('Aircraft Energy'),
               altitude_when_descending=KTI('Altitude When Descending')):
        pass


class TakeoffRatingDuration(KeyPointValueNode):

    def derive(self, toffs=S('Takeoff 5 Min Rating')):
        pass


class SATMax(KeyPointValueNode):
    name = 'SAT Max'

    def derive(self, sat=P('SAT')):
        pass


class DriftAtTouchdown(KeyPointValueNode):

    def derive(self, drift=P('Drift'), touchdown=KTI('Touchdown')):
        pass


class EngN1TakeoffDerate(KeyPointValueNode):
    name = 'Eng N1 Takeoff Derate'

    @classmethod
    def can_operate(cls, available, engine_series=A('Engine Series')):
        return engine_series and engine_series.value == 'CFM56-5B' and all_deps(cls, available)

    def derive(self, eng_n1=P('Eng (*) N1 Avg'),
               tat=P('TAT'), mach=P('Mach'),
               sage_toffs=KTI('SAGE Takeoff')):
        pass


class EngThrustTakeoffDerate(KeyPointValueNode):

    def derive(self, mach=P('Mach'),
               n1_derates=KPV('Eng N1 Takeoff Derate')):
        pass


class EngTakeoffDerateDuration(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(['Eng (*) EPR Max', 'Eng (1) EPR Limit', 'Eng (2) EPR Limit', 'Takeoff Roll', 'Airspeed',], available) or \
               all_of(['Temp Derate Status', 'Takeoff Roll', 'Airspeed',], available)

    def derive(self, epr_max=P('Eng (*) EPR Max'),
                     epr_limit_1=P('Eng (1) EPR Limit'),
                     epr_limit_2=P('Eng (2) EPR Limit'),
                     temp_derate=M('Temp Derate Status'),
                     takeoff_rolls=S('Takeoff Roll'),
                     airspeed=P('Airspeed'),):
        pass


class EngTakeoffFlexTemp(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(['Flex Temp', 'SAGE Takeoff'], available) or \
               all_of(['Eng (1) Flex Temp', 'Eng (2) Flex Temp', 'SAGE Takeoff'], available)

    def derive(self, sage_toffs=KTI('SAGE Takeoff'),
               flex=P('Flex Temp'),
               flex_1=P('Eng (1) Flex Temp'), flex_2=P('Eng (2) Flex Temp'),
               ):
        pass

class EngMaxMixin:
    pass


class EngNpMaxDuringTakeoff(EngMaxMixin, KeyPointValueNode):
    NAME_VALUES = {'durations': ['5 Sec', '20 Sec']}

    @classmethod
    def can_operate(cls, available):
        return all_of(('Takeoff 5 Min Rating', 'Eng (*) Np Max'), available)

    def derive(self,
               eng_np_max=P('Eng (*) Np Max'),
               takeoffs=S('Takeoff 5 Min Rating'),
               go_arounds=S('Go Around 5 Min Rating')):
        pass


class EngTorqueMaxDuringTakeoff(EngMaxMixin, KeyPointValueNode):
    NAME_VALUES = {'durations': ['10 Sec', '20 Sec', '5 Min']}

    @classmethod
    def can_operate(cls, available):
        return all_of(('Eng (*) Torque Max', 'Takeoff 5 Min Rating'), available)

    def derive(self,
               eng_torq_max=P('Eng (*) Torque Max'),
               takeoffs=S('Takeoff 5 Min Rating'),
               go_arounds=S('Go Around 5 Min Rating')):
        pass


class EngTorqueMaxDuringMaximumContinuousPower(EngMaxMixin, KeyPointValueNode):
    NAME_VALUES = {'durations': ['10 Sec', '20 Sec', '5 Min', '10 Min']}

    @classmethod
    def can_operate(cls, available):
        return all_of(('Eng (*) Torque Max', 'Maximum Continuous Power'), available)

    def derive(self,
               eng_torq_max=P('Eng (*) Torque Max'),
               ratings=S('Maximum Continuous Power')):
        pass


class EngN1DuringTakeoffMax(EngMaxMixin, KeyPointValueNode):
    NAME_VALUES = {'durations': ['10 Sec']}

    @classmethod
    def can_operate(cls, available):
        return all_of(('Eng (*) N1 Max', 'Takeoff 5 Min Rating'), available)

    def derive(self,
               eng_n1_max=P('Eng (*) N1 Max'),
               takeoffs=S('Takeoff 5 Min Rating'),
               go_arounds=S('Go Around 5 Min Rating')):
        pass


class EngN2DuringTakeoffForXSecMax(EngMaxMixin, KeyPointValueNode):
    NAME_VALUES = {'durations': ['10 Sec', '20 Sec', '5 Min']}

    @classmethod
    def can_operate(cls, available):
        return all_of(('Eng (*) N2 Max', 'Takeoff 5 Min Rating'), available)

    def derive(self, eng_n2_max=P('Eng (*) N2 Max'),
               takeoffs=S('Takeoff 5 Min Rating'),
               go_arounds=S('Go Around 5 Min Rating')):
        pass


class EngN2DuringMaximumContinuousPowerForXSecMax(EngMaxMixin, KeyPointValueNode):
    NAME_VALUES = {'durations': ['10 Sec', '20 Sec', '5 Min', '10 Min']}

    @classmethod
    def can_operate(cls, available):
        return all_of(('Eng (*) N2 Max', 'Maximum Continuous Power'), available)

    def derive(self,
               eng_n2_max=P('Eng (*) N2 Max'),
               ratings=S('Maximum Continuous Power')):
        pass


class TransmitInactivityDuration(KeyPointValueNode):

    def derive(self, transmitting=M('Transmitting'), airs=S('Airborne')):
        pass


class DHSelectedAt1500FtLVO(KeyPointValueNode):
    name = 'DH Selected At 1500 Ft LVO'

    @classmethod
    def can_operate(cls, available, series=A('Series')):
        if not series or series.value not in ('Falcon-7X', 'Falcon-8X', 'Falcon-2000'):
            return False
        return all_of(('Altitude When Descending', 'DH Selected'), available)

    def derive(self, alt_descending=KTI('Altitude When Descending'),
               dh_selected=P('DH Selected')):
        pass


class AltitudeDeviationFromAltitudeSelectedMax(KeyPointValueNode):

    @classmethod
    def can_operate(cls, available, manufacturer=A('Manufacturer')):
        if manufacturer and manufacturer.value == 'Airbus':
            baro_setting_sel = any((
                any_of(('Baro Setting Selection', 'Baro Correction (ISIS)'), available),
                all_of(('Baro Setting Selection (Capt)', 'Baro Setting Selection (FO)'), available)
            ))
            if not baro_setting_sel:
                return False
        return all_of(
            ('Altitude QNH', 'Altitude Selected', 'Airborne', 'Approach And Landing'),
            available
        )

    def derive(self, alt=P('Altitude QNH'),
               alt_sel=P('Altitude Selected'),
               airborne=S('Airborne'),
               apps=S('Approach And Landing'),
               bar_sel=P('Baro Setting Selection'),
               bar_sel_cpt=P('Baro Setting Selection (Capt)'),
               bar_sel_fo=P('Baro Setting Selection (FO)'),
               bar_cor_isis=P('Baro Correction (ISIS)')):
        pass
