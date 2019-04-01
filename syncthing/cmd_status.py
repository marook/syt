import argparse
import syncthing.humansize as humansize
import syncthing.repository as repository

def run(argv):
    args = parse_args(argv)
    repo = repository.find_repository()
    added_files = dict([(f.repo_path, f) for f in repo.index.added_files])
    print(repo.name)
    if args.contentSize:
        print('content size: {}'.format(humansize.format_size(repo.file_content_size)))
    for wd_file in repository.find_files(repo.repo_root):
        file_repo_path = wd_file.get_repository_path(repo)        
        status = '+' if file_repo_path in added_files else '?'
        print('{} {}'.format(status, file_repo_path))

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt status', description='Prints the status of the repository.')
    p.add_argument('--content-size', dest='contentSize', action='store_const', const=True, default=False)
    return p.parse_args(args=argv)
