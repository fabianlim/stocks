from django_cron import CronJobBase, Schedule

from populate_ticker import pull_sg_quotes


class PullQuotes(CronJobBase):
    RUN_EVERY_MINS = 30  # every 10 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'visual.pull_query'    # a unique code

    def do(self):
        pull_sg_quotes()  # focusing on SG quotes for nowl
