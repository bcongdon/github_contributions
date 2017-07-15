from collections import namedtuple

from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests

from .contributions import GithubContributions
from .utils import level_for_fill

BASE_URL = 'https://github.com'
CONTRIB_URL = BASE_URL + '/users/{}/contributions'


Day = namedtuple('Day', ['date', 'count', 'level'])


class GithubUser(object):
    def __init__(self, username, url=CONTRIB_URL):
        self._username = username
        self._url = url

    def contributions(self, end_date=None):
        params = {'from': end_date} if end_date else None
        try:
            url = self._url.format(self._username)
            req = requests.get(url, params=params)
            svg = req.content
            soup = BeautifulSoup(svg, 'html.parser')
        except Exception as ex:
            raise RuntimeError('Unable to get Github Data: {}'.format(ex))

        day_elems = soup.find_all('rect', class_='day')
        days = [Day(date=parse(x['data-date']).date(),
                    count=int(x['data-count']),
                    level=level_for_fill(x['fill']))
                for x in day_elems]
        end_date = parse(end_date).date() if end_date else day_elems[-1].date

        return GithubContributions(days=days, end_date=end_date)

    def current_streak(self):
        pass
