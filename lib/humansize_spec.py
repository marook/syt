import humansize
import unittest

class FormatSizeSpec(unittest.TestCase):

    def test_bytes(self):
        self.assertFormatted(42, '42B')

    def test_kilo_bytes(self):
        self.assertFormatted(42 * 1024, '42.0kB')

    def assertFormatted(self, size, expected_formatted):
        self.assertEqual(humansize.format_size(size), expected_formatted)

class ParseSizeSpec(unittest.TestCase):

    def test_parse_bytes(self):
        self.assertParse('42', 42)

    def test_parse_bytes_with_suffix(self):
        self.assertParse('42B', 42)

    def test_parse_bytes_with_suffix_and_space(self):
        self.assertParse('42 B', 42)

    def test_parse_kilo_bytes_with_suffix(self):
        self.assertParse('42kB', 42*1024)

    def test_parse_mega_bytes(self):
        self.assertParse('42M', 42*1024*1024)

    def assertParse(self, parsed_string, expected_size):
        self.assertEqual(humansize.parse_size(parsed_string), expected_size)

if __name__ == '__main__':
    unittest.main()
