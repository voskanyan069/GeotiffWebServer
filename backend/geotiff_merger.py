#!/usr/bin/env python3

import os
import sys
import math
from osgeo import gdal
from .geofile import GeoFile
from .geopoint import GeoPoint
from .checksum_generator import get_checksum

def merge_files(points, load_path, save_path):
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
    hash_name = id(files)
    vrt_path = build_vrt(files, save_path, hash_name)
    tif_name = build_geotiff(vrt_path, save_path, hash_name)
    remove_vrt(vrt_path)
    rename_geotiff(save_path, f'{hash_name}.tif', tif_name)
    return tif_name

def build_vrt(files, save_path, vrt_name):
    out_file = f'{save_path}/{vrt_name}.vrt'
    print(f'Creating {out_file} ...')
    gdal.BuildVRT(out_file, files)
    return out_file

def build_geotiff(vrt_path, save_path, name):
    out_file = f'{save_path}/{name}.tif'
    print(f'Creating {out_file} ...')
    options = ['-of GTiff', '-co "TILED=YES"']
    options_str = ' '.join(options)
    gdal.Translate(out_file, vrt_path, options=options_str)
    tif_name = f'{get_checksum(out_file)}.tif'
    return tif_name

def rename_geotiff(path, old, new):
    print(f'Renaming {old} to {new} ...')
    os.rename(f'{path}/{old}', f'{path}/{new}')

def remove_vrt(path):
    print(f'Removing {path} ...')
    os.remove(path)

if __name__ == '__main__':
    pts = [GeoPoint(39.799, 46.1567), GeoPoint(39.80, 47.49),
            GeoPoint(40.799, 46.4), GeoPoint(41.5, 47.4)]
    merge_files(pts, '/home/user/projects/elevation_map/resources/geotiff/',
            'OUT')
