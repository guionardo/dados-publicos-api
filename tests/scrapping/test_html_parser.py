import unittest
from datetime import datetime

from src.scrapping.html_parser import extract_date


class TestHtmlParser(unittest.TestCase):

    def test_extract_date_invalid(self):
        d = extract_date('000000')
        self.assertIsNone(d)

    def test_extract_date_valid(self):
        d = extract_date('Data da última extração: 09/07/2022')
        self.assertEqual(datetime(2022, 7, 9), d)
