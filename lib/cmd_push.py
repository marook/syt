import argparse
import file_transfer
import humansize
import repository

def run(argv):
    args = parse_args(argv)
    local_repo = repository.find_repository()
    remote_repo = repository.open_repository(args.repository)
    transfer_limit = calculate_transfer_limit(remote_repo, args.limit_repo_content_size)
    file_transfer.transfer(local_repo, remote_repo, args.file, transfer_limit=transfer_limit)

def calculate_transfer_limit(repo, limit_repo_content_size):
    if limit_repo_content_size is None:
        return None
    return max(0, limit_repo_content_size - repo.file_content_size)

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt push', description='Pushes files into a remote repository')
    p.add_argument('repository')
    p.add_argument('file', nargs='*')
    p.add_argument('--limit-repo-content-size', dest='limit_repo_content_size', help='Maximum size of the summed up file contents in the target repository. The limit can have a size modifier suffix. k for kilobytes, M for megabytes, G for gigabytes. This size limit does not include disk space needed for the syt index.', type=humansize.parse_size)
    return p.parse_args(args=argv)
