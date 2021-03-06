import sys
import json
import argparse

class ArgParser:
    def __init__(self):
        parser = argparse.ArgumentParser('Allowed options')
        parser.add_argument('-c', '--config', default='./config.json',
                help='path to config file')
        parser.add_argument('-i', '--install', default=False,
                action='store_true', help='install service')
        parser.add_argument('-u', '--uninstall', default=False,
                action='store_true', help='uninstall service')
        self.__args = parser.parse_args()

    def get_args(self):
        return self.__args

class ConfigParser:
    def __init__(self):
        pass

    def parse(self, path):
        try:
            file_ = open(path)
        except FileNotFoundError as err:
            print(f'{err.strerror}: {err.filename}')
            sys.exit(err.errno)
        else:
            data = json.load(file_)
            data = data['config']
            file_.close()
            return data
