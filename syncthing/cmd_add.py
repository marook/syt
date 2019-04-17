import argparse
import os

from syncthing import repository

def run(argv):
    args = parse_args(argv)
    repo = repository.find_repository()
    for file_path in args.file:
        if os.path.isdir(file_path):
            for root, dirs, files in os.walk(file_path):
                for f in files:
                    repo.get_file(os.path.join(root, f)).add()
        else:
            repo.get_file(file_path).add()

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt add', description='Adds files to the repo')
    p.add_argument('file', nargs='+')
    return p.parse_args(args=argv)
