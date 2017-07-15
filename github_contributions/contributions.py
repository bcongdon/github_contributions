from collections import namedtuple
from datetime import date
from dateutil.parser import parse

from .utils import level_for_fill


Day = namedtuple('Day', ['date', 'count', 'level'])


def _parse_soup(soup):
    day_elems = soup.find_all('rect', class_='day')

    days = [Day(date=parse(x['data-date']).date(),
                count=int(x['data-count']),
                level=level_for_fill(x['fill']))
            for x in day_elems]
    return days


class GithubContributions(object):
    def __init__(self, soup=None, days=None):
        if days:
            self.days = days
        else:
            self.days = _parse_soup(soup)
        self._streaks = None

    def _filter_start_date(self, start_date):
        self.days = [day for day in self.days if day.date >= start_date]

    def today(self):
        try:
            return next(e for e in self.days if e.date == date.today())
        except StopIteration:
            raise RuntimeError('No contribution data found for today')

    def streaks(self):
        if self._streaks:
            return self._streaks

        streaks = []
        current_streak = []
        for day in self.days:
            if day.count == 0 and current_streak:
                streaks.append(current_streak)
                current_streak = []
            elif day.count > 0:
                current_streak.append(day)
        if current_streak:
            streaks.append(current_streak)

        self._streaks = streaks
        return streaks

    def __str__(self):
        template = '<GithubContributions {0} days of data ending at {1}>'
        return template.format(len(self.days), self.end_date)

    def __repr__(self):
        return self.__str__()
