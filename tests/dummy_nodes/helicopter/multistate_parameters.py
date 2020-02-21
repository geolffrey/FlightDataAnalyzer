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


class AllEnginesOperative(MultistateDerivedParameterNode):

    def derive(self,
               any_running=M('Eng (*) Any Running'),
               eng_oei=M('One Engine Inoperative'),
               autorotation=S('Autorotation')):
        pass


class ASEEngaged(MultistateDerivedParameterNode):
    name = 'ASE Engaged'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type and ac_type.value == 'helicopter' and \
               any_of(cls.get_dependency_names(), available)

    def derive(self,
               ase1=M('ASE (1) Engaged'),
               ase2=M('ASE (2) Engaged'),
               ase3=M('ASE (3) Engaged')):
        pass


class ASEChannelsEngaged(MultistateDerivedParameterNode):
    name = 'ASE Channels Engaged'

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return ac_type and ac_type.value == 'helicopter' and len(available) >= 2

    def derive(self,
               ase1=M('ASE (1) Engaged'),
               ase2=M('ASE (2) Engaged'),
               ase3=M('ASE (3) Engaged')):
        pass


class Eng1OneEngineInoperative(MultistateDerivedParameterNode):
    name = 'Eng (1) One Engine Inoperative'

    def derive(self,
               eng_2_n2=P('Eng (2) N2'),
               nr=P('Nr'),
               autorotation=S('Autorotation')):
        pass


class Eng2OneEngineInoperative(MultistateDerivedParameterNode):
    name = 'Eng (2) One Engine Inoperative'

    def derive(self,
               eng_1_n2=P('Eng (1) N2'),
               nr=P('Nr'),
               autorotation=S('Autorotation')):
        pass


class GearOnGround(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        gog_available = any_of(('Gear (L) On Ground', 'Gear (R) On Ground'), available)
        if gog_available:
            return True
        elif all_of(('Vertical Speed', 'Eng (*) Torque Avg'), available):
            return True
        else:
            return False

    def derive(self,
               gl=M('Gear (L) On Ground'),
               gr=M('Gear (R) On Ground'),
               vert_spd=P('Vertical Speed'),
               torque=P('Eng (*) Torque Avg'),
               ac_series=A('Series'),
               collective=P('Collective')):
        pass


class OneEngineInoperative(MultistateDerivedParameterNode):

    def derive(self,
               eng_1_oei=M('Eng (1) One Engine Inoperative'),
               eng_2_oei=M('Eng (2) One Engine Inoperative'),
               autorotation=S('Autorotation')):
        pass


class RotorBrakeEngaged(MultistateDerivedParameterNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type')):
        return any_of(cls.get_dependency_names(), available) and \
               ac_type == helicopter

    def derive(self,
               brk1=M('Rotor Brake (1) Engaged'),
               brk2=M('Rotor Brake (2) Engaged')):
        pass


class RotorsRunning(MultistateDerivedParameterNode):

    def derive(self, nr=P('Nr')):
        pass
