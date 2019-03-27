import os.path
import repository
import shutil

def transfer(src_repo, dst_repo, src_file_paths):
    for src_file_path in src_file_paths:
        src_file = src_repo.find_tracked_file(src_file_path)
        if src_file is None:
            raise RepoFileNotFound()
        dst_file = dst_repo.get_tracked_file(src_file.repo_path)
        if not dst_file is None:
            if src_file.content_hash == dst_file.content_hash:
                continue
            else:
                raise ContentHashMissmatch('{} exists but content hash missmatch! Source {}. Destination {}.'.format(src_file.repo_path, src_file.content_hash, dst_file.content_hash))
        print('Transfering {}...'.format(src_file.repo_path))
        dst_file_path = os.path.join(dst_repo.repo_root, src_file.repo_path)
        shutil.copyfile(src_file.path, dst_file_path)
        dst_repo.add_file(repository.get_file(dst_file_path), src_file.content_hash)

class RepoFileNotFound(Exception):
    pass

class ContentHashMissmatch(Exception):
    pass
