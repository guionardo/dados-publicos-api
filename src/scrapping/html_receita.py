"""
Scrapping da página de dados públicos da receita federal
"""

import datetime
import logging
import time
from typing import Set

import requests

from src.scrapping.html_parser import RFCHTMLParser

RFB_URL = 'https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj'


class RFBScrapping:

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.html = ''
        self.data_ultima_extracao = datetime.datetime.min
        self.zips: Set[str] = set()

    def fetch_html_content(self, url: str = RFB_URL) -> bool:
        try:
            time_start = time.time()
            response = requests.get(url)
            if response.status_code == 200:
                self.html = response.text
                self.log.info('Fetched %s bytes @ %s', len(response.content),
                              datetime.timedelta(seconds=time.time()-time_start))

                return True
            self.log.warning('Failed to fetch URL %s -> %s %s',
                             url, response.status_code, response.reason)

        except Exception as exc:
            self.log.error('Exception when fetching URL %s - %s', url, exc)
        return False

    def parse_html(self, content: str = '') -> bool:
        if not self.html:
            self.log.warning('html content was empty')
            return False
        try:
            parser = RFCHTMLParser()

            parser.feed(content or self.html)
            if parser.data_ultima_extracao.year < 2000:
                self.log.warning('last extraction date is empty')
                return False
            if not parser.zips:
                self.log.warning('empty zip URLs')
                return False

            self.data_ultima_extracao = parser.data_ultima_extracao
            self.zips = parser.zips
            return True

        except Exception as exc:
            self.log.error('Exception when parsing URL - %s', exc)

        return False
