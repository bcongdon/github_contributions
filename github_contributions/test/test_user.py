import os
from datetime import date

import responses

import github_contributions
from github_contributions import GithubUser


DATA_PATH = os.path.join(os.path.dirname(__file__),
                         'data',
                         'sample_contributions.html')


@responses.activate
def test_contributions_structure():
    with open(DATA_PATH) as f:
        responses.add(responses.GET,
                      'https://github.com/users/bcongdon/contributions',
                      body=f.read())

    user = GithubUser('bcongdon')
    contributions = user.contributions()
    assert contributions.days
    assert len(contributions.days) == 370
    assert isinstance(contributions.days[0], github_contributions.user.Day)

    for day in contributions.days:
        assert isinstance(day.count, int)
        assert day.date
        assert isinstance(day.date, date)
        assert isinstance(day.level, int)

    assert contributions.days[0].level == 1
    assert contributions.days[0].count == 6
    assert contributions.days[0].date == date(2016, 7, 10)
