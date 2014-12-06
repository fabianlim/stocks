from django.test import TestCase, Client

# Create your tests here.


class TestGetData(TestCase):

    fixtures = ["dimreduce.json", ]

    def test_uri(self):

        # d = {"params": {"input": "/ticker/data/quote/?days=30"},
        #      "figtype": "eigen_dirs"}

        d = {"input": "/ticker/data/quote/?days=30",
             "algo_url": "/dimreduce/data/pca"}

        d = {'input': "/ticker/data/quote/?days=30",
             'drop': ['ID', 'ticker_id']}

        import urllib
        uri = urllib.urlencode(d)
        print "uri: {}".format(uri)

        # c = Client()

        # r = c.get('/dimreduce/pca/', d)

        # # print the response, dont know what to do
        # print r

    def test_figure(self):

        from matplotlib import pyplot as plt
        from utils import draw_pca_figure

        fig = plt.figure(tight_layout=True)

        # TODO will change
        fig = draw_pca_figure(fig)

        plt.show()
