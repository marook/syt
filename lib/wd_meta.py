import hashlib
import os

def find_files(path):
    for root, dirs, files in os.walk(path):
        if root == path:
            dirs.remove('.syt')
        for f in files:
            yield get_file(os.path.join(root, f))

def get_file(path):
    apath = os.path.abspath(path)
    return WdFile(apath)

class WdFile(object):
    def __init__(self, path):
        self.path = path

    def get_repo_path(self, rpm):
        '''get_repo_path returns the path of the file within the repo.'''
        repo_root = rpm.repo_root
        if not self.path.startswith(repo_root):
            raise FileNotInRepo()
        return self.path[len(repo_root)+1:]

    def content_hash(self):
        h = hashlib.sha224()
        with open(self.path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

class FileNotInRepo(Exception):
    pass