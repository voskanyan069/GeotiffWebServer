#!/usr/bin/env python3

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from backend import GeoPoint
from backend import GeotiffMerger
from backend import return_error, position_error_handle, process_points
from backend import messages

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address,
        default_limits=['50 per hour'])

res_path = '/home/user/projects/elevation_map/resources'
app.config['LOAD_PATH'] = f'{res_path}/geotiff/'
app.config['SAVE_PATH'] = f'{res_path}/merged_data/'
merger = GeotiffMerger(app.config['LOAD_PATH'], app.config['SAVE_PATH'])
url_prefix = '/api/v1'

request_links = {
    'routes': [
        f'{url_prefix}/polygon?sw=<lat,lon>&ne=<lat,lon>',
        f'{url_prefix}/close_connection?checksum=<file_checksum>',
    ]
}

@app.route('/')
@app.route('/help')
def root_api():
    return request_links

@app.route(f'{url_prefix}/polygon')
@limiter.limit('5 per minute')
def get_polygon_api():
    try:
        points = process_points(request.args)
        outfile = merger.merge_points(points)
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
    return return_error(err)

@app.errorhandler(429)
def requests_limit_api(err):
    return return_error(err)

if __name__ == '__main__':
    app.run(debug=True, port=6767)
