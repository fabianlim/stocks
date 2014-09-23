from django.test import TestCase

from ticker.models import Ticker

from data_plots_utils import draw_ticker_figure

from matplotlib import pyplot as plt

# Create your tests here.


class TestFigure(TestCase):

    def setUp(self):
        Ticker.objects.create(symbol='S68.SI',
                              industry="Asset Management",
                              industry_id=422,
                              name="Singapore Exchange Ltd")

    def test_figure(self):

        tick = Ticker.objects.get(symbol='S68.SI')

        # create a pyplot figure
        fig = plt.figure()

        # draw on the figure
        fig = draw_ticker_figure(tick, fig)

        # show fig
        plt.show()
