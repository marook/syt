import argparse
import syncthing.humansize as humansize
import syncthing.repository as repository

def run(argv):
    args = parse_args(argv)
    repo = repository.find_repository()
    print(repo.name)
    if args.contentSize:
        print('content size: {}'.format(humansize.format_size(repo.file_content_size)))
    for file_path in repository.find_files(repo.repo_root):
        repo_file = repo.get_file(file_path)
        status = '?' if repo_file.index is None else '?'
        print('{} {}'.format(status, repo_file.repo_path))

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt status', description='Prints the status of the repository.')
    p.add_argument('--content-size', dest='contentSize', action='store_const', const=True, default=False)
    return p.parse_args(args=argv)
