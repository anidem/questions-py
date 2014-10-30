from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

from pydoc import locate

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
    input_size = models.CharField(max_length=64, choices=[(
        '1', 'short answer: (1 row 80 cols)'), ('5', 'sentence: (5 rows 80 cols'), ('15', 'paragraph(s): (15 rows 80 cols)')], default='short')
    correct = models.TextField(blank=True)
    sequence = GenericRelation(
        'QuestionSequenceItem', related_query_name='questions')

    def get_form_class(self):
        return locate('questions.forms.TextQuestionResponseForm')

    def correct_answer(self):
        try:
            return self.correct
        except:
            return None

    def user_response(self, user):
        try:
            response = GenericRelation('QuestionResponse', related_query_name='user_response')
            return TextQuestionResponse.objects.filter(user=user.id).get(question=self.id)
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

    def get_form_class(self):
        return locate('questions.forms.OptionQuestionResponseForm')

    def options_list(self):
        options = []
        correct = []
        for i in self.options.all():
            option = []
            option.append(i.id)
            option.append(i.display_text)
            options.append(option)
        return options

    def correct_answer(self):
        try:
            return self.options.filter(correct=True)[0]
        except:
            return None

    def user_response(self, user):
        try:
            return OptionQuestionResponse.objects.filter(user=user.id).get(question=self.id)
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
    user = models.ForeignKey(User, related_name='user_response')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

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
        return reverse('questions', args=[str(self.question.id)])


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
