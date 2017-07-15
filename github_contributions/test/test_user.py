import github_contributions
from github_contributions import GithubUser
from datetime import date
import responses
import os

data_path = os.path.join(os.path.dirname(__file__),
                         'data',
                         'sample_contributions.html')


@responses.activate
def test_contributions_structure():
    with open(data_path) as f:
        responses.add(responses.GET,
                      'https://github.com/users/bcongdon/contributions',
                      body=f.read())

    user = GithubUser('bcongdon')
    contributions = user.contributions()
    assert contributions.days
    assert len(contributions.days) == 370
    assert type(contributions.days[0]) == github_contributions.user.Day

    for day in contributions.days:
        assert type(day.count) == int
        assert day.date
        assert type(day.date) == date
        assert type(day.level) == int

    assert contributions.days[0].level == 1
    assert contributions.days[0].count == 6
    assert contributions.days[0].date == date(2016, 7, 10)
