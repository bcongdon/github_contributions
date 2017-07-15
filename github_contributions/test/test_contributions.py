from datetime import date
import unittest
import pytest

from github_contributions import GithubContributions
from github_contributions.user import Day

DAYS = [
    Day(date=date.today(), level=1, count=5),
    Day(date=date(2017, 1, 1), level=3, count=10)
]


class TestGithubContributions(unittest.TestCase):
    def setUp(self):
        self.contribs = GithubContributions(DAYS, end_date=date.today())

    def test_init(self):
        assert self.contribs.days
        assert self.contribs.end_date

    def test_today(self):
        today = self.contribs.today()
        assert today
        assert isinstance(today, Day)
        assert today.level == 1
        assert today.count == 5

    def test_today_fail(self):
        self.contribs.days = self.contribs.days[1:]
        with pytest.raises(RuntimeError) as err:
            self.contribs.today()
        assert 'No contribution data' in str(err)
