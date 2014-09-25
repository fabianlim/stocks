from django.conf.urls import patterns, url

from utils import ticker_png  # bad
urlpatterns = patterns('',
                       url(r'img/(?P<symbol>[\w.]+)/$',
                           ticker_png, name='ticker_png'),
                       )
