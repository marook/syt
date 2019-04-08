"""\
Package import shall not shadow main import
"""
import unittest

class PackageSpec(unittest.TestCase):
    """Test package behaviour (__init__.py, that is)."""

    def test_package_import_shall_not_shadow_main(self):
        import syncthing
        import syncthing.main
        self.assertEqual(type(syncthing), type(syncthing.main))

if __name__ == "__main__":
    unittest.main()
