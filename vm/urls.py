# -*- coding: utf-8 -*-

from django.conf.urls import url

from vm import views

urlpatterns = [
   url(r'^$', views.homepage, name="homepage"),
   url(r'^order/$', views.order, name="order"),
   url(r'^save_order/$', views.ajax_save_order, name="api_save_order"),
   url(r'^search_order/$', views.search_order, name="search_order"),
   url(r'^administration/$', views.administration, name="administration"),
   url(r'^api/search_order/(?P<code>[a-zA-Z]{8})/$', views.ajax_search_order, name="api_search_order"),
   url(r'^api/fill_flavour/(?P<pk>[0-9]+)/$', views.ajax_fill_flavour, name='api_fill_flavour',)
]
