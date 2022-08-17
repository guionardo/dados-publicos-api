import re
from datetime import datetime
from html.parser import HTMLParser
from typing import Set, Union


class RFCHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        self.zips: Set[str] = set()
        self.data_ultima_extracao: datetime = datetime.min
        super().__init__(convert_charrefs=convert_charrefs)

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != 'a':
            return super().handle_starttag(tag, attrs)
        attr = {a[0]: a[1] for a in attrs if a[0] in ['class', 'href']}
        a_class, a_href = attr.get('class', ''), attr.get('href', '')
        if a_class == 'external-link' and a_href.endswith('.zip'):
            self.zips.add(a_href)

    def handle_data(self, data: str):
        if self.lasttag == 'div' and 'Data da última extração' in data:
            # <div style="text-align: justify; ">Data da última extração: 09/07/2022</div>
            self.data_ultima_extracao = extract_date(data)


def extract_date(data: str) -> Union[datetime, None]:
    # test_str = "<div style=\"text-align: justify; \">Data da última extração: 09/07/2022</div>"

    regex = r"(\d{2}\/\d{2}\/\d{4})"

    matches = re.finditer(regex, data, re.MULTILINE)

    for _, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            found = match.group(groupNum+1)
            return datetime.strptime(found, '%d/%m/%Y')
