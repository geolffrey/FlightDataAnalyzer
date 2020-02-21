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


class ApproachInformation(ApproachNode):

    @classmethod
    def can_operate(cls, available, ac_type=A('Aircraft Type'),
                    seg_type=A('Segment Type')):
        if seg_type and seg_type.value == 'GROUND_ONLY':
            return False
        required = ['Approach And Landing', 'Takeoff', 'Touchdown']
        required.append('Altitude AGL' if ac_type == helicopter else 'Altitude AAL')
        lat = 'Latitude Prepared' in available
        lon = 'Longitude Prepared' in available
        if  lat != lon:
            return False
        return all_of(required, available)

    def derive(self,
               alt_aal=P('Altitude AAL'),
               alt_agl=P('Altitude AGL'),
               ac_type=A('Aircraft Type'),
               app=S('Approach And Landing'),
               hdg=P('Heading Continuous'),
               lat=P('Latitude Prepared'),
               lon=P('Longitude Prepared'),
               ils_loc=P('ILS Localizer'),
               ils_gs=S('ILS Glideslope'),
               ils_freq=P('ILS Frequency'),
               land_afr_apt=A('AFR Landing Airport'),
               land_afr_rwy=A('AFR Landing Runway'),
               lat_land=KPV('Latitude At Touchdown'),
               lon_land=KPV('Longitude At Touchdown'),
               precision=A('Precise Positioning'),
               fast=S('Fast'),
               u=P('Airspeed'),
               gspd=P('Groundspeed'),
               height_from_rig=P('Altitude ADH'),
               hdot=P('Vertical Speed'),
               roll=P('Roll'),
               heading=P('Heading'),
               distance_land=P('Distance To Landing'),
               tdwns=KTI('Touchdown'),
               offshore=M('Offshore'),
               takeoff=S('Takeoff')
               ):
        pass
