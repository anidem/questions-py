from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView, CreateView, UpdateView, ListView, DetailView
from django.forms.models import inlineformset_factory, modelformset_factory

from collections import OrderedDict

from .models import TextQuestion, OptionQuestion, QuestionResponse, QuestionSequence, QuestionSequenceItem, Option
from .forms import QuestionResponseForm, OptionQuestionUpdateForm, TextQuestionUpdateForm, OptionFormset 

import os, json

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
        sequence_items = self.sequence.sequence_items.all()
        item = sequence_items[ int(self.kwargs.pop('j'))-1 ]
        self.initial['question'] = item.content_object
        self.initial['user'] = self.request.user
        return self.initial

    def get_context_data(self, **kwargs):
        context = super(QuestionResponseView, self).get_context_data(**kwargs)        
        context['worksheet'] = self.sequence
        
        # Tally -- move this to object manager...
        tally = OrderedDict()
        for i in self.sequence.sequence_items.all():
            
            try: 
                response = i.content_object.user_response_object(self.request.user).json_response()
                if i.content_object.check_answer(response):
                    tally[i.content_object] = 'success'
                else:
                    tally[i.content_object] = 'danger'
            except:
                tally[i.content_object] = 'default'

            if self.initial['question'].id == i.content_object.id:
                tally[i.content_object] = tally[i.content_object] + ' current'
        
        if self.request.user.is_staff:
            context['edit_url'] = self.initial['question'].get_edit_url()

        context['question_list'] = tally   
        return context

class QuestionSequenceItemsListView(ListView):
    model = QuestionSequenceItem
    template_name = 'question_list.html'
    question_sequence = None

    def get_queryset(self):
        self.question_sequence = QuestionSequence.objects.get(slug=self.kwargs.pop('i'))
        return self.question_sequence.questions.all()

class ImportJsonQuestion(DetailView):
    model = QuestionSequence
    # template_name = reverse('question_response')
    
    def get_context_data(self, **kwargs):
        context = super(ImportJsonQuestion, self).get_context_data(**kwargs)
        optsmap ={'A': '1', 'B': '2', 'C': '3', 'D': '4' }
        json_dir = '/Users/rmedina/Desktop/ggvworksheet-conversion/csvdir/jsondir'
        # files = []
        # for fstr in os.listdir(json_dir):
        #     if fstr != '.DS_Store':
        #         files.append(fstr)

        f = '646.json' #files[2] #for f in files:
        json_file = open('%s/%s' % (json_dir, f))
        json_data = json_file.read()
        data = json.loads(json_data) # deserialises it

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

                opts = dict((k, v) for k, v in sorted(i.items()) if k.startswith('option'))
                for k, v in opts.items():
                    order = k[7:] # get the number portion of the key: e.g.,option 1 --> 1
                    opt = Option()
                    opt.display_text = v
                    opt.display_order = order
                    opt.correct = order == optsmap[i.get('CORRECT ANSWER')]
                    opt.question = question
                    opt.save()
            
            seq = self.get_object()
            seqitem = QuestionSequenceItem(content_object=question, question_sequence=seq, order=question.display_order)
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        optionsform = OptionFormset(instance=self.get_object())
        return self.render_to_response(
            self.get_context_data(form=form, optionsform=optionsform))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        optionsform = OptionFormset(self.request.POST, instance=self.get_object())
        if form.is_valid() and optionsform.is_valid():
            return self.form_valid(form, optionsform)
        else:
            return self.form_invalid(form, optionsform)

    def form_valid(self, form, optionsform):
        self.object = form.save()
        optionsform.instance = self.object
        optionsform.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, optionsform):
        return self.render_to_response(
            self.get_context_data(form=form, optionsform=optionsform))



