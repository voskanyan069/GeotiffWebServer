#!/usr/bin/env python3

from geopoint import GeoPoint

messages = {
    'NO_MATCH_ARGS': 'no matching call with these arguments',
    'INCORRECT_ARG_SIZE': 'incorrect size of passed argument',
    'POLYGON_SIZE_LIMIT': 'too big size for polygon, please reduce it',
}

def return_error(err):
    return {'status': 'error', 'message': str(err)}

def position_error_handle(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        return GeoPoint(lat, lon)
    except ValueError as e:
        raise e

def process_points(args):
    sw = args.get('sw')
    ne = args.get('ne')
    if not sw or not ne:
        raise ValueError(messages['NO_MATCH_ARGS'])
    sw, ne = sw.split(','), ne.split(',')
    if (len(sw) != 2) or (len(ne) != 2):
        raise ValueError(messages['INCORRECT_ARG_SIZE'])
    try:
        sw = position_error_handle(sw[0], sw[1])
        ne = position_error_handle(ne[0], ne[1])
        return sw, ne
    except ValueError as e:
        raise e
