import argparse
import os.path

from syncthing import (
    humansize,
    repository,
)

def run(argv):
    args = parse_args(argv)
    repo = repository.find_repository()
    print(repo.name)
    if args.contentSize:
        print('content size: {}'.format(humansize.format_size(repo.file_content_size)))
    for file_path in repository.find_files(repo.repo_root):
        repo_file = repo.get_file(file_path)
        status = get_file_status(repo_file)
        if status == '+ ':
            # skip status of added, existing files because it's not
            # very interesting
            continue
        print('{} {}'.format(status, repo_file.repo_path))

def get_file_status(file):
    if not file.index:
        return '? '
    if file.removed:
        if os.path.exists(file.path):
            return '-!'
        else:
            return '- '
    else:
        if os.path.exists(file.path):
            return '+ '
        else:
            return '+!'

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt status', description='Prints the status of the repository.')
    p.add_argument('--content-size', dest='contentSize', action='store_const', const=True, default=False)
    return p.parse_args(args=argv)
