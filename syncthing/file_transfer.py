import os
import syncthing.repository as repository
import shutil

def passthrough(*args, **kwargs):
    return True

def transfer(src_repo, dst_repo, src_file_paths, transfer_limit=None, file_filter=passthrough):
    added_files, removed_files = lookup_files(src_repo, src_file_paths)
    for src_file in removed_files:
        dst_file_path = os.path.join(dst_repo.repo_root, src_file.repo_path)
        dst_file = dst_repo.get_file(dst_file_path)
        if os.path.exists(dst_file_path):
            if not transfer_limit is None:
                transfer_limit += dst_file.size
            os.remove(dst_file_path)
        dst_repo.index.replace_file(src_file.index)
    for src_file in added_files:
        if src_file.index is None:
            raise RepoFileNotFound('{} not found in repository'.format(src_file.path))
        if not file_filter(src_file):
            continue
        dst_file = dst_repo.get_file(os.path.join(dst_repo.repo_root, src_file.repo_path))
        if not dst_file.index is None:
            if src_file.index.content_hash == dst_file.index.content_hash:
                continue
            else:
                raise ContentHashMissmatch('{} exists but content hash missmatch! Source {}. Destination {}.'.format(src_file.repo_path, src_file.index.content_hash, dst_file.index.content_hash))
        if not transfer_limit is None:
            src_file_size = src_file.size
            if src_file_size > transfer_limit:
                # maybe we find another file which fits into the
                # remaining transfer limit
                continue
            transfer_limit -= src_file_size
        print('Transfering {}...'.format(src_file.repo_path))
        dst_file_path = dst_file.path
        os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
        shutil.copyfile(src_file.path, dst_file_path)
        dst_repo.index.insert_file(src_file.index)

def lookup_files(repo, file_paths):
    added_files = []
    removed_files = []
    for fp in file_paths:
        f = repo.get_file(fp)
        if f.removed:
            removed_files.append(f)
        else:
            added_files.append(f)
    return added_files, removed_files

class RepoFileNotFound(Exception):
    pass

class ContentHashMissmatch(Exception):
    pass
