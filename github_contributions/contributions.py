from datetime import date


class GithubContributions:
    def __init__(self, days, end_date):
        self.days = days
        self.end_date = end_date

    def today(self):
        try:
            return next(e for e in self.days if e.date == date.today())
        except StopIteration:
            return RuntimeError('No contribution data found for today')
