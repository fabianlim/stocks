from django_cron import CronJobBase, Schedule
from ticker.query import QueryInterface
from ticker.models import Ticker, Quote

class PullQuotes(CronJobBase):
    RUN_EVERY_MINS = 10 # every 10 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'visual.pull_query'    # a unique code

    def do(self):
        ticker = 'S68.SI' #singapore exchange
        q = QueryInterface.query_quote(','.join(Quote.get_fields()), ticker)
        Ticker.query_to_models(ticker, q.results, Quote)

