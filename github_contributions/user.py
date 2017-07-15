from datetime import timedelta, date

from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests

from .contributions import GithubContributions

BASE_URL = 'https://github.com'
CONTRIB_URL = BASE_URL + '/users/{0}/contributions'


class GithubUser(object):
    def __init__(self, username, url=CONTRIB_URL):
        self._username = username
        self._url = url
        self._current_data = None

    def _get_contributions(self, from_date):
        # Return cached data if applicable
        if from_date == date.today() and self._current_data:
            return self._current_data

        params = {'from': from_date} if from_date != date.today() else {}
        try:
            url = self._url.format(self._username)
            req = requests.get(url, params=params)
            svg = req.content
            soup = BeautifulSoup(svg, 'html.parser')
        except Exception as ex:
            raise RuntimeError('Unable to get Github Data: {0}'.format(ex))

        contributions = GithubContributions(soup=soup)

        if from_date == date.today():
            self._current_data = contributions

        return contributions

    def contributions(self, start_date=None, end_date=None):
        '''
        Fetches the contribution history for the given user

        Returns a GithubContributions object
        '''

        start_date = parse(str(start_date)).date() if start_date else None
        end_date = parse(str(end_date)).date() if end_date else None

        # Need to set an end_date to call Github API
        if start_date and not end_date:
            # Default end_date to be ~1 year ahead of start_date
            end_date = start_date + timedelta(days=365)
        elif not end_date:
            # Default end_date to today
            end_date = date.today()

        contributions = self._get_contributions(end_date)

        # Filter by start_date if necessary
        if start_date:
            contributions._filter_start_date(start_date)

        return contributions

    def longest_streak(self):
        streaks = self.contributions().streaks()

        # pylint: disable=unnecessary-lambda
        max_streak = max(streaks, key=lambda s: len(s))
        if len(max_streak) < 365:
            return max_streak
        return self.current_streak()

    def _get_multi_year_streak(self, curr_start, curr_streak=None):
        curr_streak = curr_streak or []
        prev_end_date = curr_start - timedelta(days=1)
        prev_contribs = self.contributions(end_date=prev_end_date)
        last_streak_start = prev_contribs.streaks()[-1][0].date
        prev_contribs_start = prev_contribs.days[0].date
        if last_streak_start != prev_contribs_start:
            return prev_contribs.streaks()[-1] + curr_streak

        combined_streak = prev_contribs.streaks()[-1] + curr_streak
        return self._get_multi_year_streak(prev_contribs_start,
                                           combined_streak)

    def current_streak(self):
        contributions = self.contributions()
        known_streaks = contributions.streaks()
        if not known_streaks:
            return known_streaks
        elif len(known_streaks[-1]) < 365:
            return known_streaks[-1]

        start_date = contributions.days[0].date
        curr_streak = known_streaks[-1]
        return self._get_multi_year_streak(start_date, curr_streak)
