import os
import shutil

def transfer(src_repo, dst_repo, index_repo_name=None):
    dst_path = dst_repo.get_remote_index_path(src_repo.name if index_repo_name is None else index_repo_name)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    src_path = src_repo.index_path if index_repo_name is None else src_repo.get_remote_index_path(index_repo_name)
    shutil.copyfile(src_path, dst_path)
