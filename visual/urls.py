from django.conf.urls import patterns, url

from visual import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^graph$', views.graph, name='graph'),
)
