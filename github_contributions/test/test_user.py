import github_contributions
from github_contributions import GithubUser
from datetime import date
import unittest
import responses
import os

data_path = os.path.join(os.path.dirname(__file__),
                         'data',
                         'sample_contributions.html')


class TestGithubUser(unittest.TestCase):
    @responses.activate
    def setUp(self):
        with open(data_path, 'r') as f:
            responses.add(responses.GET,
                          'https://github.com/users/bcongdon/contributions',
                          body=f.read())

        self.user = GithubUser('bcongdon')

    def test_get_contributions(self):
        self.user.contributions()

    def test_contributions_structure(self):
        contributions = self.user.contributions()
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
