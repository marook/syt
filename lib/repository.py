import hashlib
import os
import platform
import sqlite3
import time

repo_meta_dir = '.syt'

def find_repository(dir=os.getcwd()):
    meta_dir = os.path.join(dir, repo_meta_dir)
    if os.path.exists(meta_dir):
        return open_repository(dir)
    parent_dir = os.path.dirname(dir)
    if(parent_dir == dir):
        raise RepositoryNotFound()
    return find_repository(parent_dir)

class RepositoryNotFound(Exception):
    pass

def open_repository(repo_path):
    abs_repo_path = os.path.abspath(repo_path)
    return Repository(abs_repo_path)

class Repository(object):
    def __init__(self, repo_root):
        self.repo_root = repo_root

    def init(self):
        os.mkdir(self.meta_dir)
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('create table tracked_files (path text primary key not null, content_hash text not null, added_ts integer not null, removed_ts integer)')

    def _connect(self):
        return RepositoryDb(os.path.join(self.meta_dir, 'db.sqlite'))

    @property
    def meta_dir(self):
        return os.path.join(self.repo_root, repo_meta_dir)

    @property
    def added_files(self):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('select path, content_hash from tracked_files where removed_ts is null')
            for repo_path, content_hash in cur.fetchall():
                yield TrackedFile(self, repo_path, content_hash)

    def add_file(self, wd_file, content_hash=None):
        now = current_time_milliseconds()
        content_hash = wd_file.content_hash() if content_hash is None else content_hash
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('insert into tracked_files (path, content_hash, added_ts) values (?, ?, ?)', (wd_file.get_repository_path(self), content_hash, now))
            con.commit()

    @property
    def name(self):
        node_name = platform.node()
        return '{}:{}'.format(node_name, os.path.abspath(self.repo_root))

    def find_tracked_file(self, path):
        abs_path = os.path.abspath(path)
        if not abs_path.startswith(os.path.abspath(self.repo_root)):
            raise FileNotInRepository()
        repo_path = abs_path[len(self.repo_root)+1:]
        return self.get_tracked_file(repo_path)

    def get_tracked_file(self, repo_path):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('select content_hash from tracked_files where removed_ts is null and path = ?', (repo_path,))
            row = cur.fetchone()
            if row is None:
                return None
            (content_hash,) = row
            return TrackedFile(self, repo_path, content_hash)

def current_time_milliseconds():
    # taken from https://stackoverflow.com/a/5998359/404522
    return int(round(time.time() * 1000))

class RepositoryDb(object):
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self.connection
    
    def __exit__(self, *args, **kwargs):
        if not self.connection is None:
            self.connection.close()
            self.connection = None

class TrackedFile(object):
    def __init__(self, repo, repo_path, content_hash):
        self.repo = repo
        self.repo_path = repo_path
        self.content_hash = content_hash

    @property
    def path(self):
        return os.path.join(self.repo.repo_root, self.repo_path)

def find_files(path):
    for root, dirs, files in os.walk(path):
        if root == path:
            dirs.remove(repo_meta_dir)
        for f in files:
            yield get_file(os.path.join(root, f))

def get_file(path):
    apath = os.path.abspath(path)
    return WdFile(apath)

class WdFile(object):
    def __init__(self, path):
        self.path = path

    def get_repository_path(self, rpm):
        '''get_repository_path returns the path of the file within the repository.'''
        repo_root = rpm.repo_root
        if not self.path.startswith(repo_root):
            raise FileNotInRepository('{} not in {}'.format(self.path, repo_root))
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

class FileNotInRepository(Exception):
    pass
