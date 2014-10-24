from django.conf.urls import patterns, url

from views import pca

urlpatterns = patterns('',
                       url(r'^pca/', pca, name='pca'),)
