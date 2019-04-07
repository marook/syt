import argparse
import os
from syncthing import repository

def run(argv):
    args = parse_args(argv)
    repo = repository.find_repository()
    for file_path in args.file:
        repo_file = repo.get_file(file_path)
        repo_file.remove()
        if os.path.exists(file_path):
            os.remove(file_path)

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt rm', description='Removes files from the file system and repo index')
    p.add_argument('file', nargs='+')
    return p.parse_args(args=argv)
