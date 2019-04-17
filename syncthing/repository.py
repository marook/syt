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
        self.index.init()

    @property
    def meta_dir(self):
        return os.path.join(self.repo_root, repo_meta_dir)

    @property
    def index(self):
        return RepositoryIndex(self.meta_dir)

    @property
    def repo_host(self):
        return platform.node()

    @property
    def name(self):
        '''name contains the name of the repository.

        A name contains a host identifier and a repository identifier
        which are separated by a colon. For example
        pc123:/path/to/repo. The repository identifier can but also may
        not be a path to the repository.
        '''
        return '{}:{}'.format(self.repo_host, os.path.abspath(self.repo_root))

    def get_file(self, path):
        '''get_file returns a RepositoryFile for the given path.
        '''
        abs_path = os.path.abspath(path)
        if not abs_path.startswith(os.path.abspath(self.repo_root)):
            raise FileNotInRepository('{} not in repository {}'.format(path, self.repo_root))
        repo_path = abs_path[len(self.repo_root)+1:]
        file_index = self.index.get_file(repo_path)
        return RepositoryFile(self, repo_path, index=file_index)

    def get_remote_meta_dir(self, repo_name):
        colon_pos = repo_name.find(':')
        if colon_pos == -1:
            repo_host = self.repo_host
            repo_identifier = repo_name
        else:
            repo_host = repo_name[0:colon_pos]
            repo_identifier = repo_name[colon_pos+1:]
        paths = [self.meta_dir, 'indices', repo_host] + repo_identifier.split('/')
        return os.path.join(*paths)

    @property
    def file_content_size(self):
        size = 0
        for f in self.added_files:
            size += f.size
        return size

    @property
    def added_files(self):
        # TODO remove?
        for repo_path in self.index.added_file_paths:
            yield self.get_file(os.path.join(self.repo_root, repo_path))

    def get_remote_index(self, repo_name):
        return RepositoryIndex(self.get_remote_meta_dir(repo_name))

class FileNotInRepository(Exception):
    pass

class RepositoryIndex(object):
    def __init__(self, meta_dir):
        self.meta_dir = meta_dir

    @property
    def path(self):
        return os.path.join(self.meta_dir, index_db_file_name)

    def _connect(self):
        return RepositoryDb(self.path)

    def init(self):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('create table schema_history (migration text primary key not null)')
            cur.execute('create table tracked_files (path text primary key not null, content_hash text not null, added_ts integer not null, removed_ts integer)')

    def get_file(self, repo_path):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('select content_hash, added_ts, removed_ts from tracked_files where path = ?', (repo_path,))
            row = cur.fetchone()
            if row is None:
                return None
            (content_hash, added_ts, removed_ts) = row
            return FileIndex(repo_path, content_hash, added_ts, removed_ts)

    @property
    def tracked_file_paths(self):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('select path from tracked_files')
            for repo_path, in cur.fetchall():
                yield repo_path

    @property
    def added_file_paths(self):
        # TODO remove?
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('select path from tracked_files where removed_ts is null')
            for repo_path, in cur.fetchall():
                yield repo_path

    @property
    def added_content_hashes(self):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('select content_hash from tracked_files where removed_ts is null')
            for content_hash, in cur.fetchall():
                yield content_hash

    def insert_file(self, file_index):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('insert into tracked_files (path, content_hash, added_ts, removed_ts) values (?, ?, ?, ?)', (file_index.path, file_index.content_hash, file_index.added_ts, file_index.removed_ts))
            con.commit()

    def update_removed_ts(self, repo_path, removed_ts):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('update tracked_files set removed_ts = ? where path = ?', (removed_ts, repo_path))
            con.commit()

    def replace_file(self, file_index):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute('delete from tracked_files where path = ?', (file_index.path, ))
            cur.execute('insert into tracked_files (path, content_hash, added_ts, removed_ts) values (?, ?, ?, ?)', (file_index.path, file_index.content_hash, file_index.added_ts, file_index.removed_ts))
            con.commit()

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

class RepositoryFile(object):
    '''RepositoryFile represents a file within the repository.
    '''

    def __init__(self, repo, repo_path, index=None):
        self.repo = repo
        self.repo_path = repo_path
        self.index = index

    @property
    def path(self):
        return os.path.join(self.repo.repo_root, self.repo_path)

    @property
    def size(self):
        return os.stat(self.path).st_size

    @property
    def removed(self):
        return not self.index is None and not self.index.removed_ts is None

    def add(self):
        '''add adds this file to the repository index.
        '''
        if not self.index is None:
            raise ValueError('RepositoryFile has already an index')
        now = current_time_milliseconds()
        file_index = FileIndex(self.repo_path, self.content_hash(), now)
        self.repo.index.insert_file(file_index)
        self.index = file_index
        
    def remove(self):
        '''remove removes this file from the repository index.
        '''
        if self.index is None:
            raise ValueError('RepositoryFile has no index')
        now = current_time_milliseconds()
        self.repo.index.update_removed_ts(self.repo_path, now)
        self.index.removed_ts = now

    def content_hash(self):
        h = hashlib.sha224()
        with open(self.path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

def current_time_milliseconds():
    # taken from https://stackoverflow.com/a/5998359/404522
    return int(round(time.time() * 1000))

class FileIndex(object):
    '''FileIndex holds all values stored about a tracked file within the index.
    '''

    def __init__(self, path, content_hash, added_ts, removed_ts=None):
        self.path = path
        self.content_hash = content_hash
        self.added_ts = added_ts
        self.removed_ts = removed_ts

def find_files(path):
    '''find_files finds file paths which can be tracked.
    '''
    for root, dirs, files in os.walk(path):
        if root == path:
            dirs.remove(repo_meta_dir)
        for f in files:
            yield os.path.join(root, f)
