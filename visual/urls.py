from django.conf.urls import patterns, url

from visual import views

from ticker.utils import ticker_png
urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       # url(r'ticker/(?P<symbol>[\w.]+)/$',
                       #     views.dashboard),
                       url(r'analyze\?(?P<params>\S+)/$',
                           views.dashboard),
                       url(r'ticker/img/(?P<symbol>[\w.]+)/$',
                           ticker_png, name='ticker_png'),
                       )
