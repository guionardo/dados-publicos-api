import unittest

from src.zip.zip_file_reader import zipfile_reader


class TestZipFileReader(unittest.TestCase):

    def test_0(self):
        for line in zipfile_reader('cache/20220816/Motivos.zip'):
            print(line)
