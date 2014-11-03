# forms.py
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.forms import ModelForm

import json

from .models import TextQuestion, QuestionResponse, OptionQuestion, TextQuestionResponse, OptionQuestionResponse


class QuestionResponseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionResponseForm, self).__init__(*args, **kwargs)
        
        # question and user are assigned by the caller of the form
        # assigning to local variables for readability
        
        question = self.initial['question']
        user = self.initial['user']
        self.initial[
            'content_type'] = ContentType.objects.get_for_model(question)
        self.initial['object_id'] = question.id
        self.fields['response'] = question.get_input_widget()

        # Check for previous response to question by user
        try:
            previous_response = question.user_response(user)
            resp_data = json.loads(previous_response.response)
            self.initial['response'] = resp_data
            answer_check = question.check_answer(resp_data)
            
            # Set user feedback info (correct or incorrect response)
            if answer_check:
                self.fields['response'].help_text += 'correct'
            else:
                self.fields['response'].help_text += 'incorrect'

        except:
            pass

    # Override save method to handle previous responses.
    def save(self):
        submitted_form = super(
            QuestionResponseForm, self).save(commit=False)
        
        question = submitted_form.content_object
        user = submitted_form.user
        previous_response = question.user_response(user)

        if previous_response:
            previous_response.response = submitted_form.response.strip()
            previous_response.save()
        else:
            submitted_form.save()

        return submitted_form

    class Meta:
        model = QuestionResponse
        fields = ['user', 'content_type', 'object_id', 'response']
        widgets = {
            'user': forms.HiddenInput(),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput()
        }












# Deprecate
class OptionQuestionResponseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(OptionQuestionResponseForm, self).__init__(*args, **kwargs)

        # question and user are assigned by the caller of the form
        # assigning to local variables for readability
        question = self.initial['question']
        user = self.initial['user']

        # Initialize with question text and choices
        self.fields['response'].label = question.display_text
        self.fields['response'].choices = question.options_list()

        # Check for previous response to question by user
        try:

            previous_response = question.user_response(user)
            self.initial['response'] = previous_response.response

            # Set user feedback info (correct or incorrect response)
            if question.correct_option() == previous_response.response:
                self.fields['question'].help_text = 'correct'
            else:
                self.fields['question'].help_text = 'incorrect'

        except:
            print 'no response'
            pass

    # Override save method to handle previous responses.
    def save(self):
        submitted_form = super(
            OptionQuestionResponseForm, self).save(commit=False)

        # Update an existing response or create a new one.
        try:
            previous_response = submitted_form.question.user_response(
                submitted_form.user)
            previous_response.response = submitted_form.response
            previous_response.save()
        except:
            submitted_form.save()

        return submitted_form

    class Meta:
        model = OptionQuestionResponse
        fields = ['user', 'question', 'response']
        widgets = {
            'user': forms.HiddenInput(),
            'question': forms.HiddenInput(),
            'response': forms.RadioSelect(),
        }


class TextQuestionResponseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TextQuestionResponseForm, self).__init__(*args, **kwargs)

        # question and user are assigned by the caller of the form
        # assigning to local variables for readability
        question = self.initial['question']
        user = self.initial['user']

        # Initialize with question text

        self.fields['response'].label = question.display_text
        self.fields['response'].widget.attrs = {
            'rows': question.input_size,
            'cols': '80',
            'style': 'resize: vertical'
        }

        # Check for previous response to question by user
        try:
            previous_response = question.user_response(user)
            self.initial['response'] = previous_response.response

            # Set user feedback info (correct or incorrect response)
            print '|%s|' % question.correct
            if question.correct:
                print '|%s|' % question.correct
                if question.correct == previous_response.response:
                    self.fields['question'].help_text = 'correct'
                else:
                    self.fields['question'].help_text = 'incorrect'
        except:
            pass

    def save(self):
        submitted_form = super(
            TextQuestionResponseForm, self).save(commit=False)
        # trim whitespace
        submitted_form.response = submitted_form.response.strip()
        try:
            previous_response = submitted_form.question.user_response(
                submitted_form.user)
            previous_response.response = submitted_form.response
            previous_response.save()
        except:
            submitted_form.save()

        return submitted_form

    class Meta:
        model = TextQuestionResponse
        fields = ['user', 'question', 'response']
        widgets = {
            'user': forms.HiddenInput(),
            'question': forms.HiddenInput(),
            'response': forms.Textarea(),
        }
