#!/usr/bin/env python3

import os
from flask import Flask, request, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from backend import ArgParser, ConfigParser, GeotiffMerger, \
                    parse_points, return_error, \
                    clean_after_timeout, install_service, uninstall_service

app = Flask(__name__)
arg_parser = ArgParser()
args = arg_parser.get_args()
config_parser = ConfigParser()
config = config_parser.parse(args.config)
gt_merger = GeotiffMerger(config['load_path'], config['save_path'])
limiter = Limiter(app, key_func=get_remote_address,
        default_limits=config['request_limit'])

api_prefix = '/api/v1'
routes = {
    'routes': [
        f'{api_prefix}/polygon?sw=<lat,lon>&ne=<lat,lon>',
    ]
}

@app.route('/')
@app.route('/help')
@limiter.exempt
def help():
    return routes

@app.route(f'{api_prefix}/polygon')
def get_polygon():
    try:
        points = parse_points(request.args)
        output = gt_merger.merge_points(points).split('/')[-1]
        abs_path = f'{config["save_path"]}/{output}'
        clean_after_timeout(int(config["clean_timeout"]), abs_path)
        return send_from_directory(config['save_path'], path=output,
                as_attachment=True)
    except Exception as err:
        return return_error(err)

@app.errorhandler(404)
@limiter.exempt
def page_not_found(err):
    return return_error(err)

@app.errorhandler(429)
@limiter.exempt
def requests_limit(err):
    return return_error(err)

def main():
    if args.install:
        exec_path = os.path.abspath(__file__)
        install_service(exec_path)
        return
    if args.uninstall:
        uninstall_service()
        return
    app.run(host='0.0.0.0', port=config['port'])

if __name__ == '__main__':
    main()
