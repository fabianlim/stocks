from django.conf.urls import patterns, url

from visual import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'ticker/(?P<symbol>[\w.]+)/$',
                           views.visualize_ticker),
                       url(r'ticker/img/(?P<symbol>[\w.]+)/$',
                           views.ticker_png, name='ticker_png'),
                       )
