#!/usr/bin/env python3

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from backend import GeoFile
from backend import GeoPoint
from backend import GeotiffMerger
from backend import ConfigParser
from backend import return_error, position_error_handle, process_points
from backend import messages

app = Flask(__name__)
parser = ConfigParser()
parser.parse_arguments()
config_ = parser.config()
app.config['SAVE_PATH'] = config_['save_path']
app.config['LOAD_PATH'] = config_['load_path']
merger = GeotiffMerger(app.config['LOAD_PATH'], app.config['SAVE_PATH'])
geofile = GeoFile(save_path=app.config['SAVE_PATH'])
limiter = Limiter(app, key_func=get_remote_address,
        default_limits=config_['request_limit'])

url_prefix = '/api/v1'
request_links = {
    'routes': [
        f'{url_prefix}/polygon?sw=<lat,lon>&ne=<lat,lon>',
        f'{url_prefix}/close_connection?sw=<lat,lon>&ne=<lat,lon>',
    ]
}

@app.route('/')
@app.route('/help')
@limiter.exempt
def root_api():
    return request_links

@app.route(f'{url_prefix}/polygon')
def get_polygon_api():
    try:
        points = process_points(request.args)
        outfile = merger.merge_points(points).split('/')[-1]
        return send_from_directory(app.config['SAVE_PATH'],
                path=outfile, as_attachment=True)
    except Exception as e:
        return return_error(e)

@app.route(f'{url_prefix}/close_connection')
@limiter.exempt
def close_connection_api():
    try:
        points = process_points(request.args)
        path = f'{geofile.merged_filename(points)}.tif'
        os.remove(path)
        return {'filename': path.split('/')[-1], 'deleted': True}
    except Exception as e:
        return return_error(e)

@app.errorhandler(404)
@limiter.exempt
def page_not_found_api(err):
    return return_error(err)

@app.errorhandler(429)
@limiter.exempt
def requests_limit_api(err):
    return return_error(err)

if __name__ == '__main__':
    app.run(debug=True, port=config_['port'])
