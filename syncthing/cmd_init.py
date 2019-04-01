import argparse
import syncthing.repository as repository

def run(argv):
    args = parse_args(argv)
    rpm = repository.Repository(args.path[0])
    rpm.init()

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt init', description='Initializes a new syncthing repo')
    p.add_argument('path', nargs=1)
    return p.parse_args(args=argv)
