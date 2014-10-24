from django.test import TestCase

from models import Ticker

from utils import draw_ticker_figure

from matplotlib import pyplot as plt

# Create your tests here.

from dashboard.views import dashboard  # bad

from django.http import HttpRequest


class TestTicker(TestCase):

    def setUp(self):
        Ticker.objects.create(symbol='S68.SI',
                              industry="Asset Management",
                              industry_id=422,
                              name="Singapore Exchange Ltd")

        Ticker.objects.create(symbol='M30.SI',
                              industry="Agricultural Chemicals",
                              industry_id=112,
                              name="Meghmani Organics Ltd")

    def test_figure(self):

        tick = Ticker.objects.get(symbol='S68.SI')

        # create a pyplot figure
        fig = plt.figure()

        # draw on the figure
        fig = draw_ticker_figure(tick.symbol, fig)

        # show fig
        plt.show()

    def test_dashboard(self):
        import urllib

        d = {"ticker": {"symbol": ["S68.SI", "M30.SI"]}}
        uri = urllib.urlencode(d)

        print "uri: {}".format(uri)

        request = HttpRequest()

        dashboard(request, uri)


from ticker.models import Quote

from ticker.utils import make_numerical_pandas

import pandas as pd

from datetime import timedelta
from django.utils import timezone

import pickle


class TestFixtures(TestCase):
    """ show have to get past 30 days data from
    Django models and convert to a pandas df """

    fixtures = ["db_dump.json", ]

    def test_dump_df(self):
        q = Quote.objects.filter(
            date__gte=timezone.now().date()-timedelta(30))

        df = pd.DataFrame.from_records(q.values())

        # pickle this so I dont have to create the test
        # database (which takes a long time)
        pickle.dump(df, open('debug.p', 'wb'))


class TestPandas(TestCase):

    """ this moves from the raw df dumped from the model,
    into a numerical df ready for processing """
    def test_pandas(self):
        df = pickle.load(open('debug.p', 'rb'))

        # filt_func uses "name", because the df comes from
        # Django model, which uses "name" as field names
        make_numerical_pandas(df,
                              Quote,
                              df_fields=lambda x: x.name,
                              filt_func=lambda x: x.name)

        print df.head()
