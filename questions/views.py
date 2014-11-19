from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView, CreateView, UpdateView, ListView, DetailView, View
from django.forms.models import inlineformset_factory, modelformset_factory
from collections import OrderedDict
import os
import json

from braces.views import CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin

from .models import TextQuestion, OptionQuestion, QuestionResponse, QuestionSet, QuestionSequenceItem, Option, Note
from .forms import QuestionResponseForm, OptionQuestionUpdateForm, TextQuestionUpdateForm, OptionFormset, CreateNoteForm
from .mixins import AjaxableResponseMixin




class HomeView(ListView):
    model = QuestionSet
    template_name = 'index.html'


class QuestionResponseView(CreateView):
    model = QuestionResponse
    template_name = 'question_sequence.html'
    form_class = QuestionResponseForm
    sequence = None

    def get_success_url(self):
        return self.request.path

    def get_initial(self):
        self.sequence = get_object_or_404(
            QuestionSet, id=self.kwargs.pop('i'))
        sequence_items = self.sequence.get_ordered_question_list()
        try:
            item = sequence_items[int(self.kwargs.pop('j')) - 1]
            self.initial['question'] = item
            self.initial['user'] = self.request.user
        except:
            pass
        return self.initial

    def get_context_data(self, **kwargs):
        context = super(QuestionResponseView, self).get_context_data(**kwargs)
        context['worksheet'] = self.sequence
        current_question = self.initial['question']
        # Tally -- move this to object manager...
        tally = OrderedDict()
        for i in self.sequence.get_ordered_question_list():

            try:
                response = i.user_response_object(
                    self.request.user).json_response()
                if i.check_answer(response):
                    tally[i] = 'success'
                else:
                    tally[i] = 'danger'
            except:
                tally[i] = 'default'

            if current_question.id == i.id:
                tally[i] = tally[i] + ' current'

        if self.request.user.is_staff:
            context['edit_url'] = current_question.get_edit_url()

        context['noteform'] = CreateNoteForm()        
        context['note_list'] = Note.objects.all()
        context['question'] = current_question
        context['question_position'] = self.sequence.get_ordered_question_list().index(current_question)+1
        context['question_list'] = tally
        context['worksheet'] = self.sequence
        return context


class QuestionSequenceItemsListView(ListView):
    model = QuestionSequenceItem
    template_name = 'question_list.html'

    def get_queryset(self):
        question_sequence = QuestionSet.objects.get(slug=self.kwargs.pop('i'))
        return question_sequence.get_ordered_question_list()


class ImportJsonQuestion(DetailView):
    model = QuestionSet
    # template_name = reverse('question_response')

    def get_context_data(self, **kwargs):
        context = super(ImportJsonQuestion, self).get_context_data(**kwargs)
        optsmap = {'A': '1', 'B': '2', 'C': '3', 'D': '4'}
        json_dir = '/Users/rmedina/Desktop/ggvworksheet-conversion/csvdir/jsondir'
        # files = []
        # for fstr in os.listdir(json_dir):
        #     if fstr != '.DS_Store':
        #         files.append(fstr)

        f = '646.json'  # files[2] #for f in files:
        json_file = open('%s/%s' % (json_dir, f))
        json_data = json_file.read()
        data = json.loads(json_data)  # deserialises it

        WID = None
        for i in data:
            print i.get('QUESTION DISPLAY ORDER')
            if i.get('WID') != '':
                WID = i.get('WID')

            if i.get('SELECT TYPE') == 'text':
                question = TextQuestion()
                question.display_text = i.get('QUESTION')
                question.display_order = i.get('QUESTION DISPLAY ORDER')
                question.correct = i.get('CORRECT ANSWER')
                question.save()
            else:
                question = OptionQuestion()
                question.display_text = i.get('QUESTION')
                question.display_order = i.get('QUESTION DISPLAY ORDER')
                question.input_select = i.get('SELECT TYPE')
                question.save()

                opts = dict((k, v)
                            for k, v in sorted(i.items()) if k.startswith('option'))
                for k, v in opts.items():
                    # get the number portion of the key: e.g.,option 1 --> 1
                    order = k[7:]
                    opt = Option()
                    opt.display_text = v
                    opt.display_order = order
                    opt.correct = order == optsmap[i.get('CORRECT ANSWER')]
                    opt.question = question
                    opt.save()

            seq = self.get_object()
            seqitem = QuestionSequenceItem(
                content_object=question, question_sequence=seq)
            seqitem.save()

        json_file.close()

        return context


class TextQuestionView(DetailView):
    model = TextQuestion
    template_name = 'question_view.html'


class TextQuestionUpdateView(UpdateView):
    model = TextQuestion
    template_name = 'question_update.html'
    form_class = TextQuestionUpdateForm


class OptionQuestionView(DetailView):
    model = OptionQuestion
    template_name = 'question_view.html'

    def get_context_data(self, **kwargs):
        context = super(OptionQuestionView, self).get_context_data(**kwargs)
        context['options'] = self.get_object().options_list()
        return context


class OptionQuestionUpdateView(UpdateView):
    model = OptionQuestion
    template_name = 'question_update.html'
    form_class = OptionQuestionUpdateForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())
        optionsform = OptionFormset(
            self.request.POST, self.request.FILES, instance=self.get_object())

        if form.is_valid() and optionsform.is_valid():
            return self.form_valid(form, optionsform)
        else:
            return self.form_invalid(form, optionsform)

    def form_valid(self, form, optionsform):
        print form.cleaned_data
        optionsform.save()
        return super(OptionQuestionUpdateView, self).form_valid(form)

    def form_invalid(self, form, optionsform):
        return self.render_to_response(
            self.get_context_data(form=form, optionsform=optionsform))

    def get_context_data(self, **kwargs):
        context = super(
            OptionQuestionUpdateView, self).get_context_data(**kwargs)
        context['optionsform'] = OptionFormset(instance=self.get_object())
        return context

class NoteView(DetailView):
    model = Note
    template_name = 'note.html'

# Ajaxable
class NoteCreateView(CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, CreateView):
    model = Note
    template_name = 'note.html'
    form_class= CreateNoteForm

    def post_ajax(self, request, *args, **kwargs):
        noteform = CreateNoteForm(request.POST)
        if noteform.is_valid():
            newnote = noteform.save()
            data = noteform.cleaned_data
            data['modified'] = newnote.modified
            # print noteform
            return self.render_json_response(data)
        else:
            data = noteform.errors
            return self.render_json_response(data)
