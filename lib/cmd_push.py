import argparse
import os.path
import shutil
import repository

def run(argv):
    args = parse_args(argv)
    local_repo = repository.find_repository()
    remote_repo = repository.open_repository(args.repository)
    for file_path in args.file:
        local_file = local_repo.find_tracked_file(file_path)
        if local_file is None:
            raise RepoFileNotFound()
        remote_file = remote_repo.get_tracked_file(local_file.repo_path)
        if not remote_file is None:
            if local_file.content_hash == remote_file.content_hash:
                continue
            else:
                raise ContentHashMissmatch()
        print('Pushing {}...'.format(local_file.repo_path))
        remote_path = os.path.join(remote_repo.repo_root, local_file.repo_path)
        shutil.copyfile(local_file.path, remote_path)
        remote_repo.add_file(repository.get_file(remote_path), local_file.content_hash)

class RepoFileNotFound(Exception):
    pass

class ContentHashMissmatch(Exception):
    pass

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt push', description='Pushes files into a remote repository')
    p.add_argument('repository')
    p.add_argument('file', nargs='*')
    return p.parse_args(args=argv)
