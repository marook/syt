import argparse
import os
from syncthing import repository

def run(argv):
    args = parse_args(argv)
    repo = repository.find_repository()
    for f in args.file:
        wd_file = repository.get_file(f)
        repo.index.remove_file(wd_file)
        if os.path.exists(f):
            os.remove(f)

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt rm', description='Removes files from the file system and repo index')
    p.add_argument('file', nargs='+')
    return p.parse_args(args=argv)
