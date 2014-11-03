from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django import forms

import json

from model_utils.models import TimeStampedModel

# from questions.forms import *


class AbstractQuestion(models.Model):

    """
    A super class specifying the question text to display and the display order of the question.
    """
    display_text = models.TextField()
    display_order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.display_text

    class Meta:
        abstract = True
        ordering = ['display_order']


class TextQuestion(AbstractQuestion):

    """
    A question type that accepts text input.
    """
    input_size = models.CharField(max_length=64, choices=[
        ('1', 'short answer: (1 row 80 cols)'), 
        ('5', 'sentence: (5 rows 80 cols'), 
        ('15', 'paragraph(s): (15 rows 80 cols)')], default='short')
    correct = models.TextField(blank=True)
    sequence = GenericRelation(
        'QuestionSequenceItem', related_query_name='questions')
    responses = GenericRelation('QuestionResponse')

    def get_input_widget(self):
        widget_attrs = {
            'rows': self.input_size,
            'cols': '80',
            'style': 'resize: vertical'
        }
        return forms.CharField(label=self.display_text, widget=forms.Textarea(attrs=widget_attrs))

    def correct_answer(self):
        return self.correct

    def check_answer(self, answer):
        return answer == self.correct_answer()

    def user_response(self, user):
        """
        Returns the first response found by the user.
        """
        try:
            return self.responses.all().get(user=user)
        except:
            return None


class OptionQuestion(AbstractQuestion):

    """
    A question type that accepts a selection from a list of choices (multiple choice).
    """
    input_select = models.CharField(max_length=64, choices=[(
        'radio', 'single responses'), ('checkbox', 'multiple responses')], default='radio')

    sequence = GenericRelation(
        'QuestionSequenceItem', related_query_name='questions')
    responses = GenericRelation('QuestionResponse')

    def get_input_widget(self):
        if self.input_select == 'checkbox':
            field_widget = forms.CheckboxSelectMultiple()
            return forms.MultipleChoiceField(label=self.display_text, choices=self.options_list(), widget=field_widget)
        else:
            field_widget = forms.RadioSelect()
            return forms.ChoiceField(label=self.display_text, choices=self.options_list(), widget=field_widget)

    def options_list(self):
        options = []
        for i in self.options.all():
            option = i.id, i.display_text
            options.append(option)
        return options

    def correct_answer(self):
        return self.options.filter(correct=True)

    def check_answer(self, answer):
        # Return false if at least 1 incorrect selection found.
        # TODO: fix by implementing list comparisons for checkbox selections.
        try:
            if self.input_select == 'checkbox':               
                for i in answer:
                    opt = Option.objects.get(pk=i)
                    if not opt.correct: 
                        return False
                return True
            else:  
                opt = Option.objects.get(pk=answer)
                return opt.correct
        except:
            return False

    def user_response(self, user):
        """
        Returns the first response found for the user.
        """
        try:
            return self.responses.all().get(user=user)
        except:
            return None


class Option(models.Model):

    """
    Stores a single option to list as a choice for a :model:`questions.OptionQuestion`.
    """
    question = models.ForeignKey(OptionQuestion, related_name='options')
    correct = models.BooleanField(default=False)
    display_text = models.CharField(max_length=256)
    display_order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.display_text


class QuestionResponse(TimeStampedModel):
    user = models.ForeignKey(User, related_name='question_responses')
    response = models.TextField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        self.response = json.dumps(self.response)
        super(QuestionResponse, self).save(*args, **kwargs)

    # Fix this to contruct arguments relative to question sequence object
    # def get_absolute_url(self):
    #     return reverse('question_response', args=[str(''), str('')])


class OptionQuestionResponse(TimeStampedModel):
    user = models.ForeignKey(User)
    question = models.ForeignKey(OptionQuestion)
    response = models.ForeignKey(Option)

    def __unicode__(self):
        return self.response.display_text

    def get_absolute_url(self):
        return reverse('option_response', args=[str(self.question.id)])


class TextQuestionResponse(TimeStampedModel):

    """
    """
    user = models.ForeignKey(User)
    question = models.ForeignKey(TextQuestion)
    response = models.TextField()

    def __unicode__(self):
        return self.response

    def get_absolute_url(self):
        return reverse('text_response', args=[str(self.question.id)])


class QuestionSequence(models.Model):

    """
    A wrapper for set of questions of any defined type. This class models the
    notion of a worksheet of questions e.g., OptionQuestion or TextQuestion
    """
    title = models.CharField(max_length=256)
    description = models.TextField()
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(QuestionSequence, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_response', args=[self.slug, '1'])


class QuestionSequenceItem(models.Model):

    """
    Functions as a list of questions for QuestionSequence.
    Allow QuestionSequences to contain varied question types.
    """
    order = models.IntegerField(default=0)
    question_sequence = models.ForeignKey(
        QuestionSequence, related_name='questions')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
