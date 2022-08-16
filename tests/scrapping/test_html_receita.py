import unittest

from src.scrapping.html_receita import RFBScrapping


class TestRFBScrapping(unittest.TestCase):

    def test_fetch_html(self):
        scr = RFBScrapping()
        self.assertTrue(scr.fetch_html_content())
        self.assertTrue(scr.parse_html())

