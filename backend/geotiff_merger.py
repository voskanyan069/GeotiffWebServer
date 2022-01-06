#!/usr/bin/env python3

import os
import sys
import math
from osgeo import gdal
from geofile import GeoFile
from geopoint import GeoPoint
from checksum_generator import GenerateChecksum

class GeotiffMerger:
    def __init__(self, load_path, save_path):
        self.load_path = load_path
        self.save_path = save_path

    def merge_points(self, points):
        if ( len(points) != 2 ) and ( len(points) != 4):
            raise ValueError("Points array length must be 2 or 4")
        files = []
        gf = GeoFile(path=self.load_path)
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
        vrt_path = self.__build_vrt(files, hash_name)
        tif_name = self.__build_geotiff(vrt_path, hash_name)
        self.__remove_vrt(vrt_path)
        self.__rename_geotiff(f'{hash_name}.tif', tif_name)
        return tif_name
    
    def __build_vrt(self, files, vrt_name):
        out_file = f'{self.save_path}/{vrt_name}.vrt'
        print(f'Creating {out_file} ...')
        gdal.BuildVRT(out_file, files)
        return out_file
    
    def __build_geotiff(self, vrt_path, name):
        out_file = f'{self.save_path}/{name}.tif'
        print(f'Creating {out_file} ...')
        options = ['-of GTiff', '-co "TILED=YES"']
        options_str = ' '.join(options)
        gdal.Translate(out_file, vrt_path, options=options_str)
        tif_name = f'{GenerateChecksum(out_file)}.tif'
        return tif_name
    
    def __rename_geotiff(self, old, new):
        print(f'Renaming {old} to {new} ...')
        os.rename(f'{self.save_path}/{old}', f'{self.save_path}/{new}')
    
    def __remove_vrt(self, path):
        print(f'Removing {path} ...')
        os.remove(path)
    
if __name__ == '__main__':
    pts = [GeoPoint(40.799, 44.5476), GeoPoint(41.799, 45.5376)]
    merge_files(pts, '/home/user/projects/elevation_map/resources/geotiff/',
            'OUT')
