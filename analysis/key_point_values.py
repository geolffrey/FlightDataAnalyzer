import logging
import numpy as np

from analysis import settings
from analysis.node import  KeyPointValue, KeyPointValueNode, KTI, P, S
from analysis.library import (max_abs_value, max_continuous_unmasked, 
                              max_value, min_value, repair_mask, value_at_time)
from analysis.node import  KeyPointValue, KPV, KeyPointValueNode, KTI, P, S


class Airspeed1000To500FtMax(KeyPointValueNode):
    def derive(self, speed=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        # For commented version, see GlideslopeDeviation1500To1000FtMax
        in_band_periods = alt_aal.slices_from_to(1000, 500)
        for this_period in in_band_periods:
            index, value = max_value(speed.array, _slice=this_period)
            self.create_kpv(index, value)

'''
class AirspeedAtTouchdown(KeyPointValueNode):
    def derive(self, airspeed=P('Airspeed'), touchdowns=KTI('Touchdown')):
        self.create_kpvs_at_ktis(airspeed, touchdowns)
'''

class AirspeedAtLiftoff(KeyPointValueNode):
    def derive(self, airspeed=P('Airspeed'), liftoffs=KTI('Liftoff')):
        self.create_kpvs_at_ktis(airspeed, liftoffs)


class AirspeedAtTouchdown(KeyPointValueNode):
    def derive(self, airspeed=P('Airspeed'), touchdowns=KTI('Touchdown')):
        self.create_kpvs_at_ktis(airspeed, touchdowns)


class AirspeedMax(KeyPointValueNode):
    def derive(self, speed=P('Airspeed'),
               airs=S('Airborne')):
        # For commented version, see GlideslopeDeviation1500To1000FtMax
        for air in airs:
            index, value = max_value(speed.array, air.slice)
            self.create_kpv(index, value)
            

class HeadingAtTakeoff(KeyPointValueNode):
    def derive(self, toffs=KTI('Takeoff Peak Acceleration'), 
               head=P('Heading Continuous')):
        for toff in toffs:
            toff_head = np.ma.median(
                head.array[toff.index-5:toff.index+5])
            # Scanning 10 seconds around this point allows for short periods of
            # corrupt data during the takeoff run.
            self.create_kpv(toff.index, toff_head%360.0)

"""

TODO: Can we omit this ?!?

class AltitudeAtTakeoff(KeyPointValueNode):
    def derive(self, takeoffs=S('Takeoff'), head=P('Heading Continuous'), 
               accel=P('Acceleration Forwards For Flight Phases')):
        for toff in takeoffs:
            peak_accel_index, value = max_value(accel.array, toff.slice)
            toff_head = head.array.data[peak_accel_index] #TODO: What if data is masked on this value, use nearest valid by repairing mask?
            self.create_kpv(peak_accel_index, toff_head%360.0)

            
class AltitudeAtLiftoff(KeyPointValueNode):
    # Taken at the point of liftoff although there will be pressure errors at
    # this point. The reason for computing this is unclear as we calculate
    # Altitude AAL based upon the 35ft phase transition altitude.
    def derive(self, alt_std=P('Altitude STD'), liftoffs=KTI('Liftoff')):
        self.create_kpvs_at_ktis(alt_std, liftoffs)

    
class AltitudeAtLanding(KeyPointValueNode):
    def derive(self, lands=KTI('Touchdown'), alt_std=P('Altitude Std')):
        for land in lands:
            self.create_kpv(land.index, alt_std[land.index])
"""
class AltitudeAtTouchdown(KeyPointValueNode):
    def derive(self, alt_std=P('Altitude STD'), touchdowns=KTI('Touchdown')):
        self.create_kpvs_at_ktis(alt_std, touchdowns)


class AutopilotEngaged1AtLiftoff(KeyPointValueNode):
    name = 'Autopilot Engaged 1 At Liftoff'
    def derive(self, autopilot=KTI('Autopilot Engaged 1'),
               liftoffs=P('Liftoff')):
        self.create_kpvs_at_ktis(autopilot, liftoffs)


class AutopilotEngaged2AtLiftoff(KeyPointValueNode):
    name = 'Autopilot Engaged 2 At Liftoff'
    def derive(self, autopilot=KTI('Autopilot Engaged 2'),
               liftoffs=P('Liftoff')):
        self.create_kpvs_at_ktis(autopilot, liftoffs)


class AutopilotEngaged1AtTouchdown(KeyPointValueNode):
    name = 'Autopilot Engaged 1 At Touchdown'
    def derive(self, autopilot=KTI('Autopilot Engaged 1'),
               touchdowns=P('Touchdown')):
        self.create_kpvs_at_ktis(autopilot, touchdowns)


class AutopilotEngaged2AtTouchdown(KeyPointValueNode):
    name = 'Autopilot Engaged 2 At Touchdown'
    def derive(self, autopilot=KTI('Autopilot Engaged 2'),
               touchdowns=P('Touchdown')):
        self.create_kpvs_at_ktis(autopilot, touchdowns)

class HeadingAtLanding(KeyPointValueNode):
    """
    The landing has been found already, including and the flare and a little
    of the turn off the runway. We take the heading at the point of maximum
    deceleration, as this should lie between the touchdown when the aircraft
    may be drifting and the turnoff which could be at high speed, but should
    be at a gentler deceleration.
    """
    def derive(self, lands=KTI('Landing Peak Deceleration'), 
               head=P('Heading Continuous')):
        for land in lands:
            land_head = np.ma.median(
                head.array[land.index-5:land.index+5])
            # Scanning 10 seconds around this point allows for short periods of
            # corrupt data during the takeoff run.
            self.create_kpv(land.index, land_head%360.0)
            
class HeadingAtLowPointOnApproach(KeyPointValueNode):
    """
    The approach phase has been found already. Here we take the heading at
    the lowest point reached in the approach. This may not be a go-around, if
    the aircraft did not climb 500ft before the next approach to landing.
    """
    def derive(self, head=P('Heading Continuous'),
               lands=KTI('Approach And Landing Lowest')):
        self.create_kpvs_at_ktis(head, lands)


class LatitudeAtLanding(KeyPointValueNode):
    def derive(self, lat=P('Latitude'), lands=KTI('Landing Peak Deceleration')):
        self.create_kpvs_at_ktis(lat, lands)
            

class LongitudeAtLanding(KeyPointValueNode):
    def derive(self, lon=P('Longitude'),
               lands=KTI('Landing Peak Deceleration')):
        self.create_kpvs_at_ktis(lon, lands)
            

class ILSFrequencyOnApproach(KeyPointValueNode):
    """
    The period when the aircraft was continuously established on the ILS and
    descending to the minimum point on the approach is already defined as a
    flight phase. This KPV just picks up the frequency tuned at that point.
    """
    name='ILS Frequency On Approach' #  Set here to ensure "ILS" in uppercase.
    def derive(self, establishes=S('ILS Localizer Established'),
              lowest=KTI('Approach And Landing Lowest Point'),
              ils_frq=P('ILS Frequency')):
        
        for established in establishes:
            # For the final period of operation of the ILS during this
            # approach, the ILS frequency was:
            freq=np.ma.median(ils_frq.array[established.slice])
            # Note median picks the value most commonly recorded, so allows
            # for some masked values and perhaps one or two rogue values.

            # Identify the KPV as relating to the start of this ILS approach
            self.create_kpv(established.slice.start, freq)
            

class LatitudeAtLowPointOnApproach(KeyPointValueNode):
    def derive(self, lat=P('Latitude'), 
               lands=KTI('Approach And Landing Lowest')):
        self.create_kpvs_at_ktis(lat, lands)
            

class LongitudeAtLowPointOnApproach(KeyPointValueNode):
    def derive(self, lon=P('Longitude'), 
               lands=KTI('Approach And Landing Lowest')):
        self.create_kpvs_at_ktis(lon, lands)


##########################################
# KPV from A6RKA_KPVvalues.xls
##########################################


class PitchAtLiftoff(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'), liftoffs=KTI('Liftoff')):
        self.create_kpvs_at_ktis(pitch, liftoffs)
   
   
class FlapAtLiftoff(KeyPointValueNode):
    def derive(self, flap=P('Flap'), liftoffs=KTI('Liftoff')):
        self.create_kpvs_at_ktis(flap, liftoffs)
    

class AccelerationNormalFtTo35FtMax(KeyPointValueNode): # Q: Name?
    def derive(self, norm_g=P('Acceleration Normal'), alt_rad=P('Altitude Radio')):
        return NotImplemented


class AccelerationNormalAirborneMax(KeyPointValueNode):
    def derive(self, norm_g=P('Acceleration Normal'), airborne=S('Airborne')):
        for in_air in airborne:
            index, value = max_value(norm_g.array, in_air.slice)
            self.create_kpv(index, value)


class AccelerationNormalAirborneMin(KeyPointValueNode):
    def derive(self, norm_g=P('Acceleration Normal'), airborne=S('Airborne')):
        for in_air in airborne:
            index, value = min_value(norm_g.array, in_air.slice)
            self.create_kpv(index, value)


'''
class Pitch35To400FtMax(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'), alt_rad=P('Altitude Radio')):
        return NotImplemented
'''

class Pitch1000To100FtMax(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'),
               desc_alts=KTI('Altitude When Descending')):        
        desc_1000fts = desc_alts.get_ordered_by_index(name='1000 Ft Descending')
        desc_100fts = desc_alts.get_ordered_by_index(name='10 Ft Descending')


class Pitch5FtToTouchdownMax(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'), alt_rad=P('Altitude Radio'),
               touchdown=KTI('Touchdown')):
        return NotImplemented
    
    
class PitchCycles(KeyPointValueNode):
    """ Count
    """
    def derive(self, pitch=P('Pitch')):
        return NotImplemented


class Pitch35To400FtMin(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'), alt_rad=P('Altitude Radio')):
        return NotImplemented


class Pitch1000To100FtMin(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'), alt_aal=P('Altitude AAL')):
        return NotImplemented


class Pitch20FtToTouchdownMin(KeyPointValueNode):
    """ Q: This is 20 feet, the max uses 5 feet
    """
    def derive(self, pitch=P('Pitch'), alt_rad=P('Altitude Radio'),
               touchdown=KTI('Touchdown')):
        return NotImplemented


class PitchRateFtTo35FtMax(KeyPointValueNode):
    def derive(self, pitch_rate=P('Pitch Rate'), liftoff=KTI('Liftoff'),
               alt_rad=P('Altitude Radio')):
        return NotImplemented


class PitchRate35To1500FtMax(KeyPointValueNode):
    def derive(self, pitch_rate=P('Pitch Rate'), alt_aal=P('Altitude AAL')):
        return NotImplemented

    
class RollBelow20FtMax(KeyPointValueNode): # absolute max?
    def derive(self, roll=P('Roll'), alt_rad=P('Altitude Radio')):
        return NotImplemented


class RollBetween100And500FtMax(KeyPointValueNode): # absolute max?
    def derive(self, roll=P('Roll'), alt_aal=P('Altitude AAL')):
        return NotImplemented


class RollBetween500And1500FtMax(KeyPointValueNode):  # absolue max?
    def derive(self, roll=P('Roll'), alt_aal=P('Altitude AAL')):
        return NotImplemented   


class RollAbove1500FtMax(KeyPointValueNode):
    def derive(self, roll=P('Roll'), alt_aal=P('Altitude AAL')):
        return NotImplemented


class RollCycles1000FtToTouchdown(KeyPointValueNode):
    def derive(self, roll=P('Roll'), alt_aal=P('Altitude AAL'),
               touchdown=KTI('Touchdown')):
        return NotImplemented
    
    
class AltitudeWithFlapsMax(KeyPointValueNode):
    """
    FIXME: It's max Altitude not Max Flaps
    """
    def derive(self, flap=P('Flap'), alt_std=P('Altitude Std')):
        return NotImplemented


class MACHMax(KeyPointValueNode):
    #TODO: Test
    name = 'MACH Max'
    def derive(self, mach=P('MACH'), fast=S('Fast')):
        for sect in fast:
            index, value = max_value(mach.array, sect.slice)
            self.create_kpv(index, value)


class AltitudeAtMACHMax(KeyPointValueNode):
    #TODO: Test
    name = 'Altitude At MACH Max'
    def derive(self, max_mach=KPV('MACHMax'), alt_std=P('Altitude STD')):
        # Aligns Altitude to MACH to ensure we have the most accurate
        # altitude reading at the point of Maximum MACH
        self.create_kpvs_at_kpvs(alt_std, max_mach)


class GroundSpeedOnGroundMax(KeyPointValueNode):
    def derive(self, groundspeed=P('Groundspeed'), on_grounds=S('On Ground')):
        #max_value(groundspeed[on_ground]) # TODO: Fix.
        return NotImplemented


class FlapAtTouchdown(KeyPointValueNode):
    def derive(self, flap=P('Flap'), touchdown=KTI('Touchdown')):
        return NotImplemented


#################
# TODO: Review whether Engine measurements should be overall or for sections 
# in flight (e.g. split by airborne / on ground?)

class EngEGTMax(KeyPointValueNode):
    name = 'Eng EGT Max'
    def derive(self, eng=P('Eng (*) EGT Max')):
        index, value = max_value(eng.array)
        self.create_kpv(index, value)
        

class Eng_N1MaxDurationUnder60PercentAfterTouchdown(KeyPointValueNode): ##was named: EngN1CooldownDuration
    """
    Max duration N1 below 60% after Touchdown for engine cooldown. Using 60%
    allows for cooldown after use of Reverse Thrust.
    
    Evaluated for each engine to account for single engine taxi-in.
    
    Note: Assumes that all Engines are recorded at the same frequency.
    
    TODO: Eng_Stop KTI
    TODO: Similar KPV for duration between engine under 60 percent and engine shutdown
    """
    NAME_FORMAT = "Eng (%(eng_num)d) N1 Max Duration Under 60 Percent After Touchdown"
    NAME_VALUES = {'eng_num': [1,2,3,4]}
    
    @classmethod
    def can_operate(cls, available):
        if 'Touchdown' in available\
           and 'Eng (*) Stop' in available\
           and ('Eng (1) N1' in available\
                or 'Eng (2) N1' in available\
                or 'Eng (3) N1' in available\
                or 'Eng (4) N1' in available):
            return True
        else:
            return False
    
    def derive(self, 
               eng1=P('Eng (1) N1'),
               eng2=P('Eng (2) N1'),
               eng3=P('Eng (3) N1'),
               eng4=P('Eng (4) N1'),
               tdwn=KTI('Touchdown'), engines_stop=KTI('Eng (*) Stop')):
                
        for eng_num, eng in enumerate((eng1,eng2,eng3,eng4), start=1):
            if eng is None:
                continue # engine not available on this aircraft
            eng_stop = engines_stop.get(name='Eng (%d) Stop' % eng_num)
            if not eng_stop:
                #Q: Should we measure until the end of the flight anyway? (probably not)
                logging.debug("Engine %d did not stop on this flight, cannot measure KPV", eng_num)
                continue
            
            eng_array = repair_mask(eng.array)
            eng_below_60 = np.ma.masked_greater(eng_array, 60)
            # measure duration between final touchdown and engine stop
            duration_slice = max_continuous_unmasked(
                eng_below_60, slice(tdwn[-1].index, eng_stop[0].index))
            if duration_slice:
                #TODO future storage of slice: self.slice = duration_slice
                duration = (duration_slice.stop - duration_slice.start) / self.hz
                self.create_kpv(duration_slice.start, duration, eng_num=eng_num)
            else:
                # create KPV of 0 seconds
                self.create_kpv(eng_stop[0].index, 0.0, eng_num=eng_num)
        
        
class EngN1Max(KeyPointValueNode):
    name = 'Eng N1 Max'
    def derive(self, eng=P('Eng (*) N1 Max')):
        index, value = max_value(eng.array)
        self.create_kpv(index, value)

class EngN2Max(KeyPointValueNode):
    name = 'Eng N2 Max'
    def derive(self, eng=P('Eng (*) N2 Max')):
        index, value = max_value(eng.array)
        self.create_kpv(index, value)

class EngOilTempMax(KeyPointValueNode):
    name = 'Eng Oil Temp Max'
    def derive(self, eng=P('Eng (*) Oil Temp Max')):
        index, value = max_value(eng.array)
        self.create_kpv(index, value)


class EngVibN1Max(KeyPointValueNode):
    name = 'Eng Vib N1 Max'
    ##def derive(self, eng=P('Eng (*) Vib N1 Max'), fast=S('Fast')):
        ##for sect in fast:
            ##index, value = max_value(eng.array, sect.slice)
            ##self.create_kpv(index, value)
            
    def derive(self, eng=P('Eng (*) Vib N1 Max')):
        index, value = max_value(eng.array)
        self.create_kpv(index, value)
            
            
class EngVibN2Max(KeyPointValueNode):
    name = 'Eng Vib N2 Max'
    ##def derive(self, eng=P('Eng (*) Vib N2 Max'), fast=S('Fast')):
        ##for sect in fast:
            ##index, value = max_value(eng.array, sect.slice)
            ##self.create_kpv(index, value)
            
    def derive(self, eng=P('Eng (*) Vib N2 Max')):
        index, value = max_value(eng.array)
        self.create_kpv(index, value)
            
            
class FuelQtyMinAirborne(KeyPointValueNode):
    #TODO: TEST
    def derive(self, fuel=P('Fuel Qty'), airborne=S('Airborne')):
        for sect in airborne:
            index, value = min_value(fuel.array, sect.slice)
            self.create_kpv(index, value)


class MagneticHeadingAtLiftOff(KeyPointValue):
    """ Shouldn't this be difference between aircraft heading and runway heading???
    """
    def derive(self, heading=P('Magnetic Heading'), liftoff=KTI('Liftoff')):
        return NotImplemented


class MagneticHeadingAtTouchdown(KeyPointValue):
    """ Shouldn't this be difference between aircraft heading and runway heading???
    """
    def derive(self, heading=P('Magnetic Heading'), touchdown=KTI('Touchdown')):
        return NotImplemented
    
# TODO: Trouble with naming these
#class LatgOnGround??
#class Pitch rate (from 2 degrees of pitch?) to 35 feet minimum

    
'''Shortcut: copy n paste below!
(KeyPointValueNode):
    dependencies = []
    def derive(self, params):
        return NotImplemented
'''

##########################################
# KPV from DJ's Code

class AccelerationNormalMax(KeyPointValueNode):
    def derive(self, normal_acceleration=P('Normal Acceleration')):
        index, value = max_value(normal_acceleration.array)
        self.create_kpv(index, value)
        
        ### Use Numpy to locate the maximum g, then go back and get the value.
        ##n_acceleration_normal_max = np.ma.argmax(normal_acceleration.array.data[block])
        ##acceleration_normal_max = normal_acceleration.array.data[block][n_acceleration_normal_max]
        ### Create a key point value for this. TODO: Change to self.create_kpv()?
        ##self.create_kpv(block.start+n_acceleration_normal_max,
                        ##acceleration_normal_max)


class RateOfClimbHigh(KeyPointValueNode):
    '''
    .. TODO:: testcases
    '''
    def derive(self, rate_of_climb=P('Rate Of Climb'),
               climbing=S('Climbing')):
        #TODO: Merge with below RateOfDescentMax accepting a flightphase arg
        for climb in climbing:
            duration = climb.slice.stop - climb.slice.start
            if duration > settings.CLIMB_OR_DESCENT_MIN_DURATION:
                index, value = max_value(rate_of_climb.array, climb.slice)
                self.create_kpv(index, value)


class RateOfDescentHigh(KeyPointValueNode):
    '''
    .. TODO:: testcases
    '''
    def derive(self, rate_of_climb=P('Rate Of Climb'),
               descending=S('Descending')):
        #TODO: Merge with below RateOfDescentMax accepting a flightphase arg
        for descent in descending:
            duration = descent.slice.stop - descent.slice.start
            if duration > settings.CLIMB_OR_DESCENT_MIN_DURATION:
                index, value = min_value(rate_of_climb.array, descent.slice)
                self.create_kpv(index, value)


class RateOfDescentMax(KeyPointValueNode):
    '''
    .. TODO:: testcases ??? Do we need this if we have high and keep many highs - max must be one of these... DJ
    '''
    # Minimum period of a descent for testing against thresholds (reduces number of KPVs computed in turbulence)
    DESCENT_MIN_DURATION = 10
    
    def derive(self, rate_of_climb=P('Rate Of Climb'), descents=S('Descent')):
        for descent in descents:
            duration = descent.slice.stop - descent.slice.start
            if duration > self.DESCENT_MIN_DURATION:
                index, value = min_value(rate_of_climb.array, descent.slice)
                self.create_kpv(index, value)
             
    
'''
Wrong naming format, wrong parameter. Defunct.

class MaxIndicatedAirspeedLevelFlight(KeyPointValueNode):
    def derive(self, airspeed=P('Indicated Airspeed'),
               level_flight=S('Level Flight')):
        for level_slice in level_flight:
            duration = level_slice.stop - level_slice.start
            if duration > settings.LEVEL_FLIGHT_MIN_DURATION:
                # stable for long enough
                when = np.ma.argmax(airspeed.array[level_slice])
                howfast = airspeed.array[level_slice][when]
                self.create_kpv(level_slice.start+when, howfast)
            else:
                logging.debug('Short duration %d of level flight ignored',
                              duration)
'''

class AirspeedMinusVref500FtTo0FtMax(KeyPointValueNode):
    
    def derive(self, airspeed_minus_vref=P('AirspeedMinusVref'), 
               _500ft_to_0ft=S('500 Ft To 0 Ft')):  #Q: Label this as the list of kpv sections?
        for sect in _500ft_to_0ft:
            index, value = max_value(airspeed_minus_vref.array, sect.slice)
            self.create_kpv(index, value)
            


#TODO:
#toc = altitude_std[kpt['TopOfClimb']] # Indexing n_toc into the reduced array [block]
#kpv['Altitude_TopOfClimb'] = [(kpt['TopOfClimb'], toc, altitude_std)]
#kpv['LandingTurnOffRunway'] = [(block.start+kpt['LandingEndEstimate'],(head_mag[kpt['LandingEndEstimate']] - head_landing), head_mag.param_name)]
#kpv['Head_Landing'] = [(block.start+kpt['LandingEndEstimate'], head_landing%360, head_mag.param_name)]  # Convert to normal compass heading for display
#tod = altitude_std[kpt['TopOfDescent']] # Indexing n_toc into the reduced array [block]
#kpv['Altitude_TopOfDescent'] = [(kpt['TopOfDescent'], tod, altitude_std)]
#kpv['Head_Takeoff'] = [(block.start+kpt['TakeoffStartEstimate'], head_takeoff%360, head_mag.param_name)] # Convert to normal compass heading for display
#kpv['TakeoffTurnOntoRunway'] = [(block.start+turn_onto_runway,head_takeoff - head_mag[turn_onto_runway],head_mag.param_name)]



class AccelerationNormalDuringTakeoffMax(KeyPointValueNode):
    def derive(self, acceleration_normal=P('Acceleration Normal'),
               liftoff=KTI('Liftoff')):
        return NotImplemented

        
class AltitudeMax(KeyPointValueNode):
    def derive(self, alt_std=P('Altitude STD'),
               airs=S('Airborne')):
        # For commented version, see GlideslopeDeviation1500To1000FtMax
        for air in airs:
            index, value = max_value(alt_std.array, air.slice)
            self.create_kpv(index, value)
    """
    I think this version is not needed - DJ 23/12/11
    def derive(self, alt_std=P('Altitude STD')): ##, airborne=S('Airborne')):
        max_index = alt_std.array.argmax()
        self.create_kpv(max_index, alt_std.array[max_index])
    """
        

class AltitudeWithFlapsMax(KeyPointValueNode):
    def derive(self, alt_std=P('Altitude STD'), flap=P('Flap'),
               airborne=S('Airborne')):
        return NotImplemented


class FlapAtTouchdown(KeyPointValueNode):
    def derive(self, flap=P('Flap'), touchdown=KTI('Touchdown')):
        return NotImplemented


# FIXME: Bounced Landing name duplicated between KPV and Section!
class BouncedLanding(KeyPointValueNode):
    def derive(self, bounced_landing=S('Bounced Landing Section')):
        return NotImplemented


class RateOfDescent500ToTouchdownMax(KeyPointValueNode):
    def derive(self, roc=P('Rate Of Climb'),
               _500_ft_in_final_approach=KTI('500 Ft In Final Approach'),
               touchdown=KTI('Touchdown')):
        return NotImplemented
    

class RateOfDescent1000To500FtMax(KeyPointValueNode):
    def derive(self, roc=P('Rate Of Climb'),
               _1000_ft_in_approach=KTI('1000 Ft In Approach'),
               _500_ft_in_final_approach=KTI('500 Ft In Final Approach')):
        return NotImplemented


class RateOfDescent2000To1000FtMax(KeyPointValueNode):
    def derive(self, roc=P('Rate Of Climb'),
               _2000_ft_in_approach=KTI('2000 Ft In Approach'),
               _1000_ft_in_approach=KTI('1000 Ft In Approach')):
        return NotImplemented


class DontSinkWarning(KeyPointValueNode):
    def derive(self, gpws_dont_sink=P("GPWS Don't Sink")):
        return NotImplemented


class HeightAtConfigChangeFtTo3500FtMin(KeyPointValueNode):
    def derive(self, flap=P('Flap'), alt_aal=P('Altitude AAL'),
               liftoff=KTI('Liftoff'),
               _3500_ft_in_climb=KTI('3500 Ft In Climb')):
        return NotImplemented


class EGTTakeoffMax(KeyPointValueNode):
    name = 'EGT Takeoff Max'
    def derive(self, eng_n_egt=P('Eng EGT'), liftoff=KTI('Liftoff')):
        return NotImplemented


class GlideslopeWarning(KeyPointValueNode):
    def derive(self, gpws_glideslope=P('GPWS Glideslope')):
        return NotImplemented


class GlideslopeDeviation1000To150FtMax(KeyPointValueNode):
    def derive(self, ils_glideslope=P('ILS Glideslope'),
               alt_aal = P('Altitude AAL For Flight Phases')):
        # For commented version, see GlideslopeDeviation1500To1000FtMax
        for this_slice in alt_aal.slices_from_to(1000, 150):
            index, value = max_abs_value(ils_glideslope.array, this_slice)
            self.create_kpv(index, value)


class GlideslopeDeviation1500To1000FtMax(KeyPointValueNode):
    def derive(self, ils_glideslope=P('ILS Glideslope'),
               alt_aal = P('Altitude AAL For Flight Phases')):
        for this_slice in alt_aal.slices_from_to(1500, 1000):
            # Find where the maximum (absolute) deviation occured and
            # store the actual value. We can do abs on the statistics to
            # normalise this, but retaining the sign will make it
            # possible to look for direction of errors at specific
            # airports.
            index, value = max_abs_value(ils_glideslope.array, this_slice)
            # and create the KPV.
            self.create_kpv(index, value)


class HeightAtGoAroundMin(KeyPointValueNode):
    def derive(self, go_around=P('Go Around'),
               alt_radio=P('Altitude Radio')): # FIXME: Go Around parameter??
        return NotImplemented


class SinkRateWarning(KeyPointValueNode):
    def derive(self, gpws_sink_rate=P('GPWS Sink Rate')):
        return NotImplemented


class AccelerationNormal20FtToGroundMax(KeyPointValueNode):
    name = 'Acceleration Normal 20 Ft To Ground Max'
    def derive(self, acceleration_normal=P('Acceleration Normal')):
        return NotImplemented


class HeadingDeviation100KtsToFtMax(KeyPointValueNode):
    def derive(self, head_mag=P('Heading Magnetic'), airspeed=P('Airspeed'),
               liftoff=KTI('Liftoff')):
        return NotImplemented


class Height1MinToTouchdown(KeyPointValueNode):
    def derive(self, altitude_aal=P('Altitude AAL'),
               _1_min_to_touchdown=KTI('1 Min To Touchdown')):
        return NotImplemented


class Height2MinToTouchdown(KeyPointValueNode):
    def derive(self, altitude_aal=P('Altitude AAL'),
               _2_min_to_touchdown=KTI('2 Min To Touchdown')):
        return NotImplemented


class HeightLost1000To2000FtMax(KeyPointValueNode):
    def derive(self, altitude_std=P('Altitude STD'),
               _1000_ft_in_climb=KTI('1000 Ft In Climb'),
               _2000_ft_in_climb=KTI('2000 Ft In Climb')):
        return NotImplemented


class HeightLost50To1000Max(KeyPointValueNode):
    def derive(self, altitude_std=P('Altitude STD'),
               _50_ft_in_initial_climb=KTI('50 Ft In Initial Climb'),
               _1000_ft_in_climb=KTI('1000 Ft In Climb')):
        return NotImplemented


class LateralGOnGround(KeyPointValueNode):
    def derive(self, acc_lat=P('Acceleration Lateral'),
               taxi_out=S('Taxi Out'), taxi_in=S('Taxi In')):
        return NotImplemented


class EngN13000FtToTouchdownMax(KeyPointValueNode):
    name = 'Eng N1 3000 Ft To Touchdown Max'
    def derive(self, eng_n1_avg=P('Eng N1 Avg'),
               _3000_ft_in_approach=KTI('3000 Ft In Approach'),
               touchdown=KTI('Touchdown')):
        return NotImplemented


class EngN1TakeoffMax(KeyPointValueNode):
    name = 'Eng N1 Takeoff Max'
    def derive(self, eng_n1_max=P('Eng N1 Max'), liftoff=KTI('Liftoff')):
        return NotImplemented


class FlapAtGearSelectedDown(KeyPointValueNode):
    def derive(self, flap=P('Flap'), gear_sel_down=P('Gear Selected Down')):
        return NotImplemented


class HeightAtConfigChange1500FtToTouchdownMin(KeyPointValueNode):
    def derive(self, flap=P('Flap'),
               _1500_ft_in_approach=KTI('1500 Ft In Approach'),
               touchdown=KTI('Touchdown')):
        return NotImplemented


class HeightAtConfigChange1500FtToTouchdownMin(KeyPointValueNode):
    def derive(self, flap=P('Flap'),
               _1500_ft_in_approach=KTI('1500 Ft In Approach'),
               touchdown=KTI('Touchdown')):
        return NotImplemented


class SuspectedLevelBust(KeyPointValueNode):
    def derive(self, level_bust=S('Level Bust')):
        return NotImplemented


class LocalizerDeviation1000To150FtMax(KeyPointValueNode):
    def derive(self, ils_loc=P('ILS Localizer'),
               alt_aal = P('Altitude AAL For Flight Phases')):
        # For commented version, see GlideslopeDeviation1500To1000FtMax
        for this_period in alt_aal.slices_from_to(1000, 150):
            begin = this_period.start
            end = this_period.stop
            index = np.ma.argmax(np.ma.abs(ils_loc.array[begin:end]))
            when = begin + index
            value = ils_loc.array[when]
            self.create_kpv(when, value)


class LocalizerDeviation1500To1000FtMax(KeyPointValueNode):
    def derive(self, ils_loc=P('ILS Localizer'),
               alt_aal = P('Altitude AAL For Flight Phases')):
        # For commented version, see GlideslopeDeviation1500To1000FtMax
        for this_period in alt_aal.slices_from_to(1500, 1000):
            begin = this_period.start
            end = this_period.stop
            if alt_aal.array[begin] > alt_aal.array[end-1]:
                index = np.ma.argmax(np.ma.abs(ils_loc.array[begin:end]))
                when = begin + index
                value = ils_loc.array[when]
                self.create_kpv(when, value)


class Flare20FtToTouchdown(KeyPointValueNode):
    def derive(self, alt_rad=P('Altitude Radio'),
               _25_ft_to_touchdown=KTI('25 Ft To Touchdown'),
               touchdown=KTI('Touchdown')):
        return


class LowPowerLessThan500Ft10Sec(KeyPointValueNode):
    def derive(self, eng_n1_min=P('Eng N1 Minimum'),
               _500_ft_in_final_approach=KTI('500 Ft In Final Approach')):
        return NotImplemented


class GroundspeedRTOMax(KeyPointValueNode):
    name = 'Groundspeed RTO Max'
    def derive(self, groundspeed=P('Groundspeed'),
               rejected_takeoff=S('Rejected Takeoff')):
        return NotImplemented


class EngN2CyclesMax(KeyPointValueNode):
    def derive(self, eng_n2=P('Eng N2')):
        return NotImplemented


class EngOIPMax(KeyPointValueNode):
    name = 'Eng OIP Max'
    def derive(self, eng_oil_press=P('Eng Oil Press')):
        return NotImplemented


class EngOIPMin(KeyPointValueNode):
    name = 'Eng OIP Min'
    def derive(self, eng_oil_press_low=P('Eng Oil Press Low')):
        return NotImplemented


class EngOITMax(KeyPointValueNode):
    name = 'Eng OIT Max'
    def derive(self, eng_oil_temp=P('Eng (1) Oil Temp')):
        return NotImplemented


class FuelQtyAtLiftoff(KeyPointValueNode):
    def derive(self, fuel_qty=P('Fuel Qty'), liftoffs=KTI('Liftoff')):
        self.create_kpvs_at_ktis(fuel_qty, liftoffs)


class FuelQtyAtTouchdown(KeyPointValueNode):
    def derive(self, fuel_qty=P('Fuel Qty'), touchdowns=KTI('Touchdown')):
        self.create_kpvs_at_ktis(fuel_qty, touchdowns)


class GrossWeightAtLiftoff(KeyPointValueNode):
    def derive(self, gross_weight=P('Gross Weight'), liftoffs=KTI('Liftoff')):
        self.create_kpvs_at_ktis(gross_weight, liftoffs)


class GrossWeightAtTouchdown(KeyPointValueNode):
    def derive(self, gross_weight=P('Gross Weight'),
               touchdowns=KTI('Touchdown')):
        self.create_kpvs_at_ktis(gross_weight, touchdowns)


class PitchCyclesMax(KeyPointValueNode):
    def derive(self, pitch=P('Pitch')):
        return NotImplemented


class Pitch35To400FtMax(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'),
               alt_aal = P('Altitude AAL For Flight Phases')):
        # For commented version, see GlideslopeDeviation1500To1000FtMax
        for this_slice in alt_aal.slices_from_to(35, 400):
            index = np.ma.argmax(pitch.array[this_slice.start:this_slice.stop])
            when = this_slice.start + index
            value = pitch.array[when]
            self.create_kpv(when, value)


class Pitch1000To100FtMax(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'), _1000_ft_in_approach=KTI('1000 Ft In Approach'),
               _100_ft_in_final_approach=KTI('100 Ft In Final Approach')):
        return NotImplemented


class PitchAtLiftoff(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'), liftoffs=KTI('Liftoff')):
        self.create_kpvs_at_ktis(pitch, liftoffs)


class Pitch5FtToGroundMax(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'), landing=S('Landing')):
        return NotImplemented


class Pitch35To400FtMin(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'),
               _35_ft_in_takeoff=KTI('35 Ft In Takeoff'),
               _400_ft_in_initial_climb=KTI('400 Ft In Initial Climb')):
        return NotImplemented


class Pitch1000To100FtMin(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'),
               _1000_ft_in_approach=KTI('1000 Ft In Approach'),
               _100_ft_in_final_approach=KTI('100 Ft In Final Approach')):
        return NotImplemented


class Pitch20FtToTouchdownMin(KeyPointValueNode):
    def derive(self, pitch=P('Pitch'),
               _25_ft_to_touchdown=KTI('25 Ft To Touchdown'),
               touchdown=KTI('Touchdown')):
        return NotImplemented


class PitchRateDuringTakeoffMax(KeyPointValueNode):
    def derive(self, pitch_rate=P('Pitch Rate'), liftoff=KTI('Liftoff')):
        return NotImplemented


class PitchRate35To1500FtMax(KeyPointValueNode):
    def derive(self, pitch_rate=P('Pitch Rate'),
               _35_ft_in_takeoff=KTI('35 Ft In Takeoff'),
               _1500_ft_in_climb=KTI('1500 Ft In Climb')):
        return NotImplemented


class PitchRateFrom2DegreesOfPitchTo35FtMin(KeyPointValueNode):
    def derive(self, pitch_rate=P('Pitch Rate'), liftoff=KTI('Liftoff'),
               _35_ft_in_takeoff=KTI('35 Ft In Takeoff')):
        return NotImplemented


class PowerOnWithSpeedbrakesDeployedDurationGreaterThanLimit(KeyPointValueNode):
    def derive(self, eng_n1_average=P('Eng N1 Avg'),
               speedbrake=P('Speedbrake')):
        return NotImplemented


class PullUpWarning(KeyPointValueNode):
    def derive(self, gpws_pull_up=P('GPWS Pull Up')):
        return NotImplemented


class RollCycles1000FtToTouchdownMax(KeyPointValueNode):
    def derive(self, roll=P('Roll'),
               _1000_ft_in_approach=KTI('1000 Ft In Approach'),
               touchdown=KTI('Touchdown')):
        return NotImplemented


class RollBetween100And500FtMax(KeyPointValueNode):
    def derive(self, roll=P('Roll'),
               _100_ft_in_initial_climb=KTI('100 Ft In Initial Climb'),
               _500_ft_in_initial_climb=KTI('500 Ft In Initial Climb')):
        return NotImplemented


class RollBetween500And1500FtMax(KeyPointValueNode):
    def derive(self, roll=P('Roll'),
               _500_ft_in_initial_climb=KTI('500 Ft In Initial Climb'),
               _1500_ft_in_climb=KTI('1500 Ft In Climb')):
        return NotImplemented


class RollAbove1500FtMax(KeyPointValueNode):
    def derive(self, roll=P('Roll'), alt_rad=P('Altitude Radio')):
        for above_1500ft_slice in alt_aal.slices_above(1500):
            index, value = max_value(roll.array, _slice=above_1500ft_slice)
            self.create_kpv(index, value)


class RollBelow20FtMax(KeyPointValueNode):
    def derive(self, roll=P('Roll'),
               alt_aal = P('Altitude AAL For Flight Phases')):
        for below_20ft_slice in alt_aal.slices_below(20):
            index, value = max_value(roll.array, _slice=below_20ft_slice)
            self.create_kpv(index, value)


class RudderReversalAbove50Ft(KeyPointValueNode):
    def derive(self, rudder_reversal=S('Rudder Reversal'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        # Q: Should this be Max/Min?
        return NotImplemented


class AirspeedWithGearSelectedDownMax(KeyPointValueNode):
    def derive(self, airspeed=P('Airspeed'),
               gear_sel_down=P('Gear Selected Down')):
        '''
        Expects 'Gear Selected Down' to be a discrete parameter.
        '''
        # Mask values where gear_sel_down != 1.
        airspeed.array[gear_sel_down.array != 1] = np.ma.masked
        value, index = max_value(airspeed.array)
        self.create_kpv(index, value)


class AirspeedAtGearSelectedDown(KeyPointValueNode):
    # Q: Does this mean a KPV will be created on switching the discrete from 0
    # to 1?
    def derive(self, airspeed=P('Airspeed'),
               gear_sel_down=P('Gear Selected Down')):
        return NotImplemented


class AirspeedAtGearSelectedUp(KeyPointValueNode):
    # Q: Does this mean a KPV will be created on switching the discrete from 0
    # to 1?
    def derive(self, airspeed=P('Airspeed'), gear_sel_up=P('Gear Selected Up')):
        return NotImplemented


class TaxiSpeedTurningMax(KeyPointValueNode):
    def derive(self, groundspeed=P('Groundspeed'), on_ground=S('On Ground')):
        return NotImplemented


class AirspeedVref500FtToTouchdownMax(KeyPointValueNode):
    def derive(self, airspeed=P('Airspeed')):
        return NotImplemented


"""
Implemented above
class Airspeed1000To500FtMax(KeyPointValueNode):
    def derive(self, airspeed=P('Airspeed')):
        return NotImplemented
"""

class AirspeedWithFlapMax(KeyPointValueNode):
    NAME_FORMAT = 'Airspeed With Flap %(flap_setting)d Max'
    FLAP_SETTINGS = [1, 2, 5, 10, 15, 25, 30, 40]
    NAME_VALUES = {'flap_setting': FLAP_SETTINGS}
    
    def derive(self, airspeed=P('Airspeed'), flap=P('Flap')):
        for flap_setting in self.FLAP_SETTINGS:
            airspeed_array = np.ma.copy(airspeed.array)
            # Mask values where 'Flap' != flap_setting.
            airspeed_array[flap.array != flap_setting] = np.ma.masked
            value, index = max_value(airspeed_array)
            self.create_kpv(index, value, flap_setting=flap_setting)


class AirspeedWithFlapXMax(KeyPointValueNode):
    '''
    Flap X assumed to mean Flap enabled (non-zero).
    '''
    def derive(self, airspeed_with_flap_max=KPV('Airspeed With Flap Max')):
        max_flap = airspeed_with_flap_max.get_max()
        self.create_kpv(max_flap.index, max_flap.value)


class AirspeedVrefAtTouchdown(KeyPointValueNode):
    def derive(self, airspeed=P('Airspeed'), vref=P('Vref')):
        return NotImplemented


class AirspeedBelow3000FtMax(KeyPointValueNode):
    def derive(self, airspeed=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        for this_slice in alt_aal.slices_below(3000):
            index, value = max_value(alt_aal.array, _slice=this_slice)
            self.create_kpv(index, value)


class TaxiSpeedTurningMax(KeyPointValueNode):
    def derive(self, groundspeed=P('Groundspeed')):
        return NotImplemented


class AirspeedV2AtLiftoff(KeyPointValueNode):
    name = 'Airspeed V2 At Liftoff'
    def derive(self, airspeed=P('Airspeed'), liftoff=KTI('Liftoff')):
        return NotImplemented


class AirspeedBetween90SecToTouchdownAndTouchdownMax(KeyPointValueNode):
    def derive(self, airspeed=P('Airspeed'),
               _90_sec_to_touchdown=KTI('90 Sec To Touchdown'),
               touchdown=KTI('Touchdown')):
        return NotImplemented


class AirspeedV235To400FtMin(KeyPointValueNode):
    name = 'Airspeed V2 35 To 400 Ft Min'
    def derive(self, airspeed=P('Airspeed'),
               _35_ft_in_takeoff=KTI('35 Ft In Takeoff'),
               _400_ft_in_initial_climb=KTI('400 Ft In Initial Climb')):
        return NotImplemented


class AirspeedV2400To1500FtMin(KeyPointValueNode):
    name = 'Airspeed V2 400 To 1500 Ft Min'
    def derive(self, airspeed=P('Airspeed'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        return NotImplemented


class AirspeedVrefLast2MinutesToTouchdownMin(KeyPointValueNode):
    def derive(self, airspeed=P('Airspeed'),
               _2_min_to_touchdown=KTI('2 Min To Touchdown'),
               touchdown=KTI('Touchdown')):
        return NotImplemented


class SpeedbrakesDeployed1000To25Ft(KeyPointValueNode):
    def derive(self, speedbrake=P('Speedbrake'),
               _1000_ft_in_approach=KTI('1000 Ft In Approach'),
               _25_ft_to_touchdown=KTI('25 Ft To Touchdown')):
        return NotImplemented


class FlapWithSpeedbrakesDeployedMax(KeyPointValueNode):
    def derive(self, flap=P('Flap'), speedbrake=P('Speedbrake')):
        return NotImplemented


class StickShakerActivated(KeyPointValueNode):
    def derive(self, stick_shaker=P('Stick Shaker')):
        return NotImplemented


class GPWSTerrainWarning(KeyPointValueNode):
    name = 'GPWS Terrain Warning'
    def derive(self, gpws_terrain=P('GPWS Terrain')):
        return NotImplemented


class GPWSTerrainPullUpWarning(KeyPointValueNode):
    name = 'GPWS Terrain Pull Up Warning'
    def derive(self, gpws_terrain_pull_up=P('GPWS Terrain Pull Up')):
        return NotImplemented


class ThrottleCycles1000FtToTouchdownMax(KeyPointValueNode):
    def derive(self, thrust_lever_n=P('Thrust Lever')):
        return NotImplemented


class TooLowFlapWarning(KeyPointValueNode):
    def derive(self, gpws_too_low_flap=P('GPWS Too Low Flap'), flap=P('Flap')):
        return NotImplemented


class TooLowGearWarning(KeyPointValueNode):
    def derive(self, gpws_too_low_gear=P('GPWS Too Low Gear')):
        return NotImplemented


class GPWSTooLowTerrainWarning(KeyPointValueNode):
    name = 'GPWS Too Low Terrain Warning'
    def derive(self, gpws_too_low_terrain=P('GPWS Too Low Terrain')):
        return NotImplemented


class VibrationN1GreaterThanLimitDurationGreaterThanLimit(KeyPointValueNode):
    name = 'Vibration N1 Greater Than Limit Duration Greater Than Limit'
    def derive(self, eng_n_vib_n1=P('Eng Vib N1'),
               airborne=S('Airborne')):
        return NotImplemented


class VibrationN2GreaterThanLimitDurationGreaterThanLimit(KeyPointValueNode):
    name = 'Vibration N2 Greater Than Limit Duration Greater Than Limit'
    def derive(self, eng_vib_n2=P('Eng Vib N2'),
               airborne=S('Airborne')):
        return NotImplemented


class WindshearWarningBelow1500Ft(KeyPointValueNode):
    def derive(self, gpws_windshear=P('GPWS Windshear'),
               alt_aal=P('Altitude AAL For Flight Phases')):
        return NotImplemented


class TaxiSpeedStraight(KeyPointValueNode):
    def derive(self, groundspeed=P('Groundspeed'), rot=P('Rate Of Turn')):
        return NotImplemented


class TaxiSpeedTurning(KeyPointValueNode):
    def derive(self, groundspeed=P('Groundspeed'), rot=P('Rate Of Turn')):
        return NotImplemented


class LowPowerInFinalApproach10Sec(KeyPointValueNode):
    def derive(self, eng_avg=P('Eng N1 Average'),
               _1000_ft_in_approach=KTI('1000 Ft In Approach'),
               _50_ft_to_touchdown=KTI('50 Ft To Touchdown')):
        return NotImplemented


