#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_from_directory
from backend.geotiff_merger import merge_files
from backend.geopoint import GeoPoint

app = Flask(__name__)
app.config['LOAD_PATH'] = '/home/user/projects/elevation_map/resources/geotiff/'
app.config['SAVE_PATH'] = '/home/user/projects/elevation_map/resources/merged_data/'
url_prefix = '/api/v1'

messages = {
    'NO_MATCH_ARGS': 'no matching call with these arguments',
    'INCORRECT_ARG_SIZE': 'incorrect size of passed argument',
}

request_links = {
    'request_links': [
        f'{url_prefix}/merge_files?files=<filenames>',
        f'{url_prefix}/point?lat=<lat>&lon=<lon>',
        f'{url_prefix}/polygon?sw=<lat,lon>&ne=<lat,lon>'
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

@app.route('/')
def root_api():
    return request_links

#@app.route(f'{url_prefix}/merge_files')
#def merge_files_api():
#    filenames = request.args.get('files')
#    if not filenames:
#        return return_error(messages['NO_MATCH_ARGS'])
#    filenames = [x.strip() for x in filenames.split(',')]
#    merge_files()
#    return jsonify(filenames)

@app.route(f'{url_prefix}/point')
def get_point_api():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return return_error(messages['NO_MATCH_ARGS'])
    pos_err = position_error_handle(lat, lon)
    if type(pos_err) is dict:
        return pos_err
    return {'status': 'success'}

@app.route(f'{url_prefix}/polygon')
def get_polygon_api():
    sw = request.args.get('sw')
    ne = request.args.get('ne')
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
    points = [sw, ne]
    merge_files(points, app.config['LOAD_PATH'],
            app.config['SAVE_PATH'], str(id(points)))
    try:
        return send_from_directory(app.config['SAVE_PATH'],
            path=f'{str(id(points))}.tif', as_attachment=True)
    except Exception as e:
        return return_error(e)

if __name__ == '__main__':
    app.run(debug=True, port=6767)
