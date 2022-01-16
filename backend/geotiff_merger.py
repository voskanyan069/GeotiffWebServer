#!/usr/bin/env python3

import os
import sys
import math
from osgeo import gdal
from geofile import GeoFile
from geopoint import GeoPoint

class GeotiffMerger:
    def __init__(self, load_path, save_path):
        self.load_path = load_path
        self.save_path = save_path

    def merge_points(self, points):
        if (len(points) != 2) and (len(points) != 4):
            raise ValueError('points array length must be 2 or 4')
        files = []
        gf = GeoFile(self.load_path, self.save_path)
        gp = GeoPoint()
        sw = points[0] if ( len(points) == 2 ) else gp.min(points)
        ne = points[1] if ( len(points) == 2 ) else gp.max(points)
        x1, y1 = math.floor(sw.latitude()), math.floor(sw.longitude())
        x2, y2 = math.floor(ne.latitude()), math.floor(ne.longitude())
        if (x2-x1) + (y2-y1) > 6:
            raise ValueError('too big size for polygon, please reduce it')
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                files.append(gf.create_tif_path(GeoPoint(i, j)))
        file_path = gf.merged_filename(( GeoPoint(x1,y1), GeoPoint(x2,y2) ))
        vrt_path = self.__build_vrt(files, file_path)
        tif_name = self.__build_geotiff(file_path)
        self.__remove_vrt(vrt_path)
        return tif_name
    
    def __build_vrt(self, files, vrt_path):
        out_file = f'{vrt_path}.vrt'
        print(f'Creating {out_file} ...')
        gdal.BuildVRT(out_file, files)
        return out_file
    
    def __build_geotiff(self, path):
        out_file = f'{path}.tif'
        print(f'Creating {out_file} ...')
        options = ['-of GTiff', '-co "TILED=YES"']
        options_str = ' '.join(options)
        gdal.Translate(out_file, f'{path}.vrt', options=options_str)
        return out_file
    
    def __remove_vrt(self, vrt_path):
        print(f'Removing {vrt_path} ...')
        os.remove(vrt_path)
    
if __name__ == '__main__':
    gm = GeotiffMerger('/home/user/projects/elevation_map/resources/geotiff/',
            './OUT')
    pts = [GeoPoint(40.799, 44.5476), GeoPoint(41.799, 45.5376)]
    #pts = [GeoPoint(39.1, 43.1), GeoPoint(42.1, 47.1)]
    gm.merge_points(pts)
