import argparse
import repository

def run(argv):
    args = parse_args(argv)
    rpm = repository.find_repo_meta()
    for f in args.file:
        wd_file = repository.get_file(f)
        rpm.add_file(wd_file)

def parse_args(argv):
    p = argparse.ArgumentParser(prog='syt add', description='Adds files to the repo')
    p.add_argument('file', nargs='+')
    return p.parse_args(args=argv)
