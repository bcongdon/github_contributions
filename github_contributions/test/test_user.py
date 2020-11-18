import os
from datetime import date

import pytest
import mock
import responses

from github_contributions.contributions import Day
from github_contributions.exceptions import GithubUserNotFoundException
from github_contributions import GithubUser

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


@responses.activate
def test_contributions_structure():
    with open(os.path.join(DATA_PATH, 'bcongdon.html')) as f:
        responses.add(responses.GET,
                      'https://github.com/users/bcongdon/contributions',
                      body=f.read())

    user = GithubUser('bcongdon')
    contributions = user.contributions()
    assert contributions.days
    assert len(contributions.days) == 368
    assert isinstance(contributions.days[0], Day)

    for day in contributions.days:
        assert isinstance(day.count, int)
        assert day.date
        assert isinstance(day.date, date)
        assert isinstance(day.level, int)

    assert contributions.days[0].level == 2
    assert contributions.days[0].count == 4
    assert contributions.days[0].date == date(2019, 11, 17)


@responses.activate  # Used to disable network connectivity
def test_fetch_failed():
    user = GithubUser('bcongdon')
    with pytest.raises(RuntimeError) as err:
        user.contributions()
    assert 'Unable to get Github Data' in str(err)


@responses.activate  # Used to disable network connectivity
def test_cached_results():
    user = GithubUser('bcongdon')
    user._current_data = [1, 2, 3]
    assert user.contributions() == [1, 2, 3]


def test_start_date_default_interval():
    user = GithubUser('bcongdon')

    with mock.patch.object(user, '_get_contributions',
                           wraps=user._get_contributions) as contrib_mock:
        user.contributions(start_date='2016-01-01')
        contrib_mock.assert_called_with(date(2016, 12, 31))


@responses.activate
def test_longest_streak():
    with open(os.path.join(DATA_PATH, 'sindresorhus.html')) as f:
        responses.add(responses.GET,
                      'https://github.com/users/sindresorhus/contributions',
                      body=f.read())

    user = GithubUser('sindresorhus')
    assert len(user.longest_streak()) == 78
    assert user.longest_streak()[0].date == date(2020, 4, 1)


@responses.activate
def test_multi_year_streak():
    with open(os.path.join(DATA_PATH, 'bcongdon_2017.html')) as f:
        responses.add(responses.GET,
                      'https://github.com/users/bcongdon/contributions',
                      match_querystring=True,
                      body=f.read())
    with open(os.path.join(DATA_PATH, 'bcongdon_2016.html')) as f:
        responses.add(responses.GET,
                      ('https://github.com/users/bcongdon/contributions'
                       '?from=2016-07-09'),
                      match_querystring=True,
                      body=f.read())

    user = GithubUser('bcongdon')
    longest_streak = user.longest_streak()
    assert longest_streak
    assert longest_streak[0].date == date(2017, 1, 1)
    assert len(longest_streak) == 291


@responses.activate
def test_user_not_found():
    responses.add(responses.GET,
                  'https://github.com/users/bcongdon/contributions',
                  status=404)

    with pytest.raises(GithubUserNotFoundException):
        GithubUser('bcongdon').contributions()


@responses.activate
def test_bad_response():
    responses.add(responses.GET,
                  'https://github.com/users/bcongdon/contributions',
                  status=400)

    with pytest.raises(RuntimeError) as err:
        GithubUser('bcongdon').contributions()
    assert 'Error getting github data' in str(err)
