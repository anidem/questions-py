from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView, CreateView, UpdateView, ListView

from .models import TextQuestion, OptionQuestion, QuestionResponse, QuestionSequence, QuestionSequenceItem
from .forms import QuestionResponseForm

class HomeView(ListView):
    model = QuestionSequence
    template_name = 'index.html'

class QuestionResponseView(CreateView):
    model = QuestionResponse
    template_name = 'question_sequence.html'
    form_class = QuestionResponseForm
    sequence = None

    def get_success_url(self):
        return self.request.path

    def get_initial(self):
        self.sequence = get_object_or_404(QuestionSequence, slug=self.kwargs.pop('i'))
        question_item = get_object_or_404(self.sequence.questions, pk=self.kwargs.pop('j'))
        self.initial['question'] = question_item.content_object
        self.initial['user'] = self.request.user
        return self.initial

    def get_context_data(self, **kwargs):
        context = super(QuestionResponseView, self).get_context_data(**kwargs)        
        context['worksheet'] = self.sequence
        context['question_list'] = self.sequence.questions.all()
        return context


class QuestionSequenceItemsListView(ListView):
    model = QuestionSequenceItem
    template_name = 'question_list.html'
    question_sequence = None

    def get_queryset(self):
        self.question_sequence = QuestionSequence.objects.get(slug=self.kwargs.pop('i'))
        return self.question_sequence.questions.all()










# class OptionQuestionResponseCreateView(CreateView):
#     model = OptionQuestionResponse
#     form_class = OptionQuestionResponseForm
#     template_name = 'question.html'

#     def get_initial(self):
#         question = OptionQuestion.objects.get(id=self.kwargs.pop('i'))
#         self.initial['question'] = question
#         self.initial['user'] = self.request.user
#         return self.initial

# class TextQuestionResponseCreateView(CreateView):
#     model = TextQuestionResponse
#     form_class = TextQuestionResponseForm
#     template_name = 'question.html'

#     def get_initial(self):
#         question = TextQuestion.objects.get(id=self.kwargs.pop('i'))
#         self.initial['question'] = question
#         self.initial['user'] = self.request.user
#         return self.initial
