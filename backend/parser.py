#!/usr/bin/env python3

import sys
import json
import argparse

class ConfigParser:
    def __init__(self):
        pass

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', help = 'config file path')
        args = parser.parse_args()
        args = vars(args)
        self.config_file = args['config']
        if not self.config_file:
            self.config_file = 'config.json'

    def config(self):
        try:
            file_ = open(self.config_file)
        except FileNotFoundError as e:
            print(f' [E] {e.strerror}: {e.filename}')
            sys.exit(e.errno)
        else:
            data = json.load(file_)
            data = data['config']
            file_.close()
            return data
