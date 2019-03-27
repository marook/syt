import repo_meta
import wd_meta

def run(argv):
    rpm = repo_meta.find_repo_meta()
    added_files = dict([(f.repo_path, f) for f in rpm.added_files])
    for wd_file in wd_meta.find_files(rpm.repo_root):
        file_repo_path = wd_file.get_repo_path(rpm)        
        status = '+' if file_repo_path in added_files else '?'
        print('{} {}'.format(status, file_repo_path))
