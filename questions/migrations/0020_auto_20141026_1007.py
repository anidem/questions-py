# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0019_questionsequence_questionsequenceitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionsequenceitem',
            name='question_sequence',
            field=models.ForeignKey(related_name=b'items', to='questions.QuestionSequence'),
        ),
    ]
