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
    '''Represents a set of contributions performed by a :py:class:`GithubUser`
    '''

    def __init__(self, soup=None, days=None):
        self.days = days
        '''The list of days in the contributions object

            :type: [Day]
        '''

        if soup:
            self.days = _parse_soup(soup)
        self._streaks = None

    def _filter_date(self, start_date, end_date):
        self.days = [day for day in self.days if day.date >= start_date and day.date <= end_date]

    def today(self):
        """Returns the contribution day object for the current date.

            :returns:  the current day.
            :rtype: Day
        """

        try:
            return next(e for e in self.days if e.date == date.today())
        except StopIteration:
            raise RuntimeError('No contribution data found for today')

    def streaks(self):
        """Produces a list of streaks within the days known by the contributions object

            :returns: the list of streaks
            :rtype: list[list[Day]]
        """

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
        template = '<GithubContributions {0} days of data>'
        return template.format(len(self.days))

    def __repr__(self):
        return self.__str__()
