import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from dateutil.parser import parse
from .utils import level_for_fill
from .contributions import GithubContributions

BASE_URL = 'https://github.com'
CONTRIB_URL = BASE_URL + '/users/{}/contributions'


Day = namedtuple('Day', ['date', 'count', 'level'])


class GithubUser:
    def __init__(self, username, url=CONTRIB_URL):
        self._username = username
        self._url = url

    def _get_svg_soup(self, url, params=None):
        req = requests.get(url, params=params)
        svg = req.content
        soup = BeautifulSoup(svg, 'html.parser')
        return soup

    def contributions(self, end_date=None):
        params = {'from': end_date} if end_date else None
        try:
            soup = self._get_svg_soup(self._url.format(self._username), params)
        except Exception as e:
            raise RuntimeError('Unable to get Github Data: {}'.format(e))

        day_elems = soup.find_all('rect', class_='day')
        days = [Day(date=parse(x['data-date']).date(),
                    count=int(x['data-count']),
                    level=level_for_fill(x['fill']))
                for x in day_elems]
        end_date = parse(end_date).date() if end_date else day_elems[-1].date

        return GithubContributions(days=days, end_date=end_date)

    def current_streak(self):
        pass
