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


class AOAAbnormalOperation(MultistateDerivedParameterNode):
    name = 'AOA Abnormal Operation'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
                 aoa_l_fail=P('AOA (L) Failure'),
                 aoa_l_signal_fail=P('AOA (L) Signal Failure'),
                 aoa_l_heater=P('AOA (L) Primary Heater'),
                 aoa_r_fail=P('AOA (R) Failure'),
                 aoa_r_signal_fail=P('AOA (R) Signal Failure'),
                 aoa_r_heater=P('AOA (R) Primary Heater'),
                 aoa_signal_fail=P('AOA Signal Failure'),
                 aoa_sec_heater=P('AOA Secondary Heater'),
                 aoa_correction=P('AOA Correction Program'),):
        pass


class APEngaged(MultistateDerivedParameterNode):
    name = 'AP Engaged'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               ap1=M('AP (1) Engaged'),
               ap2=M('AP (2) Engaged'),
               ap3=M('AP (3) Engaged')):
        pass


class APChannelsEngaged(MultistateDerivedParameterNode):
    name = 'AP Channels Engaged'

    @classmethod
    def can_operate(cls, available):
        return len(available) >= 2

    def derive(self,
               ap1=M('AP (1) Engaged'),
               ap2=M('AP (2) Engaged'),
               ap3=M('AP (3) Engaged')):
        pass


class APLateralMode(MultistateDerivedParameterNode):
    name = 'AP Lateral Mode'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               lateral_mode_selected=M('Lateral Mode Selected'),
               runway_mode_active=M('Runway Mode Active'),
               nav_mode_active=M('NAV Mode Active'),
               ils_localizer_capture_active=M('ILS Localizer Capture Active'),
               ils_localizer_track_active=M('ILS Localizer Track Active'),
               roll_go_around_mode_active=M('Roll Go Around Mode Active'),
               land_track_active=M('Land Track Active'),
               heading_mode_active=M('Heading Mode Active')):
        pass


class APVerticalMode(MultistateDerivedParameterNode):
    name = 'AP Vertical Mode'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               at_active=M('AT Active'),
               climb_mode_active=M('Climb Mode Active'),
               longitudinal_mode_selected=M('Longitudinal Mode Selected'),
               ils_glideslope_capture_active=M('ILS Glideslope Capture Active'),
               ils_glideslope_active=M('ILS Glideslope Active'),
               flare_mode=M('Flare Mode'),
               open_climb_mode=M('Open Climb Mode'),
               open_descent_mode=M('Open Descent Mode'),
               altitude_capture_mode=M('Altitude Capture Mode'),
               altitude_mode=M('Altitude Mode'),
               expedite_climb_mode=M('Expedite Climb Mode'),
               expedite_descent_mode=M('Expedite Descent Mode'),
               vert_spd_engaged=M('Vertical Speed Engaged'),
               pitch_mode=M('Pitch Mode'),):
        pass


class APUOn(MultistateDerivedParameterNode):
    name = 'APU On'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, apu_1=M('APU (1) On'), apu_2=M('APU (2) On')):
        pass


class APURunning(MultistateDerivedParameterNode):
    name = 'APU Running'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, apu_n1=P('APU N1'),
               apu_voltage=P('APU Generator AC Voltage'),
               apu_bleed_valve_open=M('APU Bleed Valve Open'),
               apu_fuel_flow=P('APU Fuel Flow'),
               apu_on=M('APU On')):
        pass


class CargoSmokeOrFire(MultistateDerivedParameterNode):
    name = 'Cargo (*) Smoke Or Fire'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               s_cargo_warn=P('Smoke Cargo Warning'),
               s_cargo1_warn=P('Smoke Cargo (1) Warning'),
               s_cargo2_warn=P('Smoke Cargo (2) Warning'),
               s_cargo_aft_warn=P('Smoke Cargo Aft Warning'),
               s_cargo_aft1_warn=P('Smoke Cargo Aft (1) Warning'),
               s_cargo_aft2_warn=P('Smoke Cargo Aft (2) Warning'),
               s_cargo_fwd_warn=P('Smoke Cargo Fwd Warning'),
               s_cargo_fwd1_warn=P('Smoke Cargo Fwd (1) Warning'),
               s_cargo_fwd2_warn=P('Smoke Cargo Fwd (2) Warning'),
               s_cargo_fwd3_warn=P('Smoke Cargo Fwd (3) Warning'),
               s_cargo_loweraft_warn=P('Smoke Cargo Lower Aft Warning'),
               s_cargo_loweraft1_warn=P('Smoke Cargo Lower Aft (1) Warning'),
               s_cargo_loweraft2_warn=P('Smoke Cargo Lower Aft (2) Warning'),
               s_cargo_loweraft3_warn=P('Smoke Cargo Lower Aft (3) Warning'),
               s_cargo_loweraft4_warn=P('Smoke Cargo Lower Aft (4) Warning'),
               s_cargo_lowerfwd_warn=P('Smoke Cargo Lower Fwd Warning'),
               s_cargo_lowerfwd1_warn=P('Smoke Cargo Lower Fwd (1) Warning'),
               s_cargo_lowerfwd2_warn=P('Smoke Cargo Lower Fwd (2) Warning'),
               s_cargo_lowerfwd3_warn=P('Smoke Cargo Lower Fwd (3) Warning'),
               s_cargo_lowerfwd4_warn=P('Smoke Cargo Lower Fwd (4) Warning'),
               s_cargo_rest_warn=P('Smoke Cargo Rest Warning'),
               s_cargo_rest1_warn=P('Smoke Cargo Rest (1) Warning'),
               s_cargo_rest2_warn=P('Smoke Cargo Rest (2) Warning'),
               s_cargo_upperaft1_warn=P('Smoke Cargo Upper Aft (1) Warning'),
               s_cargo_upperaft2_warn=P('Smoke Cargo Upper Aft (2) Warning'),
               s_cargo_upperaft3_warn=P('Smoke Cargo Upper Aft (3) Warning'),
               s_cargo_upperaft4_warn=P('Smoke Cargo Upper Aft (4) Warning'),
               s_cargo_upperfwd1_warn=P('Smoke Cargo Upper Fwd (1) Warning'),
               s_cargo_upperfwd2_warn=P('Smoke Cargo Upper Fwd (2) Warning'),
               s_cargo_upperfwd3_warn=P('Smoke Cargo Upper Fwd (3) Warning'),
               s_cargo_upperfwd4_warn=P('Smoke Cargo Upper Fwd (4) Warning'),
               f_cargo=P('Cargo Fire'),
               f_cargo_aft=P('Cargo Aft Fire'),
               f_cargo_aft1=P('Cargo Aft Fire (1)'),
               f_cargo_aft2=P('Cargo Aft Fire (2)'),
               f_cargo_aft3=P('Cargo Aft Fire (3)'),
               f_cargo_aft4=P('Cargo Aft Fire (4)'),
               f_cargo_fwd=P('Cargo Fwd Fire'),
               f_cargo_fwd1=P('Cargo Fwd Fire (1)'),
               f_cargo_fwd2=P('Cargo Fwd Fire (2)'),
               f_cargo_fwd3=P('Cargo Fwd Fire (3)'),
               f_cargo_fwd4=P('Cargo Fwd Fire (4)'),
               ):
        pass


class Configuration(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available, model=A('Model'), series=A('Series'), family=A('Family'),
                    manufacturer=A('Manufacturer'),):
        if manufacturer and manufacturer.value not in ('Airbus', 'Embraer'):
            return False
        if family and family.value in ('A300', 'A310',):
            return False
        if not all_of(
            ('Slat Including Transition', 'Flap Including Transition', 'Manufacturer', 'Model', 'Series', 'Family'),
            available,
        ):
            return False
        if manufacturer and manufacturer.value == 'Embraer' and not all_of(('Approach And Landing', 'Taxi In'), available):
            return False
        try:
            at.get_conf_angles(model.value, series.value, family.value, manufacturer.value)
        except KeyError:
            cls.warning("No conf angles available for '%s', '%s', '%s'.",
                        model.value, series.value, family.value)
            return False
        return True

    def derive(self, flap=M('Flap Including Transition'), slat=M('Slat Including Transition'),
               model=A('Model'), series=A('Series'), family=A('Family'), manufacturer=A('Manufacturer'),
               approach_landing=S('Approach And Landing'), taxi_in=S('Taxi In')):
        pass


class ConfigurationExcludingTransition(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available, model=A('Model'), series=A('Series'), family=A('Family'),
                    manufacturer=A('Manufacturer'),):
        if manufacturer and not manufacturer.value == 'Airbus':
            return False
        if family and family.value in ('A300', 'A310',):
            return False
        if not all_of((
            'Slat Excluding Transition', 'Flap Excluding Transition', 'Manufacturer', 'Model', 'Series', 'Family'
        ), available):
            return False
        try:
            at.get_conf_angles(model.value, series.value, family.value)
        except KeyError:
            cls.warning("No conf angles available for '%s', '%s', '%s'.",
                        model.value, series.value, family.value)
            return False
        return True

    def derive(self, flap=M('Flap Excluding Transition'), slat=M('Slat Excluding Transition'),
               model=A('Model'), series=A('Series'), family=A('Family'), manufacturer=A('Manufacturer'),
               conf=M('Configuration')):
        pass


class Daylight(MultistateDerivedParameterNode):

    def derive(self,
               latitude=P('Latitude Smoothed'),
               longitude=P('Longitude Smoothed'),
               start_datetime=A('Start Datetime'),
               duration=A('HDF Duration')):
        pass


class DualInput(MultistateDerivedParameterNode):

    def derive(self,
               pilot=M('Pilot Flying'),
               stick_capt=P('Sidestick Angle (Capt)'),
               stick_fo=P('Sidestick Angle (FO)'),
               family=A('Family'),
               ):
        pass


class Eng_1_Fire(MultistateDerivedParameterNode):
    name = 'Eng (1) Fire'

    def derive(self,
               fire_gnd=M('Eng (1) Fire On Ground'),
               fire_air=M('Eng (1) Fire In Air')):
        pass


class Eng_2_Fire(MultistateDerivedParameterNode):
    name = 'Eng (2) Fire'

    def derive(self,
               fire_gnd=M('Eng (2) Fire On Ground'),
               fire_air=M('Eng (2) Fire In Air')):
        pass


class Eng_3_Fire(MultistateDerivedParameterNode):
    name = 'Eng (3) Fire'

    def derive(self,
               fire_gnd=M('Eng (3) Fire On Ground'),
               fire_air=M('Eng (3) Fire In Air')):
        pass


class Eng_4_Fire(MultistateDerivedParameterNode):
    name = 'Eng (4) Fire'

    def derive(self,
               fire_gnd=M('Eng (4) Fire On Ground'),
               fire_air=M('Eng (4) Fire In Air')):
        pass


class Eng_Fire(MultistateDerivedParameterNode):
    name = 'Eng (*) Fire'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=M('Eng (1) Fire'),
               eng2=M('Eng (2) Fire'),
               eng3=M('Eng (3) Fire'),
               eng4=M('Eng (4) Fire'),
               eng1_1l=M('Eng (1) Fire (1L)'),
               eng1_1r=M('Eng (1) Fire (1R)'),
               eng1_2l=M('Eng (1) Fire (2L)'),
               eng1_2r=M('Eng (1) Fire (2R)'),
               ):
        pass


class Eng_Oil_Press_Warning(MultistateDerivedParameterNode):
    name = 'Eng (*) Oil Press Warning'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=P('Eng (1) Oil Press Low'),
               eng2=P('Eng (2) Oil Press Low'),
               eng3=P('Eng (3) Oil Press Low'),
               eng4=P('Eng (4) Oil Press Low'),
               ):
        pass


class EngBleedOpen(MultistateDerivedParameterNode):
    name = 'Eng Bleed Open'

    @classmethod
    def can_operate(cls, available):
        return all_of((
            'Eng (1) Bleed',
            'Eng (2) Bleed',
        ), available)

    def derive(self,
               b1=M('Eng (1) Bleed'),
               b2=M('Eng (2) Bleed'),
               b3=M('Eng (3) Bleed'),
               b4=M('Eng (4) Bleed')):
        pass


class EngRunning(object):
    engnum = 0

    @classmethod
    def can_operate(cls, available):
        return 'Eng (%d) N1' % cls.engnum in available or \
               'Eng (%d) N2' % cls.engnum in available or \
               'Eng (%d) Np' % cls.engnum in available or \
               'Eng (%d) Fuel Flow' % cls.engnum in available


class Eng1Running(EngRunning, MultistateDerivedParameterNode):
    engnum = 1
    name = 'Eng (1) Running'

    def derive(self,
               eng_n1=P('Eng (1) N1'),
               eng_n2=P('Eng (1) N2'),
               eng_np=P('Eng (1) Np'),
               fuel_flow=P('Eng (1) Fuel Flow'),
               ac_type=A('Aircraft Type')):
        pass


class Eng2Running(EngRunning, MultistateDerivedParameterNode):
    engnum = 2
    name = 'Eng (2) Running'

    def derive(self,
               eng_n1=P('Eng (2) N1'),
               eng_n2=P('Eng (2) N2'),
               eng_np=P('Eng (2) Np'),
               fuel_flow=P('Eng (2) Fuel Flow'),
               ac_type=A('Aircraft Type')):
        pass


class Eng3Running(EngRunning, MultistateDerivedParameterNode):
    engnum = 3
    name = 'Eng (3) Running'

    def derive(self,
               eng_n1=P('Eng (3) N1'),
               eng_n2=P('Eng (3) N2'),
               eng_np=P('Eng (3) Np'),
               fuel_flow=P('Eng (3) Fuel Flow'),
               ac_type=A('Aircraft Type')):
        pass


class Eng4Running(EngRunning, MultistateDerivedParameterNode):
    engnum = 4
    name = 'Eng (4) Running'

    def derive(self,
               eng_n1=P('Eng (4) N1'),
               eng_n2=P('Eng (4) N2'),
               eng_np=P('Eng (4) Np'),
               fuel_flow=P('Eng (4) Fuel Flow'),
               ac_type=A('Aircraft Type')):
        pass


class Eng_AllRunning(MultistateDerivedParameterNode, EngRunning):
    name = 'Eng (*) All Running'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type == helicopter:
            return 'Eng (*) N1 Min' in available
        else:
            return 'Eng (*) N1 Min' in available or \
                   'Eng (*) N2 Min' in available or \
                   'Eng (*) Np Min' in available or \
                   'Eng (*) Fuel Flow Min' in available

    def derive(self,
               eng_n1=P('Eng (*) N1 Min'),
               eng_n2=P('Eng (*) N2 Min'),
               eng_np=P('Eng (*) Np Min'),
               fuel_flow=P('Eng (*) Fuel Flow Min'),
               ac_type=A('Aircraft Type')):
        pass


class Eng_AnyRunning(MultistateDerivedParameterNode, EngRunning):
    name = 'Eng (*) Any Running'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        if ac_type == helicopter:
            return 'Eng (*) N1 Max' in available
        else:
            return 'Eng (*) N1 Max' in available or \
                   'Eng (*) N2 Max' in available or \
                   'Eng (*) Np Max' in available or \
                   'Eng (*) Fuel Flow Max' in available

    def derive(self,
               eng_n1=P('Eng (*) N1 Max'),
               eng_n2=P('Eng (*) N2 Max'),
               eng_np=P('Eng (*) Np Max'),
               fuel_flow=P('Eng (*) Fuel Flow Max'),
               ac_type=A('Aircraft Type')):
        pass


class ThrustModeSelected(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               thrust_l=P('Thrust Mode Selected (L)'),
               thrust_r=P('Thrust Mode Selected (R)')):
        pass


class EventMarker(MultistateDerivedParameterNode):
    name = 'Event Marker'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               event_marker_1=M('Event Marker (1)'),
               event_marker_2=M('Event Marker (2)'),
               event_marker_3=M('Event Marker (3)'),
               event_marker_capt=M('Event Marker (Capt)'),
               event_marker_fo=M('Event Marker (FO)')):
        pass


class Flap(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available, frame=A('Frame'),
                    model=A('Model'), series=A('Series'), family=A('Family')):
        frame_name = frame.value if frame else None
        family_name = family.value if family else None
        if frame_name == 'L382-Hercules' or family_name == 'C208':
            return 'Altitude AAL' in available
        if family_name == 'Citation VLJ':
            return all_of(('HDF Duration', 'Landing', 'Takeoff'), available)
        if not all_of(('Flap Angle', 'Model', 'Series', 'Family'), available):
            return False
        try:
            at.get_flap_map(model.value, series.value, family.value)
        except KeyError:
            cls.exception("No flap mapping available for '%s', '%s', '%s'.",
                          model.value, series.value, family.value)
            return False
        return True

    def derive(self, flap=P('Flap Angle'),
               model=A('Model'), series=A('Series'), family=A('Family'),
               frame=A('Frame'), alt_aal=P('Altitude AAL'),
               hdf_duration=A('HDF Duration'),
               toffs=S('Takeoff'), lands=S('Landing')):
        pass


class FlapLever(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family')):
        if not all_of(('Flap Lever Angle', 'Model', 'Series', 'Family'), available):
            return False
        try:
            at.get_lever_map(model.value, series.value, family.value)
        except KeyError:
            cls.debug("No lever mapping available for '%s', '%s', '%s'.",
                      model.value, series.value, family.value)
            return False
        return True

    def derive(self, flap_lever=P('Flap Lever Angle'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class FlapIncludingTransition(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family')):
        if not all_of(('Flap Angle', 'Model', 'Series', 'Family'), available):
            return all_of(('Flap', 'Model', 'Series', 'Family'), available)
        try:
            at.get_flap_map(model.value, series.value, family.value)
        except KeyError:
            cls.debug("No lever mapping available for '%s', '%s', '%s'.",
                      model.value, series.value, family.value)
            return False
        return True

    def derive(self, flap_angle=P('Flap Angle'), flap=M('Flap'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class FlapExcludingTransition(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family')):
        if not all_of(('Flap Angle', 'Model', 'Series', 'Family'), available):
            return False
        try:
            at.get_flap_map(model.value, series.value, family.value)
        except KeyError:
            cls.debug("No lever mapping available for '%s', '%s', '%s'.",
                      model.value, series.value, family.value)
            return False
        return True

    def derive(self, flap_angle=P('Flap Angle'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class FlapLeverSynthetic(MultistateDerivedParameterNode):
    name = 'Flap Lever (Synthetic)'

    @classmethod
    def can_operate(cls, available, manufacturer=A('Manufacturer'),
                    model=A('Model'), series=A('Series'), family=A('Family')):
        if not all_of(('Flap', 'Model', 'Series', 'Family', 'Manufacturer'), available):
            return False
        try:
            angles = at.get_conf_angles(model.value, series.value, family.value)
        except KeyError:
            try:
                angles = at.get_lever_angles(model.value, series.value, family.value)
            except KeyError:
                cls.warning("No lever angles available for '%s', '%s', '%s'.",
                            model.value, series.value, family.value)
                return False
        can_operate = True
        slat_required = any(slat is not None for slat, flap, flaperon in
                            angles.values())
        if slat_required:
            can_operate = can_operate and 'Slat' in available
        flaperon_required = any(flaperon is not None for slat, flap, flaperon in
                                angles.values())
        if flaperon_required:
            can_operate = can_operate and 'Flaperon' in available
        return can_operate

    def derive(self, flap=M('Flap'), slat=M('Slat'), flaperon=M('Flaperon'), manufacturer=A('Manufacturer'),
               model=A('Model'), series=A('Series'), family=A('Family'),
               approach=S('Approach And Landing'), frame=A('Frame'),):
        pass


class Flaperon(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family')):
        if not all_of(('Aileron (L)', 'Aileron (R)', 'Model', 'Series', 'Family'), available):
            return False
        try:
            at.get_aileron_map(model.value, series.value, family.value)
        except KeyError:
            cls.debug("No aileron/flaperon mapping available for '%s', '%s', '%s'.",
                      model.value, series.value, family.value)
            return False
        return True

    def derive(self, al=P('Aileron (L)'), ar=P('Aileron (R)'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class FuelQty_Low(MultistateDerivedParameterNode):
    name = "Fuel Qty (*) Low"

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, fqty=M('Fuel Qty Low'),
               fqty1=M('Fuel Qty (L) Low'),
               fqty2=M('Fuel Qty (R) Low')):
        pass


class GearDown(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        gear_lever = all_of(('Gear Down Selected', 'Gear Down In Transit'), available)
        return 'Gear Position' in available or gear_lever

    def derive(self,
               gear_transit=M('Gear Down In Transit'),
               gear_sel=M('Gear Down Selected'),
               gear_pos=M('Gear Position')):
        pass


class GearDownInTransit(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available, model=A('Model'), series=A('Series'), family=A('Family')):
        gears_available = all_of(('Gear Down', 'Gear Down Selected'), available) \
            or all_of(('Gear Up', 'Gear Down'), available) \
            or all_of(('Gear Down Selected', 'Gear In Transit'), available) \
            or all_of(('Gear Up', 'Gear In Transit'), available) \
            or all_of(('Gear Down', 'Gear In Transit'), available) \
            or all_of(('Gear Down Selected', 'Gear (*) Red Warning'), available) \
            or all_of(('Gear Up', 'Gear (*) Red Warning'), available) \
            or all_of(('Gear Down', 'Gear (*) Red Warning'), available) \
            or 'Gear Position' in available
        if gears_available:
            return True
        if all_of(('Model', 'Series', 'Family', 'Airborne'), available) \
           and any_of(('Gear Down Selected', 'Gear Up', 'Gear Down'), available):
            if model and series and family:
                try:
                    at.get_gear_transition_times(model.value, series.value, family.value)
                except KeyError:
                    cls.exception("No gear transition times available for '%s', '%s', '%s'.",
                                  model.value, series.value, family.value)
                    return False
                return True
            else:
                return False
        else:
            return False

    def derive(self,
               gear_down=M('Gear Down'),
               gear_up=M('Gear Up'),
               gear_down_sel=M('Gear Down Selected'),
               gear_in_transit=M('Gear In Transit'),
               gear_red=M('Gear (*) Red Warning'),
               gear_position=M('Gear Position'),
               airborne=S('Airborne'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class GearUpInTransit(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available, model=A('Model'), series=A('Series'), family=A('Family')):
        gears_available = all_of(('Gear Up', 'Gear Up Selected'), available) \
            or all_of(('Gear Down', 'Gear Up'), available) \
            or all_of(('Gear Up Selected', 'Gear In Transit'), available) \
            or all_of(('Gear Up', 'Gear In Transit'), available) \
            or all_of(('Gear Down', 'Gear In Transit'), available) \
            or all_of(('Gear Up Selected', 'Gear (*) Red Warning'), available) \
            or all_of(('Gear Up', 'Gear (*) Red Warning'), available) \
            or all_of(('Gear Down', 'Gear (*) Red Warning'), available) \
            or 'Gear Position' in available
        if gears_available:
            return True
        if all_of(('Model', 'Series', 'Family', 'Airborne'), available) \
           and any_of(('Gear Up Selected', 'Gear Up', 'Gear Down'), available):
            if model and series and family:
                try:
                    at.get_gear_transition_times(model.value, series.value, family.value)
                except KeyError:
                    cls.exception("No gear transition times available for '%s', '%s', '%s'.",
                                  model.value, series.value, family.value)
                    return False
                return True
        else:
            return False

    def derive(self,
               gear_down=M('Gear Down'),
               gear_up=M('Gear Up'),
               gear_up_sel=M('Gear Up Selected'),
               gear_in_transit=M('Gear In Transit'),
               gear_red=M('Gear (*) Red Warning'),
               gear_position=M('Gear Position'),
               airborne=S('Airborne'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class GearUp(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        calc_gear_up = all_of(('Gear Up Selected', 'Gear Up In Transit'), available)
        gear_pos = 'Gear Position' in available
        return calc_gear_up or gear_pos

    def derive(self,
               gear_transit=M('Gear Up In Transit'),
               gear_sel=M('Gear Up Selected'),
               gear_pos=M('Gear Position')):
        pass


class GearInTransit(MultistateDerivedParameterNode):

    def derive(self,
               gear_down_transit=M('Gear Down In Transit'),
               gear_up_transit=M('Gear Up In Transit')):
        pass


class GearOnGround(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(('Gear (L) On Ground', 'Gear (R) On Ground'), available)

    def derive(self,
               gl=M('Gear (L) On Ground'),
               gr=M('Gear (R) On Ground')):
        pass


class GearDownSelected(MultistateDerivedParameterNode):

    def derive(self, up_sel=M('Gear Up Selected')):
        pass


class GearUpSelected(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return all_of(('Gear Up', 'Gear Up In Transit'), available) or \
               all_of(('Gear Down', 'Gear Down In Transit'), available) or \
               'Gear Down Selected' in available

    def derive(self,
               gear_up=M('Gear Up'),
               gear_up_transit=M('Gear Up In Transit'),
               gear_down=M('Gear Down'),
               gear_down_transit=M('Gear Down In Transit'),
               gear_down_sel=M('Gear Down Selected')):
        pass


class Gear_RedWarning(MultistateDerivedParameterNode):
    name = 'Gear (*) Red Warning'

    @classmethod
    def can_operate(cls, available):
        return 'Airborne' in available and any_of((
            'Gear (L) Red Warning',
            'Gear (N) Red Warning',
            'Gear (R) Red Warning',
        ), available)

    def derive(self,
               gear_warn_l=M('Gear (L) Red Warning'),
               gear_warn_n=M('Gear (N) Red Warning'),
               gear_warn_r=M('Gear (R) Red Warning'),
               airs=S('Airborne')):
        pass


class ILSInnerMarker(MultistateDerivedParameterNode):
    name = 'ILS Inner Marker'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               ils_mkr_capt=M('ILS Inner Marker (Capt)'),
               ils_mkr_fo=M('ILS Inner Marker (FO)')):
        pass


class ILSMiddleMarker(MultistateDerivedParameterNode):
    name = 'ILS Middle Marker'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               ils_mkr_capt=M('ILS Middle Marker (Capt)'),
               ils_mkr_fo=M('ILS Middle Marker (FO)')):
        pass


class ILSOuterMarker(MultistateDerivedParameterNode):
    name = 'ILS Outer Marker'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               ils_mkr_capt=M('ILS Outer Marker (Capt)'),
               ils_mkr_fo=M('ILS Outer Marker (FO)')):
        pass


class KeyVHFCapt(MultistateDerivedParameterNode):
    name = 'Key VHF (Capt)'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, key_vhf_1=M('Key VHF (1) (Capt)'),
               key_vhf_2=M('Key VHF (2) (Capt)'),
               key_vhf_3=M('Key VHF (3) (Capt)')):
        pass


class KeyVHFFO(MultistateDerivedParameterNode):
    name = 'Key VHF (FO)'

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, key_vhf_1=M('Key VHF (1) (FO)'),
               key_vhf_2=M('Key VHF (2) (FO)'),
               key_vhf_3=M('Key VHF (3) (FO)')):
        pass


class MasterCaution(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               capt=M('Master Caution (Capt)'),
               fo=M('Master Caution (FO)'),
               capt_2=M('Master Caution (Capt) (2)'),
               fo_2=M('Master Caution (FO) (2)'),
               ):
        pass


class MasterWarning(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               warn_capt=M('Master Warning (Capt)'),
               warn_fo=M('Master Warning (FO)')):
        pass


class PackValvesOpen(MultistateDerivedParameterNode):
    name = 'Pack Valves Open'

    @classmethod
    def can_operate(cls, available):
        '''
        '''
        return all_of(['ECS Pack (1) On', 'ECS Pack (2) On'], available)

    def derive(self,
               p1=M('ECS Pack (1) On'), p1h=M('ECS Pack (1) High Flow'),
               p2=M('ECS Pack (2) On'), p2h=M('ECS Pack (2) High Flow')):
        pass


class PilotFlying(MultistateDerivedParameterNode):

    def derive(self,
               stick_capt=P('Sidestick Angle (Capt)'),
               stick_fo=P('Sidestick Angle (FO)')):
        pass


class PitchAlternateLaw(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               alt_law_1=M('Pitch Alternate Law (1)'),
               alt_law_2=M('Pitch Alternate Law (2)')):
        pass


class PitchDisconnect(MultistateDerivedParameterNode):

    def derive(self, pitch_1=M('Pitch Disconnect (1)'),
                     pitch_2=M('Pitch Disconnect (2)'),):
        pass


class Slat(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family')):
        if not all_of(('Slat Angle', 'Model', 'Series', 'Family'), available):
            return False
        try:
            at.get_slat_map(model.value, series.value, family.value)
        except KeyError:
            cls.debug("No slat mapping available for '%s', '%s', '%s'.",
                      model.value, series.value, family.value)
            return False
        return True

    def derive(self, slat=P('Slat Angle'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class SlatExcludingTransition(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family')):
        if not all_of(('Slat Angle', 'Model', 'Series', 'Family'), available):
            return False
        try:
            at.get_slat_map(model.value, series.value, family.value)
        except KeyError:
            cls.debug("No slat mapping available for '%s', '%s', '%s'.",
                      model.value, series.value, family.value)
            return False
        return True

    def derive(self, slat=P('Slat Angle'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class SlatIncludingTransition(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available,
                    model=A('Model'), series=A('Series'), family=A('Family')):
        if not all_of(('Slat Angle', 'Model', 'Series', 'Family'), available):
            return False
        try:
            at.get_slat_map(model.value, series.value, family.value)
        except KeyError:
            cls.debug("No slat mapping available for '%s', '%s', '%s'.",
                      model.value, series.value, family.value)
            return False
        return True

    def derive(self, slat=P('Slat Angle'),
               model=A('Model'), series=A('Series'), family=A('Family')):
        pass


class SlatFullyExtended(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               slat_l1=P('Slat (L1) Fully Extended'),
               slat_l2=P('Slat (L2) Fully Extended'),
               slat_l3=P('Slat (L3) Fully Extended'),
               slat_l4=P('Slat (L4) Fully Extended'),
               slat_r1=P('Slat (R1) Fully Extended'),
               slat_r2=P('Slat (R2) Fully Extended'),
               slat_r3=P('Slat (R3) Fully Extended'),
               slat_r4=P('Slat (R4) Fully Extended'),
               slat_1=P('Slat (1) Fully Extended'),
               slat_2=P('Slat (2) Fully Extended'),
               slat_3=P('Slat (3) Fully Extended'),
               slat_4=P('Slat (4) Fully Extended'),
               slat_5=P('Slat (5) Fully Extended'),
               slat_6=P('Slat (6) Fully Extended'),
               slat_7=P('Slat (7) Fully Extended'),
               slat_8=P('Slat (8) Fully Extended'),):
        pass


class SlatPartExtended(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               slat_l1=P('Slat (L1) Part Extended'),
               slat_l2=P('Slat (L2) Part Extended'),
               slat_l3=P('Slat (L3) Part Extended'),
               slat_l4=P('Slat (L4) Part Extended'),
               slat_r1=P('Slat (R1) Part Extended'),
               slat_r2=P('Slat (R2) Part Extended'),
               slat_r3=P('Slat (R3) Part Extended'),
               slat_r4=P('Slat (R4) Part Extended'),
               slat_1=P('Slat (1) Part Extended'),
               slat_2=P('Slat (2) Part Extended'),
               slat_3=P('Slat (3) Part Extended'),
               slat_4=P('Slat (4) Part Extended'),
               slat_5=P('Slat (5) Part Extended'),
               slat_6=P('Slat (6) Part Extended'),
               slat_7=P('Slat (7) Part Extended'),
               slat_8=P('Slat (8) Part Extended')):
        pass


class SlatInTransit(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               slat_l1=P('Slat (L1) In Transit'),
               slat_l2=P('Slat (L2) In Transit'),
               slat_l3=P('Slat (L3) In Transit'),
               slat_l4=P('Slat (L4) In Transit'),
               slat_r1=P('Slat (R1) In Transit'),
               slat_r2=P('Slat (R2) In Transit'),
               slat_r3=P('Slat (R3) In Transit'),
               slat_r4=P('Slat (R4) In Transit'),
               slat_1=P('Slat (1) In Transit'),
               slat_2=P('Slat (2) In Transit'),
               slat_3=P('Slat (3) In Transit'),
               slat_4=P('Slat (4) In Transit'),
               slat_5=P('Slat (5) In Transit'),
               slat_6=P('Slat (6) In Transit'),
               slat_7=P('Slat (7) In Transit'),
               slat_8=P('Slat (8) In Transit')):
        pass


class SlatRetracted(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               slat_l1=P('Slat (L1) Retracted'),
               slat_l2=P('Slat (L2) Retracted'),
               slat_l3=P('Slat (L3) Retracted'),
               slat_l4=P('Slat (L4) Retracted'),
               slat_r1=P('Slat (R1) Retracted'),
               slat_r2=P('Slat (R2) Retracted'),
               slat_r3=P('Slat (R3) Retracted'),
               slat_r4=P('Slat (R4) Retracted')):
        pass


class StickPusher(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, spl=M('Stick Pusher (L)'),
               spr=M('Stick Pusher (R)')):
        pass


class StickShaker(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Stick Shaker (L)',
            'Stick Shaker (R)',
            'Stick Shaker (1)',
            'Stick Shaker (2)',
            'Stick Shaker (3)',
            'Stick Shaker (4)',
        ), available)

    def derive(self, ssl=M('Stick Shaker (L)'),
               ssr=M('Stick Shaker (R)'),
               ss1=M('Stick Shaker (1)'),
               ss2=M('Stick Shaker (2)'),
               ss3=M('Stick Shaker (3)'),
               ss4=M('Stick Shaker (4)'),
               frame=A('Frame')):
        pass


class StallWarning(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Stall Warning (1)',
            'Stall Warning (2)',
        ), available)

    def derive(self,
               ss1=M('Stall Warning (1)'),
               ss2=M('Stall Warning (2)'),
               frame=A('Frame'),
               ):
        pass


class SmokeWarning(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               smoke_avionics=M('Smoke Avionics Warning'),
               smoke_avionics_1=M('Smoke Avionics (1) Warning'),
               smoke_avionics_2=M('Smoke Avionics (2) Warning'),
               smoke_lav=M('Smoke Lavatory Warning'),
               smoke_lav_1=M('Smoke Lavatory (1) Warning'),
               smoke_lav_2=M('Smoke Lavatory (2) Warning'),
               smoke_cabin=M('Smoke Cabin Warning'),
               smoke_cabin_1=M('Smoke Cabin Rest (1) Warning'),
               smoke_cabin_2=M('Smoke Cabin Rest (2) Warning'),
               smoke_cargo=M('Smoke Cargo Warning'),
               smoke_cargo_fwd_1=M('Smoke Cargo Fwd (1) Warning'),
               smoke_cargo_fwd_2=M('Smoke Cargo Fwd (2) Warning'),
               smoke_cargo_aft_1=M('Smoke Cargo Aft (1) Warning'),
               smoke_cargo_aft_2=M('Smoke Cargo Aft (2) Warning'),
               smoke_cargo_rest_1=M('Smoke Cargo Rest (1) Warning'),
               smoke_cargo_rest_2=M('Smoke Cargo Rest (2) Warning'),
               smoke_lower_dec=M('Smoke Lower Deck Stowage'),
               smoke_avionic_bulk=M('Smoke Avionic Bulk'),
               smoke_ifec=M('Smoke IFEC'),
               smoke_bcrc=M('Smoke BCRC'),
               smoke_vcc=M('Smoke Autonomous VCC')):
        pass


class SpeedbrakeDeployed(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        if family and family.value == 'B787':
            return 'Speedbrake Handle' in available
        return 'Ground Spoiler Deployed' in available or \
               'Speedbrake (Tail) Deployed' in available or \
               all_of(('Spoiler (L) Deployed', 'Spoiler (R) Deployed'), available) or \
               all_of(('Ground Spoiler (L) Deployed', 'Ground Spoiler (R) Deployed'), available) or \
               all_of(('Spoiler (L) (1) Deployed', 'Spoiler (R) (1) Deployed'), available) or \
               all_of(('Spoiler (L) (2) Deployed', 'Spoiler (R) (2) Deployed'), available) or \
               all_of(('Spoiler (L) (3) Deployed', 'Spoiler (R) (3) Deployed'), available) or \
               all_of(('Spoiler (L) (4) Deployed', 'Spoiler (R) (4) Deployed'), available) or \
               all_of(('Spoiler (L) (5) Deployed', 'Spoiler (R) (5) Deployed'), available) or \
               all_of(('Spoiler (L) (6) Deployed', 'Spoiler (R) (6) Deployed'), available) or \
               all_of(('Spoiler (L) (7) Deployed', 'Spoiler (R) (7) Deployed'), available) or \
               all_of(('Ground Spoiler (L) (1) Deployed', 'Ground Spoiler (R) (1) Deployed'), available) or \
               all_of(('Ground Spoiler (L) (2) Deployed', 'Ground Spoiler (R) (2) Deployed'), available) or \
               all_of(('Spoiler (L) Outboard Deployed', 'Spoiler (R) Outboard Deployed'), available) or \
               'Spoiler' in available or \
               all_of(('Spoiler (L)', 'Spoiler (R)'), available) or \
               all_of(('Spoiler (L) (1)', 'Spoiler (R) (1)'), available) or \
               all_of(('Spoiler (L) (2)', 'Spoiler (R) (2)'), available) or \
               all_of(('Spoiler (L) (3)', 'Spoiler (R) (3)'), available) or \
               all_of(('Spoiler (L) (4)', 'Spoiler (R) (4)'), available) or \
               all_of(('Spoiler (L) (5)', 'Spoiler (R) (5)'), available) or \
               all_of(('Spoiler (L) (6)', 'Spoiler (R) (6)'), available) or \
               all_of(('Spoiler (L) (7)', 'Spoiler (R) (7)'), available) or \
               all_of(('Spoiler (L) Outboard', 'Spoiler (R) Outboard'), available)

    def derive(self, dep=M('Ground Spoiler Deployed'),
               tail=M('Speedbrake (Tail) Deployed'),
               ld=M('Spoiler (L) Deployed'),
               rd=M('Spoiler (R) Deployed'),
               gld=M('Ground Spoiler (L) Deployed'),
               grd=M('Ground Spoiler (R) Deployed'),
               l1d=M('Spoiler (L) (1) Deployed'),
               l2d=M('Spoiler (L) (2) Deployed'),
               l3d=M('Spoiler (L) (3) Deployed'),
               l4d=M('Spoiler (L) (4) Deployed'),
               l5d=M('Spoiler (L) (5) Deployed'),
               l6d=M('Spoiler (L) (6) Deployed'),
               l7d=M('Spoiler (L) (7) Deployed'),
               gl1d=M('Ground Spoiler (L) (1) Deployed'),
               gl2d=M('Ground Spoiler (L) (2) Deployed'),
               r1d=M('Spoiler (R) (1) Deployed'),
               r2d=M('Spoiler (R) (2) Deployed'),
               r3d=M('Spoiler (R) (3) Deployed'),
               r4d=M('Spoiler (R) (4) Deployed'),
               r5d=M('Spoiler (R) (5) Deployed'),
               r6d=M('Spoiler (R) (6) Deployed'),
               r7d=M('Spoiler (R) (7) Deployed'),
               gr1d=M('Ground Spoiler (R) (1) Deployed'),
               gr2d=M('Ground Spoiler (R) (2) Deployed'),
               loutd=M('Spoiler (L) Outboard Deployed'),
               routd=M('Spoiler (R) Outboard Deployed'),
               spoiler=P('Spoiler'),
               l=P('Spoiler (L)'),
               r=P('Spoiler (R)'),
               l1=P('Spoiler (L) (1)'),
               l2=P('Spoiler (L) (2)'),
               l3=P('Spoiler (L) (3)'),
               l4=P('Spoiler (L) (4)'),
               l5=P('Spoiler (L) (5)'),
               l6=P('Spoiler (L) (6)'),
               l7=P('Spoiler (L) (7)'),
               r1=P('Spoiler (R) (1)'),
               r2=P('Spoiler (R) (2)'),
               r3=P('Spoiler (R) (3)'),
               r4=P('Spoiler (R) (4)'),
               r5=P('Spoiler (R) (5)'),
               r6=P('Spoiler (R) (6)'),
               r7=P('Spoiler (R) (7)'),
               lout=P('Spoiler (L) Outboard'),
               rout=P('Spoiler (R) Outboard'),
               handle=P('Speedbrake Handle'),
               family=A('Family')):
        pass


class SpeedbrakeSelected(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available, family=A('Family')):
        '''
        '''
        x = available
        if family and family.value == 'BD-100':
            return 'Speedbrake Handle' in x and 'Speedbrake Armed' in x
        elif family and family.value == 'Global':
            return any_of(('Speedbrake', 'Speedbrake Handle'), available)
        elif family and family.value in ('CRJ 100/200', 'B777'):
            return 'Speedbrake Handle' in x
        elif family and family.value in ('A318', 'A319', 'A320', 'A321', 'MD-11'):
            return 'Speedbrake' in x and 'Speedbrake Armed' in x
        elif family and family.value in ('A340', 'A380'):
            return ('Speedbrake Deployed' in x or
                    all_of(('Speedbrake', 'Speedbrake Handle'), x))
        else:
            return ('Speedbrake Deployed' in x or
                    ('Family' in x and 'Speedbrake Switch' in x) or
                    ('Family' in x and 'Speedbrake Handle' in x) or
                    ('Family' in x and 'Speedbrake' in x))

    def derive(self,
               deployed=M('Speedbrake Deployed'),
               armed=M('Speedbrake Armed'),
               handle=P('Speedbrake Handle'),
               spdbrk=P('Speedbrake'),
               spdsw=M('Speedbrake Switch'),
               gnd_spoiler_armed=M('Ground Spoiler Armed'),
               family=A('Family')):
        pass

class StableApproachStages(object):
    pass


class StableApproach(MultistateDerivedParameterNode, StableApproachStages):

    @classmethod
    def can_operate(cls, available):
        deps = ['Approach Information', 'Descent', 'Gear Down', 'Flap',
                'Vertical Speed', 'Altitude AAL',]
        return all_of(deps, available) and (
            'Eng (*) N1 Avg For 10 Sec' in available or
            'Eng (*) EPR Avg For 10 Sec' in available)

    def derive(self,
               apps=A('Approach Information'),
               phases=S('Descent'),
               gear=M('Gear Down'),
               flap=M('Flap'),
               tdev=P('Track Deviation From Runway'),
               aspd_rel=P('Airspeed Relative For 3 Sec'),
               aspd_minus_sel=P('Airspeed Minus Airspeed Selected For 3 Sec'),
               vspd=P('Vertical Speed'),
               gdev=P('ILS Glideslope'),
               ldev=P('ILS Localizer'),
               eng_n1=P('Eng (*) N1 Avg For 10 Sec'),
               eng_epr=P('Eng (*) EPR Avg For 10 Sec'),
               alt=P('Altitude AAL'),
               vapp=P('Vapp'),
               family=A('Family'),
               model=A('Model')):
        pass


class StableApproachExcludingEngThrust(MultistateDerivedParameterNode, StableApproachStages):

    @classmethod
    def can_operate(cls, available):
        deps = ['Approach Information', 'Descent', 'Gear Down', 'Flap',
                'Vertical Speed', 'Altitude AAL',]
        return all_of(deps, available)

    def derive(self,
               apps=A('Approach Information'),
               phases=S('Descent'),
               gear=M('Gear Down'),
               flap=M('Flap'),
               tdev=P('Track Deviation From Runway'),
               aspd_rel=P('Airspeed Relative For 3 Sec'),
               aspd_minus_sel=P('Airspeed Minus Airspeed Selected For 3 Sec'),
               vspd=P('Vertical Speed'),
               gdev=P('ILS Glideslope'),
               ldev=P('ILS Localizer'),
               alt=P('Altitude AAL'),
               vapp=P('Vapp'),
               model=A('Model')):
        pass


class ThrustReversers(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of((
            'Eng (1) Thrust Reverser (L) Deployed',
            'Eng (1) Thrust Reverser (R) Deployed',
            'Eng (2) Thrust Reverser (L) Deployed',
            'Eng (2) Thrust Reverser (R) Deployed',
            'Eng (3) Thrust Reverser (L) Deployed',
            'Eng (3) Thrust Reverser (R) Deployed',
            'Eng (4) Thrust Reverser (L) Deployed',
            'Eng (4) Thrust Reverser (R) Deployed',
        ), available) or any_of((
            'Eng (1) Thrust Reverser Deployed',
            'Eng (2) Thrust Reverser Deployed',
            'Eng (3) Thrust Reverser Deployed',
            'Eng (4) Thrust Reverser Deployed',
        ), available) or any_of((
            'Eng (1) Thrust Reverser',
            'Eng (2) Thrust Reverser',
            'Eng (3) Thrust Reverser',
            'Eng (4) Thrust Reverser',
        ), available)

    def derive(self,
               e1_dep_all=M('Eng (1) Thrust Reverser Deployed'),
               e1_dep_lft=M('Eng (1) Thrust Reverser (L) Deployed'),
               e1_dep_rgt=M('Eng (1) Thrust Reverser (R) Deployed'),
               e1_ulk_all=M('Eng (1) Thrust Reverser Unlocked'),
               e1_ulk_lft=M('Eng (1) Thrust Reverser (L) Unlocked'),
               e1_ulk_rgt=M('Eng (1) Thrust Reverser (R) Unlocked'),
               e1_tst_all=M('Eng (1) Thrust Reverser In Transit'),
               e2_dep_all=M('Eng (2) Thrust Reverser Deployed'),
               e2_dep_lft=M('Eng (2) Thrust Reverser (L) Deployed'),
               e2_dep_rgt=M('Eng (2) Thrust Reverser (R) Deployed'),
               e2_ulk_all=M('Eng (2) Thrust Reverser Unlocked'),
               e2_ulk_lft=M('Eng (2) Thrust Reverser (L) Unlocked'),
               e2_ulk_rgt=M('Eng (2) Thrust Reverser (R) Unlocked'),
               e2_tst_all=M('Eng (2) Thrust Reverser In Transit'),
               e3_dep_all=M('Eng (3) Thrust Reverser Deployed'),
               e3_dep_lft=M('Eng (3) Thrust Reverser (L) Deployed'),
               e3_dep_rgt=M('Eng (3) Thrust Reverser (R) Deployed'),
               e3_ulk_all=M('Eng (3) Thrust Reverser Unlocked'),
               e3_ulk_lft=M('Eng (3) Thrust Reverser (L) Unlocked'),
               e3_ulk_rgt=M('Eng (3) Thrust Reverser (R) Unlocked'),
               e3_tst_all=M('Eng (3) Thrust Reverser In Transit'),
               e4_dep_all=M('Eng (4) Thrust Reverser Deployed'),
               e4_dep_lft=M('Eng (4) Thrust Reverser (L) Deployed'),
               e4_dep_rgt=M('Eng (4) Thrust Reverser (R) Deployed'),
               e4_ulk_all=M('Eng (4) Thrust Reverser Unlocked'),
               e4_ulk_lft=M('Eng (4) Thrust Reverser (L) Unlocked'),
               e4_ulk_rgt=M('Eng (4) Thrust Reverser (R) Unlocked'),
               e4_tst_all=M('Eng (4) Thrust Reverser In Transit'),
               e1_status=M('Eng (1) Thrust Reverser'),
               e2_status=M('Eng (2) Thrust Reverser'),
               e3_status=M('Eng (3) Thrust Reverser'),
               e4_status=M('Eng (4) Thrust Reverser')):
        pass


class ThrustReversersEffective(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        power_ok = any_of(('Eng (*) EPR Max', 'Eng (*) N1 Max'), available)
        return power_ok and all_of(('Thrust Reversers', 'Landing'), available)

    def derive(self,
               tr=M('Thrust Reversers'),
               eng_epr=P('Eng (*) EPR Max'),
               eng_n1=P('Eng (*) N1 Max'),
               landings=S('Landing')):
        pass


class TAWSAlert(MultistateDerivedParameterNode):
    name = 'TAWS Alert'

    @classmethod
    def can_operate(cls, available):
        return any_of(['TAWS Caution Terrain',
                       'TAWS Caution',
                       'TAWS Dont Sink',
                       'TAWS Glideslope',
                       'TAWS Predictive Windshear',
                       'TAWS Pull Up',
                       'TAWS Sink Rate',
                       'TAWS Terrain',
                       'TAWS Terrain Caution',
                       'TAWS Terrain Pull Up',
                       'TAWS Terrain Warning',
                       'TAWS Too Low Flap',
                       'TAWS Too Low Gear',
                       'TAWS Too Low Terrain',
                       'TAWS Windshear Warning',
                       ],
                      available)

    def derive(self, airs=S('Airborne'),
               taws_caution_terrain=M('TAWS Caution Terrain'),
               taws_caution=M('TAWS Caution'),
               taws_dont_sink=M('TAWS Dont Sink'),
               taws_glideslope=M('TAWS Glideslope'),
               taws_predictive_windshear=M('TAWS Predictive Windshear'),
               taws_pull_up=M('TAWS Pull Up'),
               taws_sink_rate=M('TAWS Sink Rate'),
               taws_terrain_pull_up=M('TAWS Terrain Pull Up'),
               taws_terrain_caution=M('TAWS Terrain Caution'),
               taws_terrain_warning=M('TAWS Terrain Warning'),
               taws_terrain=M('TAWS Terrain'),
               taws_too_low_flap=M('TAWS Too Low Flap'),
               taws_too_low_gear=M('TAWS Too Low Gear'),
               taws_too_low_terrain=M('TAWS Too Low Terrain'),
               taws_windshear_warning=M('TAWS Windshear Warning')):
        pass


class TAWSDontSink(MultistateDerivedParameterNode):
    name = 'TAWS Dont Sink'

    @classmethod
    def can_operate(cls, available):
        return ('TAWS (L) Dont Sink' in available) or \
               ('TAWS (R) Dont Sink' in available)

    def derive(self, taws_l_dont_sink=M('TAWS (L) Dont Sink'),
               taws_r_dont_sink=M('TAWS (R) Dont Sink')):
        pass


class TAWSGlideslopeCancel(MultistateDerivedParameterNode):
    name = 'TAWS Glideslope Cancel'

    @classmethod
    def can_operate(cls, available):
        return ('TAWS (L) Glideslope Cancel' in available) or \
               ('TAWS (R) Glideslope Cancel' in available)

    def derive(self, taws_l_gs=M('TAWS (L) Glideslope Cancel'),
               taws_r_gs=M('TAWS (R) Glideslope Cancel')):
        pass


class TAWSTooLowGear(MultistateDerivedParameterNode):
    name = 'TAWS Too Low Gear'

    @classmethod
    def can_operate(cls, available):
        return ('TAWS (L) Too Low Gear' in available) or \
               ('TAWS (R) Too Low Gear' in available)

    def derive(self, taws_l_gear=M('TAWS (L) Too Low Gear'),
               taws_r_gear=M('TAWS (R) Too Low Gear')):
        pass


class TAWSTerrainCaution(MultistateDerivedParameterNode):
    name = 'TAWS Terrain Caution'

    def derive(self, taws_terrain_cpt=M('TAWS Terrain Caution (Capt)'),
               taws_terrain_fo=M('TAWS Terrain Caution (FO)'),):
        pass


class TAWSTerrainWarning(MultistateDerivedParameterNode):
    name = 'TAWS Terrain Warning'

    def derive(self, taws_terrain_cpt=M('TAWS Terrain Warning (Capt)'),
               taws_terrain_fo=M('TAWS Terrain Warning (FO)'),):
        pass


class TakeoffConfigurationWarning(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self, stabilizer=M('Takeoff Configuration Stabilizer Warning'),
               parking_brake=M('Takeoff Configuration Parking Brake Warning'),
               flap=M('Takeoff Configuration Flap Warning'),
               gear=M('Takeoff Configuration Gear Warning'),
               ap=M('Takeoff Configuration AP Warning'),
               ail=M('Takeoff Configuration Aileron Warning'),
               rudder=M('Takeoff Configuration Rudder Warning'),
               spoiler=M('Takeoff Configuration Spoiler Warning')):
        pass


class TCASFailure(MultistateDerivedParameterNode):
    name = 'TCAS Failure'

    @classmethod
    def can_operate(cls, available):
        return ('TCAS (L) Failure' in available) or \
               ('TCAS (R) Failure' in available)

    def derive(self, tcas_l_failure=M('TCAS (L) Failure'),
               tcas_r_failure=M('TCAS (R) Failure')):
        pass


class TCASRA(MultistateDerivedParameterNode):
    name = 'TCAS RA'

    @classmethod
    def can_operate(cls, available):
        return ('TCAS RA (1)' in available) or \
               ('TCAS RA (2)' in available)

    def derive(self, tcas_1=M('TCAS RA (1)'),
               tcas_2=M('TCAS RA (2)')):
        pass


class SpeedControl(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               sc0a=M('Speed Control Auto'),
               sc0m=M('Speed Control Manual'),
               sc1a=M('Speed Control (1) Auto'),
               sc1m=M('Speed Control (1) Manual'),
               sc2a=M('Speed Control (2) Auto'),
               sc2m=M('Speed Control (2) Manual')):
        pass


class Transmitting(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available):
        return any(d in available for d in cls.get_dependency_names())

    def derive(self,
               hf=M('Key HF'),
               hf1=M('Key HF (1)'),
               hf2=M('Key HF (2)'),
               hf3=M('Key HF (3)'),
               hf1_capt=M('Key HF (1) (Capt)'),
               hf2_capt=M('Key HF (2) (Capt)'),
               hf3_capt=M('Key HF (3) (Capt)'),
               hf1_fo=M('Key HF (1) (FO)'),
               hf2_fo=M('Key HF (2) (FO)'),
               hf3_fo=M('Key HF (3) (FO)'),
               sc=M('Key Satcom'),
               sc1=M('Key Satcom (1)'),
               sc2=M('Key Satcom (2)'),
               vhf=M('Key VHF'),
               vhf1=M('Key VHF (1)'),
               vhf2=M('Key VHF (2)'),
               vhf3=M('Key VHF (3)'),
               vhf1_capt=M('Key VHF (1) (Capt)'),
               vhf2_capt=M('Key VHF (2) (Capt)'),
               vhf3_capt=M('Key VHF (3) (Capt)'),
               vhf1_fo=M('Key VHF (1) (FO)'),
               vhf2_fo=M('Key VHF (2) (FO)'),
               vhf3_fo=M('Key VHF (3) (FO)')):
        pass
