from django.conf.urls import patterns, url

from views import pca, data_pca, pca_stock_quotes

urlpatterns = patterns('',
                       url(r'^pca/$', pca, name='pca'),
                       url(r'^pca/stocks/', pca_stock_quotes,
                           name='pca_stock_quotes'),
                       url(r'^data/pca/', data_pca),)
