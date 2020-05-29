import numpy as np
from flightdatautilities import units as ut

from analysis_engine.node import (
    DerivedParameterNode,
    MultistateDerivedParameterNode,
    M, P, A, S)
from analysis_engine.library import (any_of,
                                     vstack_params,
                                     vstack_params_where_state,
                                     )


class EngineFlameOut(MultistateDerivedParameterNode):
    '''
    Merges all the engine Flame Out signals into one.
    '''
    name = 'Eng (*) Flame Out'
    units = None
    values_mapping = {0: '-', 1: 'Flame Out'}

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=M('Eng (1) Flame Out'),
               eng2=M('Eng (2) Flame Out'),
               eng3=M('Eng (3) Flame Out'),
               eng4=M('Eng (4) Flame Out'),
               ):

        self.array = vstack_params_where_state(
            (eng1, 'Flame Out'), (eng2, 'Flame Out'),
            (eng3, 'Flame Out'), (eng4, 'Flame Out'),
        ).any(axis=0)


class EngineFailure(MultistateDerivedParameterNode):
    '''
    Merges all the engine Flame Out signals into one.
    '''
    name = 'Eng (*) Failure'
    units = None
    values_mapping = {0: '-', 1: 'Fail'}

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               eng1=M('Eng (1) Failure'),
               eng2=M('Eng (2) Failure'),
               eng3=M('Eng (3) Failure'),
               eng4=M('Eng (4) Failure'),
               ):

        self.array = vstack_params_where_state(
            (eng1, 'Fail'), (eng2, 'Fail'),
            (eng3, 'Fail'), (eng4, 'Fail'),
        ).any(axis=0)


class BrakePedalMax(DerivedParameterNode):
    '''
    Max brake pedal angle from all sources.
    '''
    name = 'Brake Pedal (*) Max'
    units = ut.DEGREE

    @classmethod
    def can_operate(cls, available):
        return any_of(cls.get_dependency_names(), available)

    def derive(self,
               bp_cpt_l=P('Brake Pedal (Capt) (L)'),
               bp_cpt_r=P('Brake Pedal (Capt) (R)'),
               bp_fo_l=P('Brake Pedal (FO) (L)'),
               bp_fo_r=P('Brake Pedal (FO) (R)'),
               ):
        brake_params = (bp_cpt_l, bp_cpt_r, bp_fo_l, bp_fo_l)
        brake_pedals = vstack_params(*brake_params)
        self.array = np.ma.max(brake_pedals, axis=0)


class Eng1N1(DerivedParameterNode):
    '''
    N1 speed as a percentage. A330 Simulation data is actually the N1 shaft
    speed in RPM. For an A330 with GE engines 100% RPM is equal to 3320.6 rpm

    example: 3650 (rpm) = 3650/33.206 = 109.9% N1 (about takeoff %N1)
    '''
    name = 'Eng (1) N1'
    units = ut.PERCENT

    def derive(self, rpm=P('Eng (1) N1 RPM')):
        self.frequency = rpm.frequency
        self.array = rpm.array / 33.206


class Eng2N1(DerivedParameterNode):
    '''
    N1 speed as a percentage. A330 Simulation data is actually the N1 shaft
    speed in RPM. For an A330 with GE engines 100% RPM is equal to 3320.6 rpm

    example: 3650 (rpm) = 3650/33.206 = 109.9% N1 (about takeoff %N1)
    '''
    name = 'Eng (2) N1'
    units = ut.PERCENT

    def derive(self, rpm=P('Eng (2) N1 RPM')):
        self.frequency = rpm.frequency
        self.array = rpm.array / 33.206


class Eng3N1(DerivedParameterNode):
    '''
    N1 speed as a percentage. A330 Simulation data is actually the N1 shaft
    speed in RPM. For an A330 with GE engines 100% RPM is equal to 3320.6 rpm

    example: 3650 (rpm) = 3650/33.206 = 109.9% N1 (about takeoff %N1)
    '''
    name = 'Eng (3) N1'
    units = ut.PERCENT

    def derive(self, rpm=P('Eng (3) N1 RPM')):
        self.frequency = rpm.frequency
        self.array = rpm.array / 33.206


class Eng4N1(DerivedParameterNode):
    '''
    N1 speed as a percentage. A330 Simulation data is actually the N1 shaft
    speed in RPM. For an A330 with GE engines 100% RPM is equal to 3320.6 rpm

    example: 3650 (rpm) = 3650/33.206 = 109.9% N1 (about takeoff %N1)
    '''
    name = 'Eng (4) N1'
    units = ut.PERCENT

    def derive(self, rpm=P('Eng (4) N1 RPM')):
        self.frequency = rpm.frequency
        self.array = rpm.array / 33.206


class SidestickPitch(DerivedParameterNode):
    name = 'Sidestick Pitch (Capt)'
    units = ut.DEGREE

    def derive(self, pitch=P('Sidestick Pitch Position (Capt)')):
        self.array = pitch.array * 16


class SidestickRoll(DerivedParameterNode):
    name = 'Sidestick Roll (Capt)'
    units = ut.DEGREE

    def derive(self, roll=P('Sidestick Roll Position (Capt)')):
        self.array = roll.array * 20


class RudderPedal(DerivedParameterNode):
    name = 'Rudder Pedal (Capt)'
    units = ut.DEGREE

    def derive(self, rudder=P('Rudder Pedal Position (Capt)')):
        self.array = rudder.array * 31
