import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from dateutil.parser import parse

BASE_URL = 'https://github.com/'
CONTRIB_URL = BASE_URL + '/users/{}/contributions'

Day = namedtuple('Day', ['date', 'count'])


class User:
    def __init__(self, username, url=CONTRIB_URL):
        self._username = username
        self._url = url

    def _download(self, from_date=None):
        params = {'from': from_date} if from_date else None
        try:
            req = requests.get(self._url.format(self._username), params=params)
            svg = req.content
            soup = BeautifulSoup(svg, 'html.parser')
        except Exception as e:
            raise RuntimeError('Unable to get Github Data: {}'.format(e))

        day_elems = soup.find_all('rect', class_='day')
        days = [Day(date=parse(x['data-date']), count=int(x['data-count']))
                for x in day_elems]
        return days


class GithubContributions:
    @staticmethod
    def new(username):
        return User(username)
