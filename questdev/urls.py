from django.conf.urls import patterns, include, url
from django.contrib import admin

from questions.views import (
    HomeView, QuestionResponseView, QuestionSequenceItemsListView, 
    OptionQuestionView, OptionQuestionUpdateView,
    TextQuestionView, TextQuestionUpdateView,
    ImportJsonQuestion
    )

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^questions/optionquestions/(?P<pk>\d+)/$', OptionQuestionView.as_view(), name='option_question'),
    url(r'^questions/optionquestions/update/(?P<pk>\d+)/$', OptionQuestionUpdateView.as_view(), name='option_question_update'),
    
    url(r'^questions/textquestions/(?P<pk>\d+)/$', TextQuestionView.as_view(), name='text_question'),
    url(r'^questions/textquestions/update/(?P<pk>\d+)/$', TextQuestionUpdateView.as_view(), name='text_question_update'),


    url(r'^questions/(?P<i>[-\w]+)/(?P<j>\d+)/$', QuestionResponseView.as_view(), name='question_response'),
    url(r'^questions/import/(?P<slug>[-\w]+)/$', ImportJsonQuestion.as_view(), name='question_import'),

   
    url(r'^admin/', include(admin.site.urls)),
)

    # url(r'^question/option/(?P<i>\d+)/$', OptionQuestionResponseCreateView.as_view(), name='option_response'),
    # url(r'^question/text/(?P<i>\d+)/$', TextQuestionResponseCreateView.as_view(), name='text_response'),
