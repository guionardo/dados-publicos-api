import logging
import os
import sys
import unittest
from datetime import datetime

from src.download.cached_file_download import CachedFileDownload


class TestCachedFileDownload(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.basicConfig(format=logging.BASIC_FORMAT,
                            stream=sys.stdout,
                            level=logging.DEBUG)

        return super().setUpClass()

    def test_download(self):
        cfd = CachedFileDownload(
            './cache', 'http://200.152.38.155/CNPJ/Motivos.zip', datetime(2022, 8, 16))
        filename = cfd.download_file()
        self.assertTrue(os.path.isfile(filename))
