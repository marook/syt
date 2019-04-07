import argparse
import syncthing.repository as repository

def run(argv):
    args = parse_args(argv)
    repo = repository.find_repository()
    for file_path in args.file:
        repo_file = repo.get_file(file_path)
        repo_file.add()

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt add', description='Adds files to the repo')
    p.add_argument('file', nargs='+')
    return p.parse_args(args=argv)
