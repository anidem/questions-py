from django.conf.urls import patterns, include, url
from django.contrib import admin

from questions.views import (
    HomeView, QuestionResponseView, QuestionSequenceItemsListView, ImportJsonQuestion
    )

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^questions/(?P<i>[-\w]+)/(?P<j>\d+)/$', QuestionResponseView.as_view(), name='question_response'),
    url(r'^questions/import/(?P<slug>[-\w]+)/$', ImportJsonQuestion.as_view(), name='question_import'),
   
    url(r'^admin/', include(admin.site.urls)),
)

    # url(r'^question/option/(?P<i>\d+)/$', OptionQuestionResponseCreateView.as_view(), name='option_response'),
    # url(r'^question/text/(?P<i>\d+)/$', TextQuestionResponseCreateView.as_view(), name='text_response'),
