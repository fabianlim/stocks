from django_cron import CronJobBase, Schedule
from ticker.query import QueryInterface
from ticker.models import Ticker, Quote

from populate_ticker import pull_sg_quotes
class PullQuotes(CronJobBase):
    RUN_EVERY_MINS = 1 # every 10 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'visual.pull_query'    # a unique code

    def do(self):
        pull_sq_quotes()

