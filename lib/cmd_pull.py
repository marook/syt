import argparse
import file_transfer
import repository

def run(argv):
    args = parse_args(argv)
    local_repo = repository.find_repository()
    remote_repo = repository.open_repository(args.repository)
    file_transfer.transfer(remote_repo, local_repo, args.file)

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt pull', description='Pulls files from a remote repository')
    p.add_argument('repository')
    p.add_argument('file', nargs='*')
    return p.parse_args(args=argv)
