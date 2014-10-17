# forms.py
from django import forms
from django.forms import ModelForm

from .models import TextQuestion, OptionQuestion, TextQuestionResponse, OptionQuestionResponse


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
            self.initial['response'] = previous_response.response.id

            # Set user feedback info (correct or incorrect response)
            if question.correct_option() == previous_response.response:
                self.fields['question'].help_text = 'correct'
            else:
                self.fields['question'].help_text = 'incorrect'

        except:
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
        self.fields['response'].widget.attrs={
            'rows': question.input_size, 
            'cols': '80',
            'style': 'resize: vertical'
            }            

        # Check for previous response to question by user
        try:
            previous_response = question.user_response(user)
            self.initial['response'] = previous_response.response

            # Set user feedback info (correct or incorrect response)
            print '|%s|'%question.correct
            if question.correct:
                print '|%s|'%question.correct
                if question.correct == previous_response.response:
                    self.fields['question'].help_text = 'correct'
                else:
                    self.fields['question'].help_text = 'incorrect'
        except:
            pass

    def save(self):
        submitted_form = super(
            TextQuestionResponseForm, self).save(commit=False)
        submitted_form.response = submitted_form.response.strip() # trim whitespace
        
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
