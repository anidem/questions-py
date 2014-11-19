from django.contrib import admin

from django.db import models
from django import forms


from .models import (TextQuestion, OptionQuestion, Option,
                     QuestionResponse, QuestionSet, QuestionSequenceItem)


class OptionInlineAdmin(admin.TabularInline):
    model = Option
    formfield_overrides = {
        models.IntegerField: {'widget': forms.NumberInput},
    }

class OptionQuestionAdmin(admin.ModelAdmin):
    list_display = ('display_text', 'display_order')
    inlines = [ OptionInlineAdmin ]


admin.site.register(TextQuestion)
admin.site.register(OptionQuestion, OptionQuestionAdmin)
admin.site.register(Option)
admin.site.register(QuestionResponse)
admin.site.register(QuestionSet)
admin.site.register(QuestionSequenceItem)
