import argparse
import os.path

from syncthing import (
    file_transfer,
    repository,
)

def run(argv):
    args = parse_args(argv)
    local_repo = repository.find_repository()
    remote_repo = repository.open_repository(args.repository)
    if len(args.file) == 0:
        files = [os.path.join(remote_repo.repo_root, tfp) for tfp in remote_repo.index.tracked_file_paths]
    else:
        files = args.file
    file_transfer.transfer(remote_repo, local_repo, files)

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt pull', description='Pulls files from a remote repository')
    p.add_argument('repository')
    p.add_argument('file', nargs='*')
    return p.parse_args(args=argv)
