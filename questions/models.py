from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel


class AbstractQuestion(models.Model):
    display_text = models.TextField()
    display_order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.display_text

    class Meta:
        abstract = True
        ordering = ['display_order']


class TextQuestion(AbstractQuestion):
    input_size = models.CharField(max_length=64, choices=[(
        'short', 'short answer'), ('long', 'long input (essay, paragraph)')], default='short')
    correct = models.TextField()
    
    def user_response(self, user):
        try:
            return TextQuestionResponse.objects.filter(user=user.id).get(question=self.id)
        except:
            return None



class OptionQuestion(AbstractQuestion):
    input_select = models.CharField(max_length=64, choices=[(
        'radio', 'single responses'), ('checkbox', 'multiple responses')], default='radio')

    def options_list(self):
        options = []
        correct = []
        for i in self.options.all():
            option = []
            option.append(i.id)
            option.append(i.display_text)
            options.append(option)
        return options

    def correct_option(self):
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
    question = models.ForeignKey(OptionQuestion, related_name='options')
    correct = models.BooleanField(default=False)
    display_text = models.CharField(max_length=256)
    display_order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.display_text


class OptionQuestionResponse(TimeStampedModel):
    user = models.ForeignKey(User)
    question = models.ForeignKey(OptionQuestion)
    response = models.ForeignKey(Option)

    def __unicode__(self):
        return self.response.display_text

    def get_absolute_url(self):
        return reverse('respond', args=[str(self.question.id)])


class TextQuestionResponse(TimeStampedModel):
    user = models.ForeignKey(User)
    question = models.ForeignKey(TextQuestion)
    response = models.TextField()

    def __unicode__(self):
        return self.response

    def get_absolute_url(self):
        return reverse('response_text', args=[str(self.question.id)])

