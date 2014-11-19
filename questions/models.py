from django.db import models
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django import forms
from operator import itemgetter
import json

from model_utils.models import TimeStampedModel

class QuestionSet(models.Model):

    """
    A wrapper for set of questions of any defined type. This class models the
    notion of a worksheet of questions e.g., OptionQuestion or TextQuestion
    """
    title = models.CharField(max_length=256)
    description = models.TextField()
    slug = models.SlugField(blank=True)

    def get_ordered_question_list(self):
        seqitems = [(x.content_object, x.content_object.display_order) for x in self.sequence_items.all()]
        return [x[0] for x in sorted(seqitems, key=itemgetter(1))]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(QuestionSet, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_response', args=[self.id, '1'])


class QuestionSequenceItem(models.Model):

    """
    Functions as a list of questions for QuestionSequence.
    Allow QuestionSequences to contain varied question types.
    Content objects reference types derived from Abstract Question.
    """
    question_sequence = models.ForeignKey(
        QuestionSet, related_name='sequence_items')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class AbstractQuestion(models.Model):

    """
    A super class specifying the question text to display and the display order of the question.
    """
    display_text = models.TextField()
    display_order = models.IntegerField(default=0)
    display_image = models.FileField(null=True, blank=True, upload_to='img')

    def get_sequence_url(self):
        try:
            seqitem = self.sequence.get()
            worksheet = seqitem.question_sequence
            position = worksheet.get_ordered_question_list().index(self)
            return reverse('question_response', args=[worksheet.id, position+1])
        except:
            return None

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
        ('15', 'paragraph(s): (15 rows 80 cols)')], default='1')
    correct = models.TextField(blank=True)
    sequence = GenericRelation(
        QuestionSequenceItem, related_query_name='questions')
    responses = GenericRelation('QuestionResponse')


    def get_input_widget(self):
        widget_attrs = {
            'rows': self.input_size,
            'cols': '50',
            'style': 'resize: vertical'
        }
        return forms.CharField(label='', widget=forms.Textarea(attrs=widget_attrs))

    def correct_answer(self):
        return self.correct

    def check_answer(self, json_str):
        return json_str == self.correct

    def user_response_object(self, user):        
        """
        Returns a QuestionResponse object related to user.
        """
        try:
            return self.responses.all().get(user=user)
        except:
            return None

    def get_edit_url(self):
        return reverse('text_question_update', args=[self.id])

    def get_absolute_url(self):
        return reverse('text_question', args=[self.id])



class OptionQuestion(AbstractQuestion):

    """
    A question type that accepts a selection from a list of choices (multiple choice).
    """
    input_select = models.CharField(max_length=64, choices=[(
        'radio', 'single responses'), ('checkbox', 'multiple responses')], default='radio')

    sequence = GenericRelation(
        QuestionSequenceItem, related_query_name='questions')
    responses = GenericRelation('QuestionResponse')

    def get_input_widget(self):
        if self.input_select == 'checkbox':
            field_widget = forms.CheckboxSelectMultiple()
            return forms.MultipleChoiceField(label='', choices=self.options_list(), widget=field_widget)
        else:
            field_widget = forms.RadioSelect()
            return forms.ChoiceField(label='', choices=self.options_list(), widget=field_widget)

    def options_list(self):
        return [(i.id, i.display_text) for i in self.options.all()]

    def correct_answer(self):
        if self.input_select == 'checkbox':
            return [str(i.id) for i in self.options.filter(correct=True)]
        else:
            return str(self.options.get(correct=True).id)

    def check_answer(self, json_str):
        # Need to process option responses as lists. json used to coerce
        # string representation to list.
        try:
            return self.correct_answer() == json_str
        except:
            print 'error doing json compare check'

    def user_response_object(self, user):
        """
        Returns a QuestionResponse object related to user.
        """
        try:
            return self.responses.get(user=user)
        except:
            return None

    def get_edit_url(self):
        return reverse('option_question_update', args=[self.id])

    def get_absolute_url(self):
        return reverse('option_question', args=[self.id])

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

    class Meta:
        ordering = ['display_order', 'id']


class QuestionResponse(TimeStampedModel):
    """
    Generic question response container. 
    """
    user = models.ForeignKey(User, related_name='question_responses')
    response = models.TextField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def json_response(self):
        try:
            return json.loads(self.response)
        except:
            return None        

    def save(self, *args, **kwargs):
        self.response = json.dumps(self.response)
        super(QuestionResponse, self).save(*args, **kwargs)

    # Fix this to contruct arguments relative to question sequence object
    def get_absolute_url(self):
        return reverse('home')

class Note(TimeStampedModel):
    subject = models.CharField(max_length=48)
    text = models.TextField()

    def get_absolute_url(self):
        return reverse('view_note', args=[self.id])




