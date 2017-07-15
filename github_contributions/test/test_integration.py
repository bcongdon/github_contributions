from github_contributions import GithubUser


def test_integration():
    ''' Get live data from Github for sanity checking '''

    user = GithubUser('bcongdon')
    contribs = user.contributions(end_date='2016-01-01')
    assert len(contribs.days) == 370
    assert contribs.days[-10].level == 1
    assert contribs.days[-10].count == 2
