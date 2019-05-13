import pkg_resources

requirement = pkg_resources.Requirement.parse('FlightDataAnalyzer')
distribution = pkg_resources.working_set.find(requirement)

__version__ = distribution.version if distribution else 'N/A'


def analyze(fdf, aircraft_info, segment_type='START_AND_STOP', *args, **kwargs):
    '''
    Analyze a FlightDataFormat object to produce various metrics.

    :param fdf: FlightDataFormat object for a single flight.
    :type fdf: FlightDataFormat
    :param aircraft_info: Aircraft info dictionary for the aircraft which recorded the flight data.
    :type aircraft_info: dict
    :returns: FlightDataFormat nodes dictionary containing the results of analysis.
    :rtype: dict
    '''
    from analysis_engine.process_flight import process_flight

    return fdf, process_flight(
        {'File': fdf, 'Segment Type': segment_type},
        aircraft_info['Tail Number'],
        *args,
        aircraft_info=aircraft_info,
        force=True,
        **kwargs
    )


def split(fdf, aircraft_info, *args, **kwargs):
    '''
    Split a FlightDataFormat object into individual flights.

    :param fdf: FlightDataFormat object containing any number of flights.
    :type fdf: FlightDataFormat
    :param aircraft_info: Aircraft info dictionary for the aircraft which recorded the flight data.
    :type aircraft_info: dict
    :returns: A list of analysis_engine.Segment objects where the path attribute is the flight split FlightDataFormat object.
    :rtype: [Segment]
    '''
    from analysis_engine.split_hdf_to_segments import split_hdf_to_segments

    return split_hdf_to_segments(fdf, aircraft_info, *args, **kwargs)

