import math

class GeoFile:
    def __init__(self, load_path='./', save_path='./'):
        self.load_path = load_path
        self.save_path = save_path

    def generate_name(self, point):
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

    def generate_path(self, point):
        return f'{self.load_path}/{self.generate_name(point)}.tif'

    def merge_filenames(self, points):
        start = self.generate_name(points[0])
        end = self.generate_name(points[1])
        return f'{self.save_path}/{start}_{end}'
