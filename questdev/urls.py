from django.conf.urls import patterns, include, url
from django.contrib import admin

from questions.views import (
    HomeView, OptionQuestionResponseCreateView, TextQuestionResponseCreateView
    )

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^option/response/(?P<q>\d+)/$', OptionQuestionResponseCreateView.as_view(), name='respond'),
    url(r'^text/response/(?P<q>\d+)/$', TextQuestionResponseCreateView.as_view(), name='response_text'),
   
    url(r'^admin/', include(admin.site.urls)),
)
