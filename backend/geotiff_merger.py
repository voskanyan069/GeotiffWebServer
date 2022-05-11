import os
import math
from osgeo import gdal
from messages import error_messages
from merger import Merger
from geofile import GeoFile
from geopoint import GeoPoint

class GeotiffMerger(Merger):
    def __init__(self, load_path='./', save_path='./', size_limit=30):
        super().__init__(load_path, save_path)
        self.size_limit = size_limit

    def merge_points(self, points):
        if (len(points) != 2) and (len(points) != 4):
            raise ValueError(error_messages['POINTS_ARRAY_INCORRECT_SIZE'])
        files = []
        geopoint = GeoPoint()
        geofile = GeoFile(self.load_path, self.save_path)
        sw = points[0] if (len(points) == 2) else geopoint.min(points)
        ne = points[1] if (len(points) == 2) else geopoint.max(points)
        x1, y1 = math.floor(sw.latitude()), math.floor(sw.longitude())
        x2, y2 = math.floor(ne.latitude()), math.floor(ne.longitude())
        if (x2 - x1) + (y2 - y1) > self.size_limit:
            raise ValueError('POLYGON_SIZE_LIMIT')
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                filename = geofile.generate_path(GeoPoint(i,j))
                self.__check_geofile(filename)
                files.append(filename)
        file_path = geofile.merge_filenames((GeoPoint(x1,y1), GeoPoint(x2,y2)))
        vrt_path = self.__build_vrt(files, file_path)
        geotiff_name = self.__build_geotiff(file_path)
        self.__remove_vrt(vrt_path)
        return geotiff_name

    def __check_geofile(self, filename):
        if not os.path.exists(filename) or not os.path.isfile(filename):
            raise ValueError(f'{filename} does not exists')
    
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
