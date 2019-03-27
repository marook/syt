import repository

def run(argv):
    repo = repository.find_repository()
    added_files = dict([(f.repo_path, f) for f in repo.added_files])
    print(repo.name)
    for wd_file in repository.find_files(repo.repo_root):
        file_repo_path = wd_file.get_repository_path(repo)        
        status = '+' if file_repo_path in added_files else '?'
        print('{} {}'.format(status, file_repo_path))
