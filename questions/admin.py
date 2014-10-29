from django.contrib import admin

from .models import (TextQuestion, OptionQuestion, Option,
                     OptionQuestionResponse, TextQuestionResponse, QuestionSequence, QuestionSequenceItem)

admin.site.register(TextQuestion)
admin.site.register(OptionQuestion)
admin.site.register(Option)
admin.site.register(OptionQuestionResponse)
admin.site.register(TextQuestionResponse)
admin.site.register(QuestionSequence)
admin.site.register(QuestionSequenceItem)
