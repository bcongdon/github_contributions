import os
from datetime import date
import pytest
from bs4 import BeautifulSoup

from github_contributions import GithubContributions
from github_contributions.contributions import Day

DAYS = [
    Day(date=date.today(), level=1, count=5),
    Day(date=date(2017, 1, 1), level=3, count=10)
]
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


def test_init():
    contribs = GithubContributions(days=DAYS)
    assert contribs.days
    assert len(contribs.days) == 2


def test_today():
    contribs = GithubContributions(days=DAYS)
    today = contribs.today()
    assert today
    assert isinstance(today, Day)
    assert today.level == 1
    assert today.count == 5


def test_today_fail():
    contribs = GithubContributions(days=DAYS[1:])
    with pytest.raises(RuntimeError) as err:
        contribs.today()
    assert 'No contribution data' in str(err)


def test_streaks():
    with open(os.path.join(DATA_PATH, 'sindresorhus.html')) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        contributions = GithubContributions(soup=soup)

    streaks = contributions.streaks()
    assert streaks
    assert len(streaks) == 25
    assert len(streaks[0]) == 18
    assert len(streaks[-1]) == 1
    assert streaks[-1][0].date == date(2017, 7, 15)
