from django.conf.urls import patterns, url

from views import index, data_quote, ticker_png

urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'^img/',
                           ticker_png, name='ticker_png'),
                       url(r'^data/quote/', data_quote),
                       )
