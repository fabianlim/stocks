from django.test import TestCase

from models import Ticker

from utils import draw_ticker_figure

from matplotlib import pyplot as plt

# Create your tests here.

from visual.views import dashboard  # bad

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
