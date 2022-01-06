#!/usr/bin/env python3

import hashlib

def GenerateChecksum(path, filename=None):
    if filename:
        path += filename
    with open(str(path), 'rb') as file_:
        data = file_.read()
        hash_ = hashlib.md5(data).hexdigest()
        return hash_
