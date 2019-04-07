import os
import syncthing.repository as repository
import shutil

def passthrough(*args, **kwargs):
    return True

def transfer(src_repo, dst_repo, src_file_paths, transfer_limit=None, file_filter=passthrough):
    for src_file_path in src_file_paths:
        src_file = src_repo.get_file(src_file_path)
        if src_file.index is None:
            raise RepoFileNotFound('{} not found in repository'.format(src_file_path))
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

class RepoFileNotFound(Exception):
    pass

class ContentHashMissmatch(Exception):
    pass
