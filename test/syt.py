#!/usr/bin/python3
#
# syt launcher which is just used for testing.
import os.path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from syncthing.main import main as _main

if __name__ == '__main__':
    _main()
