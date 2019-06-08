from github_contributions import GithubUser


def test_integration_end_date():
    ''' Get live data from Github for sanity checking '''

    user = GithubUser('bcongdon')
    contribs = user.contributions(end_date='2016-01-01')
    assert len(contribs.days) == 366
    assert contribs.days[-10].level == 2
    assert contribs.days[-10].count == 6


def test_integration_start_and_end_date():
    ''' Get live data from Github for sanity checking '''

    user = GithubUser('bcongdon')
    contribs = user.contributions(
        start_date='2019-01-01', end_date='2019-01-02')
    assert len(contribs.days) == 2
    assert contribs.days[0].level == 1
    assert contribs.days[0].count == 2
