import urllib
import os

cur_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

from models import Data


class DashboardRegistration(object):
    """ to register to the dashboard """

    @staticmethod
    def get_app_sidebar(qdict):

        return {"template_path": cur_dir + "/" + qdict['algo']
                + '-sidebar.html',
                "args": {'procedure_name': qdict['algo']}}

    @staticmethod
    def get_app_main(qdict):
        template = qdict["algo"]
        qdict.pop("algo", None)

        print "app_main {}".format(qdict)
        return {"template_path": cur_dir + "/" + template + '-main.html',
                "args": {'input': qdict['input'],
                         'querystr': urllib.urlencode(qdict)}}

    @staticmethod
    def get_app_search(qdict):

        # run the full-text search
        # returns a query set
        search_results = Data.objects.search(
            qdict['?keys?'],
            rank_field='relevance')

        return {"template_path": cur_dir + "/" + qdict['algo'] + '-search.html',
                "args": {'search_results': search_results}}
