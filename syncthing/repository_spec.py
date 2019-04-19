import os
import shutil
import tempfile
import unittest

from syncthing import repository

class RepositoryTest(unittest.TestCase):

    def setUp(self):
        self.repo_path = tempfile.mkdtemp(prefix='syt_repository_test')
        self.repo = repository.open_repository(self.repo_path)
        self.repo.init()

    def tearDown(self):
        shutil.rmtree(self.repo_path, ignore_errors=True)
    
    def test_index_path(self):
        '''test_index_path should make sure that the repo_path is built
        in an OS independent way.
        '''
        file_path = self.create_repo_file(os.path.join('some', 'repo', 'file.txt'))
        f = self.repo.get_file(file_path)
        self.assertEqual(f.repo_path, 'some/repo/file.txt')

    def create_repo_file(self, file_path, file_content=''):
        abs_file_path = os.path.join(self.repo_path, file_path)
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, 'w') as f:
            f.write(file_content)
        return abs_file_path

if __name__ == '__main__':
    unittest.main()
