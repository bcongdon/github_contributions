# github_contributions
:octocat: A Python interface for Github's contribution system

[![Build Status](https://travis-ci.org/bcongdon/github-contributions.svg?branch=master)](https://travis-ci.org/bcongdon/github-contributions)
[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://tldrlegal.com/license/mit-license)

```python
>>> from github_contributions import GithubUser
>>> user = GithubUser('bcongdon')
>>> print(user.contributions().today())
Day(date=datetime.date(2017, 7, 15), count=2, level=1)
```

## Why github_contributions?

The Github Data API does not provide data on the contribution graphs for users. While you can get fine-grained details on the stats of specific repositories, there is not currently an API for a user's overall contributions.

Calculating a user's contributions by aggregating their repositories is expensive, and can require a prohibitive number of API calls. `github_contributions` can fetch an entire year of contribution data in 1 request.

`github_contributions` exposes user contribution data (i.e. the sum of commits, issues created, and PRs reviewed per day), and also exposes Github's 'contribution level' data (the colors displayed on the contribution graph).

## Basic Usage

### Getting a User's Contribution History

``` python
from github_contributions import GithubUser

user = GithubUser('bcongdon')
contribs = user.contributions()

print(contribs.days[0])
# Day(date=datetime.date(2016, 7, 10), count=6, level=1)

contribs_2016 = user.contributions(start_date='2016-01-01', end_date='2016-12-31')
print(sum([day.count for day in contribs_2016.days]))
# 1509
```

### Getting a User's Current Streak
``` python
from github_contributions import GithubUser

user = GithubUser('bcongdon')
streak = user.current_streak()
print(len(streak))
# 501

print(streak[0].date)
# 2016-03-02)
```

### Getting a User's Past Streaks
``` python
from github_contributions import GithubUser

user = GithubUser('sindresorhus')
contributions = user.contributions()
streaks = contributions.streaks()

print(len(streaks))
# 30

print(streaks[-1][0].date)
# 2017-07-15
```

## Documentation

Read more about the github_contributions API on the [ReadTheDocs]() page.

## Projects that use github_contributions

`github_contributions` is used in the following projects. If you have a project that does something neat with this library, submit a PR or send me a message to be added to this list. 😀

* [3d-contributions](https://github.com/bcongdon/3d-contributions) - 3D Print Your Github Contributions Chart

## Contributing

Contributions to `github_contributions` are welcomed! 😁

1. Fork the repo.
2. Create a new feature branch.
3. Add your feature / make your changes.
4. Install [tox](https://tox.readthedocs.io/) (`pip install tox`) and run `tox` in a terminal window to run the test and linting suite.
5. Create a PR.
6. ???
7. 🎉 Profit. 🎉

## Attribution

Inspired by akerl's [githubstats](https://github.com/akerl/githubstats) Ruby gem
