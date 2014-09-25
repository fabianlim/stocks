from django.conf.urls import patterns, url

from utils import ticker_png

from views import index

urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'img/(?P<symbol>[\w.]+)/$',
                           ticker_png, name='ticker_png'),
                       )
