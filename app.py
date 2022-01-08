#!/usr/bin/env python3

import os
from flask import Flask, request, jsonify, send_from_directory
from backend import GeoPoint
from backend import GeotiffMerger

app = Flask(__name__)
app.config['LOAD_PATH'] = '/home/user/projects/elevation_map/resources/geotiff/'
app.config['SAVE_PATH'] = '/home/user/projects/elevation_map/resources/merged_data/'
url_prefix = '/api/v1'
merger = GeotiffMerger(app.config['LOAD_PATH'], app.config['SAVE_PATH'])

messages = {
    'NO_MATCH_ARGS': 'no matching call with these arguments',
    'INCORRECT_ARG_SIZE': 'incorrect size of passed argument',
}

request_links = {
    'routes': [
        f'{url_prefix}/polygon?sw=<lat,lon>&ne=<lat,lon>',
        f'{url_prefix}/close_connection?checksum=<file_checksum>',
    ]
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
    if ( len(sw) != 2 ) or ( len(ne) != 2):
        return return_error(messages['INCORRECT_ARG_SIZE'])
    sw = position_error_handle(sw[0], sw[1])
    ne = position_error_handle(ne[0], ne[1])
    if type(sw) is dict:
        return sw
    if type(ne) is dict:
        return ne
    return sw, ne

@app.route('/')
@app.route('/help')
def root_api():
    return request_links

@app.route(f'{url_prefix}/polygon')
def get_polygon_api():
    points = process_points(request.args)
    outfile = merger.merge_points(points)
    try:
        return send_from_directory(app.config['SAVE_PATH'],
                path=outfile, as_attachment=True)
    except Exception as e:
        return return_error(e)

@app.route(f'{url_prefix}/close_connection')
def close_connection_api():
    checksum = request.args.get('checksum')
    if not checksum:
        return return_error(messages['NO_MATCH_ARGS'])
    try:
        os.remove(f'{app.config["SAVE_PATH"]}/{checksum}.tif')
        return {'filename': f'{checksum}.tif', 'deleted': True}
    except Exception as e:
        return return_error(e)

@app.errorhandler(404)
def page_not_found_api(err):
    return {'status': 'error', 'message': str(err)}

if __name__ == '__main__':
    app.run(debug=True, port=6767)
