from django.test import TestCase

# Create your tests here.


import urllib
import pprint
from visual.data_plots_utils import decode_parameter_uri


class TestURIDecoder(TestCase):

    def setUp(self):
        d = {"ticker": {"symbol": ["S68.SI", "M30.SI"]},
             "kmeans": {"k": 4, "time": ["now", "yest"]}}
        self.uri = urllib.urlencode(d)
        print "url: {}".format(self.uri)

    def test_uri_decoder(self):
        pprint.pprint(decode_parameter_uri(self.uri), width=1)
