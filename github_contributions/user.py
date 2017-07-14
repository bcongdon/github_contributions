import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from dateutil.parser import parse
from .utils import level_for_fill
from .contributions import GithubContributions

BASE_URL = 'https://github.com/'
CONTRIB_URL = BASE_URL + '/users/{}/contributions'


Day = namedtuple('Day', ['date', 'count', 'level'])


class GithubUser:
    def __init__(self, username, url=CONTRIB_URL):
        self._username = username
        self._url = url

    def contributions(self, end_date=None):
        params = {'from': end_date} if end_date else None
        try:
            req = requests.get(self._url.format(self._username), params=params)
            svg = req.content
            soup = BeautifulSoup(svg, 'html.parser')
        except Exception as e:
            raise RuntimeError('Unable to get Github Data: {}'.format(e))

        day_elems = soup.find_all('rect', class_='day')
        days = [Day(date=parse(x['data-date']),
                    count=int(x['data-count']),
                    level=level_for_fill(x['fill']))
                for x in day_elems]
        end_date = parse(end_date) or day_elems[-1].date

        return GithubContributions(days=days, end_date=end_date)