#!/usr/bin/env python3

from geopoint import GeoPoint

messages = {
    'NO_MATCH_ARGS': 'no matching call with these arguments',
    'INCORRECT_ARG_SIZE': 'incorrect size of passed argument',
}

def return_error(err):
    return {'status': 'error', 'message': str(err)}

def position_error_handle(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError as e:
        return return_error(e)
    else:
        return GeoPoint(lat, lon)

def process_points(args):
    sw = args.get('sw')
    ne = args.get('ne')
    if not sw or not ne:
        return return_error(messages['NO_MATCH_ARGS'])
    sw, ne = sw.split(','), ne.split(',')
    if (len(sw) != 2) or (len(ne) != 2):
        return return_error(messages['INCORRECT_ARG_SIZE'])
    sw = position_error_handle(sw[0], sw[1])
    ne = position_error_handle(ne[0], ne[1])
    if type(sw) is dict:
        return sw
    if type(ne) is dict:
        return ne
    return sw, ne
