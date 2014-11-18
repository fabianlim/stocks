from django.test import TestCase, Client

# Create your tests here.


import urllib
import pprint
from common.utils import decode_parameter_uri


class TestURIDecoder(TestCase):
    fixtures = ['ticker_db.json', ]

    def setUp(self):
        # self.d = {"ticker": {"symbol": ["S68.SI", "M30.SI"]},
        #            "kmeans": {"k": 4, "time": ["now", "yest"]}}
        self.d = {"ticker": {"symbol": ["S68.SI", "M30.SI"]},
                  "dimreduce": {"algo": "pca",
                                "input": "/ticker/data/quote/?days=30"}}
        self.d = {"ticker": {"symbol": ["M30.SI"]}}

        self.uri = urllib.urlencode(self.d)
        print "url: {}".format(self.uri)

    def test_uri_decoder(self):
        pprint.pprint(decode_parameter_uri(self.uri), width=1)

    def test_dash(self):
        c = Client()

        r = c.get('/stocks/dashboard/', self.d)

        print r

    def test_search(self):

        # d = {"ticker": {"symbol": ["S68.SI", "M30.SI"]},
        #      "search": {"keys": ["oil", "plaster"]}}

        d = {"ticker": {"symbol": ["S68.SI", "M30.SI"]},
             "search": "oil sin"}

        import urllib
        uri = urllib.urlencode(d)
        print "uri: {}".format(uri)
