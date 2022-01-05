#!/usr/bin/env python3

import os
import sys
import math
from osgeo import gdal
from .geofile import GeoFile
from .geopoint import GeoPoint

def merge_files(points, load_path, save_path, output_file):
    if ( len(points) != 2 ) and ( len(points) != 4):
        raise ValueError("Points array length must be 2 or 4")
    print(points[0].latitude())
    files = []
    gf = GeoFile(path=load_path)
    gp = GeoPoint()
    sw = points[0] if ( len(points) == 2 ) else gp.min(points)
    ne = points[1] if ( len(points) == 2 ) else gp.max(points)
    x1 = math.floor(sw.latitude())
    y1 = math.floor(sw.longitude())
    x2 = math.ceil(ne.latitude())
    y2 = math.ceil(ne.longitude())
    for i in range(x1, x2):
        for j in range(y1, y2):
            files.append(gf.filename(GeoPoint(i, j)))
    build_geotiff(files, save_path + '/' + output_file)

def build_geotiff(inputs, output):
    vrt_name = create_vrt(inputs, output)
    tif_name = vrt_to_geotiff(vrt_name, output)
    remove_vrt(vrt_name)

def create_vrt(input_files, output_file):
    output_file += '.vrt'
    print(f'Creating {output_file} ...')
    gdal.BuildVRT(output_file, input_files)
    return output_file

def vrt_to_geotiff(input_file, output_file):
    output_file += '.tif'
    print(f'Creating {output_file} ...')
    options = ['-of GTiff', '-co "TILED=YES"']
    options_str = ' '.join(options)
    gdal.Translate(output_file, input_file, options=options_str)

def remove_vrt(file_):
    print(f'Removing {file_} ...')
    os.remove(file_)

if __name__ == '__main__':
    pts = [GeoPoint(39.799, 46.1567), GeoPoint(39.80, 47.49),
            GeoPoint(40.799, 46.4), GeoPoint(41.5, 47.4)]
    merge_files(pts, '/home/user/projects/elevation_map/resources/geotiff/',
            'OUT')
