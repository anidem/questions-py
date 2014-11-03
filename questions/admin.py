from django.contrib import admin

from .models import (TextQuestion, OptionQuestion, Option,
                     QuestionResponse, QuestionSequence, QuestionSequenceItem)

admin.site.register(TextQuestion)
admin.site.register(OptionQuestion)
admin.site.register(Option)
admin.site.register(QuestionResponse)
admin.site.register(QuestionSequence)
admin.site.register(QuestionSequenceItem)
