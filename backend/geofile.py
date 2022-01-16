#!/usr/bin/env python3

import math

class GeoFile:
    def __init__(self, load_path='./', save_path='./'):
        self.load_path = load_path
        self.save_path = save_path

    def create_name(self, point):
        lat = point.latitude()
        lon = point.longitude()
        vertical = 'N'
        horizontal = 'E'
        if (lat < 0):
            vertical = 'S'
        if (lon < 0):
            horizontal = 'W'

        return '%s%02.0f%s%03.0f' % (vertical, math.floor(abs(lat)),
                horizontal, math.floor(abs(lon)))

    def create_tif_path(self, point):
        return f'{self.load_path}/{self.create_name(point)}.tif'

    def merged_filename(self, points):
        start = self.create_name(points[0])
        end = self.create_name(points[1])
        return f'{self.save_path}/{start}_{end}'
