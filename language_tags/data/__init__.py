import os
import json
from io import open

__all__ = ['get']

parent_dir = os.path.dirname(__file__)
data_dir = 'json/'

cache = {}


def get(name):
    if name not in cache:
        with open(os.path.join(parent_dir, data_dir, "%s.json" % name), encoding='utf-8') as f:
            cache[name] = json.load(f)

    return cache[name]
