from datetime import timedelta, date

from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests

from .contributions import GithubContributions
from .exceptions import GithubUserNotFoundException

BASE_URL = 'https://github.com'
CONTRIB_URL = BASE_URL + '/users/{0}/contributions'


class GithubUser(object):
    def __init__(self, username, url=None):
        '''Represents a user on github, and can poll information about that user's
            contribution history.


            :param str username: The user's Github username
            :param str url: The base Github URL -- useful for use on Github Enterprise. (Optional)
        '''

        self._username = username
        self._url = url or CONTRIB_URL
        self._current_data = None

    def _get_contributions(self, from_date):
        # Return cached data if applicable
        if from_date == date.today() and self._current_data:
            return self._current_data

        params = {'from': str(from_date)} if from_date != date.today() else {}
        try:
            url = self._url.format(self._username)
            req = requests.get(url, params=params)
        except Exception as ex:
            raise RuntimeError('Unable to get Github Data: {0}'.format(ex))

        if req.status_code == 404:
            raise GithubUserNotFoundException()
        elif req.status_code != 200:
            raise RuntimeError(
                'Error getting github data: {}'.format(req.content)
            )

        svg = req.content
        soup = BeautifulSoup(svg, 'html.parser')

        contributions = GithubContributions(soup=soup)

        if from_date == date.today():
            self._current_data = contributions

        return contributions

    def contributions(self, start_date=None, end_date=None):
        '''Fetches the contribution history for the given user

            By default, fetches 1 year of contribution history

            :param date start_date: Optional start date
            :param date end_date: Optional end date. Defaults to today.
            :returns: Returns contributions object
            :rtype: GithubContributions
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
            contributions._filter_date(start_date, end_date)

        return contributions

    def longest_streak(self):
        '''Fetches the longest contribution streak of the user

            Only checks for streaks that have started within the past year.

            :returns: Returns list of days representing longest known streak
            :rtype: list[Day]
        '''

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
        '''Returns the active streak of the user

            Will return the full list of days associated with the user's streak
            even if this streak lasts longer than 1 year.

            :returns: Returns list of days representing current streak
            :rtype: list[Day]
        '''

        contributions = self.contributions()
        known_streaks = contributions.streaks()
        if not known_streaks:
            return known_streaks
        elif len(known_streaks[-1]) < 365:
            return known_streaks[-1]

        start_date = contributions.days[0].date
        curr_streak = known_streaks[-1]
        return self._get_multi_year_streak(start_date, curr_streak)
