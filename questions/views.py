from django.shortcuts import render

from django.views.generic import TemplateView, CreateView, UpdateView

from .models import TextQuestion, OptionQuestion, OptionQuestionResponse, TextQuestionResponse
from .forms import OptionQuestionResponseForm, TextQuestionResponseForm

class HomeView(TemplateView):
    template_name = 'index.html'


class OptionQuestionResponseCreateView(CreateView):
    model = OptionQuestionResponse
    template_name = 'question.html'
    form_class = OptionQuestionResponseForm

    def get_initial(self):
        question = OptionQuestion.objects.get(id=self.kwargs.pop('q'))
        self.initial['question'] = question
        self.initial['user'] = self.request.user
        return self.initial

class TextQuestionResponseCreateView(CreateView):
    model = TextQuestionResponse
    template_name = 'question.html'
    form_class = TextQuestionResponseForm

    def get_initial(self):
        question = TextQuestion.objects.get(id=self.kwargs.pop('q'))
        self.initial['question'] = question
        self.initial['user'] = self.request.user
        return self.initial
