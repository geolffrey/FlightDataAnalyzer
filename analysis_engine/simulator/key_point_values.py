import numpy as np

from analysis_engine.node import KeyPointValueNode, KTI, P, S, A, M

from analysis_engine.library import (
    all_of,
    any_of,
    index_at_value,
    max_abs_value,
    runs_of_ones,
    slice_duration,
)

from flightdatautilities import units as ut
from flightdatautilities.geometry import great_circle_distance__haversine


class VariationFromRunwayCentrelineDuringTakeoffMax(KeyPointValueNode):

    units = ut.METER

    def derive(self, rwy_deviation=P('Distance From Runway Centre Line'), rto=S('Takeoff Roll')):
        self.create_kpvs_within_slices(rwy_deviation.array, rto, max_abs_value)


class VariationFromRunwayCentrelineDuringRejectedTakeoffMax(KeyPointValueNode):

    units = ut.METER

    def derive(self, rwy_deviation=P('Distance From Takeoff Runway Centreline'), rto=S('Rejected Takeoff')):
        self.create_kpvs_within_slices(rwy_deviation.array, rto, max_abs_value)


class DistanceFromTouchdownToFirstAircraftStop(KeyPointValueNode):

    units = ut.METER

    def derive(self, lon=P('Longitude'), lat=P('Latitude'), gspd=P('Groundspeed'), touchdown=KTI('Touchdown')):
        for start in touchdown:
            start_idx = start.index
            stop_idx = index_at_value(gspd.array, 0, _slice=slice(start_idx, None))
            if start_idx and stop_idx:
                self.create_kpv(stop_idx,
                                great_circle_distance__haversine(
                                    lat.array[start_idx],
                                    lon.array[start_idx],
                                    lat.array[stop_idx],
                                    lon.array[stop_idx]))


class EngineFailureReactionDelay(KeyPointValueNode):

    units = ut.SECOND

    @classmethod
    def can_operate(cls, available):
        return all_of(('Rudder Pedal', 'Pitch'), available) \
               and any_of(('Eng (*) Failure', 'Eng (*) Flame Out'), available)

    def derive(self, eng_fail=M('Eng (*) Failure'), eng_flameout=M('Eng (*) Flame Out'), rudder=P('Rudder Pedal'),
               pitch=P('Pitch'),):
        if eng_fail and eng_flameout:
            phases = runs_of_ones(eng_fail.array == 'Fail') or runs_of_ones(eng_flameout.array == 'Flame Out')
        elif eng_fail:
            phases = runs_of_ones(eng_fail.array == 'Fail')
        else:
            phases = runs_of_ones(eng_flameout.array == 'Flame Out')
        for failed_phase in phases:
            start_idx = failed_phase.start
            # Rudder change
            rudder_idx = index_at_value(np.ma.abs(rudder.array[failed_phase] - rudder.array[failed_phase.start]), 4)
            if rudder_idx:
                rudder_idx = rudder_idx + failed_phase.start
            # Pitch change
            pitch_idx = index_at_value(pitch.array[failed_phase] - pitch.array[failed_phase.start], 4)
            if pitch_idx:
                pitch_idx = pitch_idx + failed_phase.start
            end_idx = min([x for x in (rudder_idx, pitch_idx, failed_phase.stop) if x is not None])
            self.create_kpv(end_idx, slice_duration(slice(start_idx, end_idx), self.frequency))


class FlightFreezeDuration(KeyPointValueNode):

    units = ut.SECOND

    def derive(self, flight_freeze=P('Flight Freeze'),):
        sections = runs_of_ones(flight_freeze.array == 'Freeze')
        self.create_kpvs_from_slice_durations(sections, self.hz, min_duration=1)
