import numpy as np

from analysis_engine.settings import (
    AIRSPEED_THRESHOLD,
)

from analysis_engine.node import (
    FlightPhaseNode,
    P, S, A,
)

from analysis_engine.library import (
    runs_of_ones,
    slices_remove_small_gaps,
    find_low_alts,
)


class Fast(FlightPhaseNode):
    def derive(self, airspeed=P('Airspeed')):
        fast = np.ma.clump_unmasked(np.ma.masked_less(airspeed.array, AIRSPEED_THRESHOLD))
        fast = slices_remove_small_gaps(fast, time_limit=10, hz=self.hz)
        self.create_phases(fast)


class Airborne(FlightPhaseNode):
    def derive(self, alt=P('Altitude AAL')):
        airborne = np.ma.clump_unmasked(np.ma.masked_less_equal(alt.array, 0.5))
        airborne = slices_remove_small_gaps(airborne, time_limit=10, hz=self.hz)
        self.create_phases(airborne)


class FlightFrozen(FlightPhaseNode):
    def derive(self, ff=P('Flight Freeze'),):
        self.create_phases(runs_of_ones(ff.array == 'Freeze'))


class RejectedTakeoff(FlightPhaseNode):
    def derive(self, alt=P('Altitude Radio'),):
        if np.ma.max(alt.array) < 10:
            self.create_phases(runs_of_ones(alt.array < 10))


class GoAroundAndClimbout(FlightPhaseNode):
    '''
    We already know that the Key Time Instance has been identified at the
    lowest point of the go-around, and that it lies below the 3000ft
    approach thresholds. The function here is to expand the phase 500ft before
    to the first level off after (up to 2000ft above minimum altitude).

    Uses find_low_alts to exclude level offs and level flight sections, therefore
    approach sections may finish before reaching 2000 ft above the go around.
    '''

    @classmethod
    def can_operate(cls, available, seg_type=A('Segment Type'), ac_type=A('Aircraft Type')):
        correct_seg_type = True
        return 'Altitude AAL For Flight Phases' in available and correct_seg_type

    def derive(self, alt_aal=P('Altitude AAL For Flight Phases'),
               level_flights=S('Level Flight')):
        # Find the ups and downs in the height trace.
        level_flights = level_flights.get_slices() if level_flights else None
        low_alt_slices = find_low_alts(
            alt_aal.array, alt_aal.frequency, 3000,
            start_alt=500, stop_alt=2000,
            level_flights=level_flights,
            relative_start=True,
            relative_stop=True,
        )
        dlc_slices = []
        for low_alt in low_alt_slices:
            if (alt_aal.array[low_alt.start] and alt_aal.array[low_alt.stop - 1]):
                dlc_slices.append(low_alt)

        self.create_phases(dlc_slices)
