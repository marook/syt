import hashlib
import os
import platform
import sqlite3
import time

repo_meta_dir = '.syt'
index_db_file_name = 'index.sqlite'

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
        return RepositoryDb(self.index_path)

    @property
    def meta_dir(self):
        return os.path.join(self.repo_root, repo_meta_dir)

    @property
    def index_path(self):
        return os.path.join(self.meta_dir, index_db_file_name)

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
        '''name contains the name of the repository.

        A name contains a host identifier and a repository identifier
        which are separated by a colon. For example
        pc123:/path/to/repo. The repository identifier can but also may
        not be a path to the repository.
        '''
        node_name = platform.node()
        return '{}:{}'.format(node_name, os.path.abspath(self.repo_root))

    def find_tracked_file(self, path):
        abs_path = self.resolve_tracked_path(path)
        if not abs_path.startswith(os.path.abspath(self.repo_root)):
            raise FileNotInRepository('{} not in repository {}'.format(path, self.repo_root))
        repo_path = abs_path[len(self.repo_root)+1:]
        return self.get_tracked_file(repo_path)

    def resolve_tracked_path(self, path):
        for p in self.tracked_path_resolutions(path):
            if os.path.exists(p):
                return os.path.abspath(p)
        raise FileNotInRepository('{} not found in repository'.format(path))

    def tracked_path_resolutions(self, path):
        if os.path.isabs(path):
            yield path
            return
        yield os.path.join(self.repo_root, path)
        yield os.path.abspath(path)

    def get_tracked_file(self, repo_path):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('select content_hash from tracked_files where removed_ts is null and path = ?', (repo_path,))
            row = cur.fetchone()
            if row is None:
                return None
            (content_hash,) = row
            return TrackedFile(self, repo_path, content_hash)

    def get_remote_index_path(self, repo_name):
        repo_host, repo_identifier = repo_name.split(':')
        paths = [self.meta_dir, 'indices', repo_host] + repo_identifier.split('/') + [index_db_file_name,]
        return os.path.join(*paths)

    @property
    def file_content_size(self):
        size = 0
        for f in self.added_files:
            size += f.size
        return size

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

    @property
    def size(self):
        return os.stat(self.path).st_size

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

    @property
    def size(self):
        return os.stat(self.path).st_size

class FileNotInRepository(Exception):
    pass
