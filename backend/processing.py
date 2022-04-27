import os
import threading
from geofile import GeoFile
from geopoint import GeoPoint
from messages import error_messages

def return_error(err):
    return {'status': 'error', 'message': str(err)}

def positions2geopoint(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        return GeoPoint(lat, lon)
    except ValueError as err:
        raise err

def parse_points(args):
    sw = args.get('sw')
    ne = args.get('ne')
    if not sw or not ne:
        raise ValueError(error_messages['NO_MATCH_ARGS'])
    sw, ne = sw.split(','), ne.split(',')
    if (len(sw) != 2) or (len(ne) != 2):
        raise ValueError(error_messages['INCORRECT_ARG_SIZE'])
    try:
        sw = positions2geopoint(sw[0], sw[1])
        ne = positions2geopoint(ne[0], ne[1])
        return sw, ne
    except ValueError as err:
        raise err

def clean_after_timeout(minutes, path):
    print(f'Waiting for the clean {minutes} minutes...')
    sleep_time = minutes * 60
    cleaner = threading.Timer(sleep_time, clean, args=[path])
    cleaner.start()

def clean(path):
    print(f'Removing {path}...')
    os.remove(path)
