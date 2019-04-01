import os
import syncthing.repository as repository
import shutil

def passthrough(*args, **kwargs):
    return True

def transfer(src_repo, dst_repo, src_file_paths, transfer_limit=None, file_filter=passthrough):
    for src_file_path in src_file_paths:
        src_file = src_repo.find_tracked_file(src_file_path)
        if src_file is None:
            raise RepoFileNotFound()
        if not file_filter(src_file):
            continue
        dst_file = dst_repo.index.get_tracked_file(src_file.repo_path)
        if not dst_file is None:
            if src_file.content_hash == dst_file.content_hash:
                continue
            else:
                raise ContentHashMissmatch('{} exists but content hash missmatch! Source {}. Destination {}.'.format(src_file.repo_path, src_file.content_hash, dst_file.content_hash))
        if not transfer_limit is None:
            src_file_size = src_file.size
            if src_file_size > transfer_limit:
                # maybe we find another file which fits into the
                # remaining transfer limit
                continue
            transfer_limit -= src_file_size
        print('Transfering {}...'.format(src_file.repo_path))
        dst_file_path = os.path.join(dst_repo.repo_root, src_file.repo_path)
        os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
        shutil.copyfile(src_file.path, dst_file_path)
        dst_repo.index.add_file(repository.get_file(dst_file_path), src_file.content_hash)

class RepoFileNotFound(Exception):
    pass

class ContentHashMissmatch(Exception):
    pass
