import argparse
import index_transfer
import repository

def run(argv):
    args = parse_args(argv)
    local_repo = repository.find_repository()
    remote_repo = repository.open_repository(args.repository)
    if len(args.index) == 0:
        index_transfer.transfer(local_repo, remote_repo)
    else:
        for index_name in args.index:
            index_transfer.transfer(remote_repo, local_repo, index_name)

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt pull_index', description='Pulls an index from a remote repository')
    p.add_argument('repository')
    p.add_argument('index', nargs='*')
    return p.parse_args(args=argv)
