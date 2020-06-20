from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^parsed/$', views.parsed, name='parsed'),
    url(r'^results/$', views.results, name='results'),

    url(r'^parsed_result/$', views.parsed_result, name='parsed_result'),
    url(r'^show/(?P<pk>[a-z\d]+)/$', views.show, name='show'),
]