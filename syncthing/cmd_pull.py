import argparse
import syncthing.file_transfer as file_transfer
import syncthing.repository as repository

def run(argv):
    args = parse_args(argv)
    local_repo = repository.find_repository()
    remote_repo = repository.open_repository(args.repository)
    if len(args.file) == 0:
        files = [f.repo_path for f in remote_repo.index.added_files]
        file_transfer.transfer(remote_repo, local_repo, files)
    else:
        file_transfer.transfer(remote_repo, local_repo, args.file)

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt pull', description='Pulls files from a remote repository')
    p.add_argument('repository')
    p.add_argument('file', nargs='*')
    return p.parse_args(args=argv)
