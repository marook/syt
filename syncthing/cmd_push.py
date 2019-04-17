import argparse
import os.path

from syncthing import (
    file_transfer,
    humansize,
    repository,
)

def run(argv):
    args = parse_args(argv)
    local_repo = repository.find_repository()
    remote_repo = repository.open_repository(args.repository)
    transfer_limit = calculate_transfer_limit(remote_repo, args.limit_repo_content_size)
    file_filter = file_transfer.passthrough if args.exclude_repo_content is None else build_exclude_repo_content_filter(local_repo, args.exclude_repo_content)
    if len(args.file) == 0:
        files = [os.path.join(local_repo.repo_root, fp) for fp in local_repo.index.tracked_file_paths]
    else:
        files = args.file
    file_transfer.transfer(local_repo, remote_repo, files, transfer_limit=transfer_limit, file_filter=file_filter)

def calculate_transfer_limit(repo, limit_repo_content_size):
    if limit_repo_content_size is None:
        return None
    return max(0, limit_repo_content_size - repo.file_content_size)

def build_exclude_repo_content_filter(local_repo, repo_name):
    remote_index = local_repo.get_remote_index(repo_name)
    return ExcludeExistingFilter(remote_index).filter

class ExcludeExistingFilter(object):
    def __init__(self, remote_index):
        self.remote_index = remote_index
        self.existing_content_hashes_cache = None

    @property
    def existing_content_hashes(self):
        if self.existing_content_hashes_cache is None:
            self.existing_content_hashes_cache = frozenset(self.remote_index.added_content_hashes)
        return self.existing_content_hashes_cache

    def filter(self, repo_file):
        return not repo_file.index.content_hash in self.existing_content_hashes

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt push', description='Pushes files into a remote repository')
    p.add_argument('repository')
    p.add_argument('file', nargs='*')
    p.add_argument('--limit-repo-content-size', dest='limit_repo_content_size', help='Maximum size of the summed up file contents in the target repository. The limit can have a size modifier suffix. k for kilobytes, M for megabytes, G for gigabytes. This size limit does not include disk space needed for the syt index.', type=humansize.parse_size)
    p.add_argument('--exclude-repo-content', dest='exclude_repo_content', help='Specifies a repo which content must not be pushed.')
    return p.parse_args(args=argv)
